import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import numpy as np
import streamlit as st

import style


# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)


def base_plot(x, y, title, equal=True):
    fig, ax = plt.subplots(figsize=(6, 6))
    styled_ax(ax, fig)
    if equal: ax.set_aspect("equal")
    ax.plot(x, y, color="#e8602a", linewidth=2.2)
    ax.plot(x[0], y[0], "o", color="#3d6b5e", markersize=9, zorder=5,
            label=f"Start ({x[0]:.2f},{y[0]:.2f})")
    ax.plot(x[-1], y[-1], "s", color="#c8a96e", markersize=9, zorder=5,
            label=f"End ({x[-1]:.2f},{y[-1]:.2f})")
    ax.legend(fontsize=8.5, framealpha=0.7, facecolor="#fdfaf5", edgecolor="#e0d8cc")
    ax.set_title(title, fontsize=10, color="#4a4540")
    ax.set_xlabel("x", color="#4a4540", fontsize=9)
    ax.set_ylabel("y", color="#4a4540", fontsize=9)
    plt.tight_layout()
    return fig


# ── LINE ──────────────────────────────────────────────────────────────────────

def solve_line(x0, y0, a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Parametric line",
        """A line = starting point + direction you move in:<br><br>
<span class="mf">x(t) = x₀ + a·t &nbsp;&nbsp; y(t) = y₀ + b·t</span><br><br>
t is time. At t=0 you're at (x₀,y₀). (a,b) is your direction vector.<br>
Why use parametric form? Vertical lines are impossible with y=mx+q.
Here a=0 handles them naturally.""",
        "warm")

    add("Your line",
        f"x(t) = {x0:g} + {a:g}·t<br>y(t) = {y0:g} + {b:g}·t")

    if a != 0:
        m=b/a; q=y0-m*x0
        add("Eliminating the parameter → Cartesian form",
            f"From x(t): t = (x − {x0:g}) / {a:g}<br>"
            f"Substitute into y(t):<br>"
            f"y = {y0:g} + {b:g}·(x−{x0:g})/{a:g}<br>"
            f"y = <strong>{m:g}x + {q:.4f}</strong>",
            "sage")
    elif a==0 and b!=0:
        add("Vertical line",
            f"a=0 → x = {x0:g} for all t. Vertical line — no slope form. Parametric handles it naturally.",
            "sage")

    rows="<br>".join(
        f"t={t}: x={x0+a*t:.3f}, y={y0+b*t:.3f}"
        for t in [-2,-1,0,1,2,3]
    )
    add("Sample points", rows)

    t=np.linspace(-5,5,400)
    return {"steps":steps,"x":x0+a*t,"y":y0+b*t,
            "title":f"Line: x={x0:g}+{a:g}t, y={y0:g}+{b:g}t"}


# ── CONICS ────────────────────────────────────────────────────────────────────

def solve_conic(mode, cx, cy, a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    t=np.linspace(0,2*np.pi,400)

    if mode == "circle":
        add("Circle — where parametric truly shines",
            """Cartesian form tells you the shape. Parametric form tells you the journey.<br><br>
<span class="mf">x(t) = cx + r·cos(t) &nbsp;&nbsp; y(t) = cy + r·sin(t) &nbsp;&nbsp; t∈[0,2π]</span><br><br>
t is the angle — at each t you know exactly where you are.<br>
Eliminating: cos(t)=(x−cx)/r, sin(t)=(y−cy)/r → cos²t+sin²t=1 → (x−cx)²+(y−cy)²=r²""",
            "warm")
        r=a
        add("Your circle",
            f"x(t) = {cx:g} + {r:g}·cos(t)<br>y(t) = {cy:g} + {r:g}·sin(t)<br><br>"
            f"Cartesian: (x−{cx:g})²+(y−{cy:g})² = {r**2:g}<br>"
            f"Circumference: {2*math.pi*r:.4f} &nbsp;·&nbsp; Area: {math.pi*r**2:.4f}",
            "sage")
        x_v=cx+r*np.cos(t); y_v=cy+r*np.sin(t)
        title=f"Circle: centre=({cx},{cy}), r={r}"

    else:  # ellipse
        add("Ellipse — a stretched circle",
            """<span class="mf">x(t) = cx + a·cos(t) &nbsp;&nbsp; y(t) = cy + b·sin(t)</span><br><br>
a stretches horizontally, b vertically. When a=b you get a circle.<br>
Cartesian: (x−cx)²/a² + (y−cy)²/b² = 1""",
            "warm")
        area=math.pi*a*b
        body=(f"x(t)={cx:g}+{a:g}·cos(t), y(t)={cy:g}+{b:g}·sin(t)<br>"
              f"Area=π·a·b={area:.4f}")
        if a!=b:
            c_=math.sqrt(abs(a**2-b**2)); e=c_/max(a,b)
            body+=f"<br>c={c_:.4f}, eccentricity={e:.4f} (0=circle, →1=flat)"
        add("Your ellipse",body,"sage")
        x_v=cx+a*np.cos(t); y_v=cy+b*np.sin(t)
        title=f"Ellipse: a={a}, b={b}"

    return {"steps":steps,"x":x_v,"y":y_v,"title":title}


# ── CYCLOID / SPIRALS / LISSAJOUS ─────────────────────────────────────────────

def solve_cycloid(r, n_arch):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("The cycloid — the brachistochrone",
        """A point on a rolling wheel traces a cycloid:<br><br>
<span class="mf">x(t)=r·(t−sin t) &nbsp;&nbsp; y(t)=r·(1−cos t)</span><br><br>
<strong>Brachistochrone (1696):</strong> the fastest path under gravity is a cycloid arc, not a straight line.
Johann Bernoulli posed it; Newton solved it overnight anonymously.<br>
Bernoulli recognised the solution: <em>'I know the lion by his paw.'</em><br><br>
<strong>Tautochrone:</strong> a ball released from ANY point on a cycloid always reaches the bottom in the same time.""",
        "warm")

    add("Properties",
        f"Arc length of one arch = 8r = <strong>{8*r:.4f}</strong><br>"
        f"Area under one arch = 3πr² = <strong>{3*math.pi*r**2:.4f}</strong><br>"
        "That's exactly 3× the area of the rolling circle — discovered by Torricelli, 1644.",
        "sage")

    t=np.linspace(0,2*np.pi*n_arch,1000*n_arch)
    return {"steps":steps,"x":r*(t-np.sin(t)),"y":r*(1-np.cos(t)),
            "r":r,"n_arch":n_arch,"mode":"cycloid"}


def solve_spiral(a, turns):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Archimedean spiral",
        """Each full turn adds exactly the same distance outward.<br><br>
<span class="mf">x(t)=a·t·cos(t) &nbsp;&nbsp; y(t)=a·t·sin(t)</span><br><br>
Found in: coiled rope, vinyl record grooves, rolled paper, some shells.""",
        "warm")

    t=np.linspace(0,2*np.pi*turns,1000)
    return {"steps":steps,"x":a*t*np.cos(t),"y":a*t*np.sin(t),
            "title":f"Archimedean Spiral (a={a}, {turns} turns)","mode":"spiral"}


def solve_lissajous(A, B, a, b, delta):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Lissajous figures",
        """Two sine waves at different frequencies combined:<br><br>
<span class="mf">x(t)=A·sin(a·t+δ) &nbsp;&nbsp; y(t)=B·sin(b·t)</span><br><br>
If a:b is a simple ratio (1:1, 2:1, 3:2…) the curve closes into a clean figure.<br>
Engineers use these on oscilloscopes to compare signal frequencies.<br>
The shape immediately reveals the frequency ratio.""",
        "warm")

    ratio=a/b if b!=0 else float("inf")
    add("Your figure",
        f"a:b = {a}:{b} = {ratio:.4f}<br>"
        f"Rectangle: {2*A}×{2*B}",
        "sage")

    t=np.linspace(0,6*np.pi,3000)
    return {"steps":steps,"x":A*np.sin(a*t+delta),"y":B*np.sin(b*t),
            "title":f"Lissajous (a={a},b={b},δ={delta:.2f})","mode":"lissajous","A":A,"B":B}


# ── PROJECTILE ────────────────────────────────────────────────────────────────

def solve_projectile(v0, alpha_deg, h0):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    g=9.81; alpha_rad=math.radians(alpha_deg)
    vx=v0*math.cos(alpha_rad); vy=v0*math.sin(alpha_rad)
    disc=vy**2+2*g*h0; t_flight=(vy+math.sqrt(disc))/g
    t_max=vy/g; x_max=vx*t_max; y_max=h0+vy*t_max-0.5*g*t_max**2
    x_land=vx*t_flight

    add("Projectile motion — two independent motions",
        """Horizontal: constant speed — nothing pushes sideways.<br>
Vertical: slows then accelerates — gravity.<br><br>
<span class="mf">x(t)=v₀·cos α·t &nbsp;&nbsp; y(t)=h₀+v₀·sin α·t−½g·t²</span><br><br>
Eliminating t gives a parabola — linking back to Chapter 9.""",
        "warm")

    add("Equations of motion",
        f"x(t) = {vx:.4f}·t<br>y(t) = {h0:g} + {vy:.4f}t − {0.5*g:.4f}t²<br><br>"
        f"Horizontal speed: {vx:.4f} m/s (constant)<br>"
        f"Initial vertical: {vy:.4f} m/s")

    A_c=-0.5*g/vx**2; B_c=vy/vx
    add("Eliminating the parameter",
        f"t = x/{vx:.4f} → y = {A_c:.6f}x² + {B_c:.4f}x + {h0:g}<br>"
        "Downward parabola ✓")

    range_cur=v0**2*math.sin(2*alpha_rad)/g; range_opt=v0**2/g
    add("Key values",
        f"Time in air: {t_flight:.4f} s<br>"
        f"Peak: ({x_max:.3f}, {y_max:.3f})<br>"
        f"Range: <strong>{x_land:.4f} m</strong><br><br>"
        f"Optimal angle for max range: 45°<br>"
        f"Your range at {alpha_deg}°: {range_cur:.4f} m &nbsp;·&nbsp; At 45°: {range_opt:.4f} m"
        +(f"<br>Leaving {range_opt-range_cur:.4f} m unused." if abs(alpha_deg-45)>1 else " ✓ optimal!"),
        "sage")

    t_v=np.linspace(0,t_flight,500)
    x_v=vx*t_v; y_v=np.maximum(h0+vy*t_v-0.5*g*t_v**2,0)
    angles=np.linspace(0,90,200); ranges_v=v0**2*np.sin(2*np.radians(angles))/g

    return {"steps":steps,"x":x_v,"y":y_v,"angles":angles,"ranges":ranges_v,
            "alpha_deg":alpha_deg,"x_max":x_max,"y_max":y_max,
            "x_land":x_land,"h0":h0,"v0":v0}


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_cycloid(r, n_arch):
    t=np.linspace(0,2*np.pi*n_arch,1000*n_arch)
    x=r*(t-np.sin(t)); y=r*(1-np.cos(t))
    fig,ax=plt.subplots(figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
    styled_ax(ax,fig)
    ax.plot(x,y,color="#e8602a",linewidth=2.2,label=f"Cycloid r={r}")
    for t_p in np.linspace(np.pi*0.5,2*np.pi*n_arch-np.pi*0.5,3):
        cx_=r*(t_p-math.sin(t_p)); th=np.linspace(0,2*np.pi,80)
        ax.plot(cx_+r*np.cos(th),r+r*np.sin(th),color="#3d6b5e",linewidth=0.8,alpha=0.3)
        ax.plot(r*(t_p-math.sin(t_p)),r*(1-math.cos(t_p)),"o",color="#c8a96e",markersize=6)
    ax.axhline(0,color="#1a1814",linewidth=1); ax.set_aspect("equal")
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    ax.set_title(f"Cycloid r={r} — the brachistochrone",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


def plot_lissajous(x, y, A, B, title):
    pts=np.array([x,y]).T.reshape(-1,1,2)
    segs=np.concatenate([pts[:-1],pts[1:]],axis=1)
    lc=mc.LineCollection(segs,cmap="plasma",linewidth=1.5,alpha=0.85)
    lc.set_array(np.linspace(0,1,len(segs)))
    fig,ax=plt.subplots(figsize=(6,6)); fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5"); ax.set_aspect("equal")
    ax.add_collection(lc); ax.set_xlim(-A-0.3,A+0.3); ax.set_ylim(-B-0.3,B+0.3)
    ax.set_title(title,fontsize=10,color="#4a4540")
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(True,alpha=0.2,color="#e0d8cc")
    plt.tight_layout(); return fig


def plot_projectile(r):
    fig,axes=plt.subplots(1,2,figsize=(11,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    axes[0].plot(r["x"],r["y"],color="#e8602a",linewidth=2.2,
                 label=f"α={r['alpha_deg']}°, v₀={r['v0']}m/s")
    axes[0].plot(0,r["h0"],"o",color="#3d6b5e",markersize=10,label="Launch")
    axes[0].plot(r["x_max"],r["y_max"],"^",color="#c8a96e",markersize=10,label=f"Peak")
    axes[0].plot(r["x_land"],0,"s",color="#7b6fb0",markersize=10,label="Landing")
    axes[0].axhline(0,color="#1a1814",linewidth=0.8)
    axes[0].legend(fontsize=8,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[0].set_title("Trajectory",fontsize=10,color="#4a4540")
    axes[1].plot(r["angles"],r["ranges"],color="#3d6b5e",linewidth=2)
    axes[1].axvline(45,color="#e8602a",linewidth=1.5,linestyle="--",label="Optimal 45°")
    axes[1].axvline(r["alpha_deg"],color="#c8a96e",linewidth=1.5,
                    linestyle="--",label=f"Your {r['alpha_deg']}°")
    axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[1].set_title("Range vs angle",fontsize=10,color="#4a4540")
    axes[1].set_xlabel("Angle (°)",color="#4a4540",fontsize=9)
    plt.tight_layout(); return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Line","Circle & Ellipse","Cycloid","Archimedean Spiral",
             "Lissajous","Projectile motion"],
            key="par_topic")

        if topic == "Line":
            c1,c2=st.columns(2)
            x0=c1.number_input("x₀",value=1.0,step=1.0,key="par_x0")
            y0=c2.number_input("y₀",value=2.0,step=1.0,key="par_y0")
            a_=c1.number_input("a (dir x)",value=2.0,step=0.5,key="par_a")
            b_=c2.number_input("b (dir y)",value=1.0,step=0.5,key="par_b")

        elif topic == "Circle & Ellipse":
            shape=st.selectbox("Shape",["Circle","Ellipse"],key="par_shape")
            c1,c2=st.columns(2)
            cx=c1.number_input("Centre x",value=0.0,step=1.0,key="par_cx")
            cy=c2.number_input("Centre y",value=0.0,step=1.0,key="par_cy")
            if shape=="Circle":
                r_=st.number_input("Radius r",value=3.0,step=0.5,key="par_r")
                a__,b__=r_,r_
            else:
                a__=c1.number_input("Semi-axis a",value=4.0,step=0.5,key="par_ea")
                b__=c2.number_input("Semi-axis b",value=2.0,step=0.5,key="par_eb")

        elif topic == "Cycloid":
            r_c=st.number_input("Radius r",value=1.0,step=0.5,key="par_cr")
            n_a=st.number_input("Arches",value=2,min_value=1,max_value=6,step=1,key="par_na")

        elif topic == "Archimedean Spiral":
            a_sp=st.number_input("Growth rate a",value=0.5,step=0.1,key="par_asp")
            turns=st.number_input("Turns",value=3.0,step=0.5,key="par_turns")

        elif topic == "Lissajous":
            c1,c2=st.columns(2)
            A_l=c1.number_input("Amplitude A",value=2.0,step=0.5,key="par_A")
            B_l=c2.number_input("Amplitude B",value=2.0,step=0.5,key="par_B")
            a_l=c1.number_input("Frequency a",value=3.0,step=1.0,key="par_fa")
            b_l=c2.number_input("Frequency b",value=2.0,step=1.0,key="par_fb")
            delta=st.number_input("Phase δ (e.g. 0, 0.785=π/4, 1.571=π/2)",
                                   value=0.785,step=0.1,key="par_delta")

        else:  # Projectile
            v0=st.number_input("Speed v₀ (m/s)",value=20.0,step=1.0,key="par_v0")
            alpha=st.number_input("Angle α (degrees)",value=45.0,step=5.0,key="par_alpha")
            h0=st.number_input("Initial height h₀ (m)",value=0.0,step=1.0,key="par_h0")

        solve_btn=st.button("Draw →",key="par_solve")
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Line: <code>x₀=0, y₀=0, a=2, b=1</code><br>
    Circle: <code>r=3</code><br>
    Cycloid: <code>r=1, 3 arches</code><br>
    Lissajous: <code>a=3, b=2, δ=π/2</code><br>
    Projectile: <code>v₀=30, α=60°</code>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Line":
                r=solve_line(x0,y0,a_,b_)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Parametric line</div>',unsafe_allow_html=True)
                fig=base_plot(r["x"],r["y"],r["title"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Circle & Ellipse":
                r=solve_conic("circle" if shape=="Circle" else "ellipse",cx,cy,a__,b__)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Curve</div>',unsafe_allow_html=True)
                fig=base_plot(r["x"],r["y"],r["title"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Cycloid":
                r=solve_cycloid(r_c,int(n_a))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Cycloid</div>',unsafe_allow_html=True)
                fig=plot_cycloid(r_c,int(n_a)); st.pyplot(fig); plt.close(fig)

            elif topic == "Archimedean Spiral":
                r=solve_spiral(a_sp,turns)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Spiral</div>',unsafe_allow_html=True)
                fig=base_plot(r["x"],r["y"],r["title"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Lissajous":
                r=solve_lissajous(A_l,B_l,a_l,b_l,delta)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Lissajous figure</div>',unsafe_allow_html=True)
                fig=plot_lissajous(r["x"],r["y"],r["A"],r["B"],r["title"])
                st.pyplot(fig); plt.close(fig)

            else:
                r=solve_projectile(v0,alpha,h0)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                style.result_band(
                    ("Range",f"{r['x_land']:.2f} m"),
                    ("Peak height",f"{r['y_max']:.2f} m"),
                )
                st.markdown('<div class="graph-label">Trajectory & range</div>',unsafe_allow_html=True)
                fig=plot_projectile(r); st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("x(t),y(t)")