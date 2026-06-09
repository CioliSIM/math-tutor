import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt(z):
    r, i = z.real, z.imag
    if abs(i) < 1e-10: return f"{r:.4f}"
    if abs(r) < 1e-10: return f"{i:.4f}i"
    return f"{r:.4f} + {i:.4f}i" if i >= 0 else f"{r:.4f} − {abs(i):.4f}i"

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)


# ── OPERATIONS ────────────────────────────────────────────────────────────────

def solve_operations(a, b, c, d):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    z1, z2 = complex(a, b), complex(c, d)
    s, diff, prod = z1+z2, z1-z2, z1*z2

    add("Complex numbers — the idea",
        """A complex number z = a + bi, where <span class="mf">i² = −1</span>.<br><br>
That single rule — i² = −1 — is everything.
All operations follow from normal algebra with this substitution applied at the end.<br><br>
Geometrically: a complex number is a <strong>point on a plane</strong>.
The real numbers are just one line through it.""",
        "warm")

    add("Your numbers",
        f"z₁ = {a:g} + {b:g}i = <strong>{fmt(z1)}</strong><br>"
        f"z₂ = {c:g} + {d:g}i = <strong>{fmt(z2)}</strong>")

    add("Addition &amp; Subtraction",
        f"z₁ + z₂ = ({a:g}+{c:g}) + ({b:g}+{d:g})i = <strong>{fmt(s)}</strong><br>"
        f"z₁ − z₂ = ({a:g}−{c:g}) + ({b:g}−{d:g})i = <strong>{fmt(diff)}</strong>")

    add("Multiplication — expand then replace i²=−1",
        f"z₁·z₂ = ({a:g}+{b:g}i)({c:g}+{d:g}i)<br>"
        f"&emsp;= {a*c:g} + {a*d:g}i + {b*c:g}i + {b*d:g}i²<br>"
        f"&emsp;= {a*c:g} + {a*d:g}i + {b*c:g}i + {b*d:g}·(−1)<br>"
        f"&emsp;= ({a*c:g}−{b*d:g}) + ({a*d:g}+{b*c:g})i<br>"
        f"&emsp;= <strong>{fmt(prod)}</strong>")

    z1c = z1.conjugate()
    add("Conjugate — flip the imaginary sign",
        f"z̄₁ = {fmt(z1c)}<br><br>"
        f"z₁·z̄₁ = {a:g}² + {b:g}² = <strong>{a**2+b**2:.4f}</strong> (always real ✓)<br>"
        "This is the trick that makes division possible.")

    if abs(z2) > 1e-12:
        quot = z1 / z2
        add("Division — multiply by conjugate of denominator",
            f"z₁/z₂ = (z₁·z̄₂) / (z₂·z̄₂) = (z₁·z̄₂) / {c**2+d**2:.4f}<br>"
            f"= <strong>{fmt(quot)}</strong>")
    else:
        add("Division", "z₂ = 0 — division undefined.", "error")

    add("Modulus — distance from origin",
        f"|z₁| = √({a:g}² + {b:g}²) = <strong>{abs(z1):.4f}</strong><br>"
        f"|z₂| = √({c:g}² + {d:g}²) = <strong>{abs(z2):.4f}</strong><br><br>"
        f"Beautiful property: |z₁·z₂| = |z₁|·|z₂|<br>"
        f"{abs(z1):.4f}·{abs(z2):.4f} = {abs(z1)*abs(z2):.4f} = |z₁·z₂| = {abs(prod):.4f} ✓",
        "sage")

    return {"steps": steps, "numbers": [z1,z2,s,prod],
            "labels": ["z₁","z₂","z₁+z₂","z₁·z₂"]}


# ── POLAR FORM ────────────────────────────────────────────────────────────────

def solve_polar(a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    z     = complex(a, b)
    r     = abs(z)
    theta = math.atan2(b, a)

    add("Polar form — distance and angle",
        """Instead of coordinates (a, b), describe a complex number by:<br><br>
<strong>r = |z|</strong> — the modulus (distance from origin)<br>
<strong>θ = arg(z)</strong> — the argument (angle with real axis)<br><br>
<span class="mf">z = r·(cos θ + i·sin θ) = r·e^(iθ)</span><br><br>
The second form uses <strong>Euler's formula</strong>: e^(iθ) = cos θ + i·sin θ<br>
This connects exponentials, trigonometry, and complex numbers — three things in one.""",
        "warm")

    add("Step 1 — Modulus",
        f"r = √({a:g}² + {b:g}²) = √{a**2+b**2:.4f} = <strong>{r:.4f}</strong>")

    add("Step 2 — Argument",
        f"θ = atan2({b:g}, {a:g}) = <strong>{theta:.4f} rad = {math.degrees(theta):.2f}°</strong><br><br>"
        "We use atan2 (not arctan) because arctan can't distinguish opposite quadrants.")

    add("Step 3 — Polar form",
        f"z = {r:.4f}·(cos({theta:.4f}) + i·sin({theta:.4f}))<br>"
        f"&emsp;= {r:.4f}·e^(i·{theta:.4f})<br><br>"
        f"Verify: r·cosθ = {r:.4f}·{math.cos(theta):.4f} = {r*math.cos(theta):.4f} (expected {a:g}) ✓<br>"
        f"&emsp;&emsp;&nbsp;&nbsp;r·sinθ = {r:.4f}·{math.sin(theta):.4f} = {r*math.sin(theta):.4f} (expected {b:g}) ✓",
        "sage")

    add("Euler's identity — the most beautiful formula",
        "Set θ = π:<br><br>"
        "<span class='mf' style='font-size:1.2rem;'>e^(iπ) + 1 = 0</span><br><br>"
        "Five of the most important constants — e, i, π, 1, 0 — in one equation.<br>"
        "Mathematicians consistently call this the most beautiful formula ever written.")

    return {"steps": steps, "z": z, "r": r, "theta": theta}


# ── DE MOIVRE ─────────────────────────────────────────────────────────────────

def solve_demoivre(a, b, n):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    z      = complex(a, b)
    r      = abs(z)
    theta  = math.atan2(b, a)
    r_n    = r**n
    theta_n = n * theta
    result = complex(r_n*math.cos(theta_n), r_n*math.sin(theta_n))
    direct = z**n

    add("De Moivre's theorem",
        """<span class="mf">(cosθ + i·sinθ)^n = cos(nθ) + i·sin(nθ)</span><br><br>
Raising a complex number to the n-th power:<br>
· Multiplies the argument by n → <strong>rotates</strong><br>
· Raises the modulus to n → <strong>scales</strong><br><br>
In polar form this is just the exponent rule: (e^(iθ))^n = e^(inθ). Obvious in polar, beautiful in Cartesian.""",
        "warm")

    add("Computing z^" + str(n),
        f"z = {fmt(z)} &nbsp;·&nbsp; r = {r:.4f}, θ = {math.degrees(theta):.2f}°<br><br>"
        f"r^{n} = {r:.4f}^{n} = <strong>{r_n:.4f}</strong><br>"
        f"{n}·θ = {n}·{math.degrees(theta):.2f}° = <strong>{math.degrees(theta_n):.2f}°</strong><br><br>"
        f"z^{n} = {r_n:.4f}·(cos{math.degrees(theta_n):.2f}° + i·sin{math.degrees(theta_n):.2f}°)<br>"
        f"&emsp;&nbsp;= <strong>{fmt(result)}</strong><br><br>"
        f"Direct check: {fmt(direct)} ✓", "sage")

    powers = [z**k for k in range(1, abs(n)+1)]
    labels = [f"z^{k}" for k in range(1, abs(n)+1)]
    rows   = "<br>".join(
        f"z^{k} = {fmt(z**k)} &nbsp;(r={abs(z**k):.3f}, θ={math.degrees(math.atan2((z**k).imag,(z**k).real)):.1f}°)"
        for k in range(1, min(abs(n)+1, 8))
    )
    add("All powers z^1 to z^" + str(abs(n)), rows)

    return {"steps": steps, "powers": powers, "labels": labels,
            "title": f"Powers of z={fmt(z)}"}


# ── NTH ROOTS ─────────────────────────────────────────────────────────────────

def solve_roots(a, b, n):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    z      = complex(a, b)
    r      = abs(z)
    theta  = math.atan2(b, a)
    r_root = r**(1/n)

    add("N-th roots — the regular polygon result",
        f"""Every complex number has exactly <strong>n</strong> distinct n-th roots.<br><br>
If z = r·e^(iθ), the n roots are:<br><br>
<span class="mf">zₖ = r^(1/n) · e^(i(θ+2πk)/n) &nbsp;&nbsp; k=0,1,…,n−1</span><br><br>
All roots have the <strong>same modulus</strong> r^(1/n).<br>
They are <strong>equally spaced</strong> at 360°/n apart.<br>
Geometrically: the n roots are the <strong>vertices of a regular {n}-gon</strong>.<br><br>
Roots of unity (z=1): a perfect regular polygon centered at the origin every time.""",
        "warm")

    add(f"Setup for z = {fmt(z)}",
        f"r = {r:.4f}, θ = {math.degrees(theta):.2f}°<br>"
        f"Each root has modulus: r^(1/{n}) = <strong>{r_root:.4f}</strong><br>"
        f"Angular spacing: 360°/{n} = <strong>{360/n:.2f}°</strong>")

    roots  = []
    labels = []
    root_lines = []
    for k in range(n):
        theta_k = (theta + 2*math.pi*k) / n
        zk = complex(r_root*math.cos(theta_k), r_root*math.sin(theta_k))
        roots.append(zk)
        labels.append(f"z{k}")
        check = zk**n
        root_lines.append(
            f"z{k}: angle=({math.degrees(theta):.1f}°+{k}·360°)/{n}="
            f"{math.degrees(theta_k):.2f}°  →  {fmt(zk)}  &nbsp;check: zₖ^{n}={fmt(check)} ✓"
        )
    add("The " + str(n) + " roots", "<br>".join(root_lines), "sage")

    return {"steps": steps, "roots": roots, "labels": labels,
            "r_root": r_root, "n": n, "z": z}


# ── EQUATIONS ─────────────────────────────────────────────────────────────────

def solve_equations(mode, a, b, c=0, w_re=0, w_im=0, n_eq=2):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    if mode == "quadratic":
        delta = b**2 - 4*a*c
        add("Closing the gaps real numbers left",
            """In Module 1 we stopped when Δ &lt; 0 and said 'no real solutions'.<br>
In the complex field, those equations DO have solutions — always two complex conjugate roots.<br><br>
The <strong>Fundamental Theorem of Algebra</strong>: every degree-n polynomial has exactly n roots in ℂ.<br>
Real numbers left gaps. Complex numbers fill them all.""",
            "warm")

        add("Discriminant",
            f"Δ = {b:g}² − 4·{a:g}·{c:g} = <strong>{delta:.4f}</strong>")

        if delta >= 0:
            x1 = (-b + math.sqrt(delta))/(2*a)
            x2 = (-b - math.sqrt(delta))/(2*a)
            add("Real roots (Δ ≥ 0)",
                f"x₁ = {x1:.4f}, x₂ = {x2:.4f}<br>"
                "These are real — same as Module 1.", "sage")
            return {"steps": steps, "numbers": [complex(x1), complex(x2)],
                    "labels": ["x₁","x₂"]}
        else:
            sq = math.sqrt(-delta)
            re_ = -b/(2*a); im_ = sq/(2*a)
            z1 = complex(re_, im_); z2 = complex(re_, -im_)
            add("Complex roots (Δ &lt; 0)",
                f"√Δ = √({delta:.4f}) = {sq:.4f}i<br><br>"
                f"x = (−{b:g} ± {sq:.4f}i) / {2*a:g}<br><br>"
                f"z₁ = <strong>{fmt(z1)}</strong><br>"
                f"z₂ = <strong>{fmt(z2)}</strong><br><br>"
                "Notice: z₁ and z₂ are complex conjugates — always happens with real coefficients.",
                "sage")
            checks = []
            for z, lbl in [(z1,"z₁"),(z2,"z₂")]:
                val = a*z**2 + b*z + c
                checks.append(f"{lbl}: {a:g}·z²+{b:g}·z+{c:g} = {fmt(val)} ≈ 0 ✓")
            add("Verify", "<br>".join(checks))
            return {"steps": steps, "numbers": [z1,z2],
                    "labels": ["z₁","z₂"],
                    "title": f"Complex roots of {a:g}x²+{b:g}x+{c:g}=0"}

    else:  # z^n = w
        w      = complex(w_re, w_im)
        r      = abs(w); theta = math.atan2(w_im, w_re)
        r_root = r**(1/n_eq)
        roots  = []
        labels = []
        for k in range(n_eq):
            theta_k = (theta + 2*math.pi*k) / n_eq
            zk = complex(r_root*math.cos(theta_k), r_root*math.sin(theta_k))
            roots.append(zk); labels.append(f"z{k}")
        add("Finding all solutions to z^" + str(n_eq) + " = " + fmt(w),
            "<br>".join(f"z{k} = {fmt(roots[k])}" for k in range(n_eq)),
            "sage")
        return {"steps": steps, "roots": roots, "labels": labels,
                "r_root": r_root, "n": n_eq, "z": w}


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_plane(numbers, labels, title="Complex Plane"):
    max_v = max((max(abs(z.real),abs(z.imag)) for z in numbers if z!=0), default=1)+1
    fig, ax = plt.subplots(figsize=(6,6))
    styled_ax(ax, fig); ax.set_aspect("equal")
    colors = ["#e8602a","#3d6b5e","#7b6fb0","#c8a96e","#e8602a","#3d6b5e"]
    for z, lbl, col in zip(numbers, labels, colors):
        ax.plot(z.real, z.imag, "o", color=col, markersize=10, zorder=5)
        ax.annotate(f"  {lbl}={fmt(z)}", (z.real,z.imag), fontsize=8.5,
                    color=col, fontfamily="serif")
        ax.plot([0,z.real],[0,z.imag], color=col, linewidth=1,
                linestyle="--", alpha=0.4)
    ax.set_xlim(-max_v,max_v); ax.set_ylim(-max_v,max_v)
    ax.set_xlabel("Real", color="#4a4540", fontsize=9)
    ax.set_ylabel("Imaginary", color="#4a4540", fontsize=9)
    ax.set_title(title, fontsize=10, color="#4a4540")
    plt.tight_layout(); return fig


def plot_polar_fig(z, r, theta):
    lim = max(r+1, 2.5)
    fig, ax = plt.subplots(figsize=(6,6))
    styled_ax(ax, fig); ax.set_aspect("equal")
    t = np.linspace(0,2*np.pi,400)
    ax.plot(np.cos(t),np.sin(t), color="#b0a090",linewidth=0.8,
            linestyle="--",alpha=0.5)
    ax.plot(r*np.cos(t),r*np.sin(t), color="#3d6b5e",linewidth=0.8,
            linestyle="--",alpha=0.4,label=f"r={r:.2f}")
    ax.annotate("", xy=(z.real,z.imag), xytext=(0,0),
                arrowprops=dict(arrowstyle="->",color="#e8602a",lw=2))
    ax.plot(z.real,z.imag,"o",color="#e8602a",markersize=10,zorder=5)
    ax.annotate(f"  z={fmt(z)}\n  r={r:.2f}, θ={math.degrees(theta):.1f}°",
                (z.real,z.imag),fontsize=8.5,color="#e8602a",fontfamily="serif")
    arc_t = np.linspace(0, theta if theta>=0 else theta+2*math.pi, 100)
    arc_r = r*0.3
    ax.plot(arc_r*np.cos(arc_t),arc_r*np.sin(arc_t),color="#3d6b5e",linewidth=1.5)
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_xlabel("Real",color="#4a4540",fontsize=9)
    ax.set_ylabel("Imaginary",color="#4a4540",fontsize=9)
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout(); return fig


def plot_roots_fig(roots, labels, r_root, n, original):
    lim = max(r_root+1, abs(original)+1, 2)
    fig, ax = plt.subplots(figsize=(6,6))
    styled_ax(ax, fig); ax.set_aspect("equal")
    t = np.linspace(0,2*np.pi,400)
    ax.plot(r_root*np.cos(t),r_root*np.sin(t),
            color="#3d6b5e",linewidth=1.5,linestyle="--",alpha=0.5)
    coords = [(z.real,z.imag) for z in roots]+[(roots[0].real,roots[0].imag)]
    ax.plot([c[0] for c in coords],[c[1] for c in coords],
            color="#c8a96e",linewidth=1,alpha=0.4)
    colors = ["#e8602a","#3d6b5e","#7b6fb0","#c8a96e",
              "#e8602a","#3d6b5e","#7b6fb0","#c8a96e"]
    for z,lbl,col in zip(roots,labels,colors):
        ax.plot(z.real,z.imag,"o",color=col,markersize=11,zorder=5)
        ax.annotate(f"  {lbl}\n  {fmt(z)}",(z.real,z.imag),
                    fontsize=8,color=col,fontfamily="serif")
    ax.plot(original.real,original.imag,"*",color="#c8a96e",
            markersize=14,label=f"z={fmt(original)}",zorder=6)
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_xlabel("Real",color="#4a4540",fontsize=9)
    ax.set_ylabel("Imaginary",color="#4a4540",fontsize=9)
    ax.set_title(f"The {n} roots — vertices of a regular {n}-gon",
                 fontsize=10,color="#4a4540")
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout(); return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>',
                    unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Operations","Polar form","De Moivre","N-th roots","Equations"],
            key="cx_topic")

        if topic == "Operations":
            c1,c2 = st.columns(2)
            a=c1.number_input("z₁ real",value=3.0,step=1.0,key="cx_a")
            b=c2.number_input("z₁ imag",value=4.0,step=1.0,key="cx_b")
            cv=c1.number_input("z₂ real",value=1.0,step=1.0,key="cx_c")
            d=c2.number_input("z₂ imag",value=-2.0,step=1.0,key="cx_d")
            preview=f"z₁={a:g}+{b:g}i &nbsp;·&nbsp; z₂={cv:g}+{d:g}i"

        elif topic == "Polar form":
            a=st.number_input("Real part a",value=1.0,step=0.5,key="cx_pa")
            b=st.number_input("Imag part b",value=1.0,step=0.5,key="cx_pb")
            preview=f"z = {a:g}+{b:g}i"

        elif topic == "De Moivre":
            a=st.number_input("Real part a",value=1.0,step=0.5,key="cx_da")
            b=st.number_input("Imag part b",value=1.0,step=0.5,key="cx_db")
            nv=st.number_input("Power n",value=4,min_value=1,step=1,key="cx_dn")
            preview=f"({a:g}+{b:g}i)^{nv}"

        elif topic == "N-th roots":
            a=st.number_input("Real part a",value=1.0,step=0.5,key="cx_ra")
            b=st.number_input("Imag part b",value=0.0,step=0.5,key="cx_rb")
            nv=st.number_input("Degree n",value=3,min_value=1,step=1,key="cx_rn")
            preview=f"z^{nv} = {a:g}+{b:g}i"

        else:  # Equations
            eq_mode = st.selectbox("Type",["Quadratic (Δ<0)","z^n = w"],key="cx_em")
            if eq_mode == "Quadratic (Δ<0)":
                a=st.number_input("a",value=1.0,step=1.0,key="cx_qa")
                b=st.number_input("b",value=2.0,step=1.0,key="cx_qb")
                c_eq=st.number_input("c",value=5.0,step=1.0,key="cx_qc")
                preview=f"{a:g}x²+{b:g}x+{c_eq:g}=0"
            else:
                w_re=st.number_input("w real",value=1.0,step=0.5,key="cx_wr")
                w_im=st.number_input("w imag",value=0.0,step=0.5,key="cx_wi")
                n_eq=st.number_input("n",value=3,min_value=1,step=1,key="cx_wn")
                preview=f"z^{n_eq} = {w_re:g}+{w_im:g}i"

        st.markdown(
            f'<div class="eq-display" style="font-size:0.95rem;">{preview}</div>',
            unsafe_allow_html=True)

        solve_btn = st.button("Compute →", key="cx_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Operations: <code>z₁=3+4i, z₂=1−2i</code><br>
    Polar: <code>a=1, b=1</code> → r=√2, θ=45°<br>
    De Moivre: <code>1+i, n=8</code> → back to 16<br>
    Roots: <code>z=1, n=6</code> → regular hexagon<br>
    Equations: <code>x²+2x+5=0</code> → Δ&lt;0
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Operations":
                r = solve_operations(a, b, cv, d)
                for lbl, body, var in r["steps"]: style.step(lbl, body, var)
                st.markdown('<div class="graph-label">Complex plane</div>', unsafe_allow_html=True)
                fig = plot_plane(r["numbers"], r["labels"])
                st.pyplot(fig); plt.close(fig)

            elif topic == "Polar form":
                r = solve_polar(a, b)
                for lbl, body, var in r["steps"]: style.step(lbl, body, var)
                style.result_band(
                    ("z", fmt(r["z"])),
                    ("r = |z|", f"{r['r']:.4f}"),
                    ("θ = arg(z)", f"{math.degrees(r['theta']):.2f}°"),
                )
                st.markdown('<div class="graph-label">Polar representation</div>', unsafe_allow_html=True)
                fig = plot_polar_fig(r["z"], r["r"], r["theta"])
                st.pyplot(fig); plt.close(fig)

            elif topic == "De Moivre":
                r = solve_demoivre(a, b, int(nv))
                for lbl, body, var in r["steps"]: style.step(lbl, body, var)
                st.markdown('<div class="graph-label">Powers on the complex plane</div>', unsafe_allow_html=True)
                fig = plot_plane(r["powers"], r["labels"], r["title"])
                st.pyplot(fig); plt.close(fig)

            elif topic == "N-th roots":
                r = solve_roots(a, b, int(nv))
                for lbl, body, var in r["steps"]: style.step(lbl, body, var)
                st.markdown('<div class="graph-label">Roots — regular polygon</div>', unsafe_allow_html=True)
                fig = plot_roots_fig(r["roots"], r["labels"], r["r_root"], r["n"], r["z"])
                st.pyplot(fig); plt.close(fig)

            else:
                if eq_mode == "Quadratic (Δ<0)":
                    r = solve_equations("quadratic", a, b, c_eq)
                else:
                    r = solve_equations("zn", 0, 0, w_re=w_re, w_im=w_im, n_eq=int(n_eq))
                for lbl, body, var in r["steps"]: style.step(lbl, body, var)
                if "numbers" in r:
                    st.markdown('<div class="graph-label">Complex roots</div>', unsafe_allow_html=True)
                    fig = plot_plane(r["numbers"], r["labels"],
                                     r.get("title","Complex roots"))
                    st.pyplot(fig); plt.close(fig)
                elif "roots" in r:
                    st.markdown('<div class="graph-label">Roots</div>', unsafe_allow_html=True)
                    fig = plot_roots_fig(r["roots"], r["labels"],
                                         r["r_root"], r["n"], r["z"])
                    st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("i")