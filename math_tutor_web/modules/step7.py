import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

import style

x = sp.Symbol('x')


# ── Pure logic ────────────────────────────────────────────────────────────────

def analyze_at_point(expr_str, a_str):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    try:
        expr = sp.sympify(expr_str)
        a    = sp.sympify(a_str)
    except Exception as e:
        return {"error": str(e), "steps": [], "expr": None, "a": None}

    add("What we are computing",
        f"""<span class="mf" style="display:block;text-align:center;
font-size:1.2rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
  lim(x → {a})  f(x) = {expr}
</span><br>
As x gets closer and closer to <strong>{a}</strong>,
what does f(x) approach?<br><br>
The key insight: it does <em>not</em> matter what happens exactly
<em>at</em> x = {a}. Only what happens <em>near</em> it.
f({a}) might not even exist — the limit can still be perfectly defined.""",
        "warm")

    # direct substitution
    try:
        direct = sp.simplify(expr.subs(x, a))
        is_indet = not direct.is_finite or direct == sp.nan
    except Exception:
        direct    = None
        is_indet  = True

    if is_indet:
        add("Step 1 — Direct substitution fails",
            f"""Plugging x = {a} gives an indeterminate form (0/0, ∞/∞, or undefined).<br>
This is the <em>interesting</em> case — there is tension at x = {a}
that we need to resolve algebraically.<br><br>
Techniques available: factoring, L'Hôpital's rule, known identities.""")
    else:
        add("Step 1 — Direct substitution works",
            f"""f({a}) = <strong>{direct}</strong><br><br>
The result is finite — no indeterminate form.
No tricks needed.""")

    # compute limit
    try:
        lim_val = sp.limit(expr, x, a)
        if lim_val == sp.oo:
            lim_body = f"<strong>lim = +∞</strong><br>The function shoots upward — vertical asymptote at x = {a}."
            lim_var  = "error"
        elif lim_val == -sp.oo:
            lim_body = f"<strong>lim = −∞</strong><br>The function drops without bound — vertical asymptote at x = {a}."
            lim_var  = "error"
        else:
            lim_body = (
                f"<span class='mf'>lim(x→{a}) f(x) = <strong>{lim_val}</strong></span>"
                + (f" ≈ {float(lim_val):.6f}" if lim_val.is_number else "")
                + ("<br><br>Even though direct substitution failed, the function "
                   f"approaches <strong>{lim_val}</strong> smoothly from both sides."
                   if is_indet else "")
            )
            lim_var = "sage"
        add("Step 2 — Compute the limit", lim_body, lim_var)
    except Exception:
        lim_val = None
        add("Step 2 — Could not compute", "Try simplifying the expression by hand first.", "error")

    # continuity
    if lim_val is not None:
        try:
            val_at = sp.simplify(expr.subs(x, a))
            if not val_at.is_finite:
                cont = f"f({a}) is undefined — <strong>not continuous</strong> (removable discontinuity if the limit exists)."
                cont_var = "error"
            elif val_at == lim_val:
                cont = f"f({a}) = {val_at} = lim ✓<br><strong>Continuous</strong> at x = {a} — no break, no hole."
                cont_var = "sage"
            else:
                cont = (f"f({a}) = {val_at} but lim = {lim_val}.<br>"
                        f"<strong>Removable discontinuity</strong> — the function value is "
                        f"in the wrong place. Redefining f({a}) = {lim_val} would fix it.")
                cont_var = "error"
        except Exception:
            cont = "Could not check continuity automatically."
            cont_var = ""
        add("Step 3 — Is f continuous at x = " + str(a) + "?",
            "Continuity requires three things:<br>"
            f"&emsp;1. f({a}) exists &nbsp; 2. lim exists &nbsp; 3. they are equal<br><br>" + cont,
            cont_var)

    return {"steps": steps, "expr": expr, "a": a, "lim_val": lim_val, "error": None}


def analyze_at_infinity(expr_str):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    try:
        expr = sp.sympify(expr_str)
    except Exception as e:
        return {"error": str(e), "steps": [], "expr": None}

    add("What we are computing",
        f"""<span class="mf" style="display:block;text-align:center;
font-size:1.2rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
  lim(x → ±∞)  f(x) = {expr}
</span><br>
Instead of zooming in on a point, we zoom <em>out</em> — all the way to infinity.<br>
If f(x) settles toward a fixed value, that value is a <strong>horizontal asymptote</strong>.""",
        "warm")

    add("Key intuition",
        "For large x, the <strong>highest-degree term dominates</strong>. "
        "Lower-degree terms become negligible — they are a drop in the ocean.")

    for direction, sym, label in [("+∞", sp.oo, "x → +∞"), ("−∞", -sp.oo, "x → −∞")]:
        try:
            lim = sp.limit(expr, x, sym)
            if lim == sp.oo:
                body = f"<strong>+∞</strong> — grows without bound. No horizontal asymptote."
                var  = "error"
            elif lim == -sp.oo:
                body = f"<strong>−∞</strong> — drops without bound. No horizontal asymptote."
                var  = "error"
            else:
                body = (f"<strong>{lim}</strong>"
                        + (f" ≈ {float(lim):.6f}" if lim.is_number else "")
                        + f"<br>Horizontal asymptote: <span class='mf'>y = {lim}</span>")
                var = "sage"
            add(f"lim(x → {direction})", body, var)
        except Exception:
            add(f"lim(x → {direction})", "Could not compute.", "error")

    return {"steps": steps, "expr": expr, "a": sp.oo, "error": None}


def analyze_one_sided(expr_str, a_str):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    try:
        expr = sp.sympify(expr_str)
        a    = sp.sympify(a_str)
    except Exception as e:
        return {"error": str(e), "steps": [], "expr": None, "a": None}

    add("What we are computing",
        f"""Some functions behave differently depending on which direction
you approach a point from. That is when one-sided limits matter.<br><br>
<span class="mf">lim(x→{a}⁺)</span> — approaching from the <strong>right</strong> (x slightly &gt; {a})<br>
<span class="mf">lim(x→{a}⁻)</span> — approaching from the <strong>left</strong> &nbsp;(x slightly &lt; {a})<br><br>
The two-sided limit exists only when both sides agree.""",
        "warm")

    try:
        lr = sp.limit(expr, x, a, '+')
        add("Right-hand limit  lim(x→" + str(a) + "⁺)",
            f"Approaching from values slightly larger than {a}:<br><br>"
            f"<span class='mf'>lim(x→{a}⁺) = <strong>{lr}</strong></span>")
    except Exception:
        lr = None
        add("Right-hand limit", "Could not compute.", "error")

    try:
        ll = sp.limit(expr, x, a, '-')
        add("Left-hand limit  lim(x→" + str(a) + "⁻)",
            f"Approaching from values slightly smaller than {a}:<br><br>"
            f"<span class='mf'>lim(x→{a}⁻) = <strong>{ll}</strong></span>")
    except Exception:
        ll = None
        add("Left-hand limit", "Could not compute.", "error")

    if lr is not None and ll is not None:
        if lr == ll:
            add("Verdict — limits agree ✓",
                f"Both sides → <strong>{lr}</strong><br>"
                f"The two-sided limit exists: <span class='mf'>lim(x→{a}) = {lr}</span>",
                "sage")
        else:
            disc = "INFINITE" if (lr in [sp.oo,-sp.oo] or ll in [sp.oo,-sp.oo]) else "JUMP"
            add("Verdict — limits disagree",
                f"Left → {ll} &nbsp;·&nbsp; Right → {lr}<br>"
                f"They differ — <strong>two-sided limit does not exist</strong>.<br><br>"
                f"Type of discontinuity: <strong>{disc}</strong><br>"
                f"{'At least one side goes to ±∞ — vertical asymptote.' if disc=='INFINITE' else 'The graph jumps at x = '+str(a)+'.'}",
                "error")

    return {"steps": steps, "expr": expr, "a": a, "error": None}


NOTABLE = [
    ("sin(x)/x",       "x", 0,      "sin(x)/x → 1 as x→0",
     "At x=0, sin(0)/0 = 0/0. But for small angles, sin(x) ≈ x — the ratio → 1.<br>"
     "Without this limit you cannot differentiate sin(x)."),
    ("(1 + 1/x)**x",   "x", sp.oo,  "(1+1/x)^x → e as x→∞",
     "The base (1+1/x)→1 while the exponent x→∞. These forces balance to give <strong>e</strong>.<br>"
     "This is exactly continuous compounding — interest applied infinitely often per year."),
    ("(1 + x)**(1/x)", "x", 0,      "(1+x)^(1/x) → e as x→0",
     "Base (1+x)→1, exponent 1/x→∞. Same tension, same answer: <strong>e</strong>.<br>"
     "Two different-looking expressions, one remarkable number."),
    ("(exp(x)-1)/x",   "x", 0,      "(e^x−1)/x → 1 as x→0",
     "e^x−1 ≈ x for small x, so the ratio → 1.<br>"
     "This is the derivative of e^x at x=0 — why e is the natural base."),
    ("log(1+x)/x",     "x", 0,      "ln(1+x)/x → 1 as x→0",
     "ln(1+x) ≈ x for small x. This is the derivative of ln(x) at x=1."),
    ("x*sin(1/x)",     "x", sp.oo,  "x·sin(1/x) → 1 as x→∞",
     "sin(1/x)→0 but x·(1/x)=1. The squeeze theorem confirms the limit is 1."),
]


def analyze_notable():
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    add("Six limits every mathematician knows",
        "These are not just exercises — they are the foundation of calculus.<br>"
        "Derivatives, integrals, Taylor series — all trace back to these.",
        "warm")

    for expr_str, var, point, title, explanation in NOTABLE:
        try:
            expr = sp.sympify(expr_str)
            lim  = sp.limit(expr, x, point)
            val  = f"= <strong>e ≈ {float(sp.E):.6f}</strong>" if lim == sp.E else \
                   f"= <strong>{lim}</strong>" + (f" ≈ {float(lim):.6f}" if lim.is_number and lim != sp.E else "")
            add(title, f"{val}<br><br>{explanation}", "sage")
        except Exception:
            add(title, f"Could not compute.<br><br>{explanation}")

    add("Why these six matter",
        "When you hit an indeterminate form in calculus, the first question is always:<br>"
        "<em>does this reduce to one of these?</em><br>"
        "More often than not, the answer is yes.",
        "")

    return {"steps": steps, "expr": None, "a": None, "error": None}


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(expr, a):
    if expr is None:
        return None
    f_num = sp.lambdify(x, expr, "numpy")

    try:
        a_f = float(a) if a not in [sp.oo, -sp.oo] else None
    except Exception:
        a_f = None

    x_center = a_f if a_f is not None else 0
    x_vals   = np.linspace(x_center - 5, x_center + 5, 1000)

    with np.errstate(divide="ignore", invalid="ignore"):
        y_vals = np.array(f_num(x_vals), dtype=float)
        y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    ax.plot(x_vals, y_vals, color="#e8602a", linewidth=2.2,
            label=f"f(x) = {expr}")

    if a_f is not None:
        try:
            lv = float(sp.limit(expr, x, a))
            ax.plot(a_f, lv, "o", color="#c8a96e", markersize=9,
                    markerfacecolor="#fdfaf5", markeredgecolor="#c8a96e",
                    markeredgewidth=2.2, zorder=5,
                    label=f"lim = {lv:.4f}")
            ax.axvline(a_f, color="#b0a090", linewidth=0.8,
                       linestyle="--", alpha=0.6)
        except Exception:
            pass

    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)
    ax.set_ylim(-8, 8)
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
    if r.get("error"):
        style.step("Error", f"Could not parse: <code>{r['error']}</code>", "error")
        return

    for label, body, variant in r["steps"]:
        style.step(label, body, variant)

    if r.get("expr") is not None:
        st.markdown('<div class="graph-label">Graph</div>', unsafe_allow_html=True)
        try:
            fig = make_plot(r["expr"], r.get("a"))
            if fig:
                st.pyplot(fig)
                plt.close(fig)
        except Exception as e:
            st.warning(f"Could not render graph: {e}")


# ── Bolzano's theorem ─────────────────────────────────────────────────────────

def analyze_bolzano(expr_str, a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    try:
        expr = sp.sympify(expr_str)
        fa   = float(expr.subs(x, a))
        fb   = float(expr.subs(x, b))
    except Exception as e:
        add("Error", str(e), "error")
        return {"steps": steps}

    add("Bolzano's Theorem — the Intermediate Value Theorem for zeros",
        """If f is <strong>continuous</strong> on [a, b] and
<span class="mf">f(a) · f(b) &lt; 0</span>
(the function has opposite signs at the endpoints),<br><br>
then there exists at least one c ∈ (a, b) such that <strong>f(c) = 0</strong>.<br><br>
<em>Intuition:</em> a continuous function cannot go from positive to negative (or vice versa)
without crossing zero. It must pass through it.<br><br>
The theorem guarantees <em>existence</em> — it does not give you the exact value of c.
For that you need bisection or Newton's method.""",
        "warm")

    add(f"Step 1 — Evaluate at the endpoints",
        f"f({a}) = <strong>{fa:.6f}</strong><br>"
        f"f({b}) = <strong>{fb:.6f}</strong><br><br>"
        f"Product: f(a)·f(b) = {fa*fb:.6f}")

    if fa * fb < 0:
        add("Step 2 — Bolzano's condition is satisfied",
            f"f({a})·f({b}) = {fa*fb:.6f} &lt; 0 ✓<br><br>"
            f"The signs are opposite → at least one zero exists in ({a}, {b}).<br>"
            f"The function changes sign, so it <em>must</em> cross zero.", "sage")

        # bisection to find approximate root
        lo, hi = (a, b) if fa < 0 else (b, a)
        fa2, fb2 = (fa, fb) if fa < 0 else (fb, fa)
        lo, hi = min(a,b), max(a,b)
        for _ in range(40):
            mid = (lo + hi) / 2
            fmid = float(expr.subs(x, mid))
            if fa * fmid < 0:
                hi = mid
            else:
                lo = mid
        add("Bisection method — approximate root",
            f"Starting from [{a}, {b}], bisecting 40 times:<br>"
            f"c ≈ <strong>{mid:.8f}</strong><br>"
            f"f(c) ≈ {float(expr.subs(x, mid)):.2e} ≈ 0 ✓", "sage")
    elif abs(fa) < 1e-10:
        add("Step 2 — a is already a zero",
            f"f({a}) = 0 exactly. The zero is at the endpoint.", "sage")
    elif abs(fb) < 1e-10:
        add("Step 2 — b is already a zero",
            f"f({b}) = 0 exactly. The zero is at the endpoint.", "sage")
    else:
        add("Step 2 — Bolzano's condition is NOT satisfied",
            f"f({a})·f({b}) = {fa*fb:.6f} &gt; 0<br><br>"
            "Both values have the same sign. Bolzano's theorem does NOT apply here.<br>"
            "This does <em>not</em> mean there is no zero — there could still be an even number of zeros.<br>"
            "But the theorem cannot guarantee one.", "error")

    return {"steps": steps}


def plot_bolzano(expr_str, a, b):
    try:
        expr  = sp.sympify(expr_str)
        f_num = sp.lambdify(x, expr, "numpy")
        margin = (b - a) * 0.3
        x_r = np.linspace(a - margin, b + margin, 500)
        y_r = np.array(f_num(x_r), dtype=float)

        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
        ax.spines[["top","right"]].set_visible(False)
        ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
        ax.tick_params(colors="#4a4540", labelsize=8.5)
        ax.grid(True, alpha=0.2, color="#e0d8cc")

        ax.plot(x_r, np.where(np.isfinite(y_r), y_r, np.nan),
                color="#3d6b5e", linewidth=2.5, label=f"f(x) = {expr}")
        ax.axhline(0, color="#1a1814", linewidth=0.8)
        ax.axvline(a, color="#b0a090", linewidth=1, linestyle=":")
        ax.axvline(b, color="#b0a090", linewidth=1, linestyle=":")

        fa = float(expr.subs(x, a))
        fb = float(expr.subs(x, b))
        ax.plot(a, fa, "o", color="#e8602a", markersize=10, zorder=5,
                label=f"f({a}) = {fa:.3f}")
        ax.plot(b, fb, "o", color="#7b6fb0", markersize=10, zorder=5,
                label=f"f({b}) = {fb:.3f}")

        if fa * fb < 0:
            ax.fill_betweenx([-abs(fa)-abs(fb), abs(fa)+abs(fb)], a, b,
                             alpha=0.08, color="#3d6b5e")

        y_fin = y_r[np.isfinite(y_r)]
        if len(y_fin) > 0:
            pad = (y_fin.max() - y_fin.min()) * 0.15 + 0.3
            ax.set_ylim(y_fin.min() - pad, y_fin.max() + pad)

        ax.legend(fontsize=8.5, framealpha=0.7,
                  facecolor="#fdfaf5", edgecolor="#e0d8cc")
        ax.set_xlabel("x", color="#4a4540", fontsize=9)
        ax.set_title("Bolzano's Theorem", fontsize=10, color="#4a4540")
        plt.tight_layout()
        return fig
    except Exception:
        return None


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose limit type</div>',
                    unsafe_allow_html=True)

        lim_type = st.selectbox(
            "Type",
            ["At a point", "At infinity", "One-sided", "Notable limits", "Bolzano's theorem"],
            key="lim_type",
        )

        if lim_type == "At a point":
            expr_str = st.text_input("f(x) =", value="(x**2-1)/(x-1)", key="lim_expr")
            a_str    = st.text_input("a =",    value="1",               key="lim_a")
            preview  = f"lim(x→{a_str})  {expr_str}"

        elif lim_type == "At infinity":
            expr_str = st.text_input("f(x) =", value="(3*x**2+1)/(x**2-2)", key="lim_inf_expr")
            a_str    = "oo"
            preview  = f"lim(x→±∞)  {expr_str}"

        elif lim_type == "One-sided":
            expr_str = st.text_input("f(x) =", value="Abs(x)/x", key="lim_os_expr")
            a_str    = st.text_input("a =",    value="0",          key="lim_os_a")
            preview  = f"lim(x→{a_str}⁺⁻)  {expr_str}"

        else:
            expr_str = ""
            a_str    = ""
            preview  = "sin(x)/x · (1+1/x)^x · …"

        if lim_type == "Bolzano's theorem":
            expr_str = st.text_input("f(x) =", value="x**3 - x - 1", key="lim_bolz_expr")
            a_bz = st.number_input("a", value=1.0, step=0.5, key="lim_bz_a")
            b_bz = st.number_input("b", value=2.0, step=0.5, key="lim_bz_b")
            preview = f"Bolzano on [{a_bz}, {b_bz}]"

        st.markdown(
            f'<div class="eq-display" style="font-size:0.95rem;">{preview}</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Compute →", key="lim_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    At a point: <code>(x²−1)/(x−1)</code>, a=1<br>
    At a point: <code>sin(x)/x</code>, a=0<br>
    At ∞: <code>(3x²+1)/(x²−2)</code><br>
    One-sided: <code>1/x</code>, a=0<br>
    Bolzano: <code>x³−x−1</code>, [1, 2]
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if lim_type == "At a point":
                render_steps(analyze_at_point(expr_str, a_str))
            elif lim_type == "At infinity":
                render_steps(analyze_at_infinity(expr_str))
            elif lim_type == "One-sided":
                render_steps(analyze_one_sided(expr_str, a_str))
            elif lim_type == "Bolzano's theorem":
                render_steps(analyze_bolzano(expr_str, a_bz, b_bz))
                fig = plot_bolzano(expr_str, a_bz, b_bz)
                if fig:
                    st.markdown('<div class="graph-label">Bolzano visualisation</div>',
                                unsafe_allow_html=True)
                    st.pyplot(fig); plt.close(fig)
            else:
                render_steps(analyze_notable())
        else:
            style.empty_state("lim")