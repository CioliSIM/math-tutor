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
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)


# ── INTUITION ─────────────────────────────────────────────────────────────────

def solve_intuition():
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("From average to instantaneous speed",
        """A car travels 120 km in 2 hours → average speed = 60 km/h.<br><br>
Now harder: what is the speed at <em>exactly</em> 1:37pm?<br>
That instantaneous rate of change is the <strong>derivative</strong>.<br><br>
<strong>The construction:</strong><br>
Average speed on [t, t+h] = [f(t+h)−f(t)]/h<br>
As h→0: average → instantaneous → <span class='mf'>f'(t) = lim(h→0) [f(t+h)−f(t)]/h</span>""",
        "warm")

    add("Geometric picture",
        """Draw a curve y=f(x).<br>
Draw a line through (x, f(x)) and (x+h, f(x+h)) — that's the <strong>secant</strong>.<br>
Slope of secant = [f(x+h)−f(x)]/h<br><br>
As h→0, the second point slides into the first.<br>
The secant → <strong>tangent line</strong>.<br>
Slope of tangent = <strong>the derivative</strong>.<br><br>
f'(x) = slope of the tangent to the curve at x.<br>
Large f' → steep curve. f'=0 → horizontal tangent → candidate max/min.""")

    # numerical illustration for f(x)=x²
    add("Watching h shrink for f(x)=x² at x=1",
        "f'(1) = lim(h→0) [(1+h)²−1]/h = lim(h→0) [2+h] = 2<br><br>"
        + "<br>".join(
            f"h={10**(-k):g}: average rate = {((1+10**(-k))**2-1)/10**(-k):.8f}"
            for k in range(0,7)
        ), "sage")

    add("Formal definition",
        """<span class='mf'>f'(x) = lim(h→0) [f(x+h)−f(x)] / h</span><br><br>
<strong>Notations</strong> (all mean the same):<br>
f'(x) · df/dx · ẋ (Newton, time derivatives)<br><br>
<strong>When does f'(x) NOT exist?</strong><br>
· Corner: f(x)=|x| at x=0 — left slope −1, right slope +1, they disagree<br>
· Vertical tangent: slope=∞ (not a real number)<br>
· Discontinuity: differentiable → continuous (not vice versa)""")

    return {"steps": steps}


def plot_secant_tangent():
    fig, axes = plt.subplots(1, 3, figsize=(12,4)); fig.patch.set_facecolor("#fdfaf5")
    x_r = np.linspace(-0.5, 3, 300); y_r = x_r**2
    for ax, h in zip(axes, [2, 0.5, 0.01]):
        styled_ax(ax, fig); ax.set_aspect("auto")
        ax.plot(x_r, y_r, color="#3d6b5e", linewidth=2.2, label="f(x)=x²")
        x0,y0 = 1,1; x1,y1 = 1+h,(1+h)**2
        slope_sec = (y1-y0)/h
        xs = np.linspace(0.3, min(x1+0.3,3), 100)
        ax.plot(xs, y0+slope_sec*(xs-x0), color="#e8602a", linewidth=2,
                linestyle="--", label=f"Secant h={h} slope={slope_sec:.2f}")
        xt = np.linspace(0.3,1.7,100)
        ax.plot(xt, y0+2*(xt-x0), color="#c8a96e", linewidth=1.5,
                linestyle=":", label="Tangent slope=2")
        ax.plot(x0,y0,"o",color="#1a1814",markersize=8)
        ax.plot(x1,y1,"o",color="#e8602a",markersize=7)
        ax.set_xlim(-0.3,3); ax.set_ylim(-0.5,6)
        ax.set_title(f"h={h}",fontsize=10,color="#4a4540")
        ax.legend(fontsize=7.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        ax.set_xlabel("x",color="#4a4540",fontsize=9)
    plt.tight_layout(); return fig


# ── RULES ─────────────────────────────────────────────────────────────────────

RULES_TABLE = [
    ("CONSTANT", "f(x)=c", "f'(x)=0", "A constant never changes."),
    ("POWER RULE", "f(x)=xⁿ", "f'(x)=n·xⁿ⁻¹", "Bring exponent down, reduce by 1. Works for any real n."),
    ("NATURAL EXP", "f(x)=eˣ", "f'(x)=eˣ", "eˣ is its own derivative — the defining property of e."),
    ("EXPONENTIAL", "f(x)=aˣ", "f'(x)=aˣ·ln(a)", "When a=e: ln(e)=1, reduces to eˣ."),
    ("NATURAL LOG", "f(x)=ln(x)", "f'(x)=1/x", "Valid for x>0. Reciprocal."),
    ("SINE", "f(x)=sin(x)", "f'(x)=cos(x)", "At peak of sin: slope=0=cos(π/2). ✓"),
    ("COSINE", "f(x)=cos(x)", "f'(x)=−sin(x)", "Minus sign: cos decreasing when sin positive."),
    ("TAN", "f(x)=tan(x)", "f'(x)=1/cos²(x)", "Derived from quotient rule on sin/cos."),
]

def solve_rules(rule_name):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    if rule_name == "Basic derivatives":
        add("The building blocks",
            "Every other derivative is assembled from these. Learn them by heart.",
            "warm")
        for name, f, df, note in RULES_TABLE:
            add(name, f"<span class='mf'>{f} → {df}</span><br>{note}")
        add("A beautiful cycle",
            "sin'=cos · cos'=−sin · (−sin)'=−cos · (−cos)'=sin<br>"
            "The 4th derivative of sin is sin again — a cycle of period 4.", "sage")

    elif rule_name == "Product rule":
        add("Product rule",
            "<span class='mf'>(f·g)' = f'·g + f·g'</span><br><br>"
            "WRONG instinct: f'·g'. Check: (x·x)'=(x²)'=2x, but x'·x'=1≠2x.<br><br>"
            "Geometric intuition: area = f·g. When x grows by dx:<br>"
            "f grows by f'·dx, g grows by g'·dx → area grows by f'·dx·g + f·g'·dx.<br>"
            "Rate = f'g + fg'.", "warm")
        examples = [
            ("x**2*sin(x)", "f=x², g=sinx → 2x·sinx+x²·cosx"),
            ("exp(x)*cos(x)", "f=eˣ, g=cosx → eˣ·cosx−eˣ·sinx = eˣ(cosx−sinx)"),
            ("x*log(x)", "f=x, g=lnx → lnx+x·(1/x) = lnx+1"),
        ]
        for f_str, expl in examples:
            expr = sp.sympify(f_str)
            d = sp.simplify(sp.diff(expr, x_sym))
            add(f"Example: {f_str}", f"{expl}<br>Sympy confirms: {d}")

    elif rule_name == "Quotient rule":
        add("Quotient rule",
            "<span class='mf'>(f/g)' = (f'·g − f·g') / g²</span><br><br>"
            "Memory: 'low d-high minus high d-low, over low squared'<br>"
            "<strong>Order matters</strong> in the numerator — getting it backwards is the most common error.", "warm")
        examples = [
            ("sin(x)/x", "(cosx·x − sinx·1)/x² = (x·cosx−sinx)/x²"),
            ("(x**2+1)/(x-1)", "(2x(x−1)−(x²+1))/(x−1)² = (x²−2x−1)/(x−1)²"),
            ("exp(x)/x", "(eˣ·x−eˣ)/x² = eˣ(x−1)/x²"),
        ]
        for f_str, expl in examples:
            expr = sp.sympify(f_str)
            d = sp.simplify(sp.diff(expr, x_sym))
            add(f"Example: {f_str}", f"{expl}<br>Sympy: {d}")
        add("Deriving (tanx)' from scratch",
            "tanx = sinx/cosx<br>(tanx)' = (cosx·cosx − sinx·(−sinx))/cos²x = (cos²x+sin²x)/cos²x = 1/cos²x ✓", "sage")

    elif rule_name == "Chain rule":
        add("Chain rule — the most important",
            "<span class='mf'>(f(g(x)))' = f'(g(x)) · g'(x)</span><br><br>"
            "In Leibniz: dy/dx = dy/du · du/dx — the du cancels like a fraction.<br><br>"
            "Intuition — gears: if gear A turns 3× as fast as your hand,<br>"
            "and gear B turns 2× as fast as gear A → gear B turns 6× as fast.<br>"
            "Rates of change multiply.", "warm")
        examples = [
            ("sin(x**2)", "outer=sin(u), inner=x² → cos(x²)·2x = 2x·cos(x²)"),
            ("exp(3*x)", "outer=eᵘ, inner=3x → e^(3x)·3 = 3e^(3x)"),
            ("(x**2+1)**10", "outer=u^10, inner=x²+1 → 10(x²+1)⁹·2x = 20x(x²+1)⁹"),
            ("log(sin(x))", "outer=ln(u), inner=sinx → (1/sinx)·cosx = cotx"),
        ]
        for f_str, expl in examples:
            expr = sp.sympify(f_str)
            d = sp.simplify(sp.diff(expr, x_sym))
            add(f"Example: {f_str}", f"{expl}<br>Sympy: {d}")
        add("How to spot the chain rule",
            "Ask: is there a function INSIDE another?<br>"
            "sin(x²) → YES → chain rule.<br>"
            "sin(x)·x² → NO → product rule.", "sage")

    return {"steps": steps}


# ── APPLICATIONS ──────────────────────────────────────────────────────────────

def solve_diff(expr_str, x_val):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    try:
        expr  = sp.sympify(expr_str)
        deriv = sp.simplify(sp.diff(expr, x_sym))
        deriv2 = sp.simplify(sp.diff(deriv, x_sym))
        val   = float(deriv.subs(x_sym, x_val))

        add("Differentiation", f"f(x) = {expr}<br>f'(x) = <strong>{deriv}</strong><br>f''(x) = <strong>{deriv2}</strong>")
        add(f"Evaluate at x={x_val}", f"f'({x_val}) = <strong>{val:.6f}</strong><br>This is the slope of the tangent to f at x={x_val}.", "sage")
        return {"steps":steps,"expr":expr,"deriv":deriv,"x_val":x_val,"val":val}
    except Exception as e:
        add("Error", str(e), "error")
        return {"steps":steps}


def solve_critical(expr_str):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    try:
        expr   = sp.sympify(expr_str)
        deriv  = sp.diff(expr, x_sym)
        deriv2 = sp.diff(deriv, x_sym)
        crits  = [c for c in sp.solve(deriv, x_sym) if c.is_real]

        add("Critical points — where f'(x)=0",
            "At a maximum or minimum the tangent is horizontal → slope=0 → derivative=0.<br><br>"
            f"f(x) = {expr}<br>f'(x) = {sp.simplify(deriv)}<br>f''(x) = {sp.simplify(deriv2)}", "warm")
        add(f"Critical points", f"{crits}")

        for cp in crits:
            fv  = sp.simplify(expr.subs(x_sym,cp))
            f2v = sp.simplify(deriv2.subs(x_sym,cp))
            if f2v.is_real:
                verdict = "LOCAL MINIMUM ∪" if f2v>0 else "LOCAL MAXIMUM ∩" if f2v<0 else "Inconclusive"
            else:
                verdict = "Check manually"
            add(f"x={cp}: f({cp})={fv}", f"f''({cp})={f2v} → {verdict}", "sage" if "MIN" in verdict or "MAX" in verdict else "")

        return {"steps":steps,"expr":expr,"deriv":deriv,"deriv2":deriv2,"crits":crits}
    except Exception as e:
        add("Error", str(e), "error")
        return {"steps":steps}


def solve_lhopital(expr_str, point_str):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("De L'Hôpital's Rule",
        """If lim f(x)=0 and lim g(x)=0 (or both →∞):<br>
<span class='mf'>lim f(x)/g(x) = lim f'(x)/g'(x)</span><br><br>
Near x=a: f(x)≈f'(a)(x−a), g(x)≈g'(a)(x−a) → ratio→f'(a)/g'(a).""", "warm")

    try:
        expr = sp.sympify(expr_str)
        if point_str == "inf":
            point = sp.oo
        elif point_str == "-inf":
            point = -sp.oo
        else:
            point = sp.sympify(point_str)
        result = sp.limit(expr, x_sym, point)
        add(f"lim(x→{point_str}) {expr_str}", f"= <strong>{result}</strong>", "sage")
        return {"steps":steps}
    except Exception as e:
        add("Error", str(e), "error")
        return {"steps":steps}


def solve_approx(expr_str, a_val):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Linear approximation",
        f"Near x=a: <span class='mf'>f(x) ≈ f(a) + f'(a)·(x−a)</span><br><br>"
        "This is just the tangent line equation.<br>"
        "Works well when x is close to a. Fails for large distances.", "warm")

    try:
        expr  = sp.sympify(expr_str)
        deriv = sp.diff(expr, x_sym)
        fa    = float(expr.subs(x_sym, a_val))
        dfa   = float(deriv.subs(x_sym, a_val))
        add("Your function",
            f"f(x) = {expr}<br>f({a_val}) = {fa:.6f}<br>f'({a_val}) = {dfa:.6f}<br><br>"
            f"Approximation: f(x) ≈ {fa:.4f} + {dfa:.4f}·(x−{a_val})", "sage")

        rows = ""
        for delta in [0.1, 0.5, 1.0, 2.0]:
            for sign in [+1, -1]:
                xv = a_val + sign*delta
                exact = float(expr.subs(x_sym, xv))
                approx = fa + dfa*(xv-a_val)
                err = abs(exact-approx)
                rows += f"x={xv}: exact={exact:.4f}, approx={approx:.4f}, error={err:.2e}<br>"
        add("Accuracy at various x", rows)
        return {"steps":steps,"expr":expr,"deriv":deriv,"a_val":a_val}
    except Exception as e:
        add("Error", str(e), "error")
        return {"steps":steps}


def solve_motion(expr_str):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    t = sp.Symbol('t')
    add("Velocity and acceleration",
        """<span class='mf'>v(t) = s'(t) &nbsp;&nbsp; a(t) = v'(t) = s''(t)</span><br><br>
Newton invented calculus in the 1660s to describe planetary motion.<br>
F=ma is about the <em>second</em> derivative of position.""", "warm")

    try:
        s = sp.sympify(expr_str.replace('x','t'))
        v = sp.diff(s, t)
        a = sp.diff(v, t)
        add("Motion equations",
            f"s(t) = {s}<br>v(t) = {sp.simplify(v)}<br>a(t) = {sp.simplify(a)}")
        cv = [c for c in sp.solve(v,t) if c.is_real]
        if cv:
            lines = "<br>".join(f"t={c}: s={sp.simplify(s.subs(t,c))}" for c in cv)
            add("v=0 (momentarily at rest)", lines, "sage")
        return {"steps":steps,"s":s,"v":v,"a":a,"t":t}
    except Exception as e:
        add("Error",str(e),"error")
        return {"steps":steps}


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_diff(r):
    expr=r["expr"]; deriv=r["deriv"]; x_val=r["x_val"]; m=r["val"]
    f_n = sp.lambdify(x_sym, expr, "numpy")
    d_n = sp.lambdify(x_sym, deriv, "numpy")
    x_r = np.linspace(x_val-3, x_val+3, 500)
    try:
        y_f = np.array(f_n(x_r), dtype=float)
        y_d = np.array(d_n(x_r), dtype=float)
        y0  = float(expr.subs(x_sym, x_val))
        fig, axes = plt.subplots(1,2,figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
        for ax in axes: styled_ax(ax, fig)
        axes[0].plot(x_r, np.where(np.isfinite(y_f), y_f, np.nan),
                     color="#3d6b5e", linewidth=2.2, label=f"f(x)")
        tan = y0 + m*(x_r-x_val)
        axes[0].plot(x_r, tan, color="#e8602a", linewidth=1.8,
                     linestyle="--", label=f"Tangent slope={m:.3f}")
        axes[0].plot(x_val, y0, "o", color="#e8602a", markersize=9, zorder=5)
        y_fin = y_f[np.isfinite(y_f)]
        if len(y_fin)>0: axes[0].set_ylim(np.percentile(y_fin,2),np.percentile(y_fin,98))
        axes[0].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        axes[0].set_title("Function and tangent",fontsize=10,color="#4a4540")
        axes[0].set_xlabel("x",color="#4a4540",fontsize=9)
        axes[1].plot(x_r, np.where(np.isfinite(y_d), y_d, np.nan),
                     color="#c8a96e", linewidth=2.2, label="f'(x)")
        axes[1].axvline(x_val,color="#e8602a",linewidth=1.5,linestyle="--",alpha=0.7)
        axes[1].plot(x_val, m, "o", color="#e8602a", markersize=9, zorder=5)
        y_df = y_d[np.isfinite(y_d)]
        if len(y_df)>0: axes[1].set_ylim(np.percentile(y_df,2),np.percentile(y_df,98))
        axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        axes[1].set_title("Derivative",fontsize=10,color="#4a4540")
        axes[1].set_xlabel("x",color="#4a4540",fontsize=9)
        plt.tight_layout(); return fig
    except: return None


def plot_critical(r):
    expr=r["expr"]; deriv=r["deriv"]; deriv2=r["deriv2"]; crits=r["crits"]
    if not crits: return None
    cx = float(sum(crits)/len(crits))
    x_r = np.linspace(cx-4, cx+4, 500)
    f_n = sp.lambdify(x_sym, expr, "numpy")
    d_n = sp.lambdify(x_sym, deriv, "numpy")
    try:
        y_f = np.array(f_n(x_r), dtype=float)
        y_d = np.array(d_n(x_r), dtype=float)
        fig, axes = plt.subplots(1,2,figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
        for ax in axes: styled_ax(ax, fig)
        axes[0].plot(x_r, np.where(np.isfinite(y_f),y_f,np.nan), color="#3d6b5e", linewidth=2.2)
        for cp in crits:
            cpf=float(expr.subs(x_sym,cp)); cpd2=float(deriv2.subs(x_sym,cp))
            col="#e8602a" if cpd2<0 else "#3d6b5e" if cpd2>0 else "#c8a96e"
            lbl="max" if cpd2<0 else "min" if cpd2>0 else "?"
            axes[0].plot(float(cp),cpf,"o",color=col,markersize=11,zorder=5,label=f"x={float(cp):.2f} ({lbl})")
        y_fin=y_f[np.isfinite(y_f)]
        if len(y_fin)>0: axes[0].set_ylim(np.percentile(y_fin,2),np.percentile(y_fin,98))
        axes[0].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        axes[0].set_title("Function with critical points",fontsize=10,color="#4a4540")
        axes[0].set_xlabel("x",color="#4a4540",fontsize=9)
        axes[1].plot(x_r, np.where(np.isfinite(y_d),y_d,np.nan), color="#c8a96e", linewidth=2.2, label="f'(x)")
        axes[1].axhline(0,color="#1a1814",linewidth=1.5,linestyle="--",alpha=0.7,label="f'=0")
        for cp in crits:
            axes[1].axvline(float(cp),color="#e8602a",linewidth=1.5,linestyle=":",alpha=0.7)
            axes[1].plot(float(cp),0,"o",color="#e8602a",markersize=9,zorder=5)
        y_df=y_d[np.isfinite(y_d)]
        if len(y_df)>0: axes[1].set_ylim(np.percentile(y_df,2),np.percentile(y_df,98))
        axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        axes[1].set_title("Derivative — zeros are critical points",fontsize=10,color="#4a4540")
        axes[1].set_xlabel("x",color="#4a4540",fontsize=9)
        plt.tight_layout(); return fig
    except: return None


def plot_motion_fig(r):
    s=r["s"]; v=r["v"]; a=r["a"]; t=r["t"]
    t_r = np.linspace(0,6,400)
    try:
        s_n=sp.lambdify(t,s,"numpy"); v_n=sp.lambdify(t,v,"numpy"); a_n=sp.lambdify(t,a,"numpy")
        ys=np.array(s_n(t_r),dtype=float); yv=np.array(v_n(t_r),dtype=float); ya=np.array(a_n(t_r),dtype=float)
        fig,axes=plt.subplots(1,3,figsize=(12,4)); fig.patch.set_facecolor("#fdfaf5")
        for ax,y,lab,col in zip(axes,[ys,yv,ya],["s(t) position","v(t) velocity","a(t) acceleration"],
                                 ["#3d6b5e","#e8602a","#c8a96e"]):
            styled_ax(ax,fig)
            ax.plot(t_r,np.where(np.isfinite(y),y,np.nan),color=col,linewidth=2.2,label=lab)
            ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
            ax.set_xlabel("t",color="#4a4540",fontsize=9)
            y_fin=y[np.isfinite(y)]
            if len(y_fin)>0: ax.set_ylim(np.percentile(y_fin,1),np.percentile(y_fin,99))
        plt.tight_layout(); return fig
    except: return None


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Intuition & Definition",
             "Basic derivatives",
             "Product rule","Quotient rule","Chain rule",
             "Differentiate a function",
             "Critical points (maxima/minima)",
             "De L'Hôpital",
             "Linear approximation",
             "Physics: motion"],
            key="drv_topic")

        if topic == "Differentiate a function":
            expr_s = st.text_input("f(x) =", value="x**3 - 3*x", key="drv_expr")
            x_v    = st.number_input("Evaluate f'(x) at x=", value=1.0, step=0.5, key="drv_xv")

        elif topic == "Critical points (maxima/minima)":
            expr_s = st.text_input("f(x) =", value="x**3 - 3*x", key="drv_crit_expr")

        elif topic == "De L'Hôpital":
            expr_s = st.text_input("f(x)/g(x) =", value="sin(x)/x", key="drv_lhop")
            pt_s   = st.text_input("x→ (0, inf, -inf, or number)", value="0", key="drv_pt")

        elif topic == "Linear approximation":
            expr_s = st.text_input("f(x) =", value="sqrt(x)", key="drv_approx_expr")
            a_v    = st.number_input("Expand near x=a=", value=4.0, step=0.5, key="drv_av")

        elif topic == "Physics: motion":
            expr_s = st.text_input("s(t) =", value="t**3 - 6*t", key="drv_mot")

        solve_btn = st.button("Compute →", key="drv_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Diff: <code>x**3-3*x</code> at x=2<br>
    Diff: <code>sin(x)*exp(x)</code><br>
    Critical: <code>x**4-4*x**2</code><br>
    L'Hôpital: <code>sin(x)/x</code> x→0<br>
    L'Hôpital: <code>(exp(x)-1)/x</code> x→0<br>
    Motion: <code>t**3-6*t</code>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Intuition & Definition":
                r = solve_intuition()
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Secant → tangent</div>', unsafe_allow_html=True)
                fig = plot_secant_tangent(); st.pyplot(fig); plt.close(fig)

            elif topic in ["Basic derivatives","Product rule","Quotient rule","Chain rule"]:
                r = solve_rules(topic)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Differentiate a function":
                r = solve_diff(expr_s, x_v)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "expr" in r:
                    style.result_band(("f'(x)",str(sp.simplify(r["deriv"]))),
                                      (f"f'({x_v})",f"{r['val']:.6f}"))
                    st.markdown('<div class="graph-label">Function and derivative</div>', unsafe_allow_html=True)
                    fig = plot_diff(r)
                    if fig: st.pyplot(fig); plt.close(fig)

            elif topic == "Critical points (maxima/minima)":
                r = solve_critical(expr_s)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "crits" in r and r["crits"]:
                    st.markdown('<div class="graph-label">Critical points</div>', unsafe_allow_html=True)
                    fig = plot_critical(r)
                    if fig: st.pyplot(fig); plt.close(fig)

            elif topic == "De L'Hôpital":
                r = solve_lhopital(expr_s, pt_s)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Linear approximation":
                r = solve_approx(expr_s, a_v)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            else:
                r = solve_motion(expr_s)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "s" in r:
                    st.markdown('<div class="graph-label">Position, velocity, acceleration</div>', unsafe_allow_html=True)
                    fig = plot_motion_fig(r)
                    if fig: st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("f'(x)")