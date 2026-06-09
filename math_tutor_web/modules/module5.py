import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

import style

x = sp.Symbol('x')


# ── Pure logic ────────────────────────────────────────────────────────────────

def analyze(expr_str):
    steps   = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    try:
        expr = sp.sympify(expr_str)
    except Exception as e:
        return {"error": str(e), "steps": [], "expr": None,
                "zeros": [], "derivative": None}

    # ── Step 0: overview ─────────────────────────────────────────────────
    add("The function",
        f"""<span class="mf" style="display:block;text-align:center;
font-size:1.3rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
  f(x) = {sp.latex(expr)}
</span><br>
A function is more than a formula — it has a <strong>personality</strong>.
We will find where it lives, whether it is symmetric, where it crosses zero,
and whether it is climbing or falling.""",
        "warm")

    # ── Step 1: domain ────────────────────────────────────────────────────
    try:
        domain = sp.calculus.util.continuous_domain(expr, x, sp.S.Reals)
        domain_str = str(domain)
    except Exception:
        domain     = sp.S.Reals
        domain_str = "ℝ  (could not compute exactly — check by hand)"

    add("Step 1 — Domain",
        f"""The domain is where the function is <strong>allowed to exist</strong>.
Three things can break a function:<br><br>
&emsp;· A zero in the denominator — undefined<br>
&emsp;· A negative under a square root — not real<br>
&emsp;· A non-positive argument in a logarithm — undefined<br><br>
<strong>Domain:</strong> <code>{domain_str}</code>""")

    # ── Step 2: parity ────────────────────────────────────────────────────
    f_neg = sp.simplify(expr.subs(x, -x))
    if sp.simplify(f_neg - expr) == 0:
        parity_verdict = "<strong>EVEN</strong> — f(−x) = f(x).<br>Fold the graph along the y-axis: both halves match."
        parity_var = "sage"
    elif sp.simplify(f_neg + expr) == 0:
        parity_verdict = "<strong>ODD</strong> — f(−x) = −f(x).<br>Rotate the graph 180° around the origin: it looks the same."
        parity_var = "sage"
    else:
        parity_verdict = "<strong>No parity</strong> — neither condition holds. The function is asymmetric."
        parity_var = ""

    add("Step 2 — Parity",
        f"""Substitute −x and compare with f(x):<br><br>
f(−x) = <code>{f_neg}</code><br><br>
{parity_verdict}""",
        parity_var)

    # ── Step 3: zeros ─────────────────────────────────────────────────────
    try:
        zeros_raw  = sp.solve(expr, x)
        zeros_real = [z for z in zeros_raw if z.is_real]
        zeros_cplx = [z for z in zeros_raw if not z.is_real]

        if zeros_real:
            z_lines = "<br>".join(
                f"x = {z} &nbsp;≈ &nbsp;<strong>{float(z):.4f}</strong> ✓"
                for z in zeros_real
            )
        else:
            z_lines = "No real zeros — the graph never touches the x-axis."

        cplx_note = (
            f"<br><br>Also {len(zeros_cplx)} complex root(s) — not visible on the real graph."
            if zeros_cplx else ""
        )
        add("Step 3 — Zeros",
            f"""Where does f(x) = 0? These are the x-intercepts.<br><br>
{z_lines}{cplx_note}""")
    except Exception:
        zeros_real = []
        add("Step 3 — Zeros",
            "Could not solve symbolically. Check the graph for approximate x-intercepts.")

    # ── Step 4: sign ──────────────────────────────────────────────────────
    try:
        pos = sp.solve(expr > 0, x)
        neg = sp.solve(expr < 0, x)
        add("Step 4 — Sign",
            f"""Where is f(x) above the x-axis (positive) and where below (negative)?
The zeros from Step 3 are the only places where the sign can change.<br><br>
<strong>f(x) &gt; 0</strong> &nbsp;(above x-axis): &nbsp;<code>{pos}</code><br>
<strong>f(x) &lt; 0</strong> &nbsp;(below x-axis): &nbsp;<code>{neg}</code>""")
    except Exception:
        add("Step 4 — Sign",
            "Could not compute the sign automatically. The graph shows it visually.")

    # ── Step 5: monotonicity ──────────────────────────────────────────────
    try:
        deriv = sp.diff(expr, x)
        deriv_s = sp.simplify(deriv)

        stat_pts = sp.solve(deriv, x)
        stat_real = [s for s in stat_pts if s.is_real]

        if stat_real:
            stat_lines = "<br>".join(
                f"x = {s} &nbsp;→ &nbsp;f({s}) = {sp.simplify(expr.subs(x,s))} "
                f"≈ ({float(s):.3f}, {float(expr.subs(x,s)):.3f})"
                for s in stat_real
            )
        else:
            stat_lines = "No stationary points — strictly monotone throughout."

        try:
            inc = sp.solve(deriv > 0, x)
            dec = sp.solve(deriv < 0, x)
            mono_lines = (
                f"<br><br><strong>Increasing</strong> on: <code>{inc}</code><br>"
                f"<strong>Decreasing</strong> on: <code>{dec}</code>"
            )
        except Exception:
            mono_lines = ""

        add("Step 5 — Monotonicity",
            f"""f′(x) measures how fast the function is climbing or falling.<br><br>
<span class="mf">f′(x) = {deriv_s}</span><br><br>
<strong>Stationary points</strong> — where f′(x) = 0:<br>
{stat_lines}{mono_lines}""")

        derivative = deriv_s
    except Exception:
        derivative = None
        add("Step 5 — Monotonicity",
            "Could not compute the derivative automatically.")

    return {"steps": steps, "expr": expr, "zeros": zeros_real,
            "derivative": derivative, "domain_str": domain_str, "error": None}


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(expr, zeros_real):
    f_num = sp.lambdify(x, expr, "numpy")

    x_vals = np.linspace(-10, 10, 1000)
    with np.errstate(divide="ignore", invalid="ignore"):
        y_vals = np.array(f_num(x_vals), dtype=float)
        y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    ax.plot(x_vals, y_vals, color="#e8602a", linewidth=2.2,
            label=f"f(x) = {expr}")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)

    for z in zeros_real:
        try:
            zf = float(z)
            ax.plot(zf, 0, "o", color="#c8a96e", markersize=9, zorder=5)
            ax.annotate(f"x={zf:.2f}", (zf, 0),
                        textcoords="offset points", xytext=(0, 13),
                        ha="center", fontsize=9, fontfamily="serif",
                        color="#4a4540")
        except Exception:
            pass

    ax.set_ylim(-10, 10)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.set_xlabel("x",    color="#4a4540", fontsize=9)
    ax.set_ylabel("f(x)", color="#4a4540", fontsize=9)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    plt.tight_layout()
    return fig


# ── Render ────────────────────────────────────────────────────────────────────

def render_steps(r):
    if r["error"]:
        style.step("Error", f"Could not parse the expression: <code>{r['error']}</code>", "error")
        return

    for label, body, variant in r["steps"]:
        style.step(label, body, variant)

    # result band
    zeros_str = (
        "  ·  ".join(f"{float(z):.4f}" for z in r["zeros"])
        if r["zeros"] else "None"
    )
    deriv_str = str(r["derivative"]) if r["derivative"] is not None else "—"
    style.result_band(
        ("Domain",     r["domain_str"]),
        ("Zeros",      zeros_str),
        ("f′(x)",      deriv_str),
    )

    # graph
    st.markdown('<div class="graph-label">Graph of f(x)</div>',
                unsafe_allow_html=True)
    try:
        fig = make_plot(r["expr"], r["zeros"])
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.warning(f"Could not render the graph: {e}")

    style.step(
        "Reading the graph",
        "Gold dots mark the zeros (x-intercepts). "
        "The curve rises where f′(x) &gt; 0 and falls where f′(x) &lt; 0.<br>"
        "Compare what you see with the steps above — "
        "if something looks wrong, it usually is.",
    )


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Enter a function of x</div>',
                    unsafe_allow_html=True)

        expr_str = st.text_input(
            "f(x) =",
            value="x**2 - 4",
            key="fa_expr",
            help="Use Python syntax: x**2, sqrt(x), log(x), sin(x), 1/x …",
        )

        st.markdown(
            f'<div class="eq-display">f(x) = {expr_str}</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Analyze →", key="fa_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    <code>x**2 - 4</code> &nbsp;even, 2 zeros<br>
    <code>x**3 - x</code> &nbsp;odd, 3 zeros<br>
    <code>1/x</code> &nbsp;odd, domain ℝ∖{0}<br>
    <code>sqrt(x)</code> &nbsp;domain [0,+∞)<br>
    <code>log(x)</code> &nbsp;domain (0,+∞)<br>
    <code>sin(x)</code> &nbsp;odd, periodic
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if not expr_str.strip():
                st.error("Please enter a function.")
            else:
                render_steps(analyze(expr_str))
        else:
            style.empty_state("f(x)")