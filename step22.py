import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_area_between(f_expr, g_expr, a, b, x_sym):
    f_num = sp.lambdify(x_sym, f_expr, "numpy")
    g_num = sp.lambdify(x_sym, g_expr, "numpy")

    x_r      = np.linspace(a-0.5, b+0.5, 500)
    x_fill   = np.linspace(a, b, 500)
    y_f      = f_num(x_r)
    y_g      = g_num(x_r)
    y_f_fill = f_num(x_fill)
    y_g_fill = g_num(x_fill)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(x_r, y_f, color="steelblue", linewidth=2.5,
            label=f"f(x) = {f_expr}")
    ax.plot(x_r, y_g, color="crimson",   linewidth=2.5,
            label=f"g(x) = {g_expr}")
    ax.fill_between(x_fill, y_f_fill, y_g_fill,
                    where=y_f_fill >= y_g_fill,
                    alpha=0.3, color="steelblue", label="Area (f≥g)")
    ax.fill_between(x_fill, y_f_fill, y_g_fill,
                    where=y_f_fill < y_g_fill,
                    alpha=0.3, color="crimson",   label="Area (g>f)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(a, color="gray", linewidth=1, linestyle=":")
    ax.axvline(b, color="gray", linewidth=1, linestyle=":")
    ax.set_title("Area between two curves", fontsize=13)
    ax.set_xlabel("x")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    y_all = np.concatenate([y_f[np.isfinite(y_f)], y_g[np.isfinite(y_g)]])
    if len(y_all) > 0:
        ax.set_ylim(np.percentile(y_all, 2), np.percentile(y_all, 98))
    plt.tight_layout()
    plt.show()


def plot_average_value(f_expr, a, b, f_avg, x_sym):
    f_num   = sp.lambdify(x_sym, f_expr, "numpy")
    x_r     = np.linspace(a-0.3, b+0.3, 400)
    y_r     = np.array(f_num(x_r), dtype=float)
    x_fill  = np.linspace(a, b, 400)
    y_fill  = np.array(f_num(x_fill), dtype=float)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x_r, y_r, color="steelblue", linewidth=2.5,
            label=f"f(x) = {f_expr}")
    ax.fill_between(x_fill, y_fill, alpha=0.15, color="steelblue",
                    label="Area under f")
    ax.axhline(f_avg, color="crimson", linewidth=2.5, linestyle="--",
               label=f"Average value = {f_avg:.4f}")
    ax.fill_between([a, b], [f_avg, f_avg], [0, 0],
                    alpha=0.2, color="crimson",
                    label="Rectangle with same area")
    ax.axvline(a, color="gray", linewidth=1, linestyle=":")
    ax.axvline(b, color="gray", linewidth=1, linestyle=":")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Average value of a function", fontsize=13)
    ax.set_xlabel("x")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    y_finite = y_r[np.isfinite(y_r)]
    if len(y_finite) > 0:
        ax.set_ylim(min(np.percentile(y_finite, 2), f_avg-1),
                    max(np.percentile(y_finite, 98), f_avg+1))
    plt.tight_layout()
    plt.show()


def intuition_integral():
    print(f"\n{'='*50}")
    print(f"WHAT IS AN INTEGRAL?")
    print(f"{'='*50}")
    print(f"")
    print(f"  Start with the simplest area you know:")
    print(f"  a rectangle.  Base × height.  Done.")
    print(f"")
    print(f"  Now the harder question:")
    print(f"  what is the area under a curve?")
    print(f"  The boundary isn't straight — rectangles don't fit perfectly.")
    print(f"")
    print(f"  The idea: fill the region with many thin rectangles.")
    print(f"  The thinner they are, the better they fit the curve.")
    print(f"  At the limit — infinitely many, infinitely thin —")
    print(f"  you get the exact area.")
    print(f"  That limit is the INTEGRAL.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  THE CONNECTION TO VELOCITY")
    print(f"")
    print(f"  A car moves with varying velocity v(t).")
    print(f"  How far does it travel from t=0 to t=T?")
    print(f"")
    print(f"  If v were constant: distance = v·T.  One rectangle.")
    print(f"")
    print(f"  If v varies: divide time into n small intervals.")
    print(f"  In interval k, velocity ≈ v(tₖ).  Distance ≈ v(tₖ)·Δt.")
    print(f"  Total ≈ Σ v(tₖ)·Δt.")
    print(f"  As Δt → 0 and n → ∞:")
    print(f"")
    print(f"      distance = ∫₀ᵀ v(t) dt")
    print(f"")
    print(f"  The integral IS the area under the velocity curve.")
    print(f"  And that area IS the distance traveled.")
    print(f"  Geometry and physics — the same thing.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  THE NOTATION")
    print(f"")
    print(f"      ∫ₐᵇ f(x) dx")
    print(f"")
    print(f"  · ∫  is an elongated S — for 'Sum'.")
    print(f"    Leibniz chose it deliberately.")
    print(f"  · f(x) is the height of each rectangle.")
    print(f"  · dx is the infinitesimal width.")
    print(f"  · a and b are where you start and stop.")
    print(f"")
    print(f"  The integral is literally an infinite sum of")
    print(f"  infinitely thin rectangles f(x)·dx.")
    print(f"  The notation was designed to remind you of this.")

    plot_integral_intuition()


def plot_integral_intuition():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    x = np.linspace(0, 3, 300)
    y = x**2 + 1

    for ax, n in zip(axes, [4, 10, 50]):
        ax.plot(x, y, color="steelblue", linewidth=2.5,
                label="f(x) = x²+1")
        ax.fill_between(x, y, alpha=0.08, color="steelblue")

        x_rects = np.linspace(0, 3, n+1)
        for i in range(n):
            xi    = x_rects[i]
            xi1   = x_rects[i+1]
            mid   = (xi + xi1) / 2
            h     = mid**2 + 1
            width = xi1 - xi
            rect  = plt.Rectangle((xi, 0), width, h,
                                   edgecolor="crimson",
                                   facecolor="crimson",
                                   alpha=0.3, linewidth=0.8)
            ax.add_patch(rect)

        ax.set_xlim(0, 3)
        ax.set_ylim(0, 12)
        ax.set_title(f"n = {n} rectangles", fontsize=12)
        ax.set_xlabel("x")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.suptitle("More rectangles → closer to the exact area",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def riemann_sums():
    print(f"\n{'='*50}")
    print(f"RIEMANN SUMS")
    print(f"{'='*50}")
    print(f"")
    print(f"  The formal version of 'many thin rectangles'.")
    print(f"  Named after Bernhard Riemann (1826-1866),")
    print(f"  who gave integration its rigorous foundation.")
    print(f"")
    print(f"  SETUP:")
    print(f"  Divide [a,b] into n equal subintervals of width Δx=(b-a)/n.")
    print(f"  In each subinterval [xᵢ, xᵢ₊₁], pick a sample point xᵢ*.")
    print(f"  The rectangle at position i has:")
    print(f"  · height = f(xᵢ*)  (value of f at the sample point)")
    print(f"  · width  = Δx")
    print(f"  · area   = f(xᵢ*)·Δx")
    print(f"")
    print(f"  RIEMANN SUM:")
    print(f"  Sₙ = Σᵢ f(xᵢ*)·Δx")
    print(f"")
    print(f"  Three common choices for xᵢ*:")
    print(f"  · LEFT endpoint:   xᵢ* = xᵢ          (often overestimates or underestimates)")
    print(f"  · RIGHT endpoint:  xᵢ* = xᵢ₊₁")
    print(f"  · MIDPOINT:        xᵢ* = (xᵢ+xᵢ₊₁)/2 (most accurate for the same n)")
    print(f"")
    print(f"  THE DEFINITION OF THE INTEGRAL:")
    print(f"  ∫ₐᵇ f(x) dx = lim(n→∞) Sₙ")
    print(f"")
    print(f"  This limit exists for all continuous functions.")
    print(f"  When it does, f is called INTEGRABLE on [a,b].")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  WATCHING THE CONVERGENCE")
    print(f"")
    print(f"  ∫₀¹ x² dx — exact answer is 1/3 ≈ 0.33333...")
    print(f"")
    print(f"  {'n':>8}  {'Left':>12}  {'Right':>12}"
          f"  {'Midpoint':>12}  {'Error (mid)':>12}")
    print(f"  {'─'*60}")
    exact = 1/3
    for n in [2, 5, 10, 50, 100, 1000]:
        dx    = 1/n
        xs    = np.linspace(0, 1, n+1)
        left  = sum(xs[i]**2 * dx             for i in range(n))
        right = sum(xs[i+1]**2 * dx           for i in range(n))
        mid   = sum(((xs[i]+xs[i+1])/2)**2*dx for i in range(n))
        err   = abs(mid - exact)
        print(f"  {n:>8}  {left:>12.8f}  {right:>12.8f}"
              f"  {mid:>12.8f}  {err:>12.2e}")

    print(f"")
    print(f"  Exact: {exact:.8f}")
    print(f"  All three converge. Midpoint is the most accurate.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  TRY IT YOURSELF")
    print(f"")

    x_sym    = sp.Symbol('x')
    expr_str = input("  f(x) = ")
    a        = float(input("  a = "))
    b        = float(input("  b = "))
    n        = int(input("  n = "))

    try:
        expr  = sp.sympify(expr_str)
        f_num = sp.lambdify(x_sym, expr, "numpy")

        dx    = (b-a)/n
        xs    = np.linspace(a, b, n+1)
        left  = sum(f_num(xs[i])*dx             for i in range(n))
        right = sum(f_num(xs[i+1])*dx           for i in range(n))
        mid   = sum(f_num((xs[i]+xs[i+1])/2)*dx for i in range(n))
        exact_val = float(sp.integrate(expr, (x_sym, a, b)))

        print(f"\n  Results with n={n} rectangles:")
        print(f"  Left sum:       {left:.8f}")
        print(f"  Right sum:      {right:.8f}")
        print(f"  Midpoint sum:   {mid:.8f}")
        print(f"  Exact value:    {exact_val:.8f}")
        print(f"  Midpoint error: {abs(mid-exact_val):.2e}")

        plot_riemann(expr, f_num, a, b, n)

    except Exception as e:
        print(f"  Could not compute: {e}")


def plot_riemann(expr, f_num, a, b, n):
    x_plot = np.linspace(a-0.2, b+0.2, 400)
    y_plot = f_num(x_plot)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, method, color, label in [
        (axes[0], "left", "crimson",   "Left Riemann sum"),
        (axes[1], "mid",  "steelblue", "Midpoint Riemann sum"),
    ]:
        ax.plot(x_plot, y_plot, color="black", linewidth=2.5,
                label=f"f(x) = {expr}")
        ax.fill_between(np.linspace(a, b, 400),
                        f_num(np.linspace(a, b, 400)),
                        alpha=0.08, color=color)

        dx    = (b-a)/n
        xs    = np.linspace(a, b, n+1)
        total = 0
        for i in range(n):
            xi = xs[i] if method == "left" else (xs[i]+xs[i+1])/2
            h  = f_num(xi)
            total += h * dx
            rect   = plt.Rectangle((xs[i], min(0,h)), dx, abs(h),
                                    edgecolor=color, facecolor=color,
                                    alpha=0.3, linewidth=0.8)
            ax.add_patch(rect)

        ax.set_title(f"{label}\nApprox = {total:.6f}", fontsize=11)
        ax.set_xlabel("x")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.axhline(0, color="black", linewidth=0.8)

    plt.suptitle(f"Riemann sums for ∫f(x)dx from {a} to {b}",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def fundamental_theorem():
    print(f"\n{'='*50}")
    print(f"THE FUNDAMENTAL THEOREM OF CALCULUS")
    print(f"{'='*50}")
    print(f"")
    print(f"  This is the most important theorem in all of calculus.")
    print(f"  It connects two ideas that seem completely unrelated:")
    print(f"  the area under a curve  and  the derivative.")
    print(f"")
    print(f"  Before this theorem, computing areas was hard —")
    print(f"  a different geometric argument for every function.")
    print(f"  After this theorem, it becomes pure algebra.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  PART 1 — The area function has a derivative")
    print(f"")
    print(f"  Define A(x) = ∫ₐˣ f(t) dt")
    print(f"  A(x) is the area under f from a to x.")
    print(f"  As x moves right, A(x) grows.")
    print(f"")
    print(f"  How fast does it grow?")
    print(f"  A(x+h) - A(x) = a thin strip of width h, height ≈ f(x).")
    print(f"  So [A(x+h)-A(x)]/h ≈ f(x).")
    print(f"  As h → 0: A'(x) = f(x).")
    print(f"")
    print(f"  THE FIRST PART:")
    print(f"  If F(x) = ∫ₐˣ f(t) dt,  then  F'(x) = f(x).")
    print(f"")
    print(f"  The derivative of the area function IS the original function.")
    print(f"  Integration and differentiation are inverse operations.")
    print(f"  Like + and -, like × and ÷ — but far more surprising.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  PART 2 — How to compute integrals")
    print(f"")
    print(f"  THE SECOND PART:")
    print(f"  If F'(x) = f(x), then:")
    print(f"")
    print(f"      ∫ₐᵇ f(x) dx = F(b) - F(a)")
    print(f"")
    print(f"  To find the area: find any function whose derivative")
    print(f"  is f, evaluate at b and a, subtract.")
    print(f"  No infinite sums. No limits. Pure algebra.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  WHY IS THIS SO SURPRISING?")
    print(f"")
    print(f"  Computing ∫₀¹ x² dx with Riemann sums:")
    print(f"  Take n rectangles, add them up, take the limit.")
    print(f"  Long, technical, specific to x².")
    print(f"")
    print(f"  Using the theorem:")
    print(f"  What function has derivative x²?  →  x³/3.")
    print(f"  ∫₀¹ x² dx = [x³/3]₀¹ = 1/3 - 0 = 1/3.")
    print(f"  Two lines. Done.")
    print(f"")
    print(f"  The theorem turns a geometric problem into an algebraic one.")
    print(f"  This is one of the most powerful ideas in all of mathematics.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  EXAMPLES")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("x²",     0,      1,
         "Primitive: x³/3\n"
         "  [x³/3]₀¹ = 1/3 - 0 = 1/3"),
        ("sin(x)", 0,      sp.pi,
         "Primitive: -cos(x)\n"
         "  [-cos x]₀^π = -cos π + cos 0 = 1+1 = 2"),
        ("exp(x)", 0,      1,
         "Primitive: eˣ\n"
         "  [eˣ]₀¹ = e - 1 ≈ 1.718"),
        ("1/x",    1,      sp.E,
         "Primitive: ln x\n"
         "  [ln x]₁^e = ln e - ln 1 = 1 - 0 = 1"),
    ]

    for func_str, a, b, explanation in examples:
        expr   = sp.sympify(func_str)
        result = sp.integrate(expr, (x, a, b))
        a_disp = "π" if a==sp.pi else "e" if a==sp.E else str(a)
        b_disp = "π" if b==sp.pi else "e" if b==sp.E else str(b)
        print(f"  ∫_{a_disp}^{b_disp} {func_str} dx")
        for line in explanation.split('\n'):
            print(f"  {line}")
        print(f"  = {sp.simplify(result)} ≈ {float(result):.6f}")
        print(f"")

    plot_fundamental_theorem()


def plot_fundamental_theorem():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    x_r = np.linspace(0, 2, 300)
    f   = x_r**2
    A   = x_r**3 / 3

    axes[0].plot(x_r, f, color="steelblue", linewidth=2.5,
                 label="f(x) = x²")
    x_mark  = 1.5
    x_fill  = np.linspace(0, x_mark, 200)
    axes[0].fill_between(x_fill, x_fill**2, alpha=0.35,
                         color="crimson",
                         label=f"A({x_mark}) = {x_mark**3/3:.3f}")
    axes[0].axvline(x_mark, color="crimson", linewidth=2, linestyle="--")
    axes[0].set_title("A(x) = ∫₀ˣ t² dt\n(area grows as x moves right)",
                      fontsize=11)
    axes[0].set_xlabel("x")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(x_r, A, color="green",     linewidth=2.5,
                 label="A(x) = x³/3  (primitive)")
    axes[1].plot(x_r, f, color="steelblue", linewidth=2.5,
                 linestyle="--", label="f(x) = x²  = A'(x)")
    axes[1].plot(x_mark, x_mark**3/3, "o", color="green", markersize=10)
    axes[1].annotate(f"slope here = {x_mark**2:.2f}",
                     (x_mark, x_mark**3/3),
                     textcoords="offset points",
                     xytext=(15, -20), fontsize=9)
    axes[1].set_title("A'(x) = f(x)\nThe derivative of the area IS the function",
                      fontsize=11)
    axes[1].set_xlabel("x")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Fundamental Theorem of Calculus",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def antiderivatives():
    print(f"\n{'='*50}")
    print(f"ANTIDERIVATIVES AND PRIMITIVES")
    print(f"{'='*50}")
    print(f"")
    print(f"  A primitive of f(x) is any function F(x) such that")
    print(f"  F'(x) = f(x).")
    print(f"  Also called antiderivative or indefinite integral.")
    print(f"")
    print(f"  THE +C:")
    print(f"  If F(x) is a primitive, so is F(x)+C for any constant C.")
    print(f"  Why? (F+C)' = F' + 0 = f.  Constants vanish.")
    print(f"  So there's a whole family of primitives — one per value of C.")
    print(f"")
    print(f"  We write: ∫ f(x) dx = F(x) + C")
    print(f"  This is the INDEFINITE integral.")
    print(f"  The +C is not optional — it must always appear.")
    print(f"")
    print(f"  WHEN DOES +C DISAPPEAR?")
    print(f"  In a DEFINITE integral ∫ₐᵇ:")
    print(f"  [F(x)+C]ₐᵇ = (F(b)+C) - (F(a)+C) = F(b)-F(a).")
    print(f"  The C cancels. So for definite integrals,")
    print(f"  any primitive gives the same answer.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  TABLE OF BASIC PRIMITIVES")
    print(f"  (The derivative table — read backwards)")
    print(f"")

    primitives = [
        ("xⁿ  (n≠-1)",
         "xⁿ⁺¹/(n+1) + C",
         "Power rule in reverse.\n"
         "  Exponent goes up by 1, divide by the new exponent.\n"
         "  x² → x³/3,   x⁻² → -x⁻¹,   √x → (2/3)x^(3/2)"),
        ("1/x",
         "ln|x| + C",
         "The absolute value handles x<0.\n"
         "  This fills the gap in the power rule (n=-1 was excluded)."),
        ("eˣ",
         "eˣ + C",
         "eˣ is its own derivative AND its own primitive.\n"
         "  No other function has this property."),
        ("aˣ",
         "aˣ/ln(a) + C",
         "For any base a>0, a≠1.\n"
         "  When a=e: ln(e)=1, reduces to eˣ. ✓"),
        ("sin(x)",
         "-cos(x) + C",
         "Because (-cos x)' = sin x. ✓"),
        ("cos(x)",
         "sin(x) + C",
         "Because (sin x)' = cos x. ✓"),
        ("1/cos²(x)",
         "tan(x) + C",
         "Because (tan x)' = 1/cos²x. ✓"),
        ("1/√(1-x²)",
         "arcsin(x) + C",
         "Inverse trig primitives — appear often in geometry and physics."),
        ("1/(1+x²)",
         "arctan(x) + C",
         "A beautiful fact: ∫₋∞^∞ 1/(1+x²) dx = π."),
    ]

    for func, prim, note in primitives:
        print(f"  {'─'*46}")
        print(f"  ∫ {func} dx  =  {prim}")
        for line in note.split('\n'):
            print(f"  {line}")
        print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  COMPUTE A PRIMITIVE")
    print(f"")
    x = sp.Symbol('x')
    expr_str = input("  f(x) = ")
    try:
        expr = sp.sympify(expr_str)
        F    = sp.integrate(expr, x)
        F_s  = sp.simplify(F)
        df   = sp.simplify(sp.diff(F_s, x) - expr)
        ok   = df == 0
        print(f"")
        print(f"  ∫ {expr} dx = {F_s} + C")
        print(f"  Verify: d/dx[{F_s}] = {sp.simplify(sp.diff(F_s,x))}")
        print(f"  {'= f(x) ✓' if ok else 'check manually'}")
    except Exception as e:
        print(f"  Could not compute: {e}")


def integration_techniques():
    print(f"\n{'='*50}")
    print(f"INTEGRATION TECHNIQUES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Finding derivatives is mechanical — you apply rules.")
    print(f"  Finding primitives is an ART.")
    print(f"  No single algorithm works for everything.")
    print(f"  You need to recognize patterns and choose the right move.")
    print(f"")
    print(f"  A few techniques cover most of what you'll meet in liceo.")
    print(f"")
    print(f"  1 — Immediate integration  (direct recognition)")
    print(f"  2 — Substitution           (chain rule reversed)")
    print(f"  3 — Integration by parts   (product rule reversed)")
    print(f"  4 — Partial fractions      (rational functions)")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        immediate_integration()
    elif choice == "2":
        substitution()
    elif choice == "3":
        integration_by_parts()
    elif choice == "4":
        partial_fractions()
    else:
        print(f"  Invalid choice.")


def immediate_integration():
    print(f"\n{'='*50}")
    print(f"IMMEDIATE INTEGRATION")
    print(f"{'='*50}")
    print(f"")
    print(f"  These are integrals you can write down directly —")
    print(f"  by recognizing the integrand as a known primitive.")
    print(f"  No technique needed, just pattern recognition.")
    print(f"")
    print(f"  The most important pattern to spot:")
    print(f"  if you see  f'(g(x))·g'(x),")
    print(f"  the primitive is  f(g(x)) + C.")
    print(f"  Chain rule in reverse.")
    print(f"")
    print(f"  THREE TEMPLATES:")
    print(f"")
    print(f"  ∫ [g(x)]ⁿ · g'(x) dx = [g(x)]ⁿ⁺¹/(n+1) + C")
    print(f"  ∫ g'(x) / g(x)  dx  = ln|g(x)| + C")
    print(f"  ∫ g'(x) · e^g(x) dx = e^g(x) + C")
    print(f"")
    print(f"  In all three: the derivative of the 'inside'")
    print(f"  is sitting right there as a factor.")
    print(f"  That's the signal.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("2x·e^(x²)",
         "Inside: x².  Its derivative: 2x.  Present? YES.\n"
         "  Template 3: ∫ g'·e^g = e^g\n"
         "  Primitive: e^(x²) + C",
         "exp(x**2)"),
        ("cos(x)·e^(sin x)",
         "Inside: sin x.  Its derivative: cos x.  Present? YES.\n"
         "  Primitive: e^(sin x) + C",
         "exp(sin(x))"),
        ("x/(x²+1)",
         "Inside: x²+1.  Its derivative: 2x.  We have x — off by 1/2.\n"
         "  x/(x²+1) = ½·[2x/(x²+1)]\n"
         "  Template 2: ∫ g'/g = ln|g|\n"
         "  Primitive: ½·ln(x²+1) + C",
         "log(x**2+1)/2"),
        ("1/(2x+3)",
         "Inside: 2x+3.  Its derivative: 2.  We have 1 — off by 1/2.\n"
         "  1/(2x+3) = ½·[2/(2x+3)]\n"
         "  Primitive: ½·ln|2x+3| + C",
         "log(2*x+3)/2"),
    ]

    for func_str, explanation, prim_str in examples:
        print(f"  ∫ {func_str} dx")
        for line in explanation.split('\n'):
            print(f"  {line}")
        F  = sp.sympify(prim_str)
        df = sp.simplify(sp.diff(F, x))
        print(f"  Verify: d/dx[{prim_str}] = {df}")
        print(f"")

    plot_immediate(x)


def plot_immediate(x):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x_r = np.linspace(-2, 2, 400)
    axes[0].plot(x_r, 2*x_r*np.exp(x_r**2), color="crimson",
                 linewidth=2.5, label="f(x) = 2x·e^(x²)")
    axes[0].plot(x_r, np.exp(x_r**2), color="steelblue",
                 linewidth=2.5, linestyle="--",
                 label="F(x) = e^(x²)")
    axes[0].set_title("d/dx[e^(x²)] = 2x·e^(x²)\nImmediate recognition",
                      fontsize=11)
    axes[0].set_ylim(-5, 20)
    axes[0].set_xlabel("x")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(0, color="black", linewidth=0.8)

    x_r2 = np.linspace(-4, 4, 400)
    axes[1].plot(x_r2, x_r2/(x_r2**2+1), color="crimson",
                 linewidth=2.5, label="f(x) = x/(x²+1)")
    axes[1].plot(x_r2, 0.5*np.log(x_r2**2+1), color="steelblue",
                 linewidth=2.5, linestyle="--",
                 label="F(x) = ½ln(x²+1)")
    axes[1].set_title("d/dx[½ln(x²+1)] = x/(x²+1)\nLog template",
                      fontsize=11)
    axes[1].set_xlabel("x")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(0, color="black", linewidth=0.8)

    plt.suptitle("Immediate integration — f (red) and its primitive F (blue)",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def substitution():
    print(f"\n{'='*50}")
    print(f"INTEGRATION BY SUBSTITUTION")
    print(f"{'='*50}")
    print(f"")
    print(f"  Substitution is the chain rule reversed.")
    print(f"  When you differentiated f(g(x)) you got f'(g(x))·g'(x).")
    print(f"  Substitution recognizes that pattern and undoes it.")
    print(f"")
    print(f"  THE METHOD:")
    print(f"  If you see g'(x) as a factor, set u = g(x).")
    print(f"  Then du = g'(x)·dx — the g'(x)·dx becomes just du.")
    print(f"  The integral simplifies to one in u.")
    print(f"  Integrate in u, then substitute x back.")
    print(f"")
    print(f"  TEMPLATE:")
    print(f"  ∫ f(g(x))·g'(x) dx")
    print(f"  → let u=g(x), du=g'(x)dx")
    print(f"  = ∫ f(u) du = F(u) + C = F(g(x)) + C")
    print(f"")
    print(f"  HOW TO SPOT IT:")
    print(f"  1. Find a composite function f(g(x)).")
    print(f"  2. Check if g'(x) appears as a factor (even up to a constant).")
    print(f"  3. If yes — substitution works.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        {
            "integral": "∫ 2x·cos(x²) dx",
            "func":     "2*x*cos(x**2)",
            "steps": [
                "Composite: cos(x²).  Inside: x².  Its derivative: 2x — present!",
                "Let u = x²,   du = 2x dx.",
                "∫ 2x·cos(x²) dx = ∫ cos(u) du = sin(u) + C",
                "Substitute back: sin(x²) + C",
            ],
        },
        {
            "integral": "∫ eˣ/(eˣ+1) dx",
            "func":     "exp(x)/(exp(x)+1)",
            "steps": [
                "Inside: eˣ+1.  Its derivative: eˣ — present!",
                "Let u = eˣ+1,   du = eˣ dx.",
                "∫ eˣ/(eˣ+1) dx = ∫ 1/u du = ln|u| + C",
                "Substitute back: ln(eˣ+1) + C",
            ],
        },
        {
            "integral": "∫ x·√(x²+4) dx",
            "func":     "x*sqrt(x**2+4)",
            "steps": [
                "Inside: x²+4.  Its derivative: 2x.  We have x — off by 1/2.",
                "Let u = x²+4,   du = 2x dx  →  x dx = du/2.",
                "∫ x·√(x²+4) dx = (1/2)·∫ √u du = (1/2)·u^(3/2)/(3/2) + C",
                "= (x²+4)^(3/2)/3 + C",
            ],
        },
        {
            "integral": "∫ sin(x)·cos³(x) dx",
            "func":     "sin(x)*cos(x)**3",
            "steps": [
                "Inside: cos(x).  Its derivative: -sin(x).  We have sin(x) — off by -1.",
                "Let u = cos(x),   du = -sin(x) dx  →  sin(x) dx = -du.",
                "∫ sin(x)·cos³(x) dx = ∫ u³·(-du) = -u⁴/4 + C",
                "Substitute back: -cos⁴(x)/4 + C",
            ],
        },
    ]

    for ex in examples:
        print(f"  {ex['integral']}")
        for step in ex['steps']:
            print(f"  · {step}")
        F   = sp.simplify(sp.integrate(sp.sympify(ex['func']), x))
        df  = sp.simplify(sp.diff(F, x) - sp.sympify(ex['func']))
        ok  = df == 0
        print(f"  Sympy: {F} + C")
        print(f"  {'  ✓' if ok else '  check manually'}")
        print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  SUBSTITUTION FOR DEFINITE INTEGRALS")
    print(f"")
    print(f"  When computing ∫ₐᵇ, also change the limits.")
    print(f"  If u = g(x): lower limit → g(a),  upper limit → g(b).")
    print(f"")
    print(f"  Example: ∫₀¹ 2x·cos(x²) dx")
    print(f"  u=x²: x=0→u=0, x=1→u=1.")
    print(f"  = ∫₀¹ cos(u) du = [sin u]₀¹ = sin(1) ≈ {math.sin(1):.6f}")
    x_sym = sp.Symbol('x')
    exact = float(sp.integrate(2*x_sym*sp.cos(x_sym**2), (x_sym,0,1)))
    print(f"  Sympy confirms: {exact:.6f} ✓")

    plot_substitution()


def plot_substitution():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(-2, 2, 400)
    axes[0].plot(x, 2*x*np.cos(x**2), color="crimson",   linewidth=2.5,
                 label="f(x) = 2x·cos(x²)")
    axes[0].plot(x, np.sin(x**2),      color="steelblue", linewidth=2.5,
                 linestyle="--", label="F(x) = sin(x²)")
    axes[0].set_title("u=x²  →  ∫2x·cos(x²)dx = sin(x²)+C",
                      fontsize=11)
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_xlabel("x")

    x2   = np.linspace(0, 1, 300)
    f2   = 2*x2*np.cos(x2**2)
    axes[1].plot(np.linspace(-0.3, 1.5, 400),
                 2*np.linspace(-0.3,1.5,400)*np.cos(np.linspace(-0.3,1.5,400)**2),
                 color="steelblue", linewidth=2.5,
                 label="f(x) = 2x·cos(x²)")
    axes[1].fill_between(x2, f2, alpha=0.4, color="crimson",
                         label=f"∫₀¹ = sin(1) ≈ {math.sin(1):.4f}")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title(f"Definite integral = sin(1) ≈ {math.sin(1):.4f}",
                      fontsize=11)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlabel("x")

    plt.suptitle("Substitution — chain rule reversed",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def integration_by_parts():
    print(f"\n{'='*50}")
    print(f"INTEGRATION BY PARTS")
    print(f"{'='*50}")
    print(f"")
    print(f"  The product rule says: (u·v)' = u'·v + u·v'")
    print(f"  Integrate both sides:")
    print(f"  u·v = ∫ u'·v dx + ∫ u·v' dx")
    print(f"  Rearrange:")
    print(f"")
    print(f"      ∫ u·v' dx = u·v - ∫ v·u' dx")
    print(f"")
    print(f"  Or in the classic notation:")
    print(f"      ∫ u dv = u·v - ∫ v du")
    print(f"")
    print(f"  You swap one integral for another.")
    print(f"  The art: choose u and dv so the new integral is SIMPLER.")
    print(f"")
    print(f"  HOW TO CHOOSE — use LIATE for u:")
    print(f"  L — Logarithms   (ln x, log x)")
    print(f"  I — Inverse trig (arcsin, arctan)")
    print(f"  A — Algebraic    (xⁿ, polynomials)")
    print(f"  T — Trig         (sin, cos)")
    print(f"  E — Exponential  (eˣ)")
    print(f"")
    print(f"  Pick the highest on the list as u.")
    print(f"  Everything else becomes dv.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        {
            "integral": "∫ x·eˣ dx",
            "func":     "x*exp(x)",
            "steps": [
                "LIATE: x=Algebraic, eˣ=Exponential.  A before E → u=x, dv=eˣdx.",
                "du = dx,   v = eˣ.",
                "∫ x·eˣ dx = x·eˣ - ∫ eˣ dx = x·eˣ - eˣ + C = eˣ(x-1) + C",
            ],
        },
        {
            "integral": "∫ x·sin(x) dx",
            "func":     "x*sin(x)",
            "steps": [
                "LIATE: x=Algebraic, sin=Trig.  A before T → u=x, dv=sin(x)dx.",
                "du = dx,   v = -cos(x).",
                "∫ x·sin(x) dx = -x·cos(x) + ∫ cos(x) dx = -x·cos(x) + sin(x) + C",
            ],
        },
        {
            "integral": "∫ ln(x) dx",
            "func":     "log(x)",
            "steps": [
                "Write as ln(x)·1.  LIATE: ln=Log, 1=Algebraic.  L first → u=ln(x), dv=dx.",
                "du = (1/x)dx,   v = x.",
                "∫ ln(x) dx = x·ln(x) - ∫ x·(1/x) dx = x·ln(x) - x + C = x(ln x-1) + C",
            ],
        },
        {
            "integral": "∫ eˣ·sin(x) dx",
            "func":     "exp(x)*sin(x)",
            "steps": [
                "Both at the bottom of LIATE — choose u=sin(x), dv=eˣdx.",
                "du = cos(x)dx,   v = eˣ.",
                "∫ eˣsin x dx = eˣsin x - ∫ eˣcos x dx",
                "Apply parts again to ∫ eˣcos x dx  (u=cos x, dv=eˣdx):",
                "= eˣcos x + ∫ eˣsin x dx",
                "So: ∫ eˣsin x dx = eˣsin x - eˣcos x - ∫ eˣsin x dx",
                "2·∫ eˣsin x dx = eˣ(sin x - cos x)",
                "∫ eˣsin x dx = eˣ(sin x - cos x)/2 + C",
                "TRICK: the integral appeared on both sides — solve algebraically!",
            ],
        },
    ]

    for ex in examples:
        print(f"  {ex['integral']}")
        for step in ex['steps']:
            print(f"  · {step}")
        F  = sp.simplify(sp.integrate(sp.sympify(ex['func']), x))
        df = sp.simplify(sp.diff(F, x) - sp.sympify(ex['func']))
        ok = df == 0
        print(f"  Sympy: {F} + C")
        print(f"  {'  ✓' if ok else '  check manually'}")
        print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  THE CIRCULAR TRICK:")
    print(f"  When parts brings you back to the same integral,")
    print(f"  call it I, get  I = [something] - I,")
    print(f"  then  2I = [something],  so  I = [something]/2.")
    print(f"  One of the most elegant moves in calculus.")

    plot_by_parts()


def plot_by_parts():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 3, 400)
    axes[0].plot(x, x*np.exp(x), color="crimson",   linewidth=2.5,
                 label="f(x) = x·eˣ")
    axes[0].plot(x, np.exp(x)*(x-1), color="steelblue", linewidth=2.5,
                 linestyle="--", label="F(x) = eˣ(x-1)")
    x2 = np.linspace(0, 2, 200)
    axes[0].fill_between(x2, x2*np.exp(x2), alpha=0.2, color="crimson")
    axes[0].set_title("∫ x·eˣ dx = eˣ(x-1) + C", fontsize=11)
    axes[0].set_ylim(-5, 30)
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_xlabel("x")

    x3 = np.linspace(0, 4*np.pi, 400)
    axes[1].plot(x3, x3*np.sin(x3), color="crimson",   linewidth=2.5,
                 label="f(x) = x·sin(x)")
    axes[1].plot(x3, -x3*np.cos(x3)+np.sin(x3),
                 color="steelblue", linewidth=2.5, linestyle="--",
                 label="F(x) = -x·cos(x)+sin(x)")
    axes[1].set_title("∫ x·sin(x) dx = -x·cos(x)+sin(x)+C", fontsize=11)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_xlabel("x")

    plt.suptitle("Integration by Parts — product rule reversed",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def partial_fractions():
    print(f"\n{'='*50}")
    print(f"PARTIAL FRACTIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  How do you integrate (x+3)/(x²-1)?")
    print(f"  The denominator factors: x²-1 = (x-1)(x+1).")
    print(f"  The idea: break the fraction into simpler pieces.")
    print(f"")
    print(f"  (x+3)/((x-1)(x+1)) = A/(x-1) + B/(x+1)")
    print(f"")
    print(f"  Each piece integrates to a log.")
    print(f"  ∫ 1/(x-1) dx = ln|x-1| + C")
    print(f"  ∫ 1/(x+1) dx = ln|x+1| + C")
    print(f"")
    print(f"  FINDING A AND B:")
    print(f"  Multiply both sides by (x-1)(x+1):")
    print(f"  x+3 = A(x+1) + B(x-1)")
    print(f"")
    print(f"  Substitute the roots of the denominator:")
    print(f"  x=1:   4 = 2A      →  A = 2")
    print(f"  x=-1:  2 = -2B     →  B = -1")
    print(f"")
    print(f"  So: (x+3)/(x²-1) = 2/(x-1) - 1/(x+1)")
    print(f"  ∫ (x+3)/(x²-1) dx = 2ln|x-1| - ln|x+1| + C")
    print(f"                     = ln((x-1)²/|x+1|) + C")
    print(f"")

    x    = sp.Symbol('x')
    expr = (x+3)/(x**2-1)
    F    = sp.integrate(expr, x)
    print(f"  Sympy confirms: {sp.simplify(F)} + C")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  WHEN TO USE PARTIAL FRACTIONS:")
    print(f"  · The integrand is a ratio of polynomials.")
    print(f"  · The denominator factors into linear factors.")
    print(f"  · After decomposition, each piece integrates to a log.")
    print(f"")
    print(f"  EXAMPLE 2: ∫ 1/(x²+x) dx")
    print(f"  x²+x = x(x+1)")
    print(f"  1/(x(x+1)) = A/x + B/(x+1)")
    print(f"  x=0:   1 = A    →  A = 1")
    print(f"  x=-1:  1 = -B   →  B = -1")
    print(f"  ∫ 1/(x²+x) dx = ln|x| - ln|x+1| + C = ln|x/(x+1)| + C")
    expr2 = 1/(x**2+x)
    F2    = sp.integrate(expr2, x)
    print(f"  Sympy confirms: {sp.simplify(F2)} + C")

    plot_partial_fractions()


def plot_partial_fractions():
    fig, ax = plt.subplots(figsize=(10, 5))

    x_r  = np.linspace(-3, 3, 600)
    mask = (np.abs(x_r-1)>0.1) & (np.abs(x_r+1)>0.1)
    x_m  = x_r[mask]

    ax.plot(x_m, (x_m+3)/(x_m**2-1), color="steelblue", linewidth=2.5,
            label="(x+3)/(x²-1)  original")
    ax.plot(x_m,  2/(x_m-1),          color="crimson",   linewidth=2,
            linestyle="--", label="2/(x-1)  part A")
    ax.plot(x_m, -1/(x_m+1),          color="green",     linewidth=2,
            linestyle=":",  label="-1/(x+1)  part B")
    ax.axvline( 1, color="gray", linewidth=1, linestyle="--", alpha=0.5)
    ax.axvline(-1, color="gray", linewidth=1, linestyle="--", alpha=0.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(-10, 10)
    ax.set_title("Partial fractions: decompose → each part integrates to a log",
                 fontsize=12)
    ax.set_xlabel("x")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def integral_applications():
    print(f"\n{'='*50}")
    print(f"APPLICATIONS OF INTEGRALS")
    print(f"{'='*50}")
    print(f"")
    print(f"  The integral computes far more than just areas.")
    print(f"  Any quantity that accumulates continuously")
    print(f"  — distance, volume, mass, probability —")
    print(f"  is an integral.")
    print(f"")
    print(f"  1 — Area between two curves")
    print(f"  2 — Volume of solids of revolution")
    print(f"  3 — Average value of a function")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        area_between_curves()
    elif choice == "2":
        volume_revolution()
    elif choice == "3":
        average_value()
    else:
        print(f"  Invalid choice.")


def area_between_curves():
    print(f"\n{'='*50}")
    print(f"AREA BETWEEN TWO CURVES")
    print(f"{'='*50}")
    print(f"")
    print(f"  The area between f(x) and g(x) on [a,b]:")
    print(f"      Area = ∫ₐᵇ |f(x) - g(x)| dx")
    print(f"")
    print(f"  At each x, the height of the region is |f(x)-g(x)|.")
    print(f"  The integral sums all those heights times dx.")
    print(f"")
    print(f"  If the curves cross, split the integral at each crossing.")
    print(f"  Or just use the absolute value — sympy handles it.")
    print(f"")

    x     = sp.Symbol('x')
    f_str = input("  f(x) = ")
    g_str = input("  g(x) = ")
    a     = float(input("  a = "))
    b     = float(input("  b = "))

    try:
        f_expr = sp.sympify(f_str)
        g_expr = sp.sympify(g_str)
        diff   = f_expr - g_expr
        area   = float(sp.integrate(sp.Abs(diff), (x, a, b)).evalf())

        print(f"\n  f(x) = {f_expr}")
        print(f"  g(x) = {g_expr}")
        print(f"  Area = ∫_{a}^{b} |f-g| dx = {area:.6f}")

        intersections = [float(p) for p in sp.solve(diff, x)
                         if sp.sympify(p).is_real and a<=float(p)<=b]
        if intersections:
            print(f"  Curves cross at x = {[f'{p:.4f}' for p in intersections]}")

        plot_area_between(f_expr, g_expr, a, b, x)

    except Exception as e:
        print(f"  Could not compute: {e}")


def volume_revolution():
    print(f"\n{'='*50}")
    print(f"VOLUME OF SOLIDS OF REVOLUTION")
    print(f"{'='*50}")
    print(f"")
    print(f"  Spin the curve y=f(x) around the x-axis.")
    print(f"  You get a 3D solid — like something turned on a lathe.")
    print(f"")
    print(f"      V = π · ∫ₐᵇ [f(x)]² dx")
    print(f"")
    print(f"  WHY?")
    print(f"  Slice the solid into thin discs perpendicular to x.")
    print(f"  Each disc at position x has radius f(x) and thickness dx.")
    print(f"  Volume of one disc = π·[f(x)]²·dx.")
    print(f"  Integrate → total volume.")
    print(f"")
    print(f"  CLASSIC EXAMPLE: the sphere.")
    print(f"  Rotate y=√(r²-x²) around the x-axis.")
    print(f"  V = π·∫₋ᵣʳ (r²-x²) dx = 4πr³/3")
    print(f"  The sphere formula — derived from integration. ✓")
    print(f"")

    x     = sp.Symbol('x')
    f_str = input("  f(x) = ")
    a     = float(input("  a = "))
    b     = float(input("  b = "))

    try:
        f_expr = sp.sympify(f_str)
        volume = sp.pi * sp.integrate(f_expr**2, (x, a, b))
        vol_n  = float(volume.evalf())

        print(f"\n  f(x) = {f_expr}")
        print(f"  V = π · ∫_{a}^{b} [{f_expr}]² dx")
        print(f"    = {sp.simplify(volume)}")
        print(f"    ≈ {vol_n:.6f}")

        plot_revolution(f_expr, a, b, x)

    except Exception as e:
        print(f"  Could not compute: {e}")


def plot_revolution(f_expr, a, b, x_sym):
    f_num = sp.lambdify(x_sym, f_expr, "numpy")
    x_r   = np.linspace(a, b, 200)

    try:
        y_r = np.abs(np.array(f_num(x_r), dtype=float))

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        x_plot = np.linspace(a-0.3, b+0.3, 400)
        y_plot = np.array(f_num(x_plot), dtype=float)
        ax1.plot(x_plot, y_plot, color="steelblue", linewidth=2.5,
                 label=f"f(x) = {f_expr}")
        ax1.fill_between(x_r,  y_r, alpha=0.2, color="steelblue")
        ax1.fill_between(x_r, -y_r, alpha=0.2, color="crimson",
                         label="rotation region")
        ax1.axhline(0, color="black", linewidth=1)
        ax1.set_title("Curve to rotate", fontsize=12)
        ax1.set_xlabel("x")
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        ax2    = fig.add_subplot(122, projection='3d')
        theta  = np.linspace(0, 2*np.pi, 60)
        X, T   = np.meshgrid(x_r, theta)
        R      = np.array([y_r]*len(theta))
        Y      = R * np.cos(T)
        Z      = R * np.sin(T)
        ax2.plot_surface(X, Y, Z, alpha=0.4, color="steelblue",
                         edgecolor="none")
        ax2.set_title("Solid of revolution", fontsize=12)
        ax2.set_xlabel("x")
        ax2.set_ylabel("y")
        ax2.set_zlabel("z")

        plt.suptitle(f"Rotating f(x)={f_expr} around the x-axis",
                     fontsize=13, fontweight="bold")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"  Could not plot: {e}")


def average_value():
    print(f"\n{'='*50}")
    print(f"AVERAGE VALUE OF A FUNCTION")
    print(f"{'='*50}")
    print(f"")
    print(f"  Average of n numbers: sum and divide by n.")
    print(f"  Average of a continuous function on [a,b]:")
    print(f"  integrate and divide by the length (b-a).")
    print(f"")
    print(f"      f_avg = (1/(b-a)) · ∫ₐᵇ f(x) dx")
    print(f"")
    print(f"  GEOMETRIC MEANING:")
    print(f"  f_avg is the height of the rectangle on [a,b]")
    print(f"  that has the SAME AREA as the region under f.")
    print(f"  It 'flattens' all the peaks and fills all the valleys.")
    print(f"")
    print(f"  MEAN VALUE THEOREM FOR INTEGRALS:")
    print(f"  If f is continuous on [a,b], there exists c ∈ [a,b]")
    print(f"  with f(c) = f_avg.")
    print(f"  The function actually HITS its average value somewhere.")
    print(f"")
    print(f"  REAL USE: average temperature over a day.")
    print(f"  T_avg = (1/24) · ∫₀²⁴ T(t) dt")
    print(f"  This is how meteorologists compute daily averages.")
    print(f"")

    x     = sp.Symbol('x')
    f_str = input("  f(x) = ")
    a     = float(input("  a = "))
    b     = float(input("  b = "))

    try:
        f_expr  = sp.sympify(f_str)
        area    = sp.integrate(f_expr, (x, a, b))
        f_avg   = area / (b-a)
        f_avg_n = float(f_avg.evalf())

        print(f"\n  f(x) = {f_expr}")
        print(f"  ∫_{a}^{b} f(x) dx = {sp.simplify(area)}")
        print(f"  f_avg = {sp.simplify(f_avg)} ≈ {f_avg_n:.6f}")

        c_sols = [float(c) for c in sp.solve(f_expr - f_avg, x)
                  if sp.sympify(c).is_real and a<=float(c)<=b]
        if c_sols:
            print(f"  Mean value theorem: f({c_sols[0]:.4f}) = f_avg ✓")

        plot_average_value(f_expr, a, b, f_avg_n, x)

    except Exception as e:
        print(f"  Could not compute: {e}")


def surprising_facts():
    print(f"\n{'='*50}")
    print(f"SURPRISING FACTS ABOUT INTEGRALS")
    print(f"{'='*50}")
    print(f"")
    print(f"  These are the results that make integration beautiful.")
    print(f"  Things that don't usually appear in textbooks,")
    print(f"  but that any curious student should know.")
    print(f"")
    print(f"  1 — The Gaussian integral: ∫₋∞^∞ e^(-x²) dx = √π")
    print(f"  2 — Improper integrals: infinite region, finite area")
    print(f"  3 — Why eˣ is miraculous")
    print(f"  4 — Functions with no elementary primitive")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        gaussian_integral()
    elif choice == "2":
        improper_integrals()
    elif choice == "3":
        exponential_miracle()
    elif choice == "4":
        no_elementary_primitive()
    else:
        print(f"  Invalid choice.")


def gaussian_integral():
    print(f"\n{'='*50}")
    print(f"THE GAUSSIAN INTEGRAL")
    print(f"{'='*50}")
    print(f"")
    print(f"  ∫₋∞^∞ e^(-x²) dx = √π")
    print(f"")
    print(f"  This is one of the most beautiful results in mathematics.")
    print(f"  e^(-x²) is the bell curve — the normal distribution.")
    print(f"  It appears in probability, physics, signal processing.")
    print(f"")
    print(f"  WHY IS IT SURPRISING?")
    print(f"  e^(-x²) has NO elementary primitive.")
    print(f"  You cannot write ∫ e^(-x²) dx in any standard form.")
    print(f"  Yet the integral over ALL of ℝ is exactly √π.")
    print(f"  A finite, clean answer — despite no antiderivative.")
    print(f"")
    print(f"  HOW IS IT COMPUTED?")
    print(f"  A brilliant trick: square the integral.")
    print(f"")
    print(f"  Let I = ∫₋∞^∞ e^(-x²) dx.")
    print(f"  I² = (∫e^(-x²)dx)(∫e^(-y²)dy) = ∫∫ e^(-(x²+y²)) dx dy")
    print(f"")
    print(f"  Switch to polar coordinates: r², dxdy = r dr dθ")
    print(f"  I² = ∫₀^2π ∫₀^∞ e^(-r²)·r dr dθ")
    print(f"     = 2π · ∫₀^∞ r·e^(-r²) dr")
    print(f"     = 2π · [-e^(-r²)/2]₀^∞")
    print(f"     = 2π · (1/2) = π")
    print(f"  Therefore I = √π. □")
    print(f"")
    print(f"  The 1/√(2π) in the normal distribution comes from here.")
    print(f"  Without this result, probability theory couldn't")
    print(f"  even normalize the bell curve properly.")
    print(f"")

    from scipy import integrate as sci_int
    result, _ = sci_int.quad(lambda x: np.exp(-x**2), -10, 10)
    print(f"  Numerical check:")
    print(f"  ∫₋₁₀^₁₀ e^(-x²) dx ≈ {result:.10f}")
    print(f"  √π                  = {math.sqrt(math.pi):.10f}")
    print(f"  Difference: {abs(result-math.sqrt(math.pi)):.2e}  (tails negligible)")

    plot_gaussian()


def plot_gaussian():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    x = np.linspace(-4, 4, 500)
    y = np.exp(-x**2)

    axes[0].plot(x, y, color="steelblue", linewidth=2.5,
                 label="e^(-x²)")
    axes[0].fill_between(x, y, alpha=0.25, color="steelblue",
                         label=f"Area = √π ≈ {math.sqrt(math.pi):.4f}")
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_title("∫₋∞^∞ e^(-x²) dx = √π\nThe Gaussian integral",
                      fontsize=12)
    axes[0].set_xlabel("x")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    dx    = x[1]-x[0]
    cumul = np.cumsum(y) * dx
    axes[1].plot(x, cumul, color="crimson", linewidth=2.5,
                 label="Running integral")
    axes[1].axhline(math.sqrt(math.pi), color="steelblue",
                    linewidth=2, linestyle="--",
                    label=f"√π = {math.sqrt(math.pi):.4f}")
    axes[1].set_title("Cumulative integral → √π",
                      fontsize=12)
    axes[1].set_xlabel("x")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("The Gaussian Integral — no antiderivative, but exact total area",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def improper_integrals():
    print(f"\n{'='*50}")
    print(f"IMPROPER INTEGRALS")
    print(f"{'='*50}")
    print(f"")
    print(f"  What if the interval is infinite?")
    print(f"  ∫₁^∞ f(x) dx = lim(b→∞) ∫₁^b f(x) dx")
    print(f"")
    print(f"  If the limit exists: CONVERGES.")
    print(f"  If not: DIVERGES.")
    print(f"")
    print(f"  THE CRITICAL FAMILY: ∫₁^∞ 1/xᵖ dx")
    print(f"  · p > 1:  converges to 1/(p-1)")
    print(f"  · p ≤ 1:  diverges")
    print(f"")
    print(f"  Why surprising?")
    print(f"  Both 1/x and 1/x² go to 0 as x→∞.")
    print(f"  But 1/x goes too slowly — its area is infinite.")
    print(f"  1/x² goes fast enough — its area is 1.")
    print(f"  The boundary is exactly p=1.")
    print(f"")

    x = sp.Symbol('x')
    print(f"  Computations:")
    for p_val in [2, 3, 1]:
        f = 1/x**p_val
        try:
            result = sp.integrate(f, (x, 1, sp.oo))
            print(f"  ∫₁^∞ 1/x^{p_val} dx = {result}")
        except Exception:
            print(f"  ∫₁^∞ 1/x^{p_val} dx = diverges")

    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  GABRIEL'S HORN")
    print(f"")
    print(f"  Rotate y=1/x (x≥1) around the x-axis.")
    print(f"")
    print(f"  Volume:       π·∫₁^∞ (1/x)² dx = π·1 = π")
    print(f"  Surface area: 2π·∫₁^∞ (1/x)·√(1+1/x⁴) dx > 2π·∫₁^∞ 1/x dx = ∞")
    print(f"")
    print(f"  FINITE volume, INFINITE surface area.")
    print(f"  You could fill it with paint,")
    print(f"  but you could never coat its surface.")
    print(f"  Not a paradox — a precise mathematical fact.")

    plot_improper()


def plot_improper():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    x = np.linspace(0.1, 5, 400)
    for p, color, label in [(1,"crimson","1/x  (diverges)"),
                             (2,"steelblue","1/x²  (converges)"),
                             (3,"green","1/x³  (converges faster)")]:
        axes[0].plot(x, 1/x**p, color=color, linewidth=2, label=label)

    axes[0].fill_between(x, 1/x**2, alpha=0.15, color="steelblue",
                         label="∫₁^∞ 1/x² dx = 1")
    axes[0].set_xlim(0.5, 5)
    axes[0].set_ylim(0, 4)
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].axvline(1, color="gray",  linewidth=1, linestyle=":")
    axes[0].set_title("1/xᵖ: converges iff p>1", fontsize=12)
    axes[0].set_xlabel("x")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    x2 = np.linspace(1, 6, 300)
    y2 = 1/x2
    axes[1].plot(x2,  y2, color="steelblue", linewidth=2.5)
    axes[1].plot(x2, -y2, color="steelblue", linewidth=2.5,
                 label="y = ±1/x")
    axes[1].fill_between(x2,  y2, alpha=0.2, color="steelblue")
    axes[1].fill_between(x2, -y2, alpha=0.2, color="steelblue")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("Gabriel's Horn\nVolume=π,  Surface area=∞",
                      fontsize=12)
    axes[1].set_xlabel("x")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Improper Integrals — infinite intervals, surprising results",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def exponential_miracle():
    print(f"\n{'='*50}")
    print(f"WHY eˣ IS MIRACULOUS")
    print(f"{'='*50}")
    print(f"")
    print(f"  (eˣ)' = eˣ.  And ∫ eˣ dx = eˣ + C.")
    print(f"  Same function — derivative, primitive, everything.")
    print(f"")
    print(f"  This is not a coincidence.")
    print(f"  It's the DEFINING PROPERTY of eˣ.")
    print(f"  e is the unique base for which this holds.")
    print(f"")
    print(f"  WHAT IS e?")
    print(f"  e = lim(n→∞) (1 + 1/n)ⁿ")
    print(f"")
    print(f"  Imagine 1€ invested at 100% annual interest.")
    print(f"  Yearly compounding:     (1+1)¹ = 2.000€")
    print(f"  Monthly compounding:    (1+1/12)^12 ≈ 2.613€")
    print(f"  Daily compounding:      (1+1/365)^365 ≈ 2.714€")
    print(f"  Continuous compounding: e ≈ 2.718€")
    print(f"")
    print(f"  e is the limit of continuous compounding.")
    print(f"  The most natural base for growth.")
    print(f"")
    print(f"  {'n':>10}  {'(1+1/n)^n':>14}  {'error from e':>14}")
    print(f"  {'─'*42}")
    for n in [1, 2, 5, 10, 100, 1000, 10000]:
        approx = (1+1/n)**n
        print(f"  {n:>10}  {approx:>14.8f}  {abs(approx-math.e):>14.2e}")

    print(f"")
    print(f"  THE DEEPER REASON:")
    print(f"  f'(x) = f(x) has a unique solution with f(0)=1 — it's eˣ.")
    print(f"  'I grow at exactly the rate I currently have.'")
    print(f"  This self-referential property makes eˣ appear")
    print(f"  everywhere in nature:")
    print(f"  · Radioactive decay:  N(t) = N₀·e^(-λt)")
    print(f"  · Population growth:  P(t) = P₀·e^(rt)")
    print(f"  · Cooling law:        T(t) = T∞ + (T₀-T∞)·e^(-kt)")
    print(f"  All governed by f'=cf. All solved by eˣ.")

    plot_exponential_miracle()


def plot_exponential_miracle():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    x = np.linspace(-2, 3, 400)
    y = np.exp(x)

    axes[0].plot(x, y, color="steelblue", linewidth=2.5,
                 label="f(x) = eˣ")
    axes[0].plot(x, y, color="crimson",   linewidth=2,
                 linestyle="--", label="f'(x) = eˣ  (same!)")
    x0    = 1
    y0    = math.e
    x_tan = np.linspace(0.3, 1.7, 100)
    y_tan = y0 + y0*(x_tan-x0)
    axes[0].plot(x_tan, y_tan, color="green", linewidth=2,
                 linestyle=":", label=f"Tangent at x=1 (slope=e)")
    axes[0].plot(x0, y0, "o", color="green", markersize=10)
    axes[0].set_ylim(-0.5, 10)
    axes[0].set_title("eˣ = its own derivative\nslope at every point = value",
                      fontsize=11)
    axes[0].set_xlabel("x")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(0, color="black", linewidth=0.8)

    ns      = np.arange(1, 101)
    approxs = (1+1/ns)**ns
    axes[1].plot(ns, approxs, color="crimson", linewidth=2,
                 label="(1+1/n)ⁿ")
    axes[1].axhline(math.e, color="steelblue", linewidth=2,
                    linestyle="--", label=f"e = {math.e:.6f}")
    axes[1].set_title("(1+1/n)ⁿ → e\nthe natural limit of compounding",
                      fontsize=11)
    axes[1].set_xlabel("n")
    axes[1].set_ylim(2, 2.9)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Why eˣ is the most special function in mathematics",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def no_elementary_primitive():
    print(f"\n{'='*50}")
    print(f"FUNCTIONS WITH NO ELEMENTARY PRIMITIVE")
    print(f"{'='*50}")
    print(f"")
    print(f"  Here's something nobody tells you in liceo:")
    print(f"  MOST functions have no elementary primitive.")
    print(f"  The ones you can integrate analytically are the exception.")
    print(f"")
    print(f"  'Elementary' means: a combination of polynomials,")
    print(f"  exponentials, logarithms, and trig functions.")
    print(f"")
    print(f"  These simple-looking functions have NO such primitive:")
    print(f"")

    functions = [
        ("e^(-x²)",
         "The bell curve.\n"
         "  Its integral defines the error function erf(x).\n"
         "  Used in every statistics calculation."),
        ("sin(x)/x",
         "The sinc function — core of signal processing.\n"
         "  ∫₀^∞ sin(x)/x dx = π/2  (exact, but not elementary)."),
        ("1/ln(x)",
         "The logarithmic integral li(x).\n"
         "  Describes how prime numbers are distributed."),
        ("√(1-k²sin²x)",
         "The elliptic integral.\n"
         "  Governs pendulum motion for large angles.\n"
         "  The simple pendulum has no closed-form period!"),
    ]

    for func, note in functions:
        print(f"  {'─'*44}")
        print(f"  ∫ {func} dx  →  no elementary form")
        for line in note.split('\n'):
            print(f"  {line}")
        print(f"")

    print(f"  {'─'*44}")
    print(f"  WHY DOES THIS MATTER?")
    print(f"")
    print(f"  Physics and engineering constantly need these integrals.")
    print(f"  The solution: NUMERICAL INTEGRATION.")
    print(f"  Approximate to any desired precision.")
    print(f"  Computers do this billions of times per second.")
    print(f"  Riemann sums, Simpson's rule, Gaussian quadrature —")
    print(f"  all are ways to compute integrals without formulas.")
    print(f"")
    print(f"  THE DEEPER POINT:")
    print(f"  The functions we can integrate analytically")
    print(f"  are a tiny island in an ocean of functions.")
    print(f"  That's not a failure of mathematics.")
    print(f"  It's a reminder that the universe is richer")
    print(f"  than any set of formulas.")

    plot_no_primitive()


def plot_no_primitive():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    from scipy import integrate as sci_int

    x = np.linspace(-3, 3, 400)
    y_gauss = np.exp(-x**2)
    y_erf   = np.array([sci_int.quad(lambda t: np.exp(-t**2), 0, xi)[0]
                        for xi in x])

    axes[0].plot(x, y_gauss, color="steelblue", linewidth=2.5,
                 label="e^(-x²)  (no primitive)")
    axes[0].plot(x, y_erf,   color="crimson",   linewidth=2.5,
                 linestyle="--", label="∫₀ˣ e^(-t²)dt  (numerical)")
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_title("e^(-x²) has no elementary primitive\n"
                      "but the integral exists numerically",
                      fontsize=11)
    axes[0].set_xlabel("x")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    x2    = np.linspace(0.01, 20, 500)
    sinc  = np.sin(x2)/x2
    cumul = np.array([sci_int.quad(lambda t: np.sin(t)/t if t>0 else 1,
                                   0.001, xi)[0] for xi in x2])

    axes[1].plot(x2, sinc,  color="steelblue", linewidth=2.5,
                 label="sin(x)/x")
    axes[1].plot(x2, cumul, color="crimson",   linewidth=2.5,
                 linestyle="--", label="Running integral → π/2")
    axes[1].axhline(math.pi/2, color="green", linewidth=1.5,
                    linestyle=":", label=f"π/2 ≈ {math.pi/2:.4f}")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("∫₀^∞ sin(x)/x dx = π/2\nBeautiful result, no antiderivative",
                      fontsize=11)
    axes[1].set_xlabel("x")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Functions with no elementary primitive — "
                 "yet their integrals exist",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def integrals():
    print(f"\n{'='*50}")
    print(f"INTEGRALS")
    print(f"{'='*50}")
    print(f"")
    print(f"  The derivative answers: how fast is this changing?")
    print(f"  The integral answers: how much has accumulated?")
    print(f"")
    print(f"  Velocity → position.  Force → work.  Rate → total.")
    print(f"  Any quantity that builds up continuously")
    print(f"  is computed by an integral.")
    print(f"")
    print(f"  The deepest result: the Fundamental Theorem.")
    print(f"  To find an area, find the antiderivative and evaluate.")
    print(f"  Two completely different ideas — the same operation.")
    print(f"  Newton and Leibniz discovered this in the 1660s-70s")
    print(f"  and it changed mathematics forever.")
    print(f"")
    print(f"  1 — What is an integral?")
    print(f"       intuition, rectangles, velocity")
    print(f"  2 — Riemann sums")
    print(f"       the formal definition as a limit")
    print(f"  3 — Fundamental theorem of calculus")
    print(f"       the most important result in calculus")
    print(f"  4 — Antiderivatives and primitives")
    print(f"       the basic integral table")
    print(f"  5 — Integration techniques")
    print(f"       substitution, by parts, partial fractions")
    print(f"  6 — Applications")
    print(f"       area, volume, average value")
    print(f"  7 — Surprising facts")
    print(f"       Gaussian, Gabriel's Horn, why eˣ is special")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, 5, 6, or 7: ")

    if choice == "1":
        intuition_integral()
    elif choice == "2":
        riemann_sums()
    elif choice == "3":
        fundamental_theorem()
    elif choice == "4":
        antiderivatives()
    elif choice == "5":
        integration_techniques()
    elif choice == "6":
        integral_applications()
    elif choice == "7":
        surprising_facts()
    else:
        print(f"  Invalid choice. Please enter 1 to 7.")


if __name__ == "__main__":
    integrals()