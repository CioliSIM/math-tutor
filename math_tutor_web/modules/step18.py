import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt3(v): return f"({v[0]:.3f}, {v[1]:.3f}, {v[2]:.3f})"


# ── VECTORS ───────────────────────────────────────────────────────────────────

def solve_vectors(v, w, u):
    steps = []
    def add(l, bo, va=""): steps.append((l, bo, va))

    v=np.array(v,dtype=float); w=np.array(w,dtype=float); u=np.array(u,dtype=float)

    add("Vectors in 3D space",
        """A vector v=(x,y,z) has three components — one per axis.<br>
It represents direction and magnitude simultaneously.<br><br>
Vectors are the natural language of 3D geometry:
forces, velocities, fields — all vectors.""",
        "warm")

    s=v+w; d=v-w
    add("Addition & Subtraction",
        f"v+w = {fmt3(s)}<br>v−w = {fmt3(d)}")

    mv=np.linalg.norm(v); mw=np.linalg.norm(w)
    add("Modulus — Pythagoras in 3D",
        f"|v| = √(x²+y²+z²) = <strong>{mv:.4f}</strong><br>"
        f"|w| = <strong>{mw:.4f}</strong>"
        +("<br><br>Unit vector v̂ = v/|v| = "+fmt3(v/mv) if mv>1e-10 else ""))

    dot=np.dot(v,w)
    body=f"v·w = {v[0]:g}·{w[0]:g}+{v[1]:g}·{w[1]:g}+{v[2]:g}·{w[2]:g} = <strong>{dot:.4f}</strong>"
    if mv>1e-10 and mw>1e-10:
        cos_t=max(-1,min(1,dot/(mv*mw))); theta=math.degrees(math.acos(cos_t))
        body+=f"<br><br>θ = arccos(v·w / |v||w|) = <strong>{theta:.4f}°</strong>"
        body+=("<br>v·w=0 → <strong>PERPENDICULAR</strong> ✓" if abs(dot)<1e-10 else "")
    add("Dot product — cos(θ) = v·w / |v||w|", body)

    cross=np.cross(v,w); area=np.linalg.norm(cross)
    add("Cross product — perpendicular vector",
        f"""v×w = <strong>{fmt3(cross)}</strong><br><br>
|v×w| = {area:.4f} = area of parallelogram formed by v and w<br>
Area of triangle = {area/2:.4f}<br><br>
Verify: (v×w)·v = {np.dot(cross,v):.2e} ≈ 0 ✓ &nbsp;·&nbsp; (v×w)·w = {np.dot(cross,w):.2e} ≈ 0 ✓""",
        "sage")

    triple=np.dot(v,np.cross(w,u))
    coplanar=abs(triple)<1e-10
    add("Triple product — volume of parallelepiped",
        f"v·(w×u) = <strong>{triple:.6f}</strong><br><br>"
        +("= 0 → v, w, u are <strong>COPLANAR</strong> — all in the same plane." if coplanar else
          f"Volume = |{triple:.4f}| = {abs(triple):.4f}<br>v, w, u are NOT coplanar."),
        "sage" if coplanar else "")

    return {"steps":steps,"v":v,"w":w,"cross":cross}


def plot_vectors(v, w, cross):
    fig=plt.figure(figsize=(6,6)); fig.patch.set_facecolor("#fdfaf5")
    ax=fig.add_subplot(111,projection="3d"); ax.set_facecolor("#fdfaf5")
    def draw(vec,col,lbl):
        ax.quiver(0,0,0,vec[0],vec[1],vec[2],color=col,linewidth=2,
                  arrow_length_ratio=0.15,label=lbl)
    draw(v,"#e8602a","v"); draw(w,"#3d6b5e","w")
    draw(cross,"#c8a96e",f"v×w")
    corners=np.array([np.zeros(3),v,v+w,w,np.zeros(3)])
    ax.plot(corners[:,0],corners[:,1],corners[:,2],color="#b0a090",linewidth=1,
            linestyle="--",alpha=0.5)
    lim=max(np.max(np.abs(v)),np.max(np.abs(w)),np.max(np.abs(cross))*0.5,1)+0.5
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.set_zlim(-lim,lim)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.legend(fontsize=8); ax.set_title("Vectors in 3D",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── LINES ─────────────────────────────────────────────────────────────────────

def solve_lines(p1, d1, p2, d2):
    steps = []
    def add(l, bo, va=""): steps.append((l, bo, va))
    p1=np.array(p1,dtype=float); d1=np.array(d1,dtype=float)
    p2=np.array(p2,dtype=float); d2=np.array(d2,dtype=float)

    add("Lines in 3D space",
        """A line = point + direction:<br>
<span class="mf">x=x₀+at, y=y₀+bt, z=z₀+ct</span><br><br>
In 3D, two lines can be: coincident, parallel, intersecting, or <strong>skew</strong>.<br>
Skew lines: not parallel, never meet. Impossible in 2D — unique to 3D.""",
        "warm")

    cross_d=np.cross(d1,d2); mag_c=np.linalg.norm(cross_d)
    parallel=mag_c<1e-10
    add("Step 1 — Are they parallel? (d1×d2=0?)",
        f"d1×d2 = {fmt3(cross_d)}, |d1×d2| = {mag_c:.6f}<br>"
        +("= 0 → parallel or coincident." if parallel else "≠ 0 → NOT parallel."))

    if parallel:
        diff=p2-p1; check=np.cross(diff,d1)
        if np.linalg.norm(check)<1e-10:
            add("Result","Lines are <strong>COINCIDENT</strong>.","sage")
        else:
            dist=np.linalg.norm(check)/np.linalg.norm(d1)
            add("Result",f"Lines are <strong>PARALLEL</strong>. Distance = {dist:.4f}","error")
    else:
        diff=p2-p1; triple=np.dot(diff,cross_d)
        add("Step 2 — Do they intersect? ((p2−p1)·(d1×d2)=0?)",
            f"(p2−p1)·(d1×d2) = {triple:.6f}<br>"
            +("= 0 → INTERSECT." if abs(triple)<1e-10 else "≠ 0 → SKEW."))

        if abs(triple)<1e-10:
            A_mat=np.array([[d1[0],-d2[0]],[d1[1],-d2[1]],[d1[2],-d2[2]]])
            b_vec=p2-p1
            ts=np.linalg.lstsq(A_mat,b_vec,rcond=None)[0]
            pt=p1+ts[0]*d1
            add("Intersection point",f"<strong>{fmt3(pt)}</strong>","sage")
        else:
            dist=abs(triple)/mag_c
            add("Skew lines — distance",
                f"d = |(p2−p1)·(d1×d2)| / |d1×d2| = |{triple:.4f}|/{mag_c:.4f} = <strong>{dist:.4f}</strong><br>"
                "This is the length of the common perpendicular — the unique segment meeting both lines at 90°.",
                "sage")

    return {"steps":steps,"p1":p1,"d1":d1,"p2":p2,"d2":d2}


def plot_lines(p1, d1, p2, d2):
    fig=plt.figure(figsize=(6,6)); fig.patch.set_facecolor("#fdfaf5")
    ax=fig.add_subplot(111,projection="3d"); ax.set_facecolor("#fdfaf5")
    t=np.linspace(-3,3,100)
    l1=np.array([p1+ti*d1 for ti in t]); l2=np.array([p2+ti*d2 for ti in t])
    ax.plot(l1[:,0],l1[:,1],l1[:,2],color="#e8602a",linewidth=2,label="Line 1")
    ax.plot(l2[:,0],l2[:,1],l2[:,2],color="#3d6b5e",linewidth=2,label="Line 2")
    ax.scatter(*p1,color="#e8602a",s=50,zorder=5)
    ax.scatter(*p2,color="#3d6b5e",s=50,zorder=5)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.legend(fontsize=8); ax.set_title("Lines in 3D",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── PLANES ────────────────────────────────────────────────────────────────────

def solve_plane_point_normal(x0,y0,z0,a,b,c):
    steps=[]
    def add(l,bo,va=""): steps.append((l,bo,va))
    d=-(a*x0+b*y0+c*z0)
    add("Plane from point and normal vector",
        """A plane is completely determined by a point and a normal vector.<br><br>
<span class="mf">a(x−x₀)+b(y−y₀)+c(z−z₀)=0 &nbsp;→&nbsp; ax+by+cz+d=0</span><br><br>
(a,b,c) is the normal — every vector in the plane is perpendicular to it.""",
        "warm")
    add("Equation",
        f"Normal: ({a:g},{b:g},{c:g}) &nbsp;·&nbsp; Point: ({x0:g},{y0:g},{z0:g})<br><br>"
        f"<span class='mf'>{a:g}x + {b:g}y + {c:g}z + {d:.4f} = 0</span>","sage")
    return {"steps":steps,"a":a,"b":b,"c":c,"d":d}


def solve_plane_three_points(A,B,C):
    steps=[]
    def add(l,bo,va=""): steps.append((l,bo,va))
    A=np.array(A,dtype=float); B=np.array(B,dtype=float); C=np.array(C,dtype=float)
    AB=B-A; AC=C-A; n=np.cross(AB,AC)
    add("Plane through three points",
        "Build two vectors in the plane (AB and AC), then n=AB×AC gives the normal.",
        "warm")
    if np.linalg.norm(n)<1e-10:
        add("Error","Points are collinear — no unique plane.","error")
        return {"steps":steps,"valid":False}
    d=-(n[0]*A[0]+n[1]*A[1]+n[2]*A[2])
    checks="<br>".join(
        f"{lbl}: {n[0]*P[0]+n[1]*P[1]+n[2]*P[2]+d:.2e} ≈ 0 ✓"
        for P,lbl in [(A,"A"),(B,"B"),(C,"C")]
    )
    add("Result",
        f"AB = {fmt3(AB)}<br>AC = {fmt3(AC)}<br>n = AB×AC = {fmt3(n)}<br><br>"
        f"<span class='mf'>{n[0]:.4f}x + {n[1]:.4f}y + {n[2]:.4f}z + {d:.4f} = 0</span><br><br>"
        f"Verify:<br>{checks}","sage")
    return {"steps":steps,"a":n[0],"b":n[1],"c":n[2],"d":d,"valid":True,
            "points":[A,B,C]}


def solve_plane_angle(a1,b1,c1,a2,b2,c2):
    steps=[]
    def add(l,bo,va=""): steps.append((l,bo,va))
    n1=np.array([a1,b1,c1],dtype=float); n2=np.array([a2,b2,c2],dtype=float)
    dot=np.dot(n1,n2); cos_t=min(1,abs(dot)/(np.linalg.norm(n1)*np.linalg.norm(n2)))
    theta=math.degrees(math.acos(cos_t))
    add("Angle between planes",
        "The angle between two planes = the angle between their normal vectors.<br>"
        "We take the acute angle (≤ 90°).",
        "warm")
    verdict=("→ PARALLEL" if theta<1e-4 else "→ PERPENDICULAR ✓" if abs(theta-90)<1e-2 else f"→ meet at {theta:.4f}°")
    add("Result",
        f"n1·n2 = {dot:.4f}<br>"
        f"θ = arccos(|n1·n2|/|n1||n2|) = <strong>{theta:.4f}°</strong> {verdict}",
        "sage")
    return {"steps":steps}


def solve_point_to_plane(a,b,c,D,px,py,pz):
    steps=[]
    def add(l,bo,va=""): steps.append((l,bo,va))
    add("Distance from point to plane",
        "<span class='mf'>d = |ax₀+by₀+cz₀+D| / √(a²+b²+c²)</span><br><br>"
        "Numerator = how much the point violates the plane equation.<br>"
        "Denominator = length of normal (normalizes to perpendicular distance).",
        "warm")
    num=abs(a*px+b*py+c*pz+D); den=math.sqrt(a**2+b**2+c**2); dist=num/den
    add("Result",
        f"Numerator: |{a:g}·{px:g}+{b:g}·{py:g}+{c:g}·{pz:g}+{D:g}| = {num:.4f}<br>"
        f"Denominator: √{a**2+b**2+c**2:.4f} = {den:.4f}<br>"
        f"d = <strong>{dist:.4f}</strong>"
        +("<br>Point lies ON the plane." if dist<1e-10 else ""),"sage")
    return {"steps":steps}


def plot_plane_fig(a,b,c,d,points=None):
    fig=plt.figure(figsize=(6,6)); fig.patch.set_facecolor("#fdfaf5")
    ax=fig.add_subplot(111,projection="3d"); ax.set_facecolor("#fdfaf5")
    xx,yy=np.meshgrid(np.linspace(-3,3,20),np.linspace(-3,3,20))
    if abs(c)>1e-10: zz=(-a*xx-b*yy-d)/c
    else: zz=np.zeros_like(xx)
    ax.plot_surface(xx,yy,zz,alpha=0.25,color="#3d6b5e")
    z0=float(-d/c) if abs(c)>1e-10 else 0
    ax.quiver(0,0,z0,a,b,c,color="#e8602a",linewidth=2,arrow_length_ratio=0.15,label="Normal n")
    if points:
        for pt in points: ax.scatter(*pt,color="#c8a96e",s=80,zorder=5)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.legend(fontsize=8); ax.set_title(f"{a:.2f}x+{b:.2f}y+{c:.2f}z+{d:.2f}=0",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── INTERSECTIONS ─────────────────────────────────────────────────────────────

def solve_line_plane(px,py,pz,dx,dy,dz,a,b,c,D):
    steps=[]
    def add(l,bo,va=""): steps.append((l,bo,va))
    P=np.array([px,py,pz],dtype=float); dv=np.array([dx,dy,dz],dtype=float)
    n=np.array([a,b,c],dtype=float); nd=np.dot(n,dv)
    add("Line-plane intersection",
        "Substitute the parametric line into the plane equation and solve for t.",
        "warm")
    const=np.dot(n,P)+D
    add("Substitution",
        f"{const:.4f} + {nd:.4f}·t = 0")
    if abs(nd)<1e-10:
        if abs(const)<1e-10:
            add("Result","Line lies <strong>INSIDE</strong> the plane.","sage")
        else:
            dist=abs(const)/np.linalg.norm(n)
            add("Result",f"Line is <strong>PARALLEL</strong> to the plane. Distance={dist:.4f}","error")
    else:
        t=-const/nd; pt=P+t*dv
        check=a*pt[0]+b*pt[1]+c*pt[2]+D
        add("Intersection",
            f"t = {t:.4f}<br>Point: <strong>{fmt3(pt)}</strong><br>"
            f"Verify on plane: {check:.2e} ≈ 0 ✓","sage")
    return {"steps":steps}


def solve_dist_point_line(ax,ay,az,vx,vy,vz,px,py,pz):
    steps=[]
    def add(l,bo,va=""): steps.append((l,bo,va))
    A=np.array([ax,ay,az],dtype=float); v=np.array([vx,vy,vz],dtype=float)
    P=np.array([px,py,pz],dtype=float)
    AP=P-A; cross=np.cross(AP,v); dist=np.linalg.norm(cross)/np.linalg.norm(v)
    add("Distance from point to line in 3D",
        "<span class='mf'>d = |AP×v| / |v|</span><br><br>"
        "|AP×v| = area of parallelogram = base×height = |v|×distance<br>"
        "So distance = |AP×v| / |v|.",
        "warm")
    add("Result",
        f"AP = {fmt3(AP)}<br>AP×v = {fmt3(cross)}<br>"
        f"|AP×v| = {np.linalg.norm(cross):.4f}, |v| = {np.linalg.norm(v):.4f}<br>"
        f"d = <strong>{dist:.4f}</strong>","sage")
    return {"steps":steps}


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Vectors","Lines in space","Plane from point+normal",
             "Plane through 3 points","Angle between planes",
             "Point to plane distance","Line-plane intersection",
             "Point to line distance"],
            key="3d_topic")

        def v3(label, defaults, key_prefix):
            c1,c2,c3=st.columns(3)
            x=c1.number_input(f"{label} x",value=float(defaults[0]),step=1.0,key=f"{key_prefix}_x")
            y=c2.number_input(f"{label} y",value=float(defaults[1]),step=1.0,key=f"{key_prefix}_y")
            z=c3.number_input(f"{label} z",value=float(defaults[2]),step=1.0,key=f"{key_prefix}_z")
            return x,y,z

        if topic == "Vectors":
            vx,vy,vz=v3("v",[1,2,3],"vv")
            wx,wy,wz=v3("w",[4,0,-1],"vw")
            ux,uy,uz=v3("u (for triple product)",[1,1,0],"vu")

        elif topic == "Lines in space":
            p1x,p1y,p1z=v3("Line 1 point",[0,0,0],"l1p")
            d1x,d1y,d1z=v3("Line 1 direction",[1,1,0],"l1d")
            p2x,p2y,p2z=v3("Line 2 point",[1,0,1],"l2p")
            d2x,d2y,d2z=v3("Line 2 direction",[1,-1,0],"l2d")

        elif topic == "Plane from point+normal":
            x0,y0,z0=v3("Point",[1,2,3],"pn_pt")
            a,b,c=v3("Normal",[1,-1,2],"pn_n")

        elif topic == "Plane through 3 points":
            ax_,ay_,az_=v3("A",[0,0,0],"pp_A")
            bx_,by_,bz_=v3("B",[1,0,0],"pp_B")
            cx_,cy_,cz_=v3("C",[0,1,1],"pp_C")

        elif topic == "Angle between planes":
            a1,b1,c1=v3("Plane 1 normal",[1,0,0],"ang1")
            a2,b2,c2=v3("Plane 2 normal",[0,1,0],"ang2")

        elif topic == "Point to plane distance":
            a,b,c=v3("Plane normal",[1,1,1],"ptpl_n")
            D=st.number_input("Plane D (ax+by+cz+D=0)",value=-3.0,step=1.0,key="ptpl_D")
            px_,py_,pz_=v3("Point P",[1,1,1],"ptpl_P")

        elif topic == "Line-plane intersection":
            plx,ply,plz=v3("Line point",[0,0,0],"lp_pt")
            dlx,dly,dlz=v3("Line direction",[1,1,1],"lp_d")
            a,b,c=v3("Plane normal",[1,0,-1],"lp_n")
            Dlp=st.number_input("Plane D",value=-2.0,step=1.0,key="lp_D")

        else:  # Point to line
            alx,aly,alz=v3("Line point A",[0,0,0],"ptl_A")
            vlx,vly,vlz=v3("Line direction v",[1,0,0],"ptl_v")
            plx2,ply2,plz2=v3("External point P",[1,2,3],"ptl_P")

        solve_btn=st.button("Compute →",key="3d_solve")
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Vectors: v=(1,2,3), w=(4,0,−1)<br>
    Lines: check for skew vs intersecting<br>
    Plane (3 pts): A(0,0,0) B(1,0,0) C(0,1,1)<br>
    Angle: (1,0,0) vs (0,1,0) → 90°
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Vectors":
                r=solve_vectors([vx,vy,vz],[wx,wy,wz],[ux,uy,uz])
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">3D vectors</div>',unsafe_allow_html=True)
                fig=plot_vectors(r["v"],r["w"],r["cross"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Lines in space":
                r=solve_lines([p1x,p1y,p1z],[d1x,d1y,d1z],[p2x,p2y,p2z],[d2x,d2y,d2z])
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Lines in 3D</div>',unsafe_allow_html=True)
                fig=plot_lines(r["p1"],r["d1"],r["p2"],r["d2"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Plane from point+normal":
                r=solve_plane_point_normal(x0,y0,z0,a,b,c)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Plane</div>',unsafe_allow_html=True)
                fig=plot_plane_fig(r["a"],r["b"],r["c"],r["d"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Plane through 3 points":
                r=solve_plane_three_points([ax_,ay_,az_],[bx_,by_,bz_],[cx_,cy_,cz_])
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if r.get("valid"):
                    st.markdown('<div class="graph-label">Plane</div>',unsafe_allow_html=True)
                    fig=plot_plane_fig(r["a"],r["b"],r["c"],r["d"],r["points"])
                    st.pyplot(fig); plt.close(fig)

            elif topic == "Angle between planes":
                r=solve_plane_angle(a1,b1,c1,a2,b2,c2)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Point to plane distance":
                r=solve_point_to_plane(a,b,c,D,px_,py_,pz_)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Line-plane intersection":
                r=solve_line_plane(plx,ply,plz,dlx,dly,dlz,a,b,c,Dlp)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            else:
                r=solve_dist_point_line(alx,aly,alz,vlx,vly,vlz,plx2,ply2,plz2)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
        else:
            style.empty_state("xyz")