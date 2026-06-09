import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import math

x = sp.Symbol('x')


def plot_function(expr, domain, zeros):
    f_numeric = sp.lambdify(x, expr, 'numpy')

    try:
        x_min, x_max = -10, 10
        if domain != sp.S.Reals:
            intervals = sp.calculus.util.continuous_domain(expr, x, sp.S.Reals)
            if hasattr(intervals, 'start') and intervals.start != -sp.oo:
                x_min = max(-10, float(intervals.start))
            if hasattr(intervals, 'end') and intervals.end != sp.oo:
                x_max = min(10, float(intervals.end))
    except:
        x_min, x_max = -10, 10

    x_vals = np.linspace(x_min, x_max, 1000)

    with np.errstate(divide='ignore', invalid='ignore'):
        y_vals = f_numeric(x_vals)
        y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y_vals, color="crimson", linewidth=2, label=f"f(x) = {expr}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    for z in zeros:
        if z.is_real:
            try:
                ax.plot(float(z), 0, "o", color="steelblue", markersize=8)
                ax.annotate(f"x={float(z):.2f}", (float(z), 0),
                            textcoords="offset points",
                            xytext=(0, 12), ha="center", fontsize=10)
            except:
                pass

    ax.set_ylim(-10, 10)
    ax.set_title(f"f(x) = {expr}", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def analyze_function(expr_str):
    print(f"\n{'='*50}")
    print(f"FUNCTION ANALYZER")
    print(f"{'='*50}")

    expr = sp.sympify(expr_str)

    print(f"\n  f(x) = {expr}")
    print(f"")
    print(f"  A function is more than just a formula — it has")
    print(f"  a personality. We're going to figure out where")
    print(f"  it lives, whether it's symmetric, where it crosses")
    print(f"  zero, where it's positive or negative, and whether")
    print(f"  it's climbing or falling. Let's go step by step.")

    # ── Step 1: Domain ──────────────────────────────────────
    print(f"\n--- Step 1: Domain ---")
    print(f"  The domain is where the function is allowed to exist.")
    print(f"  Three things can break a function:")
    print(f"  · A zero in the denominator — undefined")
    print(f"  · A negative under a square root — not real")
    print(f"  · A non-positive argument in a logarithm — undefined")
    print(f"")

    try:
        domain = sp.calculus.util.continuous_domain(expr, x, sp.S.Reals)
        print(f"  Domain: {domain}")
    except Exception:
        domain = sp.S.Reals
        print(f"  Couldn't compute the domain automatically.")
        print(f"  Assuming ℝ — double-check this by hand.")

    # ── Step 2: Parity ──────────────────────────────────────
    print(f"\n--- Step 2: Parity ---")
    print(f"  We substitute -x and see what happens.")
    print(f"  If f(-x) = f(x)  →  even  (mirror on y-axis)")
    print(f"  If f(-x) = -f(x) →  odd   (rotational symmetry)")
    print(f"  Otherwise        →  no parity at all")
    print(f"")

    f_neg = expr.subs(x, -x)
    f_neg_simplified = sp.simplify(f_neg)
    print(f"  f(-x) = {f_neg_simplified}")
    print(f"")

    if sp.simplify(f_neg - expr) == 0:
        print(f"  f(-x) = f(x) ✓ — EVEN function.")
        print(f"  Fold the graph along the y-axis and the two halves match.")
    elif sp.simplify(f_neg + expr) == 0:
        print(f"  f(-x) = -f(x) ✓ — ODD function.")
        print(f"  Rotate the graph 180° around the origin — it looks the same.")
    else:
        print(f"  Neither condition holds — NO parity.")
        print(f"  The function is asymmetric. No shortcuts here.")

    # ── Step 3: Zeros ───────────────────────────────────────
    print(f"\n--- Step 3: Zeros ---")
    print(f"  Where does the graph cross the x-axis?")
    print(f"  We solve f(x) = 0 and report every real solution.")
    print(f"  Complex solutions exist mathematically but don't")
    print(f"  show up on a real graph — we flag them separately.")
    print(f"")

    try:
        zeros = sp.solve(expr, x)
        if zeros:
            print(f"  Solving {expr} = 0:")
            for z in zeros:
                if z.is_real:
                    print(f"  x = {z} ≈ {float(z):.4f} ✓")
                else:
                    print(f"  x = {z}  (complex — not on real graph)")
        else:
            print(f"  No zeros — the graph never touches the x-axis.")
    except Exception:
        zeros = []
        print(f"  Couldn't solve this symbolically.")
        print(f"  Check the graph to estimate where it crosses zero.")

    # ── Step 4: Sign ────────────────────────────────────────
    print(f"\n--- Step 4: Sign ---")
    print(f"  We figure out where the function is above")
    print(f"  the x-axis (positive) and where it's below (negative).")
    print(f"  The zeros from Step 3 are the boundaries — the sign")
    print(f"  can only change at those points.")
    print(f"")

    try:
        positive = sp.solve(expr > 0, x)
        negative = sp.solve(expr < 0, x)
        print(f"  f(x) > 0  (above x-axis) for: {positive}")
        print(f"  f(x) < 0  (below x-axis) for: {negative}")
    except Exception:
        print(f"  Couldn't compute the sign automatically.")
        print(f"  The graph below will show it visually.")

    # ── Step 5: Monotonicity ─────────────────────────────────
    print(f"\n--- Step 5: Monotonicity ---")
    print(f"  Is the function climbing or falling?")
    print(f"  We compute the derivative f'(x) — it measures")
    print(f"  the instantaneous rate of change at every point.")
    print(f"  f'(x) > 0  →  increasing")
    print(f"  f'(x) < 0  →  decreasing")
    print(f"  f'(x) = 0  →  stationary point (possible max or min)")
    print(f"")

    try:
        derivative = sp.diff(expr, x)
        print(f"  f'(x) = {derivative}")
        print(f"")

        stationary = sp.solve(derivative, x)
        if stationary:
            print(f"  Stationary points — where the function pauses:")
            for s in stationary:
                if s.is_real:
                    val = expr.subs(x, s)
                    print(f"  x = {s}  →  f({s}) = {val}  ≈  ({float(s):.4f}, {float(val):.4f})")
        else:
            print(f"  No stationary points — strictly monotone the whole way.")

        print(f"")
        increasing = sp.solve(derivative > 0, x)
        decreasing = sp.solve(derivative < 0, x)
        print(f"  Increasing on: {increasing}")
        print(f"  Decreasing on: {decreasing}")

    except Exception:
        print(f"  Couldn't compute the derivative automatically.")

    # ── Graph ────────────────────────────────────────────────
    print(f"\n--- Graph ---")
    print(f"  Everything we just found — domain, zeros, monotonicity —")
    print(f"  should be visible here. Use the graph to sanity-check")
    print(f"  every result above. If something looks wrong, it probably is.")
    print(f"")

    try:
        zeros_list = sp.solve(expr, x)
    except:
        zeros_list = []

    plot_function(expr, domain, zeros_list)


# ── Input ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Function Analyzer ===")
    print("Enter a function of x using Python syntax.")
    print("Examples:  x**2 - 4  |  1/x  |  sqrt(x)  |  x**3 - x\n")
    expr_str = input("f(x) = ")
    analyze_function(expr_str)