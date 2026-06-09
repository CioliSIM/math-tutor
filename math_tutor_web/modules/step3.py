import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Pure logic ────────────────────────────────────────────────────────────────

def choose_method(a1, b1, a2, b2):
    if abs(a1) == 1 or abs(b1) == 1 or abs(a2) == 1 or abs(b2) == 1:
        return "substitution"
    if a1 == a2 or a1 == -a2 or b1 == b2 or b1 == -b2:
        return "elimination"
    return "elimination"


def solve(a1, b1, c1, a2, b2, c2):
    method = choose_method(a1, b1, a2, b2)
    steps  = []   # list of (label, body, variant) for rendering
    x = y  = None
    special = None  # "infinite" | "none"

    # ── helpers ──────────────────────────────────────────────────────────
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    # ── SUBSTITUTION ─────────────────────────────────────────────────────
    if method == "substitution":
        add("Why substitution?",
            "One coefficient is 1 or −1 — we can isolate a variable immediately "
            "without fractions. It is the cleanest path.")

        # pick which variable to isolate
        if abs(a1) == 1:
            # isolate x from eq1
            # x = (c1 - b1*y) / a1
            sign = "" if b1 <= 0 else "− "
            add("Step 1 — Isolate x from equation 1",
                f"<span class='mf'>{a1:g}x + {b1:g}y = {c1:g}</span><br><br>"
                f"x = ({c1:g} − {b1:g}y) / {a1:g}<br>"
                f"x = <strong>{c1/a1:g} − {b1/a1:g}y</strong>")
            coeff_y = b2 - (a2 * b1) / a1
            const   = c2 - (a2 * c1) / a1
            add("Step 2 — Substitute into equation 2",
                f"Replace x in: <span class='mf'>{a2:g}x + {b2:g}y = {c2:g}</span><br><br>"
                f"{a2:g}·({c1/a1:g} − {b1/a1:g}y) + {b2:g}y = {c2:g}<br>"
                f"{coeff_y:g}y = {const:g}")
            if coeff_y == 0:
                special = "infinite" if const == 0 else "none"
            else:
                y = const / coeff_y
                x = (c1 - b1 * y) / a1
                add("Step 3 — Back-substitute to find x",
                    f"y = {const:g} / {coeff_y:g} = <strong>{y:.4f}</strong><br><br>"
                    f"x = ({c1:g} − {b1:g}·{y:.4f}) / {a1:g} = <strong>{x:.4f}</strong>")

        elif abs(b1) == 1:
            # isolate y from eq1
            add("Step 1 — Isolate y from equation 1",
                f"<span class='mf'>{a1:g}x + {b1:g}y = {c1:g}</span><br><br>"
                f"y = ({c1:g} − {a1:g}x) / {b1:g}<br>"
                f"y = <strong>{c1/b1:g} − {a1/b1:g}x</strong>")
            coeff_x = a2 - (b2 * a1) / b1
            const   = c2 - (b2 * c1) / b1
            add("Step 2 — Substitute into equation 2",
                f"Replace y in: <span class='mf'>{a2:g}x + {b2:g}y = {c2:g}</span><br><br>"
                f"{coeff_x:g}x = {const:g}")
            if coeff_x == 0:
                special = "infinite" if const == 0 else "none"
            else:
                x = const / coeff_x
                y = (c1 - a1 * x) / b1
                add("Step 3 — Back-substitute to find y",
                    f"x = {const:g} / {coeff_x:g} = <strong>{x:.4f}</strong><br><br>"
                    f"y = ({c1:g} − {a1:g}·{x:.4f}) / {b1:g} = <strong>{y:.4f}</strong>")

        else:
            # fall back: use eq2 to isolate
            if abs(a2) == 1:
                add("Step 1 — Isolate x from equation 2",
                    f"<span class='mf'>{a2:g}x + {b2:g}y = {c2:g}</span><br><br>"
                    f"x = <strong>{c2/a2:g} − {b2/a2:g}y</strong>")
                coeff_y = b1 - (a1 * b2) / a2
                const   = c1 - (a1 * c2) / a2
                if coeff_y == 0:
                    special = "infinite" if const == 0 else "none"
                else:
                    y = const / coeff_y
                    x = (c2 - b2 * y) / a2
                    add("Step 2–3 — Solve and back-substitute",
                        f"y = {const:g} / {coeff_y:g} = <strong>{y:.4f}</strong><br>"
                        f"x = <strong>{x:.4f}</strong>")
            else:
                add("Step 1 — Isolate y from equation 2",
                    f"<span class='mf'>{a2:g}x + {b2:g}y = {c2:g}</span><br><br>"
                    f"y = <strong>{c2/b2:g} − {a2/b2:g}x</strong>")
                coeff_x = a1 - (b1 * a2) / b2
                const   = c1 - (b1 * c2) / b2
                if coeff_x == 0:
                    special = "infinite" if const == 0 else "none"
                else:
                    x = const / coeff_x
                    y = (c2 - a2 * x) / b2
                    add("Step 2–3 — Solve and back-substitute",
                        f"x = {const:g} / {coeff_x:g} = <strong>{x:.4f}</strong><br>"
                        f"y = <strong>{y:.4f}</strong>")

    # ── ELIMINATION ───────────────────────────────────────────────────────
    else:
        add("Why elimination?",
            "No coefficient is ±1, so substitution would introduce fractions. "
            "Elimination cancels a variable directly by adding or subtracting equations.")

        # try to cancel y first
        if b1 == -b2:
            new_a, new_c = a1 + a2, c1 + c2
            add("Step 1 — Eliminate y (add equations)",
                f"y-coefficients are opposite ({b1:g} and {b2:g}) — add directly.<br><br>"
                f"({a1:g}x + {b1:g}y = {c1:g})<br>"
                f"+ ({a2:g}x + {b2:g}y = {c2:g})<br>"
                f"{'─'*28}<br>"
                f"<strong>{new_a:g}x = {new_c:g}</strong>")
        elif b1 == b2:
            new_a, new_c = a1 - a2, c1 - c2
            add("Step 1 — Eliminate y (subtract equations)",
                f"y-coefficients are equal ({b1:g}) — subtract directly.<br><br>"
                f"({a1:g}x + {b1:g}y = {c1:g})<br>"
                f"− ({a2:g}x + {b2:g}y = {c2:g})<br>"
                f"{'─'*28}<br>"
                f"<strong>{new_a:g}x = {new_c:g}</strong>")
        elif a1 == -a2:
            new_b, new_c = b1 + b2, c1 + c2
            add("Step 1 — Eliminate x (add equations)",
                f"x-coefficients are opposite ({a1:g} and {a2:g}) — add directly.<br><br>"
                f"<strong>{new_b:g}y = {new_c:g}</strong>")
            if new_b == 0:
                special = "infinite" if new_c == 0 else "none"
            else:
                y = new_c / new_b
                x = (c1 - b1 * y) / a1
                add("Step 2 — Back-substitute",
                    f"y = {new_c:g} / {new_b:g} = <strong>{y:.4f}</strong><br><br>"
                    f"x = ({c1:g} − {b1:g}·{y:.4f}) / {a1:g} = <strong>{x:.4f}</strong>")
            new_a = None  # skip further processing
        elif a1 == a2:
            new_b, new_c = b1 - b2, c1 - c2
            add("Step 1 — Eliminate x (subtract equations)",
                f"x-coefficients are equal ({a1:g}) — subtract directly.<br><br>"
                f"<strong>{new_b:g}y = {new_c:g}</strong>")
            if new_b == 0:
                special = "infinite" if new_c == 0 else "none"
            else:
                y = new_c / new_b
                x = (c1 - b1 * y) / a1
                add("Step 2 — Back-substitute",
                    f"y = {new_c:g} / {new_b:g} = <strong>{y:.4f}</strong><br><br>"
                    f"x = ({c1:g} − {b1:g}·{y:.4f}) / {a1:g} = <strong>{x:.4f}</strong>")
            new_a = None
        else:
            # general: multiply to cancel y
            lcm_b = abs(int(b1) * int(b2)) // math.gcd(abs(int(b1)), abs(int(b2)))
            m1    = lcm_b // abs(int(b1))
            m2    = lcm_b // abs(int(b2))
            na1, nb1, nc1 = a1*m1, b1*m1, c1*m1
            na2, nb2, nc2 = a2*m2, b2*m2, c2*m2
            add("Step 1 — Multiply to create opposite coefficients",
                f"LCM of |{b1:g}| and |{b2:g}| = {lcm_b}<br><br>"
                f"Eq.1 × {m1}: &nbsp;<span class='mf'>{na1:g}x + {nb1:g}y = {nc1:g}</span><br>"
                f"Eq.2 × {m2}: &nbsp;<span class='mf'>{na2:g}x + {nb2:g}y = {nc2:g}</span>")
            if nb1 == -nb2:
                new_a, new_c = na1 + na2, nc1 + nc2
                op_word = "Adding"
            else:
                new_a, new_c = na1 - na2, nc1 - nc2
                op_word = "Subtracting"
            add("Step 2 — Eliminate y",
                f"{op_word} the two equations:<br><br>"
                f"<strong>{new_a:g}x = {new_c:g}</strong>")

        # resolve x if new_a is set (not None from x-elimination branch)
        if special is None and x is None and 'new_a' in dir() and new_a is not None:
            if new_a == 0:
                special = "infinite" if new_c == 0 else "none"
            else:
                x = new_c / new_a
                y = (c1 - a1 * x) / b1
                add("Step 3 — Back-substitute",
                    f"x = {new_c:g} / {new_a:g} = <strong>{x:.4f}</strong><br><br>"
                    f"Plug into equation 1:<br>"
                    f"{a1:g}·({x:.4f}) + {b1:g}y = {c1:g}<br>"
                    f"y = <strong>{y:.4f}</strong>")

    return {"steps": steps, "x": x, "y": y, "special": special,
            "method": method,
            "a1": a1, "b1": b1, "c1": c1, "a2": a2, "b2": b2, "c2": c2}


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(a1, b1, c1, a2, b2, c2, x_sol, y_sol):
    cx = x_sol if x_sol is not None else 0
    cy = y_sol if y_sol is not None else 0
    x_vals = np.linspace(cx - 6, cx + 6, 400)

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    if b1 != 0:
        ax.plot(x_vals, (c1 - a1*x_vals)/b1, color="#e8602a", linewidth=2.2,
                label=f"{a1:g}x + {b1:g}y = {c1:g}")
    if b2 != 0:
        ax.plot(x_vals, (c2 - a2*x_vals)/b2, color="#3d6b5e", linewidth=2.2,
                label=f"{a2:g}x + {b2:g}y = {c2:g}")

    if x_sol is not None and y_sol is not None:
        ax.plot(x_sol, y_sol, "o", color="#c8a96e", markersize=10,
                zorder=5, label=f"Solution ({x_sol:.2f}, {y_sol:.2f})")
        ax.annotate(f"({x_sol:.2f}, {y_sol:.2f})", (x_sol, y_sol),
                    textcoords="offset points", xytext=(10, 10),
                    fontsize=9.5, fontfamily="serif", color="#4a4540")

    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.set_xlabel("x", color="#4a4540", fontsize=9)
    ax.set_ylabel("y", color="#4a4540", fontsize=9)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    plt.tight_layout()
    return fig


# ── Render ────────────────────────────────────────────────────────────────────

def render_steps(r):
    a1, b1, c1 = r["a1"], r["b1"], r["c1"]
    a2, b2, c2 = r["a2"], r["b2"], r["c2"]
    x, y       = r["x"], r["y"]

    def s(n):
        return f"+ {n:g}" if n >= 0 else f"− {abs(n):g}"

    # ── Equation display ──────────────────────────────────────────────────
    style.step(
        "The system",
        f"""We have two equations and two unknowns.<br>
We want x and y that satisfy <strong>both at once</strong> —
the point where the two lines cross.<br><br>
<span class="mf" style="display:block;padding:0.4rem 0.8rem;
background:var(--bg2);border-radius:6px;line-height:2.1;font-size:1.1rem;">
  {a1:g}x &nbsp;{s(b1)}y &nbsp;= &nbsp;{c1:g}<br>
  {a2:g}x &nbsp;{s(b2)}y &nbsp;= &nbsp;{c2:g}
</span><br>
Method chosen: <strong>{"Substitution" if r["method"]=="substitution" else "Elimination"}</strong>""",
        "warm",
    )

    # ── Computed steps ────────────────────────────────────────────────────
    for label, body, variant in r["steps"]:
        style.step(label, body, variant)

    # ── Special cases ─────────────────────────────────────────────────────
    if r["special"] == "infinite":
        style.step(
            "Result — Infinite solutions",
            "The two equations describe the <strong>same line</strong>.<br>"
            "Every point on that line is a solution — infinitely many.<br>"
            "The system is called <em>dependent</em>.",
            "error",
        )
        return

    if r["special"] == "none":
        style.step(
            "Result — No solution",
            "The two equations describe <strong>parallel lines</strong> — "
            "they never intersect.<br>"
            "There is no x, y that satisfies both simultaneously.<br>"
            "The system is called <em>inconsistent</em>.",
            "error",
        )
        return

    # ── Verify ────────────────────────────────────────────────────────────
    chk1 = a1*x + b1*y
    chk2 = a2*x + b2*y
    style.step(
        "Verify — plug back into both equations",
        f"Eq.1: {a1:g}·({x:.4f}) + {b1:g}·({y:.4f}) = {chk1:.6f} &nbsp;(expected {c1:g}) ✓<br>"
        f"Eq.2: {a2:g}·({x:.4f}) + {b2:g}·({y:.4f}) = {chk2:.6f} &nbsp;(expected {c2:g}) ✓",
        "sage",
    )

    # ── Result band ───────────────────────────────────────────────────────
    style.result_band(
        ("x", f"{x:.4f}"),
        ("y", f"{y:.4f}"),
        ("Intersection", f"({x:.3f}, {y:.3f})"),
    )

    # ── Graph ─────────────────────────────────────────────────────────────
    st.markdown('<div class="graph-label">The two lines and their intersection</div>',
                unsafe_allow_html=True)
    fig = make_plot(a1, b1, c1, a2, b2, c2, x, y)
    st.pyplot(fig)
    plt.close(fig)

    style.step(
        "Reading the graph",
        "Each equation is a straight line. "
        "The solution is the single point where they cross — "
        "the only (x, y) that satisfies both simultaneously.<br><br>"
        "Parallel lines → no solution. &nbsp;Identical lines → infinite solutions.",
    )


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Equation 1: &nbsp;a₁x + b₁y = c₁</div>',
                    unsafe_allow_html=True)
        a1 = st.number_input("a₁", value=2.0, step=1.0, format="%.4g", key="s_a1")
        b1 = st.number_input("b₁", value=1.0, step=1.0, format="%.4g", key="s_b1")
        c1 = st.number_input("c₁", value=5.0, step=1.0, format="%.4g", key="s_c1")

        st.markdown('<div class="input-panel-label" style="margin-top:0.8rem;">'
                    'Equation 2: &nbsp;a₂x + b₂y = c₂</div>',
                    unsafe_allow_html=True)
        a2 = st.number_input("a₂", value=1.0, step=1.0, format="%.4g", key="s_a2")
        b2 = st.number_input("b₂", value=3.0, step=1.0, format="%.4g", key="s_b2")
        c2 = st.number_input("c₂", value=7.0, step=1.0, format="%.4g", key="s_c2")

        def s(n):
            return f"+ {n:g}" if n >= 0 else f"− {abs(n):g}"

        st.markdown(f"""
<div class="eq-display" style="font-size:1.05rem;line-height:2;">
  {a1:g}x &nbsp;{s(b1)}y &nbsp;= &nbsp;{c1:g}<br>
  {a2:g}x &nbsp;{s(b2)}y &nbsp;= &nbsp;{c2:g}
</div>""", unsafe_allow_html=True)

        solve_btn = st.button("Solve →", key="s_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    <code>2, 1, 5 / 1, 3, 7</code> &nbsp;→ unique solution<br>
    <code>1, −1, 0 / 2, −2, 0</code> &nbsp;→ infinite solutions<br>
    <code>1, 1, 3 / 1, 1, 5</code> &nbsp;→ no solution
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if a1 == 0 and b1 == 0:
                st.error("Equation 1 is trivial (0 = c₁). Enter valid coefficients.")
            elif a2 == 0 and b2 == 0:
                st.error("Equation 2 is trivial (0 = c₂). Enter valid coefficients.")
            else:
                render_steps(solve(a1, b1, c1, a2, b2, c2))
        else:
            style.empty_state("x + y")