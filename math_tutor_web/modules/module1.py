import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Pure logic ────────────────────────────────────────────────────────────────

def solve(a, b, c):
    delta = b**2 - 4 * a * c
    vx    = -b / (2 * a)
    vy    = a * vx**2 + b * vx + c
    out   = {"a": a, "b": b, "c": c, "delta": delta,
             "vertex": (vx, vy), "case": None, "x1": None, "x2": None}
    if delta > 0:
        r              = math.sqrt(delta)
        out["case"]        = "two"
        out["sqrt_delta"]  = r
        out["x1"]          = (-b + r) / (2 * a)
        out["x2"]          = (-b - r) / (2 * a)
    elif delta == 0:
        out["case"] = "one"
        out["x1"]   = -b / (2 * a)
    else:
        out["case"] = "none"
    return out


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(a, b, c, x1=None, x2=None):
    center = -b / (2 * a)
    spread = max(abs(x1 - x2) * 2 if x1 and x2 else 4, 4)

    x  = np.linspace(center - spread, center + spread, 400)
    y  = a * x**2 + b * x + c

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    ax.plot(x, y, color="#e8602a", linewidth=2.2,
            label=f"f(x) = {a}x² + {b}x + {c}")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)

    if x1 is not None and x2 is not None:
        ax.plot([x1, x2], [0, 0], "o", color="#c8a96e",
                markersize=9, zorder=5, label="Roots")
        for xi, lbl in [(x1, "x₁"), (x2, "x₂")]:
            ax.annotate(f"{lbl} = {xi:.3f}", (xi, 0),
                        textcoords="offset points", xytext=(0, 13),
                        ha="center", fontsize=9.5,
                        fontfamily="serif", color="#4a4540")
    elif x1 is not None:
        ax.plot([x1], [0], "o", color="#c8a96e",
                markersize=9, zorder=5, label="Double root")
        ax.annotate(f"x = {x1:.3f}", (x1, 0),
                    textcoords="offset points", xytext=(0, 13),
                    ha="center", fontsize=9.5,
                    fontfamily="serif", color="#4a4540")

    ax.spines[["top", "right"]].set_visible(False)
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


# ── Render steps ──────────────────────────────────────────────────────────────

def render_steps(r):
    a, b, c   = r["a"], r["b"], r["c"]
    delta     = r["delta"]
    vx, vy    = r["vertex"]

    def s(n):
        return f"+ {n:g}" if n >= 0 else f"− {abs(n):g}"

    style.step(
        "The equation",
        f"""We are looking for every value of <code>x</code> that satisfies:<br><br>
<span class="mf" style="display:block;text-align:center;font-size:1.3rem;padding:0.4rem 0;">
  {a:g}x² {s(b)}x {s(c)} = 0
</span><br>
There could be 0, 1, or 2 real solutions.
The <strong>discriminant Δ</strong> tells us which case we are in.""",
        "warm",
    )

    style.step(
        "Step 1 — Compute the discriminant",
        f"""<span class="mf">Δ = b² − 4ac</span><br><br>
This expression comes directly from the quadratic formula.
The sign of Δ decides everything:<br><br>
&emsp;<code>Δ &gt; 0</code> &nbsp;→ two distinct real solutions<br>
&emsp;<code>Δ = 0</code> &nbsp;→ one repeated solution (double root)<br>
&emsp;<code>Δ &lt; 0</code> &nbsp;→ no real solutions<br><br>
<strong>Computing:</strong><br>
Δ = ({b:g})² − 4 · ({a:g}) · ({c:g})<br>
&ensp;= {b**2:g} − {4*a*c:g}<br>
&ensp;= <strong>{delta:g}</strong>""",
    )

    if delta > 0:
        meaning = f"Δ = {delta:g} &gt; 0 — <strong>two distinct real solutions.</strong> The parabola crosses the x-axis at two separate points."
    elif delta == 0:
        meaning = "Δ = 0 — <strong>exactly one solution</strong>, called a double root. The parabola touches the x-axis at one point but does not cross it."
    else:
        meaning = f"Δ = {delta:g} &lt; 0 — <strong>no real solutions.</strong> Taking √{delta:g} requires imaginary numbers. The parabola never touches the x-axis."

    style.step("Step 2 — What does Δ tell us?", meaning)

    if delta > 0:
        r_val = r["sqrt_delta"]
        x1, x2 = r["x1"], r["x2"]
        style.step(
            "Step 3 — Apply the quadratic formula",
            f"""<span class="mf">x = (−b ± √Δ) / 2a</span><br><br>
The ± gives us two solutions — one with +, one with −.<br><br>
√Δ = √{delta:g} = <strong>{r_val:.6f}</strong><br><br>
<strong>x₁</strong> = ({-b:g} + {r_val:.6f}) / {2*a:g} = <strong>{x1:.6f}</strong><br>
<strong>x₂</strong> = ({-b:g} − {r_val:.6f}) / {2*a:g} = <strong>{x2:.6f}</strong>""",
        )
    elif delta == 0:
        x1 = r["x1"]
        style.step(
            "Step 3 — Apply the formula",
            f"""Since Δ = 0, the ± collapses: √0 = 0, so there is only one value.<br><br>
<span class="mf">x = −b / 2a</span><br><br>
x = {-b:g} / {2*a:g} = <strong>{x1:g}</strong>""",
        )
    else:
        style.step(
            "No real solutions",
            f"""√({delta:g}) is not a real number — so there are no real solutions.<br><br>
The parabola's vertex sits entirely
{"above" if a > 0 else "below"} the x-axis, never touching it.<br><br>
Complex solutions exist and involve <span class="mf">i = √(−1)</span> —
covered in Chapter 13.""",
            "error",
        )

    if delta >= 0:
        def f(x): return a * x**2 + b * x + c

        if delta > 0:
            x1, x2 = r["x1"], r["x2"]
            style.step(
                "Step 4 — Verify",
                "Substitute each solution back into the original equation. "
                "The result must be zero (or very close to it due to floating point).",
                "sage",
            )
            style.pills(
                f"x₁ = {x1:.4f} → f(x₁) = {f(x1):.8f} ✓",
                f"x₂ = {x2:.4f} → f(x₂) = {f(x2):.8f} ✓",
            )
        else:
            x1 = r["x1"]
            style.step("Step 4 — Verify",
                       "Substitute the solution back into the original equation.",
                       "sage")
            style.pills(f"x = {x1:g} → f(x) = {f(x1):.8f} ✓")

    if delta > 0:
        x1, x2 = r["x1"], r["x2"]
        style.result_band(
            ("Solution 1",   f"x₁ = {x1:.4f}"),
            ("Solution 2",   f"x₂ = {x2:.4f}"),
            ("Discriminant", f"Δ = {delta:g}"),
        )
    elif delta == 0:
        style.result_band(
            ("Double root",  f"x = {r['x1']:g}"),
            ("Discriminant", "Δ = 0"),
        )
    else:
        style.result_band(
            ("Real solutions", "None"),
            ("Discriminant",   f"Δ = {delta:g}"),
        )

    st.markdown('<div class="graph-label">The parabola</div>',
                unsafe_allow_html=True)

    if delta > 0:
        fig = make_plot(a, b, c, r["x1"], r["x2"])
    elif delta == 0:
        fig = make_plot(a, b, c, r["x1"])
    else:
        fig = make_plot(a, b, c)

    st.pyplot(fig)
    plt.close(fig)

    opens  = "upward — it has a minimum" if a > 0 else "downward — it has a maximum"
    crosses = (
        "The roots are the two x-intercepts."    if delta > 0  else
        "The vertex sits exactly on the x-axis." if delta == 0 else
        "The curve never reaches the x-axis."
    )
    style.step(
        "Reading the graph",
        f"""The parabola opens <strong>{opens}</strong>.<br>
Vertex at <strong>({vx:.3f}, {vy:.3f})</strong> — the
{"lowest" if a > 0 else "highest"} point of the curve.<br>
{crosses}""",
    )


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Enter coefficients</div>',
                    unsafe_allow_html=True)

        a = st.number_input("a  (coefficient of x²)", value=1.0,
                            step=0.5, format="%.4g", key="q_a")
        b = st.number_input("b  (coefficient of x)",  value=-3.0,
                            step=0.5, format="%.4g", key="q_b")
        c = st.number_input("c  (constant term)",     value=2.0,
                            step=0.5, format="%.4g", key="q_c")

        def s(n):
            return f"+ {n:g}" if n >= 0 else f"− {abs(n):g}"

        st.markdown(
            f'<div class="eq-display">{a:g}x² {s(b)}x {s(c)} = 0</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Solve →", key="q_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    <code>a=1, b=−3, c=2</code> &nbsp;→ two roots<br>
    <code>a=1, b=−2, c=1</code> &nbsp;→ double root<br>
    <code>a=1, b= 0, c=1</code> &nbsp;→ no real roots
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if a == 0:
                st.error("a cannot be zero — that would be a linear equation, not quadratic.")
            else:
                render_steps(solve(a, b, c))
        else:
            style.empty_state("x²")