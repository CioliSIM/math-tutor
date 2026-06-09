import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Pure logic ────────────────────────────────────────────────────────────────

def solve(a, b, c, op):
    delta = b**2 - 4 * a * c
    out   = {"a": a, "b": b, "c": c, "op": op, "delta": delta,
             "case": None, "x1": None, "x2": None, "solution": None}

    if delta > 0:
        r  = math.sqrt(delta)
        x1 = (-b - r) / (2 * a)
        x2 = (-b + r) / (2 * a)
        if x1 > x2:
            x1, x2 = x2, x1
        out["case"] = "two"
        out["x1"]   = x1
        out["x2"]   = x2

        strict  = op in [">", "<"]
        agrees  = (a > 0 and op in [">", ">="]) or (a < 0 and op in ["<", "<="])
        l = "(" if strict else "["
        r_br = ")" if strict else "]"
        if agrees:
            out["solution"] = f"x ∈ (−∞, {x1:.4f}{r_br} ∪ {l}{x2:.4f}, +∞)"
        else:
            out["solution"] = f"x ∈ {l}{x1:.4f}, {x2:.4f}{r_br}"

    elif delta == 0:
        x = -b / (2 * a)
        out["case"] = "one"
        out["x1"]   = x
        if a > 0:
            if op == ">=": out["solution"] = "x ∈ ℝ"
            elif op == ">": out["solution"] = f"x ∈ ℝ \\ {{{x:.4f}}}"
            else:            out["solution"] = "No solution"
        else:
            if op == "<=": out["solution"] = "x ∈ ℝ"
            elif op == "<": out["solution"] = f"x ∈ ℝ \\ {{{x:.4f}}}"
            else:            out["solution"] = "No solution"

    else:
        out["case"] = "none"
        if (a > 0 and op in [">", ">="]) or (a < 0 and op in ["<", "<="]):
            out["solution"] = "x ∈ ℝ  (all real numbers)"
        else:
            out["solution"] = "No solution"

    return out


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(a, b, c, op, x1, x2, delta):
    if x1 is not None and x2 is not None and x1 != x2:
        center = (x1 + x2) / 2
        spread = max(abs(x2 - x1) * 2, 4)
    else:
        center = -b / (2 * a)
        spread = 6

    x = np.linspace(center - spread, center + spread, 600)
    y = a * x**2 + b * x + c

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    # Solution shading
    if delta > 0 and x1 is not None and x2 is not None:
        agrees = (a > 0 and op in [">", ">="]) or (a < 0 and op in ["<", "<="])
        if agrees:
            ax.fill_between(x, y, 0, where=(x <= x1),
                            alpha=0.22, color="#3d6b5e", label="Solution region")
            ax.fill_between(x, y, 0, where=(x >= x2),
                            alpha=0.22, color="#3d6b5e")
        else:
            ax.fill_between(x, y, 0, where=((x >= x1) & (x <= x2)),
                            alpha=0.22, color="#3d6b5e", label="Solution region")

        strict = op in [">", "<"]
        mfc    = "#fdfaf5" if strict else "#c8a96e"
        ax.plot([x1, x2], [0, 0], "o", markersize=9,
                color="#c8a96e", markerfacecolor=mfc,
                markeredgecolor="#c8a96e", markeredgewidth=2, zorder=5)
        ax.annotate(f"x₁={x1:.3f}", (x1, 0),
                    textcoords="offset points", xytext=(0, 13),
                    ha="center", fontsize=9, fontfamily="serif", color="#4a4540")
        ax.annotate(f"x₂={x2:.3f}", (x2, 0),
                    textcoords="offset points", xytext=(0, 13),
                    ha="center", fontsize=9, fontfamily="serif", color="#4a4540")

    ax.plot(x, y, color="#e8602a", linewidth=2.2,
            label=f"f(x) = {a}x² + {b}x + {c}")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)

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
    a, b, c  = r["a"], r["b"], r["c"]
    op       = r["op"]
    delta    = r["delta"]
    x1, x2   = r["x1"], r["x2"]

    def s(n):
        return f"+ {n:g}" if n >= 0 else f"− {abs(n):g}"

    op_words = {">": "greater than", "<": "less than",
                ">=": "greater than or equal to", "<=": "less than or equal to"}

    # ── Step 0: the inequality ────────────────────────────────────────────
    style.step(
        "The inequality",
        f"""We want every value of <code>x</code> that makes this true:<br><br>
<span class="mf" style="display:block;text-align:center;font-size:1.3rem;padding:0.4rem 0;">
  {a:g}x² {s(b)}x {s(c)} &nbsp;{op}&nbsp; 0
</span><br>
Unlike an equation, the answer is not a single number — it is an
<strong>interval</strong> (or union of intervals) of x values.<br>
Strategy: find where the parabola crosses zero, then determine
which side satisfies <strong>{op} 0</strong>.""",
        "warm",
    )

    # ── Step 1: discriminant ──────────────────────────────────────────────
    style.step(
        "Step 1 — Find the boundary points",
        f"""Temporarily replace the inequality with an equality and solve:<br><br>
<span class="mf">{a:g}x² {s(b)}x {s(c)} = 0</span><br><br>
The roots are the points where the expression <strong>changes sign</strong> —
they are the boundaries of our solution.<br><br>
Δ = ({b:g})² − 4·({a:g})·({c:g}) = {b**2:g} − {4*a*c:g} = <strong>{delta:g}</strong>""",
    )

    # ── Step 2: roots ─────────────────────────────────────────────────────
    if delta > 0:
        style.step(
            "Step 2 — Two boundary points",
            f"""Δ &gt; 0 — two distinct roots: <strong>x₁ = {x1:.4f}</strong>,
<strong>x₂ = {x2:.4f}</strong><br><br>
These split the number line into three intervals:<br><br>
&emsp;<code>(−∞, {x1:.4f})</code> &nbsp;&nbsp;
<code>({x1:.4f}, {x2:.4f})</code> &nbsp;&nbsp;
<code>({x2:.4f}, +∞)</code><br><br>
The expression keeps the same sign throughout each interval.
We just need to identify which ones satisfy <code>{op} 0</code>.""",
        )

        # ── Step 3: parabola direction ────────────────────────────────────
        direction = "upward (∪ shape)" if a > 0 else "downward (∩ shape)"
        if a > 0:
            sign_outside = "positive"
            sign_inside  = "negative"
            image        = "Think of a valley — it dips below zero between the roots."
        else:
            sign_outside = "negative"
            sign_inside  = "positive"
            image        = "Think of a hill — it rises above zero between the roots."

        style.step(
            "Step 3 — Which way does the parabola open?",
            f"""a = {a:g} → the parabola opens <strong>{direction}</strong>.<br>
{image}<br><br>
The expression is <strong>{sign_outside}</strong> outside the roots
and <strong>{sign_inside}</strong> between them.""",
        )

        # ── Step 4: pick the region ────────────────────────────────────────
        agrees = (a > 0 and op in [">", ">="]) or (a < 0 and op in ["<", "<="])
        strict = op in [">", "<"]
        l      = "(" if strict else "["
        r_br   = ")" if strict else "]"

        if agrees:
            region_desc = (
                f"We want <code>{op} 0</code> and the parabola opens "
                f"{'upward' if a > 0 else 'downward'} — the sign agrees.<br>"
                f"The expression is {sign_outside} <strong>outside</strong> the roots."
                f"<br><br>Solution: <span class='mf'>"
                f"x ∈ (−∞, {x1:.4f}{r_br} ∪ {l}{x2:.4f}, +∞)</span>"
            )
        else:
            region_desc = (
                f"We want <code>{op} 0</code> but the parabola opens "
                f"{'upward' if a > 0 else 'downward'} — the sign disagrees.<br>"
                f"The expression is {sign_inside} <strong>between</strong> the roots."
                f"<br><br>Solution: <span class='mf'>"
                f"x ∈ {l}{x1:.4f}, {x2:.4f}{r_br}</span>"
            )

        style.step("Step 4 — Pick the right region", region_desc, "sage")

    elif delta == 0:
        x = x1
        direction = "upward" if a > 0 else "downward"
        always    = "positive" if a > 0 else "negative"
        style.step(
            "Step 2 — One boundary point (double root)",
            f"""Δ = 0 — one repeated root at <strong>x = {x:.4f}</strong>.<br><br>
The parabola opens <strong>{direction}</strong> and just touches the x-axis
at this one point without crossing it.<br>
The expression is always <strong>{always}</strong> — except at x = {x:.4f} where it equals zero.""",
        )
        style.step(
            "Step 3 — Apply the operator",
            f"""We want <code>{op} 0</code>. The expression is always {always}.<br><br>
Solution: <span class="mf">{r["solution"]}</span>""",
            "sage",
        )

    else:
        direction = "upward" if a > 0 else "downward"
        always    = "positive" if a > 0 else "negative"
        style.step(
            "Step 2 — No boundary points",
            f"""Δ &lt; 0 — the parabola never crosses the x-axis.<br><br>
It opens <strong>{direction}</strong> and is always <strong>{always}</strong>
for every real x — no exceptions.""",
        )
        style.step(
            "Step 3 — Apply the operator",
            f"""We want <code>{op} 0</code>. The expression is always {always}.<br><br>
Solution: <span class="mf">{r["solution"]}</span>""",
            "sage",
        )

    # ── Result band ───────────────────────────────────────────────────────
    style.result_band(
        ("Inequality",   f"{a:g}x² {b:+g}x {c:+g} {op} 0"),
        ("Discriminant", f"Δ = {delta:g}"),
        ("Solution",     r["solution"]),
    )

    # ── Graph ─────────────────────────────────────────────────────────────
    st.markdown('<div class="graph-label">The parabola and solution region</div>',
                unsafe_allow_html=True)
    fig = make_plot(a, b, c, op, x1, x2, delta)
    st.pyplot(fig)
    plt.close(fig)

    # ── Reading note ──────────────────────────────────────────────────────
    shading = "The shaded region shows where the inequality is satisfied."
    if delta > 0:
        strict  = op in [">", "<"]
        dot_note = "Open dots (○) mean the endpoints are excluded (strict inequality)." if strict \
              else "Filled dots (●) mean the endpoints are included."
        reading = f"{shading}<br>{dot_note}"
    else:
        reading = shading

    style.step("Reading the graph", reading)


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Enter coefficients</div>',
                    unsafe_allow_html=True)

        a  = st.number_input("a  (coefficient of x²)", value=1.0,
                             step=0.5, format="%.4g", key="qi_a")
        b  = st.number_input("b  (coefficient of x)",  value=-1.0,
                             step=0.5, format="%.4g", key="qi_b")
        c  = st.number_input("c  (constant term)",     value=-2.0,
                             step=0.5, format="%.4g", key="qi_c")
        op = st.selectbox("Operator", [">", ">=", "<", "<="], key="qi_op")

        def s(n):
            return f"+ {n:g}" if n >= 0 else f"− {abs(n):g}"

        st.markdown(
            f'<div class="eq-display">{a:g}x² {s(b)}x {s(c)} &nbsp;{op}&nbsp; 0</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Solve →", key="qi_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    <code>1, −1, −2, &gt;</code> &nbsp;→ outer intervals<br>
    <code>1, −1, −2, &lt;</code> &nbsp;→ inner interval<br>
    <code>1,  0,  1, &gt;</code> &nbsp;→ all of ℝ<br>
    <code>1,  0,  1, &lt;</code> &nbsp;→ no solution
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if a == 0:
                st.error("a cannot be zero — that would be a linear inequality, not quadratic.")
            else:
                render_steps(solve(a, b, c, op))
        else:
            style.empty_state("x² > 0")