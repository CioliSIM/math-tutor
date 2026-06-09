import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

import style

x_sym = sp.Symbol('x')


# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)
    ax.grid(True, alpha=0.2, color="#e0d8cc")


# ── LOGARITHMS ────────────────────────────────────────────────────────────────

def solve_log_compute(b, x_val):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("What is a logarithm?",
        f"""log_b(x) answers: <em>to what power must I raise b to get x?</em><br><br>
<span class="mf">log_b(x) = y &nbsp; means &nbsp; b^y = x</span><br><br>
So log_{b:g}({x_val:g}) = y means {b:g}^y = {x_val:g}.""",
        "warm")

    if b <= 0 or b == 1:
        add("Invalid base", f"Base b = {b:g} is not valid. Choose b &gt; 0, b ≠ 1.", "error")
        return {"steps": steps}
    if x_val <= 0:
        add("Invalid argument",
            f"x = {x_val:g} is not valid. Logarithms require x &gt; 0.<br>"
            "No real exponent can give a zero or negative result for b &gt; 0.", "error")
        return {"steps": steps}

    result = math.log(x_val) / math.log(b)
    add("Compute using change of base",
        f"<span class='mf'>log_{b:g}({x_val:g}) = ln({x_val:g}) / ln({b:g})</span><br><br>"
        f"= {math.log(x_val):.6f} / {math.log(b):.6f}<br>"
        f"= <strong>{result:.6f}</strong>")

    check = b**result
    add("Verify",
        f"{b:g}^{result:.6f} = {check:.8f} &nbsp;(expected {x_val:g}) ✓<br><br>"
        + (f"result &gt; 0 → x &gt; 1 — you need a positive exponent." if result > 0 else
           f"result &lt; 0 → 0 &lt; x &lt; 1 — a negative exponent gives a fraction." if result < 0 else
           f"result = 0 → x = 1 — b^0 = 1 for any base."),
        "sage")

    return {"steps": steps, "result": result, "b": b, "x_val": x_val}


def solve_log_properties(a, c, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Three rules — that is all",
        """Every logarithm manipulation traces back to one of these three.<br><br>
<strong>1. Product:</strong> &nbsp;log_b(a·c) = log_b(a) + log_b(c)<br>
<strong>2. Quotient:</strong> log_b(a/c) = log_b(a) − log_b(c)<br>
<strong>3. Power:</strong> &nbsp;&nbsp;log_b(aⁿ) = n·log_b(a)<br><br>
All three come from the same source: exponent rules run in reverse.""",
        "warm")

    if a <= 0 or c <= 0 or b <= 0 or b == 1:
        add("Invalid inputs", "All values must be positive, b ≠ 1.", "error")
        return {"steps": steps}

    la = math.log(a) / math.log(b)
    lc = math.log(c) / math.log(b)
    add("Verify with your numbers",
        f"log_{b:g}({a:g}) = <strong>{la:.6f}</strong><br>"
        f"log_{b:g}({c:g}) = <strong>{lc:.6f}</strong><br><br>"
        f"<strong>Product:</strong> log_{b:g}({a:g}·{c:g}) = {math.log(a*c)/math.log(b):.6f} "
        f"vs {la:.6f}+{lc:.6f} = {la+lc:.6f} ✓<br>"
        f"<strong>Quotient:</strong> log_{b:g}({a:g}/{c:g}) = {math.log(a/c)/math.log(b):.6f} "
        f"vs {la:.6f}−{lc:.6f} = {la-lc:.6f} ✓<br>"
        f"<strong>Power:</strong> log_{b:g}({a:g}³) = {math.log(a**3)/math.log(b):.6f} "
        f"vs 3·{la:.6f} = {3*la:.6f} ✓",
        "sage")

    return {"steps": steps}


def solve_log_equation(b, expr_str, k):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Strategy",
        "The unknown is inside a log — isolate the log, then exponentiate to undo it.<br><br>"
        "<span class='mf'>log_b(A) = k &nbsp;→&nbsp; A = b^k</span><br><br>"
        "<strong>Always check</strong>: the argument must be &gt; 0 after solving. "
        "Algebra can produce extraneous solutions.",
        "warm")

    try:
        expr = sp.sympify(expr_str)
    except Exception as e:
        add("Parse error", str(e), "error")
        return {"steps": steps}

    rhs = b**k
    add("Step 1 — Exponentiate both sides",
        f"log_{b:g}({expr}) = {k:g}<br><br>"
        f"{expr} = {b:g}^{k:g} = <strong>{rhs:.6f}</strong>")

    rhs_sym  = sp.Rational(rhs).limit_denominator(10000)
    solutions = sp.solve(expr - rhs_sym, x_sym)
    add("Step 2 — Solve the resulting equation",
        f"{expr} = {rhs:.6f}<br>"
        f"Raw solutions: <code>{solutions}</code>")

    valid = []
    pill_items = []
    for sol in solutions:
        val = float(expr.subs(x_sym, sol))
        if val > 0:
            valid.append(sol)
            pill_items.append(f"x={sol} → arg={val:.4f} &gt; 0 ✓")
        else:
            pill_items.append(f"x={sol} → arg={val:.4f} ≤ 0 ✗ extraneous")

    body = "Check argument &gt; 0 for each solution:"
    add("Step 3 — Validate", body, "sage" if valid else "error")
    style_items = pill_items  # we'll render pills separately

    verdict = f"Valid solution(s): <strong>{valid}</strong>" if valid else \
              "No valid solutions — all were extraneous."
    add("Result", verdict, "sage" if valid else "error")

    return {"steps": steps, "pills": pill_items}


# ── EXPONENTIALS ──────────────────────────────────────────────────────────────

def solve_exp_compute(b, exp):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    if b <= 0:
        add("Invalid base", "Base must be positive.", "error")
        return {"steps": steps}

    result = b**exp
    if exp == int(exp) and abs(exp) < 10:
        if exp > 0:
            body = f"{b:g}^{int(exp)} means multiplying {b:g} by itself {int(exp)} time(s).<br>= <strong>{result:.6f}</strong>"
        elif exp < 0:
            body = f"Negative exponent = reciprocal:<br>{b:g}^{int(exp)} = 1/{b:g}^{int(-exp)} = 1/{b**(-exp):.6f} = <strong>{result:.6f}</strong>"
        else:
            body = f"Any non-zero number to the power 0 equals 1.<br>{b:g}^0 = <strong>1</strong>"
    else:
        body = (f"For non-integer exponents: b^x = e^(x·ln(b))<br><br>"
                f"= e^({exp:g}·{math.log(b):.6f})<br>"
                f"= e^{exp*math.log(b):.6f}<br>"
                f"= <strong>{result:.6f}</strong>")

    add("Computation", body, "sage")
    return {"steps": steps, "result": result}


def solve_exp_equation(b, expr_str, k):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Strategy",
        "The unknown is in the exponent — take log of both sides to bring it down.<br><br>"
        "<span class='mf'>b^(expression) = k &nbsp;→&nbsp; expression = log_b(k)</span>",
        "warm")

    if b <= 0 or b == 1:
        add("Invalid base", "b must be positive and ≠ 1.", "error")
        return {"steps": steps}
    if k <= 0:
        add("No solution",
            f"k = {k:g} ≤ 0. Exponentials are always positive — no solution.", "error")
        return {"steps": steps}

    try:
        expr = sp.sympify(expr_str)
    except Exception as e:
        add("Parse error", str(e), "error")
        return {"steps": steps}

    rhs = math.log(k) / math.log(b)
    add("Step 1 — Take log_b of both sides",
        f"{b:g}^({expr}) = {k:g}<br><br>"
        f"log_{b:g}({b:g}^({expr})) = log_{b:g}({k:g})<br>"
        f"{expr} = <strong>{rhs:.6f}</strong>")

    solutions = sp.solve(expr - sp.Rational(rhs).limit_denominator(10000), x_sym)
    add("Step 2 — Solve and verify",
        f"Solutions: <strong>{solutions}</strong>", "sage")

    for sol in solutions:
        exp_val = float(expr.subs(x_sym, sol))
        check   = b**exp_val
        add(f"Verify x = {sol}",
            f"exponent = {exp_val:.4f}<br>"
            f"{b:g}^{exp_val:.4f} = {check:.6f} (expected {k:g}) "
            f"{'✓' if abs(check-k)<1e-6 else '✗'}",
            "sage")

    return {"steps": steps}


def solve_growth_decay(A0, k, t_end):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    kind = "growth" if k > 0 else "decay"
    add("The exponential model",
        f"""Whenever a quantity changes proportionally to its current size,
the result is always exponential.<br><br>
<span class="mf" style="display:block;text-align:center;
font-size:1.2rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
A(t) = {A0:g} · e^({k:g}·t)
</span><br>
A₀ = {A0:g} &nbsp;·&nbsp; k = {k:g} ({kind}) &nbsp;·&nbsp; t ∈ [0, {t_end:g}]""",
        "warm")

    rows = ""
    for t in [0, t_end/4, t_end/2, 3*t_end/4, t_end]:
        val = A0 * math.exp(k * t)
        rows += f"A({t:.2f}) = {A0:g}·e^({k:g}·{t:.2f}) = <strong>{val:.4f}</strong><br>"
    add("Values at key moments", rows)

    if k > 0:
        dt = math.log(2)/k
        add("Doubling time",
            f"Solve 2·A₀ = A₀·e^(k·t): &nbsp; t = ln(2)/k = {math.log(2):.4f}/{k:g} = <strong>{dt:.4f}</strong><br>"
            f"Every {dt:.4f} units of time, the amount doubles.",
            "sage")
    elif k < 0:
        hl = math.log(2)/(-k)
        add("Half-life",
            f"Solve A₀/2 = A₀·e^(k·t): &nbsp; t = ln(2)/|k| = {math.log(2):.4f}/{-k:g} = <strong>{hl:.4f}</strong><br>"
            f"Every {hl:.4f} units of time, the amount halves.",
            "sage")

    return {"steps": steps, "A0": A0, "k": k, "t_end": t_end}


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_log_graphs():
    x_v  = np.linspace(0.01, 10, 1000)
    bases  = [math.e, 10, 2, 0.5]
    colors = ["#e8602a","#3d6b5e","#7b6fb0","#c8a96e"]
    labels = ["ln(x) — base e","log(x) — base 10","log₂(x) — base 2","log₀.₅(x)"]

    fig, ax = plt.subplots(figsize=(7, 5))
    styled_ax(ax, fig)
    for b, col, lab in zip(bases, colors, labels):
        ax.plot(x_v, np.log(x_v)/np.log(b), color=col, linewidth=2, label=lab)
    ax.plot([0,10],[0,10], color="#b0a090", linewidth=1,
            linestyle="--", alpha=0.5, label="y=x (mirror)")
    ax.plot(1,0,"o",color="#1a1814",markersize=8)
    ax.annotate("  (1,0) — all logs pass here",(1,0),fontsize=8.5,color="#4a4540")
    ax.set_xlim(-0.5,10); ax.set_ylim(-4,4)
    ax.set_xlabel("x",color="#4a4540",fontsize=9)
    ax.set_ylabel("log_b(x)",color="#4a4540",fontsize=9)
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout()
    return fig


def plot_exp_graphs():
    x_v  = np.linspace(-3, 3, 400)
    bases  = [math.e, 2, 3, 0.5]
    colors = ["#e8602a","#3d6b5e","#7b6fb0","#c8a96e"]
    labels = ["eˣ (natural)","2ˣ","3ˣ","(0.5)ˣ — decay"]

    fig, ax = plt.subplots(figsize=(7, 5))
    styled_ax(ax, fig)
    for b, col, lab in zip(bases, colors, labels):
        ax.plot(x_v, b**x_v, color=col, linewidth=2, label=lab)
    ax.axhline(1,color="#b0a090",linewidth=0.8,linestyle="--",alpha=0.5)
    ax.plot(0,1,"o",color="#1a1814",markersize=8)
    ax.annotate("  (0,1) — all exponentials pass here",(0,1),fontsize=8.5,color="#4a4540")
    ax.set_ylim(-0.5,10)
    ax.set_xlabel("x",color="#4a4540",fontsize=9)
    ax.set_ylabel("b^x",color="#4a4540",fontsize=9)
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout()
    return fig


def plot_growth_decay(r):
    A0, k, t_end = r["A0"], r["k"], r["t_end"]
    t_v = np.linspace(0, t_end, 400)
    A_v = A0 * np.exp(k * t_v)

    fig, ax = plt.subplots(figsize=(7, 4))
    styled_ax(ax, fig)
    ax.plot(t_v, A_v, color="#e8602a", linewidth=2.2,
            label=f"A(t) = {A0:g}·e^({k:g}t)")
    ax.axhline(A0, color="#c8a96e", linewidth=1, linestyle="--",
               alpha=0.7, label=f"A₀ = {A0:g}")
    ax.plot(0, A0, "o", color="#c8a96e", markersize=9, zorder=5)

    if k > 0:
        dt = math.log(2)/k
        if dt <= t_end:
            ax.axvline(dt, color="#3d6b5e", linewidth=1.5, linestyle="--",
                       label=f"Doubling t={dt:.2f}")
    elif k < 0:
        hl = math.log(2)/(-k)
        if hl <= t_end:
            ax.axvline(hl, color="#3d6b5e", linewidth=1.5, linestyle="--",
                       label=f"Half-life t={hl:.2f}")

    ax.set_xlabel("t", color="#4a4540", fontsize=9)
    ax.set_ylabel("A(t)", color="#4a4540", fontsize=9)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    plt.tight_layout()
    return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>',
                    unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Log — Compute", "Log — Properties", "Log — Equations",
             "Log — Graphs", "Exp — Compute", "Exp — Equations",
             "Exp — Graphs", "Growth & Decay"],
            key="le_topic")

        if topic == "Log — Compute":
            b     = st.number_input("Base b", value=10.0, step=1.0, key="lc_b")
            x_val = st.number_input("Argument x", value=100.0, step=1.0, key="lc_x")
        elif topic == "Log — Properties":
            a = st.number_input("a", value=4.0, step=1.0, key="lp_a")
            c = st.number_input("c", value=8.0, step=1.0, key="lp_c")
            b = st.number_input("Base b", value=2.0, step=1.0, key="lp_b")
        elif topic == "Log — Equations":
            b     = st.number_input("Base b", value=2.0, step=1.0, key="leq_b")
            expr  = st.text_input("Expression (in x)", value="2*x+1", key="leq_expr")
            k     = st.number_input("RHS k", value=3.0, step=0.5, key="leq_k")
        elif topic == "Exp — Compute":
            b   = st.number_input("Base b", value=math.e, step=1.0, key="ec_b")
            exp = st.number_input("Exponent", value=2.0, step=0.5, key="ec_exp")
        elif topic == "Exp — Equations":
            b    = st.number_input("Base b", value=2.0, step=1.0, key="eeq_b")
            expr = st.text_input("Exponent (in x)", value="3*x-1", key="eeq_expr")
            k    = st.number_input("RHS k", value=8.0, step=1.0, key="eeq_k")
        elif topic == "Growth & Decay":
            A0    = st.number_input("Initial amount A₀", value=100.0, step=10.0, key="gd_a0")
            k_val = st.number_input("Rate k  (+ growth, − decay)", value=-0.1,
                                    step=0.05, format="%.4g", key="gd_k")
            t_end = st.number_input("Time span", value=20.0, step=5.0, key="gd_t")

        solve_btn = st.button("Compute →", key="le_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Log compute: <code>b=10, x=1000</code> → 3<br>
    Log compute: <code>b=2, x=64</code> → 6<br>
    Log equation: <code>b=2, 2x+1=3</code> → x=3.5<br>
    Exp equation: <code>b=2, 3x−1=8</code><br>
    Growth: <code>A₀=100, k=0.1</code><br>
    Decay: &nbsp;<code>A₀=100, k=−0.05</code>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Log — Compute":
                r = solve_log_compute(b, x_val)
            elif topic == "Log — Properties":
                r = solve_log_properties(a, c, b)
            elif topic == "Log — Equations":
                r = solve_log_equation(b, expr, k)
            elif topic == "Log — Graphs":
                r = {"steps": []}
            elif topic == "Exp — Compute":
                r = solve_exp_compute(b, exp)
            elif topic == "Exp — Equations":
                r = solve_exp_equation(b, expr, k)
            elif topic == "Exp — Graphs":
                r = {"steps": []}
            else:
                r = solve_growth_decay(A0, k_val, t_end)

            for label, body, variant in r["steps"]:
                style.step(label, body, variant)

            # pills if present
            if r.get("pills"):
                style.pills(*r["pills"])

            # graphs
            if topic == "Log — Graphs":
                style.step("Log graphs",
                    "Every log graph passes through (1,0) — because log_b(1)=0 always.<br>"
                    "Increasing for b&gt;1, decreasing for 0&lt;b&lt;1.<br>"
                    "The log and its inverse exponential are mirrors across y=x.",
                    "warm")
                st.markdown('<div class="graph-label">Logarithmic functions</div>',
                            unsafe_allow_html=True)
                st.pyplot(plot_log_graphs()); plt.close()

            elif topic == "Exp — Graphs":
                style.step("Exp graphs",
                    "Every exponential passes through (0,1) — because b^0=1 always.<br>"
                    "Always positive. Grows faster than any polynomial for b&gt;1.<br>"
                    "e^x is the only function equal to its own derivative.",
                    "warm")
                st.markdown('<div class="graph-label">Exponential functions</div>',
                            unsafe_allow_html=True)
                st.pyplot(plot_exp_graphs()); plt.close()

            elif topic == "Growth & Decay" and "A0" in r:
                st.markdown('<div class="graph-label">Growth / decay curve</div>',
                            unsafe_allow_html=True)
                st.pyplot(plot_growth_decay(r)); plt.close()
        else:
            style.empty_state("eˣ")