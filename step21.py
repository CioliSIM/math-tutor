import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_function_and_derivative(expr, deriv, x_val):
    x_sym   = sp.Symbol('x')
    f_num   = sp.lambdify(x_sym, expr,  "numpy")
    df_num  = sp.lambdify(x_sym, deriv, "numpy")
    x_range = np.linspace(x_val - 3, x_val + 3, 500)

    try:
        y_f  = f_num(x_range)
        y_df = df_num(x_range)
        y0   = float(expr.subs(x_sym, x_val))
        m    = float(deriv.subs(x_sym, x_val))

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        axes[0].plot(x_range, y_f, color="steelblue",
                     linewidth=2.5, label=f"f(x) = {expr}")
        tan_y = y0 + m * (x_range - x_val)
        axes[0].plot(x_range, tan_y, color="crimson",
                     linewidth=1.8, linestyle="--",
                     label=f"Tangent at x={x_val:.2f}  (slope={m:.3f})")
        axes[0].plot(x_val, y0, "o", color="crimson", markersize=10)
        axes[0].set_title("Function and tangent line", fontsize=12)
        axes[0].set_xlabel("x")
        axes[0].legend(fontsize=9)
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(0, color="black", linewidth=0.8)
        axes[0].axvline(0, color="black", linewidth=0.8)
        y_f_finite = y_f[np.isfinite(y_f)]
        if len(y_f_finite) > 0:
            axes[0].set_ylim(np.percentile(y_f_finite, 2),
                             np.percentile(y_f_finite, 98))

        axes[1].plot(x_range, y_df, color="green",
                     linewidth=2.5, label=f"f'(x) = {deriv}")
        axes[1].axhline(0, color="black", linewidth=0.8)
        axes[1].axvline(x_val, color="crimson", linewidth=1.5,
                        linestyle="--", alpha=0.7)
        axes[1].plot(x_val, m, "o", color="crimson", markersize=10,
                     label=f"f'({x_val:.2f}) = {m:.3f}")
        axes[1].set_title("Derivative", fontsize=12)
        axes[1].set_xlabel("x")
        axes[1].legend(fontsize=9)
        axes[1].grid(True, alpha=0.3)
        y_df_finite = y_df[np.isfinite(y_df)]
        if len(y_df_finite) > 0:
            axes[1].set_ylim(np.percentile(y_df_finite, 2),
                             np.percentile(y_df_finite, 98))

        plt.suptitle(f"f(x) = {expr}   and   f'(x) = {deriv}",
                     fontsize=13, fontweight="bold")
        plt.tight_layout()
        plt.show()
    except Exception:
        print(f"  Could not plot — function may be complex in this range.")


def plot_with_critical_points(expr, deriv, deriv2, critical_pts):
    x_sym = sp.Symbol('x')
    if not critical_pts:
        return

    x_center = float(sum(critical_pts) / len(critical_pts))
    x_range  = np.linspace(x_center - 4, x_center + 4, 600)

    f_num  = sp.lambdify(x_sym, expr,   "numpy")
    df_num = sp.lambdify(x_sym, deriv,  "numpy")

    try:
        y_f  = f_num(x_range)
        y_df = df_num(x_range)

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        axes[0].plot(x_range, y_f, color="steelblue",
                     linewidth=2.5, label="f(x)")
        axes[0].axhline(0, color="black", linewidth=0.8)

        for cp in critical_pts:
            cp_f  = float(expr.subs(x_sym, cp))
            cp_d2 = float(deriv2.subs(x_sym, cp))
            color  = "crimson" if cp_d2 < 0 else \
                     "green"   if cp_d2 > 0 else "orange"
            label  = "max" if cp_d2 < 0 else \
                     "min" if cp_d2 > 0 else "?"
            axes[0].plot(float(cp), cp_f, "o", color=color,
                         markersize=12,
                         label=f"x={float(cp):.3f}  ({label})")
            axes[0].axvline(float(cp), color=color,
                            linewidth=1, linestyle=":", alpha=0.5)

        axes[0].set_title("Function with critical points", fontsize=12)
        axes[0].set_xlabel("x")
        axes[0].legend(fontsize=9)
        axes[0].grid(True, alpha=0.3)
        y_f_finite = y_f[np.isfinite(y_f)]
        if len(y_f_finite) > 0:
            axes[0].set_ylim(np.percentile(y_f_finite, 2),
                             np.percentile(y_f_finite, 98))

        axes[1].plot(x_range, y_df, color="green",
                     linewidth=2.5, label="f'(x)")
        axes[1].axhline(0, color="black", linewidth=1.5,
                        linestyle="--", alpha=0.7, label="f'(x) = 0")
        for cp in critical_pts:
            axes[1].axvline(float(cp), color="crimson",
                            linewidth=1.5, linestyle=":", alpha=0.7)
            axes[1].plot(float(cp), 0, "o", color="crimson",
                         markersize=10)

        axes[1].set_title("Derivative — zeros are critical points",
                          fontsize=12)
        axes[1].set_xlabel("x")
        axes[1].legend(fontsize=9)
        axes[1].grid(True, alpha=0.3)
        y_df_finite = y_df[np.isfinite(y_df)]
        if len(y_df_finite) > 0:
            axes[1].set_ylim(np.percentile(y_df_finite, 2),
                             np.percentile(y_df_finite, 98))

        plt.suptitle("Maxima, Minima, and Critical Points",
                     fontsize=13, fontweight="bold")
        plt.tight_layout()
        plt.show()
    except Exception:
        pass


def plot_complete_study(expr, df, d2f):
    x_sym = sp.Symbol('x')
    f_n   = sp.lambdify(x_sym, expr, "numpy")
    df_n  = sp.lambdify(x_sym, df,   "numpy")
    d2f_n = sp.lambdify(x_sym, d2f,  "numpy")

    x_r  = np.linspace(-2.5, 2.5, 500)
    y_f  = f_n(x_r)
    y_df = df_n(x_r)
    y_d2 = d2f_n(x_r)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].plot(x_r, y_f, color="steelblue", linewidth=2.5,
                 label="f(x) = x³-3x")
    axes[0].plot(-1,  2, "^", color="crimson",   markersize=12,
                 label="max (-1, 2)")
    axes[0].plot( 1, -2, "v", color="green",     markersize=12,
                 label="min (1, -2)")
    axes[0].plot( 0,  0, "s", color="orange",    markersize=10,
                 label="inflection (0, 0)")
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].axvline(0, color="black", linewidth=0.8)
    axes[0].set_title("f(x) = x³ - 3x", fontsize=12)
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(x_r, y_df, color="green", linewidth=2.5,
                 label="f'(x) = 3x²-3")
    axes[1].fill_between(x_r, y_df, 0,
                         where=y_df > 0, alpha=0.2, color="green",
                         label="f'>0  (increasing)")
    axes[1].fill_between(x_r, y_df, 0,
                         where=y_df < 0, alpha=0.2, color="crimson",
                         label="f'<0  (decreasing)")
    axes[1].axhline(0, color="black", linewidth=1)
    axes[1].plot([-1, 1], [0, 0], "o", color="black", markersize=8)
    axes[1].set_title("f'(x) — monotonicity", fontsize=12)
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(x_r, y_d2, color="orange", linewidth=2.5,
                 label="f''(x) = 6x")
    axes[2].fill_between(x_r, y_d2, 0,
                         where=y_d2 > 0, alpha=0.2, color="steelblue",
                         label="f''>0  (concave up ∪)")
    axes[2].fill_between(x_r, y_d2, 0,
                         where=y_d2 < 0, alpha=0.2, color="orange",
                         label="f''<0  (concave down ∩)")
    axes[2].axhline(0, color="black", linewidth=1)
    axes[2].plot(0, 0, "o", color="black", markersize=8)
    axes[2].set_title("f''(x) — concavity", fontsize=12)
    axes[2].legend(fontsize=8)
    axes[2].grid(True, alpha=0.3)

    plt.suptitle("Complete study: f(x) = x³ - 3x",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_motion(s_expr, v_expr, a_expr):
    t_sym = sp.Symbol('t')
    s_n   = sp.lambdify(t_sym, s_expr, "numpy")
    v_n   = sp.lambdify(t_sym, v_expr, "numpy")
    a_n   = sp.lambdify(t_sym, a_expr, "numpy")

    t_r = np.linspace(0, 6, 500)
    try:
        ys = np.array(s_n(t_r), dtype=float)
        yv = np.array(v_n(t_r), dtype=float)
        ya = np.array(a_n(t_r), dtype=float)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for ax, y, label, color, title in [
            (axes[0], ys, "s(t) — position",     "steelblue", "Position"),
            (axes[1], yv, "v(t) — velocity",     "green",     "Velocity"),
            (axes[2], ya, "a(t) — acceleration", "crimson",   "Acceleration"),
        ]:
            ax.plot(t_r, y, color=color, linewidth=2.5, label=label)
            ax.axhline(0, color="black", linewidth=0.8)
            ax.set_xlabel("t")
            ax.set_title(title, fontsize=12)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
            y_f = y[np.isfinite(y)]
            if len(y_f) > 0:
                ax.set_ylim(np.percentile(y_f, 1), np.percentile(y_f, 99))

        plt.suptitle("Position, Velocity, Acceleration",
                     fontsize=13, fontweight="bold")
        plt.tight_layout()
        plt.show()
    except Exception:
        pass


def intuition_derivative():
    print(f"\n{'='*50}")
    print(f"WHAT IS A DERIVATIVE?")
    print(f"{'='*50}")
    print(f"")
    print(f"  Start with something you already know.")
    print(f"")
    print(f"  A car travels 120 km in 2 hours.")
    print(f"  Average speed = 120/2 = 60 km/h. Easy.")
    print(f"")
    print(f"  Now the harder question:")
    print(f"  What is the car's speed at EXACTLY 1:37pm?")
    print(f"  Not the average — the instantaneous speed.")
    print(f"  The number the tachometer shows at that precise moment.")
    print(f"")
    print(f"  That is what a derivative computes.")
    print(f"  The instantaneous rate of change of any quantity.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  FROM AVERAGE TO INSTANTANEOUS")
    print(f"")
    print(f"  Suppose the car's position is f(t) = t² km.")
    print(f"  (Not realistic, but simple.)")
    print(f"")
    print(f"  Average speed on [1, 1+h] = [f(1+h) - f(1)] / h")
    print(f"")
    print(f"  Watch what happens as h shrinks:")
    print(f"  {'h':>12}  {'average speed':>16}  {'→':>5}")
    print(f"  {'─'*38}")
    for exp in [0, -1, -2, -3, -4, -6]:
        h    = 10**exp
        rate = ((1+h)**2 - 1) / h
        print(f"  {h:>12}  {rate:>16.8f}  {'→ 2' if exp <= -4 else '':>5}")

    print(f"")
    print(f"  The average speed approaches 2 as h → 0.")
    print(f"  The INSTANTANEOUS speed at t=1 is exactly 2.")
    print(f"  This limiting value is the DERIVATIVE of f at t=1.")
    print(f"  Written: f'(1) = 2.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  THE GEOMETRIC PICTURE")
    print(f"")
    print(f"  Draw the graph of f(x) = x².")
    print(f"  Draw a line through (1, f(1)) and (1+h, f(1+h)).")
    print(f"  That line is called a SECANT.")
    print(f"  Its slope = [f(1+h)-f(1)]/h = average rate.")
    print(f"")
    print(f"  As h → 0, the second point slides toward (1,1).")
    print(f"  The secant approaches the TANGENT LINE at (1,1).")
    print(f"  The slope of the tangent = the derivative.")
    print(f"")
    print(f"  In one sentence:")
    print(f"  The derivative at a point = the slope of the tangent")
    print(f"  to the curve at that point.")
    print(f"")
    print(f"  · Steep curve → large derivative  (changes fast)")
    print(f"  · Flat curve  → small derivative  (changes slowly)")
    print(f"  · Horizontal tangent → derivative = 0  (max or min!)")

    plot_secant_to_tangent()


def plot_secant_to_tangent():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    x = np.linspace(-0.5, 3, 300)
    y = x**2

    for ax, h in zip(axes, [2, 0.5, 0.01]):
        ax.plot(x, y, color="steelblue", linewidth=2.5,
                label="f(x) = x²")

        x0, y0 = 1, 1
        x1, y1 = 1+h, (1+h)**2
        slope_sec = (y1 - y0) / h
        x_sec = np.linspace(x0 - 0.5, x1 + 0.3, 100)
        y_sec = y0 + slope_sec*(x_sec - x0)
        ax.plot(x_sec, y_sec, color="crimson", linewidth=2,
                linestyle="--",
                label=f"Secant  (h={h}, slope={slope_sec:.2f})")

        x_tan = np.linspace(x0 - 0.8, x0 + 0.8, 100)
        y_tan = y0 + 2*(x_tan - x0)
        ax.plot(x_tan, y_tan, color="green", linewidth=2,
                linestyle=":", label="Tangent  (slope=2)")

        ax.plot(x0, y0, "o", color="black",  markersize=8)
        ax.plot(x1, y1, "o", color="crimson", markersize=8)

        ax.set_xlim(-0.3, 3)
        ax.set_ylim(-0.5, 6)
        ax.set_title(f"h = {h}", fontsize=13)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)

    plt.suptitle("As h shrinks, the secant becomes the tangent — "
                 "the derivative appears",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def definition_derivative():
    print(f"\n{'='*50}")
    print(f"THE FORMAL DEFINITION")
    print(f"{'='*50}")
    print(f"")
    print(f"  Now that the idea is clear, here is the precise definition.")
    print(f"")
    print(f"  The derivative of f at x is:")
    print(f"")
    print(f"      f'(x) = lim(h→0) [f(x+h) - f(x)] / h")
    print(f"")
    print(f"  If this limit exists, f is DIFFERENTIABLE at x.")
    print(f"")
    print(f"  Other notations — all mean the same thing:")
    print(f"  · f'(x)   Lagrange  (most common in liceo)")
    print(f"  · df/dx   Leibniz   (most used in physics)")
    print(f"  · ẋ       Newton    (for time derivatives)")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  COMPUTING f'(x) FROM THE DEFINITION — f(x) = x²")
    print(f"")
    print(f"  f'(x) = lim(h→0) [(x+h)² - x²] / h")
    print(f"        = lim(h→0) [x²+2xh+h² - x²] / h")
    print(f"        = lim(h→0) [2xh + h²] / h")
    print(f"        = lim(h→0) [2x + h]")
    print(f"        = 2x")
    print(f"")
    print(f"  f(x) = x²  →  f'(x) = 2x.")
    print(f"  At x=1: f'(1)=2.  Matches the numerical result. ✓")
    print(f"  At x=3: f'(3)=6.  The curve is steeper there.")
    print(f"  At x=0: f'(0)=0.  Horizontal tangent — it's the minimum!")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  COMPUTING f'(x) FROM THE DEFINITION — f(x) = x³")
    print(f"")
    print(f"  (x+h)³ = x³ + 3x²h + 3xh² + h³")
    print(f"")
    print(f"  f'(x) = lim(h→0) [3x²h + 3xh² + h³] / h")
    print(f"        = lim(h→0) [3x² + 3xh + h²]")
    print(f"        = 3x²")
    print(f"")
    print(f"  x²  →  2x")
    print(f"  x³  →  3x²")
    print(f"  Pattern: (xⁿ)' = n·xⁿ⁻¹  — the POWER RULE.")
    print(f"  This is the most used rule in calculus.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  WHEN DOES THE DERIVATIVE NOT EXIST?")
    print(f"")
    print(f"  1. CORNER — f(x) = |x| at x=0.")
    print(f"     From the left slope=-1, from the right slope=+1.")
    print(f"     They disagree → no derivative.")
    print(f"")
    print(f"  2. VERTICAL TANGENT — f(x) = x^(1/3) at x=0.")
    print(f"     Tangent is vertical → slope = ∞ → not a real number.")
    print(f"")
    print(f"  3. DISCONTINUITY — if f jumps at x,")
    print(f"     it can't be differentiable there.")
    print(f"     Differentiable → continuous.  (Not vice versa.)")

    plot_non_differentiable()


def plot_non_differentiable():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    x = np.linspace(-2, 2, 400)
    axes[0].plot(x, np.abs(x), color="steelblue", linewidth=2.5)
    axes[0].plot(0, 0, "o", color="crimson", markersize=10)
    axes[0].set_title("f(x) = |x|\ncorner at x=0 — no derivative",
                      fontsize=11)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].axvline(0, color="black", linewidth=0.8)

    x2 = np.linspace(-2, 2, 400)
    y2 = np.sign(x2) * np.abs(x2)**(1/3)
    axes[1].plot(x2, y2, color="steelblue", linewidth=2.5)
    axes[1].plot(0, 0, "o", color="crimson", markersize=10)
    axes[1].axvline(0, color="crimson", linewidth=1.5,
                    linestyle="--", label="vertical tangent")
    axes[1].set_title("f(x) = x^(1/3)\nvertical tangent — no derivative",
                      fontsize=11)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(0, color="black", linewidth=0.8)

    x3 = np.linspace(-2, 2, 400)
    y3 = np.where(x3 < 0, x3+1, x3-1)
    axes[2].plot(x3[x3 <  0], y3[x3 <  0], color="steelblue",
                 linewidth=2.5)
    axes[2].plot(x3[x3 >= 0], y3[x3 >= 0], color="steelblue",
                 linewidth=2.5)
    axes[2].plot(0,  1, "o", color="steelblue",
                 markersize=8, markerfacecolor="white")
    axes[2].plot(0, -1, "o", color="crimson", markersize=8)
    axes[2].set_title("Discontinuity at x=0\nno derivative",
                      fontsize=11)
    axes[2].grid(True, alpha=0.3)
    axes[2].axhline(0, color="black", linewidth=0.8)
    axes[2].axvline(0, color="black", linewidth=0.8)

    plt.suptitle("Three cases where the derivative does not exist",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def derivative_rules():
    print(f"\n{'='*50}")
    print(f"DERIVATIVE RULES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Computing derivatives from the definition every time")
    print(f"  would take forever. Mathematicians derived general rules")
    print(f"  that work for any function.")
    print(f"  Learn these and you can differentiate almost anything.")
    print(f"")
    print(f"  1 — Basic derivatives  (the building blocks)")
    print(f"  2 — Sum and difference rule")
    print(f"  3 — Product rule")
    print(f"  4 — Quotient rule")
    print(f"  5 — Chain rule  (the most important)")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        basic_derivatives()
    elif choice == "2":
        sum_rule()
    elif choice == "3":
        product_rule()
    elif choice == "4":
        quotient_rule()
    elif choice == "5":
        chain_rule()
    else:
        print(f"  Invalid choice.")


def basic_derivatives():
    print(f"\n{'='*50}")
    print(f"BASIC DERIVATIVES")
    print(f"{'='*50}")
    print(f"")
    print(f"  These are the building blocks.")
    print(f"  Every other derivative is assembled from these.")
    print(f"  Learn them by heart.")
    print(f"")

    rules = [
        ("CONSTANT",
         "f(x) = c   →   f'(x) = 0",
         "A constant never changes — its rate of change is zero.\n"
         "  Geometrically: a horizontal line has slope 0 everywhere."),

        ("IDENTITY",
         "f(x) = x   →   f'(x) = 1",
         "x grows at a steady rate of 1.\n"
         "  The line y=x has slope 1 everywhere."),

        ("POWER RULE",
         "f(x) = xⁿ  →   f'(x) = n·xⁿ⁻¹",
         "Bring the exponent down, reduce it by 1.\n"
         "  Works for any real n — positive, negative, fractional.\n"
         "  x² → 2x    x³ → 3x²    x⁻¹ → -x⁻²    √x → 1/(2√x)"),

        ("NATURAL EXPONENTIAL",
         "f(x) = eˣ  →   f'(x) = eˣ",
         "The most remarkable fact in calculus:\n"
         "  eˣ is its own derivative.\n"
         "  It grows at exactly the rate it currently has.\n"
         "  This is WHY e is the natural base for exponentials.\n"
         "  No other base has this property."),

        ("EXPONENTIAL BASE a",
         "f(x) = aˣ  →   f'(x) = aˣ·ln(a)",
         "For any base a > 0, a ≠ 1.\n"
         "  When a = e: ln(e) = 1, so (eˣ)' = eˣ. ✓"),

        ("NATURAL LOG",
         "f(x) = ln(x)  →   f'(x) = 1/x",
         "Valid for x > 0.\n"
         "  The derivative of the logarithm is the reciprocal.\n"
         "  This is why ln appears so often in integration."),

        ("SINE",
         "f(x) = sin(x)  →   f'(x) = cos(x)",
         "At x=0: sin is rising fast, cos(0)=1. ✓\n"
         "  At x=π/2: sin reaches its peak, cos(π/2)=0. ✓\n"
         "  Slope zero at the maximum — exactly as expected."),

        ("COSINE",
         "f(x) = cos(x)  →   f'(x) = -sin(x)",
         "The minus sign: cos is decreasing when sin is positive."),

        ("TANGENT",
         "f(x) = tan(x)  →   f'(x) = 1/cos²(x)",
         "Derived from the quotient rule on sin/cos.\n"
         "  Also written as sec²(x)."),
    ]

    for name, formula, note in rules:
        print(f"  {'─'*46}")
        print(f"  {name}")
        print(f"  {formula}")
        print(f"")
        for line in note.split('\n'):
            print(f"  {line}")
        print(f"")

    print(f"  {'─'*46}")
    print(f"  A BEAUTIFUL PATTERN:")
    print(f"  sin' = cos,  cos' = -sin,  (-sin)' = -cos,  (-cos)' = sin")
    print(f"  The fourth derivative of sin is sin again.")
    print(f"  A cycle of period 4 — like a clock.")
    print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  COMPUTE A DERIVATIVE")
    print(f"  Enter any function and I'll differentiate it.")
    print(f"  Examples: x**3 + sin(x),  exp(x)*cos(x),  log(x**2+1)")
    print(f"")
    x = sp.Symbol('x')
    expr_str = input("  f(x) = ")
    try:
        expr  = sp.sympify(expr_str)
        deriv = sp.simplify(sp.diff(expr, x))
        print(f"")
        print(f"  f(x)  = {expr}")
        print(f"  f'(x) = {deriv}")
        print(f"")
        x_val = float(input("  Evaluate f'(x) at x = "))
        val   = float(deriv.subs(x, x_val))
        print(f"  f'({x_val}) = {val:.6f}")
        print(f"  This is the slope of the tangent to f at x = {x_val}.")
        plot_function_and_derivative(expr, deriv, x_val)
    except Exception as e:
        print(f"  Could not compute: {e}")


def sum_rule():
    print(f"\n{'='*50}")
    print(f"SUM AND DIFFERENCE RULE")
    print(f"{'='*50}")
    print(f"")
    print(f"  (f + g)' = f' + g'")
    print(f"  (f - g)' = f' - g'")
    print(f"  (c·f)'   = c·f'")
    print(f"")
    print(f"  The derivative of a sum is the sum of the derivatives.")
    print(f"  Constants factor out.")
    print(f"  This is the simplest rule — and the most used.")
    print(f"")
    print(f"  WHY? The limit distributes over sums:")
    print(f"  lim[f(x+h)+g(x+h) - f(x)-g(x)]/h")
    print(f"  = lim[f(x+h)-f(x)]/h  +  lim[g(x+h)-g(x)]/h")
    print(f"  = f'(x) + g'(x). □")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("x**3 + 5*x**2 - 2*x + 7",
         "Power rule on each term:\n"
         "  (x³)' = 3x²\n"
         "  (5x²)' = 10x\n"
         "  (-2x)' = -2\n"
         "  (7)' = 0\n"
         "  Total: 3x² + 10x - 2"),
        ("sin(x) + exp(x)",
         "(sin x)' = cos x\n"
         "  (eˣ)' = eˣ\n"
         "  Total: cos x + eˣ"),
        ("3*log(x) - 4*cos(x)",
         "(3 ln x)' = 3/x\n"
         "  (-4 cos x)' = 4 sin x\n"
         "  Total: 3/x + 4 sin x"),
    ]

    for func_str, explanation in examples:
        expr  = sp.sympify(func_str)
        deriv = sp.simplify(sp.diff(expr, x))
        print(f"  f(x) = {func_str}")
        for line in explanation.split('\n'):
            print(f"  {line}")
        print(f"  Sympy confirms: f'(x) = {deriv}")
        print(f"")


def product_rule():
    print(f"\n{'='*50}")
    print(f"PRODUCT RULE")
    print(f"{'='*50}")
    print(f"")
    print(f"  What is the derivative of f(x)·g(x)?")
    print(f"")
    print(f"  WRONG instinct: f'(x)·g'(x).")
    print(f"  Check: (x·x)' = (x²)' = 2x.")
    print(f"  But x'·x' = 1·1 = 1 ≠ 2x.  Completely wrong.")
    print(f"")
    print(f"  THE CORRECT RULE:")
    print(f"  (f·g)' = f'·g + f·g'")
    print(f"")
    print(f"  Read it as:")
    print(f"  'derivative of first × second  +  first × derivative of second'")
    print(f"")
    print(f"  WHY? Imagine f and g as the sides of a rectangle.")
    print(f"  Area = f·g.")
    print(f"  When x increases slightly:")
    print(f"  · f grows by f'·h")
    print(f"  · g grows by g'·h")
    print(f"  · Area grows by f'·h·g + f·g'·h + (tiny f'·h·g'·h)")
    print(f"  · Rate of growth = f'g + fg'  (the tiny term vanishes)")
    print(f"  This geometric picture captures the exact right intuition.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("x**2 * sin(x)",
         "f=x², g=sin x\n"
         "  f'=2x,  g'=cos x\n"
         "  Result: 2x·sin x + x²·cos x"),
        ("exp(x) * cos(x)",
         "f=eˣ, g=cos x\n"
         "  f'=eˣ,  g'=-sin x\n"
         "  Result: eˣ·cos x - eˣ·sin x = eˣ(cos x - sin x)"),
        ("x * log(x)",
         "f=x, g=ln x\n"
         "  f'=1,  g'=1/x\n"
         "  Result: 1·ln x + x·(1/x) = ln x + 1"),
    ]

    for func_str, explanation in examples:
        expr  = sp.sympify(func_str)
        deriv = sp.simplify(sp.diff(expr, x))
        print(f"  f(x) = {func_str}")
        for line in explanation.split('\n'):
            print(f"  {line}")
        print(f"  Sympy confirms: {deriv}")
        print(f"")


def quotient_rule():
    print(f"\n{'='*50}")
    print(f"QUOTIENT RULE")
    print(f"{'='*50}")
    print(f"")
    print(f"  (f/g)' = (f'·g - f·g') / g²")
    print(f"")
    print(f"  Memory trick: 'low d-high minus high d-low, over low squared'")
    print(f"  (low=g, high=f, d=derivative)")
    print(f"")
    print(f"  ORDER MATTERS in the numerator.")
    print(f"  It's f'g - fg', not fg' - f'g.")
    print(f"  Getting it backwards is the most common error here.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("sin(x)/x",
         "f=sin x, g=x\n"
         "  f'=cos x,  g'=1\n"
         "  Result: (cos x·x - sin x·1) / x²\n"
         "        = (x cos x - sin x) / x²"),
        ("(x**2+1)/(x-1)",
         "f=x²+1, g=x-1\n"
         "  f'=2x,  g'=1\n"
         "  Result: (2x(x-1) - (x²+1)) / (x-1)²\n"
         "        = (x²-2x-1) / (x-1)²"),
        ("exp(x)/x",
         "f=eˣ, g=x\n"
         "  f'=eˣ,  g'=1\n"
         "  Result: (eˣ·x - eˣ) / x²\n"
         "        = eˣ(x-1) / x²"),
    ]

    for func_str, explanation in examples:
        expr  = sp.sympify(func_str)
        deriv = sp.simplify(sp.diff(expr, x))
        print(f"  f(x) = {func_str}")
        for line in explanation.split('\n'):
            print(f"  {line}")
        print(f"  Sympy confirms: {deriv}")
        print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  DERIVING (tan x)' FROM THE QUOTIENT RULE:")
    print(f"  tan x = sin x / cos x")
    print(f"  (tan x)' = (cos x·cos x - sin x·(-sin x)) / cos²x")
    print(f"           = (cos²x + sin²x) / cos²x")
    print(f"           = 1 / cos²x    [since cos²+sin²=1]")
    print(f"  The table entry for tan x — derived from scratch. ✓")


def chain_rule():
    print(f"\n{'='*50}")
    print(f"CHAIN RULE")
    print(f"{'='*50}")
    print(f"")
    print(f"  The most important differentiation rule.")
    print(f"  Used more often than any other.")
    print(f"")
    print(f"  What is the derivative of f(g(x)) — a function inside a function?")
    print(f"")
    print(f"  (f(g(x)))' = f'(g(x)) · g'(x)")
    print(f"")
    print(f"  'Derivative of the outer function at the inner,")
    print(f"   times derivative of the inner function.'")
    print(f"")
    print(f"  In Leibniz notation:")
    print(f"  If y = f(u) and u = g(x):")
    print(f"  dy/dx = dy/du · du/dx")
    print(f"  The du cancels like a fraction. Beautiful and memorable.")
    print(f"")
    print(f"  INTUITION — gears:")
    print(f"  If gear A turns 3× as fast as your hand,")
    print(f"  and gear B turns 2× as fast as gear A,")
    print(f"  then gear B turns 6× as fast as your hand.")
    print(f"  Rates of change MULTIPLY. That's the chain rule.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("sin(x**2)",
         "outer: sin(u),  inner: u=x²\n"
         "  outer' = cos(u) = cos(x²)\n"
         "  inner' = 2x\n"
         "  Result: cos(x²) · 2x = 2x cos(x²)"),
        ("exp(3*x)",
         "outer: eᵘ,  inner: u=3x\n"
         "  outer' = eᵘ = e^(3x)\n"
         "  inner' = 3\n"
         "  Result: 3e^(3x)"),
        ("(x**2+1)**10",
         "outer: u^10,  inner: u=x²+1\n"
         "  outer' = 10u⁹ = 10(x²+1)⁹\n"
         "  inner' = 2x\n"
         "  Result: 20x(x²+1)⁹"),
        ("log(sin(x))",
         "outer: ln(u),  inner: u=sin x\n"
         "  outer' = 1/u = 1/sin x\n"
         "  inner' = cos x\n"
         "  Result: cos x / sin x = cot x"),
        ("sin(cos(x**2))",
         "Three nested functions — chain rule twice.\n"
         "  outer: sin(u),  middle: cos(v),  inner: v=x²\n"
         "  = cos(cos(x²)) · (-sin(x²)) · 2x\n"
         "  = -2x sin(x²) cos(cos(x²))"),
    ]

    for func_str, explanation in examples:
        expr  = sp.sympify(func_str)
        deriv = sp.simplify(sp.diff(expr, x))
        print(f"  f(x) = {func_str}")
        for line in explanation.split('\n'):
            print(f"  {line}")
        print(f"  Sympy confirms: {deriv}")
        print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  HOW TO SPOT THE CHAIN RULE:")
    print(f"  Ask: 'Is there a function INSIDE another function?'")
    print(f"  sin(x²)      → YES — sin of (x²)    → chain rule")
    print(f"  sin(x)·x²    → NO  — product         → product rule")
    print(f"  e^(x²+3x)    → YES — e of (x²+3x)  → chain rule")
    print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  PRACTICE — enter a composed function:")
    expr_str = input("  f(x) = ")
    try:
        expr  = sp.sympify(expr_str)
        deriv = sp.simplify(sp.diff(expr, x))
        print(f"  f'(x) = {deriv}")
        plot_function_and_derivative(expr, deriv, 1.0)
    except Exception as e:
        print(f"  Could not compute: {e}")


def maxima_minima():
    print(f"\n{'='*50}")
    print(f"MAXIMA AND MINIMA")
    print(f"{'='*50}")
    print(f"")
    print(f"  One of the most useful applications of derivatives.")
    print(f"  Physics, economics, engineering — all need to find")
    print(f"  the best value of something.")
    print(f"")
    print(f"  KEY IDEA:")
    print(f"  At a maximum or minimum, the tangent is horizontal.")
    print(f"  Horizontal tangent → slope zero → derivative zero.")
    print(f"")
    print(f"  If f has a max or min at x₀, then f'(x₀) = 0.")
    print(f"  Points where f'(x) = 0 are called CRITICAL POINTS.")
    print(f"  They are CANDIDATES for maxima and minima.")
    print(f"  Not every critical point is one — it might be an inflection.")
    print(f"")
    print(f"  HOW TO CLASSIFY:")
    print(f"")
    print(f"  METHOD 1 — First derivative test:")
    print(f"  Check the sign of f' around the critical point.")
    print(f"  f' goes  + → - :  maximum")
    print(f"  f' goes  - → + :  minimum")
    print(f"  f' doesn't change sign:  inflection point")
    print(f"")
    print(f"  METHOD 2 — Second derivative test:")
    print(f"  f'(x₀) = 0 and:")
    print(f"  f''(x₀) > 0  →  minimum   (curve bends up  ∪)")
    print(f"  f''(x₀) < 0  →  maximum   (curve bends down ∩)")
    print(f"  f''(x₀) = 0  →  inconclusive")
    print(f"")
    print(f"  SECOND DERIVATIVE INTUITION:")
    print(f"  f'' > 0 means the slope is increasing → bend upward ∪")
    print(f"  f'' < 0 means the slope is decreasing → bend downward ∩")
    print(f"  This is called CONCAVITY.")
    print(f"")

    x = sp.Symbol('x')
    expr_str = input("  f(x) = ")
    try:
        expr   = sp.sympify(expr_str)
        deriv  = sp.diff(expr, x)
        deriv2 = sp.diff(deriv, x)

        print(f"\n  f(x)   = {expr}")
        print(f"  f'(x)  = {sp.simplify(deriv)}")
        print(f"  f''(x) = {sp.simplify(deriv2)}")

        critical      = sp.solve(deriv, x)
        real_critical = [c for c in critical if c.is_real]

        print(f"\n  Critical points (f'=0): {real_critical}")
        print(f"")

        for cp in real_critical:
            f_val  = sp.simplify(expr.subs(x, cp))
            f2_val = deriv2.subs(x, cp)
            print(f"  x = {cp}:")
            print(f"    f({cp})  = {f_val}")
            print(f"    f''({cp}) = {sp.simplify(f2_val)}")
            if f2_val.is_real:
                if f2_val > 0:
                    print(f"    → LOCAL MINIMUM  ∪")
                elif f2_val < 0:
                    print(f"    → LOCAL MAXIMUM  ∩")
                else:
                    print(f"    → Inconclusive — check f' sign change")
            print(f"")

        plot_with_critical_points(expr, deriv, deriv2, real_critical)

    except Exception as e:
        print(f"  Could not compute: {e}")


def function_study():
    print(f"\n{'='*50}")
    print(f"COMPLETE FUNCTION STUDY")
    print(f"{'='*50}")
    print(f"")
    print(f"  In liceo, 'studio di funzione' means analyzing a function")
    print(f"  completely — domain, sign, limits, derivatives, graph.")
    print(f"  Derivatives are the central tool.")
    print(f"")
    print(f"  THE CHECKLIST:")
    print(f"")
    print(f"  1. DOMAIN — where is f(x) defined?")
    print(f"     Denominators ≠ 0, logs > 0, square roots ≥ 0.")
    print(f"")
    print(f"  2. SYMMETRY — even, odd, or neither?")
    print(f"     f(-x) = f(x)  → even   (symmetric about y-axis)")
    print(f"     f(-x) = -f(x) → odd    (symmetric about origin)")
    print(f"")
    print(f"  3. INTERCEPTS")
    print(f"     y-intercept: f(0)")
    print(f"     x-intercepts: solve f(x) = 0")
    print(f"")
    print(f"  4. LIMITS AND ASYMPTOTES")
    print(f"     x → ±∞:  horizontal asymptotes")
    print(f"     x → excluded points:  vertical asymptotes")
    print(f"")
    print(f"  5. FIRST DERIVATIVE → monotonicity")
    print(f"     f' > 0 → increasing")
    print(f"     f' < 0 → decreasing")
    print(f"     f' = 0 → critical point (candidate max/min)")
    print(f"")
    print(f"  6. SECOND DERIVATIVE → concavity")
    print(f"     f'' > 0 → concave up  ∪")
    print(f"     f'' < 0 → concave down ∩")
    print(f"     f'' = 0 → candidate inflection point")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  WORKED EXAMPLE: f(x) = x³ - 3x")
    print(f"")

    x    = sp.Symbol('x')
    expr = x**3 - 3*x
    df   = sp.diff(expr, x)
    d2f  = sp.diff(df, x)

    print(f"  f(x)   = x³ - 3x")
    print(f"  f'(x)  = {df}")
    print(f"  f''(x) = {d2f}")
    print(f"")
    print(f"  1. DOMAIN: all of ℝ  (polynomial)")
    print(f"")
    print(f"  2. SYMMETRY: f(-x) = -x³+3x = -(x³-3x) = -f(x)")
    print(f"     ODD — symmetric about the origin.")
    print(f"")
    zeros = sp.solve(expr, x)
    print(f"  3. INTERCEPTS:")
    print(f"     f(0) = 0  (passes through the origin)")
    print(f"     Zeros: {zeros}")
    print(f"")
    print(f"  4. LIMITS: → ±∞  as x → ±∞.  No asymptotes.")
    print(f"")
    print(f"  5. f'(x) = 3x²-3 = 3(x-1)(x+1)")
    crit = sp.solve(df, x)
    print(f"     Critical points: x = {crit}")
    print(f"     x < -1:   f' > 0  increasing")
    print(f"     -1 < x < 1:  f' < 0  decreasing")
    print(f"     x > 1:    f' > 0  increasing")
    print(f"     x = -1: f(-1) = {expr.subs(x,-1)}  →  LOCAL MAX")
    print(f"     x =  1: f(1)  = {expr.subs(x, 1)}  →  LOCAL MIN")
    print(f"")
    print(f"  6. f''(x) = 6x")
    infl = sp.solve(d2f, x)
    print(f"     f'' = 0 at x = {infl}")
    print(f"     x < 0: f'' < 0  concave down ∩")
    print(f"     x > 0: f'' > 0  concave up   ∪")
    print(f"     x = 0: inflection point")

    plot_complete_study(expr, df, d2f)


def lhopital():
    print(f"\n{'='*50}")
    print(f"DE L'HÔPITAL'S RULE")
    print(f"{'='*50}")
    print(f"")
    print(f"  Some limits give 0/0 or ∞/∞ — indeterminate forms.")
    print(f"  They're not 1 or ∞ or anything obvious.")
    print(f"  De L'Hôpital's rule resolves them cleanly.")
    print(f"")
    print(f"  THE RULE:")
    print(f"  If lim f(x) = 0 and lim g(x) = 0  (or both → ∞),")
    print(f"  then:")
    print(f"      lim f(x)/g(x) = lim f'(x)/g'(x)")
    print(f"")
    print(f"  Replace numerator and denominator with their derivatives.")
    print(f"  Apply as many times as needed.")
    print(f"")
    print(f"  WHY DOES IT WORK?")
    print(f"  Near x=a, f(x) ≈ f'(a)·(x-a) and g(x) ≈ g'(a)·(x-a).")
    print(f"  So f(x)/g(x) ≈ f'(a)/g'(a).")
    print(f"  The (x-a) factors cancel — that's the rule.")
    print(f"")
    print(f"  EXAMPLES:")
    print(f"")

    x = sp.Symbol('x')
    examples = [
        ("sin(x)/x",     "x→0", 0,
         "0/0 form.\n"
         "  f'=cos x, g'=1.\n"
         "  lim cos(x)/1 = cos(0) = 1."),
        ("(exp(x)-1)/x", "x→0", 0,
         "0/0 form.\n"
         "  f'=eˣ, g'=1.\n"
         "  lim eˣ/1 = e⁰ = 1."),
        ("x**2/exp(x)",  "x→∞", None,
         "∞/∞ form.\n"
         "  Apply once: 2x/eˣ  (still ∞/∞)\n"
         "  Apply again: 2/eˣ → 0.\n"
         "  Exponential always beats any power of x."),
        ("(1-cos(x))/x**2", "x→0", 0,
         "0/0 form.\n"
         "  Apply once: sin(x)/2x  (still 0/0)\n"
         "  Apply again: cos(x)/2 → 1/2."),
    ]

    for func_str, point, val, explanation in examples:
        print(f"  lim ({point}) {func_str}")
        for line in explanation.split('\n'):
            print(f"  {line}")
        expr = sp.sympify(func_str)
        lim  = sp.limit(expr, x, val if val is not None else sp.oo)
        print(f"  Sympy confirms: {lim}")
        print(f"")

    print(f"  ─────────────────────────────────────────────")
    print(f"  THE MOST FAMOUS LIMIT IN CALCULUS:")
    print(f"")
    print(f"  lim(x→0) sin(x)/x = 1")
    print(f"")
    print(f"  This means: for small angles (in radians), sin(x) ≈ x.")
    print(f"  A 0.01 radian angle: sin(0.01) = {math.sin(0.01):.10f}")
    print(f"  Basically the same as 0.01.")
    print(f"  This approximation is used everywhere in physics.")

    plot_lhopital()


def plot_lhopital():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    x = np.linspace(0.001, 1.5, 500)
    axes[0].plot(x, np.sin(x)/x, color="steelblue", linewidth=2.5,
                 label="sin(x)/x")
    axes[0].plot(0, 1, "o", color="crimson", markersize=12,
                 label="limit = 1 at x=0")
    axes[0].axhline(1, color="crimson", linewidth=1,
                    linestyle="--", alpha=0.5)
    axes[0].set_title("lim(x→0) sin(x)/x = 1", fontsize=12)
    axes[0].set_xlabel("x")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0.9, 1.02)

    x2 = np.linspace(0, 10, 400)
    axes[1].plot(x2, x2**2,     color="steelblue", linewidth=2.5,
                 label="x²")
    axes[1].plot(x2, np.exp(x2), color="crimson",   linewidth=2.5,
                 label="eˣ")
    axes[1].set_ylim(0, 500)
    axes[1].set_title("eˣ grows faster than any xⁿ\nlim(x→∞) x²/eˣ = 0",
                      fontsize=12)
    axes[1].set_xlabel("x")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("De L'Hôpital — classic limits",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def linear_approximation():
    print(f"\n{'='*50}")
    print(f"LINEAR APPROXIMATION")
    print(f"{'='*50}")
    print(f"")
    print(f"  Near any point where f is differentiable,")
    print(f"  the function looks like its tangent line.")
    print(f"  So we can APPROXIMATE f(x) with that line.")
    print(f"")
    print(f"  Near x=a:")
    print(f"      f(x) ≈ f(a) + f'(a)·(x-a)")
    print(f"")
    print(f"  This is just the tangent line equation.")
    print(f"  Works well when x is close to a.")
    print(f"  Fails when x is far from a.")
    print(f"")
    print(f"  WHY IS THIS USEFUL?")
    print(f"")
    print(f"  · √(1.02) without a calculator:")
    print(f"    f(x)=√x, a=1, f'(1)=1/2")
    print(f"    √(1.02) ≈ 1 + 0.5·0.02 = 1.01")
    print(f"    Actual: {math.sqrt(1.02):.8f}  — very close!")
    print(f"")
    print(f"  · In physics: sin(θ) ≈ θ for small angles.")
    print(f"    Simplifies almost every problem in mechanics and optics.")
    print(f"")
    print(f"  · In economics: marginal cost = derivative of total cost.")
    print(f"    'Marginal' in economics always means derivative.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  CLASSIC APPROXIMATIONS near x=0:")
    print(f"")

    xv = 0.1
    rows = [
        ("sin(x)",   lambda x: math.sin(x),          lambda x: x,
         "sin(x) ≈ x"),
        ("cos(x)",   lambda x: math.cos(x),          lambda x: 1-x**2/2,
         "cos(x) ≈ 1-x²/2"),
        ("eˣ",       lambda x: math.exp(x),          lambda x: 1+x,
         "eˣ ≈ 1+x"),
        ("ln(1+x)",  lambda x: math.log(1+x),        lambda x: x,
         "ln(1+x) ≈ x"),
        ("√(1+x)",   lambda x: math.sqrt(1+x),       lambda x: 1+x/2,
         "√(1+x) ≈ 1+x/2"),
    ]

    print(f"  {'Function':>12}  {'Approx':>14}  {'Exact at 0.1':>14}"
          f"  {'Approx at 0.1':>14}  {'Error':>8}")
    print(f"  {'─'*68}")
    for fname, f, approx, desc in rows:
        exact = f(xv)
        appr  = approx(xv)
        err   = abs(exact - appr)
        print(f"  {fname:>12}  {desc:>14}  {exact:>14.8f}"
              f"  {appr:>14.8f}  {err:>8.2e}")

    print(f"")
    print(f"  All errors tiny at x=0.1.")
    print(f"  They grow as x moves away from 0.")

    plot_linear_approx()


def plot_linear_approx():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    x = np.linspace(-1.5, 1.5, 400)

    funcs = [
        (np.sin,  lambda x: x,        "sin(x)", "x"),
        (np.exp,  lambda x: 1+x,      "eˣ",     "1+x"),
        (np.cos,  lambda x: 1-x**2/2, "cos(x)", "1-x²/2"),
    ]

    for ax, (f, appr, fname, aname) in zip(axes, funcs):
        ax.plot(x, f(x),    color="steelblue", linewidth=2.5,
                label=fname)
        ax.plot(x, appr(x), color="crimson",   linewidth=2,
                linestyle="--", label=f"≈ {aname}")
        ax.plot(0, f(0), "o", color="black", markersize=8)
        ax.set_title(f"{fname} ≈ {aname}  near x=0", fontsize=11)
        ax.set_xlabel("x")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-2, 3)

    plt.suptitle("Approximations near x=0 — how close are they?",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def physics_motion():
    print(f"\n{'='*50}")
    print(f"PHYSICS: VELOCITY AND ACCELERATION")
    print(f"{'='*50}")
    print(f"")
    print(f"  This was the original motivation for calculus.")
    print(f"  Newton invented it in the 1660s to describe")
    print(f"  the motion of planets.")
    print(f"")
    print(f"  Let s(t) = position at time t.")
    print(f"")
    print(f"  VELOCITY = rate of change of position:")
    print(f"      v(t) = s'(t)")
    print(f"")
    print(f"  ACCELERATION = rate of change of velocity:")
    print(f"      a(t) = v'(t) = s''(t)")
    print(f"")
    print(f"  The second derivative of position is acceleration.")
    print(f"  Newton's second law F = ma is about the second derivative.")
    print(f"  The entire history of classical mechanics")
    print(f"  is written in second derivatives.")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  EXAMPLE: free fall from 100m.")
    print(f"")
    print(f"  s(t) = 100 - ½·9.81·t²  (height in meters)")
    print(f"  v(t) = -9.81t            (velocity, negative = downward)")
    print(f"  a(t) = -9.81             (constant — gravity is constant)")
    print(f"")
    t_ground = math.sqrt(100/4.905)
    v_impact = -9.81 * t_ground
    print(f"  Hits the ground when s=0:")
    print(f"  t = √(100/4.905) = {t_ground:.3f} s")
    print(f"  Impact speed: {abs(v_impact):.2f} m/s = {abs(v_impact)*3.6:.1f} km/h")
    print(f"")
    print(f"  ─────────────────────────────────────────────")
    print(f"  YOUR MOTION — enter s(t):")
    print(f"  Examples: 100 - 9.81/2*t**2,  sin(t),  t**3 - 6*t")
    print(f"")

    t = sp.Symbol('t')
    expr_str = input("  s(t) = ")
    try:
        s  = sp.sympify(expr_str)
        v  = sp.diff(s, t)
        a  = sp.diff(v, t)
        print(f"")
        print(f"  s(t) = {s}")
        print(f"  v(t) = {sp.simplify(v)}")
        print(f"  a(t) = {sp.simplify(a)}")

        cv = [c for c in sp.solve(v, t) if c.is_real]
        if cv:
            print(f"")
            print(f"  v=0 at t={cv}  (momentarily at rest)")
            for tc in cv:
                print(f"  Position: s({tc}) = {sp.simplify(s.subs(t,tc))}")

        plot_motion(s, v, a)
    except Exception as e:
        print(f"  Could not compute: {e}")


def derivative_applications():
    print(f"\n{'='*50}")
    print(f"APPLICATIONS OF DERIVATIVES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Derivatives answer concrete questions about the world.")
    print(f"  Where is the maximum? Where does the function change?")
    print(f"  How fast is this falling? How close is this approximation?")
    print(f"")
    print(f"  1 — Maxima and minima")
    print(f"  2 — Complete function study")
    print(f"  3 — De L'Hôpital's rule")
    print(f"  4 — Linear approximation")
    print(f"  5 — Physics: velocity and acceleration")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        maxima_minima()
    elif choice == "2":
        function_study()
    elif choice == "3":
        lhopital()
    elif choice == "4":
        linear_approximation()
    elif choice == "5":
        physics_motion()
    else:
        print(f"  Invalid choice.")


def derivatives():
    print(f"\n{'='*50}")
    print(f"DERIVATIVES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Calculus was invented independently by Newton and Leibniz")
    print(f"  in the 1660s-1680s — one of the greatest disputes")
    print(f"  in the history of mathematics.")
    print(f"  Newton needed it to describe planetary motion.")
    print(f"  Leibniz needed it to solve geometric problems.")
    print(f"  Today it underpins physics, engineering, economics,")
    print(f"  machine learning — anything that changes over time.")
    print(f"")
    print(f"  The core idea:")
    print(f"  how fast is something changing RIGHT NOW?")
    print(f"  Not on average — at this precise instant.")
    print(f"  That instantaneous rate of change is the derivative.")
    print(f"")
    print(f"  1 — What is a derivative?")
    print(f"       intuition and formal definition")
    print(f"  2 — Derivative rules")
    print(f"       power, product, quotient, chain")
    print(f"  3 — Applications")
    print(f"       maxima, function study, L'Hôpital, physics")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        print(f"")
        print(f"  1 — From average to instantaneous speed")
        print(f"  2 — The formal definition and non-differentiable cases")
        print(f"")
        sub = input("  Enter 1 or 2: ")
        if sub == "1":
            intuition_derivative()
        elif sub == "2":
            definition_derivative()
        else:
            print(f"  Invalid choice.")
    elif choice == "2":
        derivative_rules()
    elif choice == "3":
        derivative_applications()
    else:
        print(f"  Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    derivatives()