import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

import style

x_sym = sp.Symbol('x')
t_sym = sp.Symbol('t')

# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    ax.axhline(0, color="#1a1814", linewidth=0.6)


# ── INTUITION ─────────────────────────────────────────────────────────────────

def solve_intuition():
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("The area problem",
        """A car moves with varying velocity v(t). How far does it travel from t=0 to t=T?<br><br>
If v were constant: distance = v·T. One rectangle.<br><br>
If v varies: divide time into n intervals, approx v(tₖ) in each, distance ≈ Σ v(tₖ)·Δt.<br>
As Δt→0: <span class='mf'>distance = ∫₀ᵀ v(t) dt</span><br><br>
The integral IS the area under the velocity curve. Geometry and physics — the same thing.""", "warm")

    add("The notation ∫ₐᵇ f(x) dx",
        """· ∫ is an elongated S — for <em>Sum</em> (Leibniz chose deliberately)<br>
· f(x) is the height of each rectangle<br>
· dx is the infinitesimal width<br>
· a and b are where you start and stop<br><br>
The integral is literally an infinite sum of infinitely thin rectangles f(x)·dx.""")

    add("Riemann sums — watching convergence",
        "∫₀¹ x² dx = 1/3 ≈ 0.33333…<br><br>"
        + "<br>".join(
            f"n={n}: midpoint sum = {sum(((k+0.5)/n)**2*(1/n) for k in range(n)):.6f}"
            for n in [2,5,10,50,100]
        ), "sage")

    return {"steps": steps}


def plot_riemann(expr_str, a, b, n):
    try:
        expr = sp.sympify(expr_str)
        f_n  = sp.lambdify(x_sym, expr, "numpy")
        x_r  = np.linspace(a-0.2, b+0.2, 400)
        y_r  = np.array(f_n(x_r), dtype=float)
        fig, axes = plt.subplots(1,2,figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
        for ax, method, col, lbl in [(axes[0],"left","#e8602a","Left sum"),
                                     (axes[1],"mid","#3d6b5e","Midpoint sum")]:
            styled_ax(ax, fig)
            ax.plot(x_r, np.where(np.isfinite(y_r),y_r,np.nan),
                    color="#1a1814", linewidth=2.2, label=f"f(x)={expr}")
            dx = (b-a)/n; xs = np.linspace(a,b,n+1); total=0
            for i in range(n):
                xi = xs[i] if method=="left" else (xs[i]+xs[i+1])/2
                h  = float(f_n(xi)); total+=h*dx
                rect=plt.Rectangle((xs[i],min(0,h)),dx,abs(h),
                                    edgecolor=col,facecolor=col,alpha=0.3,linewidth=0.7)
                ax.add_patch(rect)
            ax.set_title(f"{lbl} = {total:.4f}",fontsize=10,color="#4a4540")
            ax.set_xlabel("x",color="#4a4540",fontsize=9)
            ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        plt.tight_layout(); return fig
    except: return None


# ── FTC ───────────────────────────────────────────────────────────────────────

def solve_ftc():
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("The most important theorem in calculus",
        """Before this theorem: computing areas required a different geometric argument per function.<br>
After: pure algebra. Two completely unrelated ideas — the same operation.<br><br>
<strong>Part 1:</strong> If F(x) = ∫ₐˣ f(t)dt, then F'(x) = f(x).<br>
The derivative of the area function IS the original function.<br>
Integration and differentiation are inverse operations.<br><br>
<strong>Part 2:</strong> ∫ₐᵇ f(x)dx = F(b) − F(a)<br>
To find the area: find any antiderivative F, evaluate at b and a, subtract.""", "warm")

    add("Why is Part 2 so powerful?",
        """∫₀¹ x² dx with Riemann sums: take n rectangles, add them up, take the limit. Long.<br><br>
Using FTC: what function has derivative x²? → x³/3<br>
∫₀¹ x² dx = [x³/3]₀¹ = 1/3 − 0 = 1/3. <strong>Two lines. Done.</strong>""")

    examples = [
        ("x**2", 0, 1, "x³/3", "1/3−0 = 1/3"),
        ("sin(x)", 0, "pi", "−cos(x)", "−cos(π)+cos(0) = 1+1 = 2"),
        ("exp(x)", 0, 1, "eˣ", "e−1 ≈ 1.718"),
        ("1/x", 1, "E", "ln(x)", "ln(e)−ln(1) = 1−0 = 1"),
    ]
    for f_s, a, b, prim, expl in examples:
        expr = sp.sympify(f_s)
        b_s  = "π" if b=="pi" else "e" if b=="E" else str(b)
        res  = float(sp.integrate(expr, (x_sym, sp.sympify(str(a)), sp.sympify(b.replace("E","E").replace("pi","pi")))).evalf())
        add(f"∫_{a}^{b_s} {f_s} dx",
            f"Primitive: {prim}<br>{expl}<br>≈ {res:.6f}", "sage")

    return {"steps": steps}


# ── ANTIDERIVATIVES ───────────────────────────────────────────────────────────

PRIMITIVES_TABLE = [
    ("xⁿ (n≠−1)", "xⁿ⁺¹/(n+1)+C", "Power rule in reverse. x²→x³/3, x⁻²→−x⁻¹, √x→(2/3)x^(3/2)"),
    ("1/x", "ln|x|+C", "Fills the gap at n=−1. Absolute value handles x<0."),
    ("eˣ", "eˣ+C", "eˣ is its own antiderivative — the only such function."),
    ("aˣ", "aˣ/ln(a)+C", "For any base a>0, a≠1."),
    ("sin(x)", "−cos(x)+C", "(−cosx)' = sinx ✓"),
    ("cos(x)", "sin(x)+C", "(sinx)' = cosx ✓"),
    ("1/cos²(x)", "tan(x)+C", "(tanx)' = 1/cos²x ✓"),
    ("1/√(1−x²)", "arcsin(x)+C", "Inverse trig — appears in geometry."),
    ("1/(1+x²)", "arctan(x)+C", "∫₋∞^∞ 1/(1+x²)dx = π (beautiful fact)."),
]

def solve_antideriv(expr_str):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("The +C",
        """If F(x) is a primitive of f(x), so is F(x)+C for any constant C.<br>
(F+C)' = F' + 0 = f. Constants vanish under differentiation.<br><br>
<strong>∫f(x)dx = F(x)+C</strong> — the <em>indefinite</em> integral.<br>
The +C is not optional.<br><br>
In a definite integral: [F(b)+C]−[F(a)+C] = F(b)−F(a). The C cancels.""", "warm")

    add("Table of basic primitives",
        "<br>".join(f"∫ {f} dx = {p} &nbsp;→ {n}" for f,p,n in PRIMITIVES_TABLE))

    try:
        expr = sp.sympify(expr_str)
        F    = sp.simplify(sp.integrate(expr, x_sym))
        df   = sp.simplify(sp.diff(F, x_sym) - expr)
        ok   = df == 0
        add("Your integral",
            f"∫ {expr} dx = <strong>{F}</strong> + C<br>"
            f"Verify: d/dx[{F}] = {sp.simplify(sp.diff(F,x_sym))}"
            +(" = f(x) ✓" if ok else " — check manually"),
            "sage")
    except Exception as e:
        add("Error", str(e), "error")

    return {"steps": steps}


# ── TECHNIQUES ────────────────────────────────────────────────────────────────

def solve_technique(name, expr_str, a=None, b=None):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    if name == "Substitution":
        add("Substitution — chain rule reversed",
            """If you see g'(x) as a factor, set u=g(x), du=g'(x)dx.<br><br>
<span class='mf'>∫f(g(x))·g'(x)dx → let u=g(x) → ∫f(u)du = F(u)+C = F(g(x))+C</span><br><br>
Signal: a composite function f(g(x)) with g'(x) sitting nearby as a factor.""", "warm")
        examples = [
            ("2*x*cos(x**2)", "u=x², du=2xdx → ∫cos(u)du = sin(u)+C = sin(x²)+C"),
            ("exp(x)/(exp(x)+1)", "u=eˣ+1, du=eˣdx → ∫1/u du = ln|u|+C = ln(eˣ+1)+C"),
            ("x*sqrt(x**2+4)", "u=x²+4, du=2xdx → (1/2)∫√u du = (x²+4)^(3/2)/3 + C"),
        ]
        for f_s, expl in examples:
            F = sp.simplify(sp.integrate(sp.sympify(f_s), x_sym))
            add(f"∫ {f_s} dx", f"{expl}<br>Sympy: {F}+C")
        if expr_str:
            try:
                expr = sp.sympify(expr_str)
                F = sp.simplify(sp.integrate(expr, x_sym))
                add("Your integral", f"∫ {expr} dx = <strong>{F}</strong> + C", "sage")
                if a is not None and b is not None:
                    res = float(sp.integrate(expr,(x_sym,a,b)).evalf())
                    add(f"Definite ∫_{a}^{b}", f"= <strong>{res:.6f}</strong>", "sage")
            except Exception as e:
                add("Error", str(e), "error")

    elif name == "Integration by parts":
        add("Integration by parts — product rule reversed",
            """(u·v)' = u'·v + u·v' → integrate → <span class='mf'>∫u dv = u·v − ∫v du</span><br><br>
<strong>LIATE</strong> — choose u as the highest on this list:<br>
L=Logarithms · I=Inverse trig · A=Algebraic · T=Trig · E=Exponential""", "warm")
        examples = [
            ("x*exp(x)", "u=x, dv=eˣdx → du=dx, v=eˣ → x·eˣ − ∫eˣdx = eˣ(x−1)+C"),
            ("x*sin(x)", "u=x, dv=sinxdx → du=dx, v=−cosx → −x·cosx+∫cosdx = −x·cosx+sinx+C"),
            ("log(x)", "write as ln(x)·1, u=lnx, dv=dx → x·lnx−∫dx = x(lnx−1)+C"),
            ("exp(x)*sin(x)", "Parts twice: I=eˣ(sinx−cosx)/2+C (circular trick!)"),
        ]
        for f_s, expl in examples:
            F = sp.simplify(sp.integrate(sp.sympify(f_s), x_sym))
            add(f"∫ {f_s} dx", f"{expl}<br>Sympy: {F}+C")
        if expr_str:
            try:
                expr = sp.sympify(expr_str)
                F = sp.simplify(sp.integrate(expr, x_sym))
                add("Your integral", f"∫ {expr} dx = <strong>{F}</strong> + C", "sage")
            except Exception as e:
                add("Error", str(e), "error")

    elif name == "Partial fractions":
        add("Partial fractions",
            """Decompose a rational function into simpler pieces, each integrating to a log.<br><br>
(x+3)/((x−1)(x+1)) = A/(x−1) + B/(x+1)<br>
x=1 → 4=2A → A=2. x=−1 → 2=−2B → B=−1.<br><br>
∫(x+3)/(x²−1)dx = 2ln|x−1| − ln|x+1| + C""", "warm")
        if expr_str:
            try:
                expr = sp.sympify(expr_str)
                F = sp.simplify(sp.integrate(expr, x_sym))
                add("Your integral", f"∫ {expr} dx = <strong>{F}</strong> + C", "sage")
            except Exception as e:
                add("Error", str(e), "error")

    return {"steps": steps}


# ── APPLICATIONS ──────────────────────────────────────────────────────────────

def solve_area(f_str, g_str, a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Area between two curves",
        f"Area = ∫_{a}^{b} |f(x)−g(x)| dx<br><br>"
        "At each x, the height of the region is |f(x)−g(x)|.", "warm")
    try:
        f_expr = sp.sympify(f_str); g_expr = sp.sympify(g_str)
        diff   = f_expr - g_expr
        area   = float(sp.integrate(sp.Abs(diff),(x_sym,a,b)).evalf())
        ints   = [float(p) for p in sp.solve(diff,x_sym)
                  if sp.sympify(p).is_real and a<=float(p)<=b]
        body   = f"f(x) = {f_expr}<br>g(x) = {g_expr}<br><br>Area = <strong>{area:.6f}</strong>"
        if ints: body += f"<br>Curves cross at x={[f'{p:.4f}' for p in ints]}"
        add("Result", body, "sage")
        return {"steps":steps,"f_expr":f_expr,"g_expr":g_expr,"a":a,"b":b,"area":area}
    except Exception as e:
        add("Error",str(e),"error"); return {"steps":steps}


def solve_volume(f_str, a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Volume of solid of revolution",
        "<span class='mf'>V = π·∫ₐᵇ [f(x)]² dx</span><br><br>"
        "Slice into discs: each disc has radius f(x), thickness dx, volume π[f(x)]²dx.", "warm")
    try:
        f_expr = sp.sympify(f_str)
        V = sp.pi * sp.integrate(f_expr**2,(x_sym,a,b))
        add("Result",
            f"f(x) = {f_expr}<br>"
            f"V = π·∫_{a}^{b} [{f_expr}]² dx = {sp.simplify(V)} ≈ {float(V.evalf()):.6f}",
            "sage")
        return {"steps":steps,"f_expr":f_expr,"a":a,"b":b}
    except Exception as e:
        add("Error",str(e),"error"); return {"steps":steps}


def solve_average(f_str, a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Average value of a function",
        "<span class='mf'>f_avg = (1/(b−a))·∫ₐᵇ f(x)dx</span><br><br>"
        "The height of the rectangle on [a,b] with the same area as the region under f.<br>"
        "Mean Value Theorem: f actually HITS its average at some c∈[a,b].", "warm")
    try:
        f_expr = sp.sympify(f_str)
        area   = sp.integrate(f_expr,(x_sym,a,b))
        f_avg  = area/(b-a)
        f_avg_n= float(f_avg.evalf())
        cs     = [float(c) for c in sp.solve(f_expr-f_avg,x_sym)
                  if sp.sympify(c).is_real and a<=float(c)<=b]
        body   = f"∫_{a}^{b} f dx = {sp.simplify(area)}<br>f_avg = <strong>{f_avg_n:.6f}</strong>"
        if cs: body += f"<br>f({cs[0]:.4f}) = f_avg ✓ (Mean Value Theorem)"
        add("Result", body, "sage")
        return {"steps":steps,"f_expr":f_expr,"a":a,"b":b,"f_avg":f_avg_n}
    except Exception as e:
        add("Error",str(e),"error"); return {"steps":steps}


def solve_surprises(choice):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    if choice == "Gaussian integral":
        add("∫₋∞^∞ e^(−x²) dx = √π",
            """One of the most beautiful results in mathematics.<br>
e^(−x²) has NO elementary primitive — yet the integral over all ℝ is exactly √π.<br><br>
<strong>The proof (squaring trick):</strong><br>
Let I = ∫₋∞^∞ e^(−x²)dx.<br>
I² = ∫∫ e^(−(x²+y²)) dx dy = ∫₀^{2π} ∫₀^∞ e^(−r²)·r dr dθ<br>
= 2π·[−e^(−r²)/2]₀^∞ = 2π·(1/2) = π<br>
Therefore I = √π. □""", "warm")
        from scipy import integrate as sci_int
        result,_ = sci_int.quad(lambda x: np.exp(-x**2), -10, 10)
        add("Numerical check",
            f"∫₋₁₀^₁₀ e^(−x²) dx ≈ {result:.10f}<br>"
            f"√π = {math.sqrt(math.pi):.10f}<br>"
            f"Error: {abs(result-math.sqrt(math.pi)):.2e}", "sage")

    elif choice == "Gabriel's Horn":
        add("Gabriel's Horn — finite volume, infinite surface",
            """Rotate y=1/x (x≥1) around the x-axis.<br><br>
Volume = π·∫₁^∞ (1/x)² dx = π·[−1/x]₁^∞ = π <strong>(finite!)</strong><br><br>
Surface area > 2π·∫₁^∞ 1/x dx = ∞ <strong>(infinite!)</strong><br><br>
You could fill it with paint, but you could never coat its surface.<br>
Not a paradox — a precise mathematical fact.""", "warm")

    elif choice == "Why eˣ is special":
        add("eˣ = its own derivative AND its own antiderivative",
            """No other function has this property.<br><br>
f'(x) = f(x) has a unique solution with f(0)=1: it's eˣ.<br>
'I grow at exactly the rate I currently have.' This self-referential property<br>
makes eˣ appear everywhere: radioactive decay, population growth, cooling law.<br><br>
<strong>What is e?</strong><br>
e = lim(n→∞)(1+1/n)ⁿ — the limit of continuous compounding.""", "warm")
        rows="".join(
            f"n={n}: (1+1/n)^n = {(1+1/n)**n:.8f}<br>"
            for n in [1,2,5,10,100,1000,10000])
        rows += f"e = {math.e:.8f}"
        add("Convergence to e", rows, "sage")

    elif choice == "No elementary primitive":
        add("Most functions have no elementary primitive",
            """'Elementary' = combination of polynomials, exponentials, logs, trig.<br><br>
These simple functions have NO elementary primitive:<br>
· e^(−x²) — the bell curve; defines erf(x)<br>
· sin(x)/x — the sinc function; ∫₀^∞ sin(x)/x dx = π/2 (exact, not elementary)<br>
· 1/ln(x) — the logarithmic integral; describes prime distribution<br>
· √(1−k²sin²x) — elliptic integral; governs pendulum motion<br><br>
This is not a failure. It's a reminder that the universe is richer<br>
than any set of formulas. The solution: numerical integration.""")
        try:
            from scipy import integrate as sci_int
            r1,_ = sci_int.quad(lambda x: np.sin(x)/x if x!=0 else 1.0, 0.001, 100)
            add("∫₀^∞ sin(x)/x dx", f"Numerical: {r1:.8f} vs π/2={math.pi/2:.8f}", "sage")
        except: pass

    return {"steps": steps}


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_area_fig(r):
    f_expr=r["f_expr"]; g_expr=r["g_expr"]; a=r["a"]; b=r["b"]
    f_n=sp.lambdify(x_sym,f_expr,"numpy"); g_n=sp.lambdify(x_sym,g_expr,"numpy")
    x_r=np.linspace(a-0.5,b+0.5,500); x_f=np.linspace(a,b,500)
    y_f=np.array(f_n(x_r),dtype=float); y_g=np.array(g_n(x_r),dtype=float)
    yf_fill=np.array(f_n(x_f),dtype=float); yg_fill=np.array(g_n(x_f),dtype=float)
    fig,ax=plt.subplots(figsize=(8,4)); fig.patch.set_facecolor("#fdfaf5"); styled_ax(ax,fig)
    ax.plot(x_r,np.where(np.isfinite(y_f),y_f,np.nan),color="#3d6b5e",linewidth=2.2,label=f"f={f_expr}")
    ax.plot(x_r,np.where(np.isfinite(y_g),y_g,np.nan),color="#e8602a",linewidth=2.2,label=f"g={g_expr}")
    ax.fill_between(x_f,yf_fill,yg_fill,where=yf_fill>=yg_fill,alpha=0.3,color="#3d6b5e")
    ax.fill_between(x_f,yf_fill,yg_fill,where=yf_fill<yg_fill,alpha=0.3,color="#e8602a")
    y_all=np.concatenate([y_f[np.isfinite(y_f)],y_g[np.isfinite(y_g)]])
    if len(y_all)>0: ax.set_ylim(np.percentile(y_all,2),np.percentile(y_all,98))
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    ax.set_xlabel("x",color="#4a4540",fontsize=9)
    ax.set_title("Area between curves",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


def plot_volume_fig(r):
    f_expr=r["f_expr"]; a=r["a"]; b=r["b"]
    f_n=sp.lambdify(x_sym,f_expr,"numpy")
    x_r=np.linspace(a,b,200)
    try:
        y_r=np.abs(np.array(f_n(x_r),dtype=float))
        fig=plt.figure(figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
        ax1=fig.add_subplot(121)
        styled_ax(ax1,fig)
        x_plot=np.linspace(a-0.3,b+0.3,400)
        y_plot=np.array(f_n(x_plot),dtype=float)
        ax1.plot(x_plot,np.where(np.isfinite(y_plot),y_plot,np.nan),color="#3d6b5e",linewidth=2.2)
        ax1.fill_between(x_r,y_r,alpha=0.2,color="#3d6b5e")
        ax1.fill_between(x_r,-y_r,alpha=0.2,color="#e8602a",label="rotation region")
        ax1.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
        ax1.set_title("Curve to rotate",fontsize=10,color="#4a4540"); ax1.set_xlabel("x",color="#4a4540",fontsize=9)
        ax2=fig.add_subplot(122,projection='3d'); ax2.set_facecolor("#fdfaf5")
        theta=np.linspace(0,2*np.pi,50)
        X,T=np.meshgrid(x_r,theta); R=np.array([y_r]*len(theta))
        Y=R*np.cos(T); Z=R*np.sin(T)
        ax2.plot_surface(X,Y,Z,alpha=0.4,color="#3d6b5e",edgecolor="none")
        ax2.set_title("Solid of revolution",fontsize=10,color="#4a4540")
        plt.tight_layout(); return fig
    except: return None


def plot_avg_fig(r):
    f_expr=r["f_expr"]; a=r["a"]; b=r["b"]; f_avg=r["f_avg"]
    f_n=sp.lambdify(x_sym,f_expr,"numpy")
    x_r=np.linspace(a-0.3,b+0.3,400)
    x_fill=np.linspace(a,b,400)
    y_r=np.array(f_n(x_r),dtype=float); y_fill=np.array(f_n(x_fill),dtype=float)
    fig,ax=plt.subplots(figsize=(8,4)); fig.patch.set_facecolor("#fdfaf5"); styled_ax(ax,fig)
    ax.plot(x_r,np.where(np.isfinite(y_r),y_r,np.nan),color="#3d6b5e",linewidth=2.2,label=f"f={f_expr}")
    ax.fill_between(x_fill,np.where(np.isfinite(y_fill),y_fill,0),alpha=0.15,color="#3d6b5e")
    ax.axhline(f_avg,color="#e8602a",linewidth=2.5,linestyle="--",label=f"Average={f_avg:.4f}")
    ax.fill_between([a,b],[f_avg,f_avg],[0,0],alpha=0.2,color="#e8602a",label="Same-area rectangle")
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    ax.set_xlabel("x",color="#4a4540",fontsize=9)
    ax.set_title("Average value",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


def plot_gaussian():
    from scipy import integrate as sci_int
    x_r=np.linspace(-4,4,500); y_r=np.exp(-x_r**2)
    cumul=np.array([sci_int.quad(lambda t: np.exp(-t**2),-4,xi)[0] for xi in x_r])
    fig,axes=plt.subplots(1,2,figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    axes[0].plot(x_r,y_r,color="#3d6b5e",linewidth=2.2,label="e^(−x²)")
    axes[0].fill_between(x_r,y_r,alpha=0.25,color="#3d6b5e",label=f"Area=√π≈{math.sqrt(math.pi):.4f}")
    axes[0].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[0].set_xlabel("x",color="#4a4540",fontsize=9); axes[0].set_title("∫₋∞^∞ e^(−x²)dx=√π",fontsize=10,color="#4a4540")
    axes[1].plot(x_r,cumul,color="#e8602a",linewidth=2.2,label="Running integral")
    axes[1].axhline(math.sqrt(math.pi),color="#3d6b5e",linewidth=2,linestyle="--",label=f"√π={math.sqrt(math.pi):.4f}")
    axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[1].set_xlabel("x",color="#4a4540",fontsize=9); axes[1].set_title("Cumulative → √π",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Intuition & Riemann sums",
             "Fundamental theorem",
             "Antiderivatives",
             "Substitution",
             "Integration by parts",
             "Partial fractions",
             "Area between curves",
             "Volume of revolution",
             "Average value",
             "Surprising facts"],
            key="int_topic")

        if topic == "Intuition & Riemann sums":
            expr_r = st.text_input("f(x) =", value="x**2+1", key="int_rf")
            a_r    = st.number_input("a", value=0.0, step=0.5, key="int_ra")
            b_r    = st.number_input("b", value=3.0, step=0.5, key="int_rb")
            n_r    = st.number_input("n rectangles", value=8, min_value=1, max_value=100, step=4, key="int_rn")

        elif topic == "Antiderivatives":
            expr_a = st.text_input("f(x) =", value="x**2*sin(x)", key="int_af")

        elif topic in ["Substitution","Integration by parts","Partial fractions"]:
            expr_t = st.text_input("Integrand f(x) =", value="" , key="int_tf")
            use_def = st.checkbox("Definite integral?", key="int_tdef")
            if use_def:
                a_t = st.number_input("a", value=0.0, step=0.5, key="int_ta")
                b_t = st.number_input("b", value=1.0, step=0.5, key="int_tb")

        elif topic == "Area between curves":
            f_str_a = st.text_input("f(x) =", value="x**2", key="int_af2")
            g_str_a = st.text_input("g(x) =", value="x", key="int_ag2")
            a_ar    = st.number_input("a", value=0.0, step=0.5, key="int_aa")
            b_ar    = st.number_input("b", value=1.0, step=0.5, key="int_ab")

        elif topic == "Volume of revolution":
            f_str_v = st.text_input("f(x) =", value="sqrt(x)", key="int_vf")
            a_vr    = st.number_input("a", value=0.0, step=0.5, key="int_va")
            b_vr    = st.number_input("b", value=4.0, step=0.5, key="int_vb")

        elif topic == "Average value":
            f_str_av = st.text_input("f(x) =", value="sin(x)", key="int_avf")
            a_avr    = st.number_input("a", value=0.0, step=0.5, key="int_ava")
            b_avr    = st.number_input("b", value=float(math.pi), step=0.5, key="int_avb")

        elif topic == "Surprising facts":
            surp = st.selectbox("Which",
                ["Gaussian integral","Gabriel's Horn","Why eˣ is special","No elementary primitive"],
                key="int_surp")

        solve_btn = st.button("Compute →", key="int_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Antideriv: <code>x**2*sin(x)</code><br>
    Subst: <code>2*x*cos(x**2)</code><br>
    Parts: <code>x*exp(x)</code><br>
    Area: f=x², g=x, [0,1]<br>
    Volume: f=sqrt(x), [0,4]<br>
    Gaussian: see √π emerge
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Intuition & Riemann sums":
                r = solve_intuition()
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Riemann sums</div>', unsafe_allow_html=True)
                fig = plot_riemann(expr_r, a_r, b_r, int(n_r))
                if fig: st.pyplot(fig); plt.close(fig)

            elif topic == "Fundamental theorem":
                r = solve_ftc()
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Antiderivatives":
                r = solve_antideriv(expr_a)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic in ["Substitution","Integration by parts","Partial fractions"]:
                a_def = a_t if use_def else None
                b_def = b_t if use_def else None
                r = solve_technique(topic, expr_t, a_def, b_def)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Area between curves":
                r = solve_area(f_str_a, g_str_a, a_ar, b_ar)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "area" in r:
                    style.result_band(("Area", f"{r['area']:.6f}"))
                    st.markdown('<div class="graph-label">Area between curves</div>', unsafe_allow_html=True)
                    fig = plot_area_fig(r); st.pyplot(fig); plt.close(fig)

            elif topic == "Volume of revolution":
                r = solve_volume(f_str_v, a_vr, b_vr)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "f_expr" in r:
                    st.markdown('<div class="graph-label">Solid of revolution</div>', unsafe_allow_html=True)
                    fig = plot_volume_fig(r)
                    if fig: st.pyplot(fig); plt.close(fig)

            elif topic == "Average value":
                r = solve_average(f_str_av, a_avr, b_avr)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "f_avg" in r:
                    style.result_band(("f_avg", f"{r['f_avg']:.6f}"))
                    st.markdown('<div class="graph-label">Average value</div>', unsafe_allow_html=True)
                    fig = plot_avg_fig(r); st.pyplot(fig); plt.close(fig)

            else:
                r = solve_surprises(surp)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if surp == "Gaussian integral":
                    st.markdown('<div class="graph-label">Gaussian integral</div>', unsafe_allow_html=True)
                    fig = plot_gaussian(); st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("∫f(x)dx")