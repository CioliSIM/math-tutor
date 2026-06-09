import math
import matplotlib.pyplot as plt
import numpy as np

def solve_inequality(a, b, c, op):
    print(f"\n{'='*50}")
    print(f"QUADRATIC INEQUALITY SOLVER")
    print(f"{'='*50}")
    print(f"  {a}x² + {b}x + {c}  {op}  0")
    print(f"")
    print(f"  Unlike an equation, we're not looking for a single")
    print(f"  value — we want an entire interval of x values")
    print(f"  that make this inequality true.")
    print(f"  The strategy: find where the parabola crosses zero,")
    print(f"  then figure out which side satisfies the inequality.")

    print(f"\n--- Step 1: Find the boundary points ---")
    print(f"  We temporarily ignore the inequality and solve")
    print(f"  the equality: {a}x² + {b}x + {c} = 0")
    print(f"  These roots are the points where the expression")
    print(f"  changes sign — they're the boundaries of our solution.")
    print(f"")
    delta = b**2 - 4*a*c
    print(f"  Δ = ({b})² - 4·({a})·({c}) = {delta}")

    print(f"\n--- Step 2: What does Δ = {delta} tell us? ---")

    if delta > 0:
        radice = math.sqrt(delta)
        x1 = (-b - radice) / (2*a)
        x2 = (-b + radice) / (2*a)
        if x1 > x2:
            x1, x2 = x2, x1

        print(f"  Δ > 0 — two distinct roots: x₁ = {x1:.4f}, x₂ = {x2:.4f}")
        print(f"  These split the number line into three intervals:")
        print(f"")
        print(f"    (-∞, {x1:.4f})  |  ({x1:.4f}, {x2:.4f})  |  ({x2:.4f}, +∞)")
        print(f"")
        print(f"  In each interval, the expression keeps the same sign.")
        print(f"  We just need to figure out which intervals satisfy {op} 0.")

        print(f"\n--- Step 3: Which way does the parabola open? ---")
        if a > 0:
            print(f"  a = {a} > 0 → parabola opens UPWARD (∪ shape).")
            print(f"  Think of it like a valley — the parabola dips below")
            print(f"  zero between the roots and rises above zero outside them.")
            print(f"")
            print(f"  So the expression is:")
            print(f"    POSITIVE outside the roots  →  x < {x1:.4f} or x > {x2:.4f}")
            print(f"    NEGATIVE between the roots  →  {x1:.4f} < x < {x2:.4f}")
        else:
            print(f"  a = {a} < 0 → parabola opens DOWNWARD (∩ shape).")
            print(f"  Think of it like a hill — the parabola rises above")
            print(f"  zero between the roots and drops below zero outside them.")
            print(f"")
            print(f"  So the expression is:")
            print(f"    NEGATIVE outside the roots  →  x < {x1:.4f} or x > {x2:.4f}")
            print(f"    POSITIVE between the roots  →  {x1:.4f} < x < {x2:.4f}")

        print(f"\n--- Step 4: Pick the right interval ---")
        interpret(op, x1, x2, a)
        plot_inequality(a, b, c, op, x1, x2, delta)

    elif delta == 0:
        x = -b / (2*a)
        print(f"  Δ = 0 — one repeated root at x = {x:.4f}.")
        print(f"  The parabola just touches the x-axis at one point")
        print(f"  without crossing it. The expression is either always")
        print(f"  positive or always negative — except at that one point.")

        print(f"\n--- Step 3: Which way does the parabola open? ---")
        if a > 0:
            print(f"  a = {a} > 0 → parabola opens UPWARD.")
            print(f"  The expression is ≥ 0 everywhere — it only hits zero at x = {x:.4f}.")
            if op in [">", ">="]:
                sol = "x ∈ ℝ" if op == ">=" else f"x ∈ ℝ \\ {{{x:.4f}}}"
                print(f"  We want {op} 0, and the expression is always positive.")
                print(f"  Solution: {sol}")
            else:
                print(f"  We want {op} 0, but the expression is never negative.")
                print(f"  No solution.")
        else:
            print(f"  a = {a} < 0 → parabola opens DOWNWARD.")
            print(f"  The expression is ≤ 0 everywhere — it only hits zero at x = {x:.4f}.")
            if op in ["<", "<="]:
                sol = "x ∈ ℝ" if op == "<=" else f"x ∈ ℝ \\ {{{x:.4f}}}"
                print(f"  We want {op} 0, and the expression is always negative.")
                print(f"  Solution: {sol}")
            else:
                print(f"  We want {op} 0, but the expression is never positive.")
                print(f"  No solution.")
        plot_inequality(a, b, c, op, x, x, delta)

    else:
        print(f"  Δ < 0 — no real roots at all.")
        print(f"  The parabola never crosses the x-axis, which means")
        print(f"  the expression never changes sign. It's either always")
        print(f"  positive or always negative — for every single x.")

        print(f"\n--- Step 3: Which way does the parabola open? ---")
        if a > 0:
            print(f"  a = {a} > 0 → parabola opens UPWARD, always above the x-axis.")
            print(f"  The expression is always positive — no exceptions.")
            if op in [">", ">="]:
                print(f"  We want {op} 0, and it's always positive.")
                print(f"  Solution: x ∈ ℝ (every real number works)")
            else:
                print(f"  We want {op} 0, but it's never negative.")
                print(f"  No solution.")
        else:
            print(f"  a = {a} < 0 → parabola opens DOWNWARD, always below the x-axis.")
            print(f"  The expression is always negative — no exceptions.")
            if op in ["<", "<="]:
                print(f"  We want {op} 0, and it's always negative.")
                print(f"  Solution: x ∈ ℝ (every real number works)")
            else:
                print(f"  We want {op} 0, but it's never positive.")
                print(f"  No solution.")
        plot_inequality(a, b, c, op, None, None, delta)


def interpret(op, x1, x2, a):
    strict = op in [">", "<"]
    l = "(" if strict else "["
    r = ")" if strict else "]"
    agrees = (a > 0 and op in [">", ">="]) or (a < 0 and op in ["<", "<="])

    print(f"  Here's the key question: does the sign of a agree")
    print(f"  with the operator? In other words — does the parabola")
    print(f"  open in the direction we want?")
    print(f"")

    if agrees:
        print(f"  YES — a is {'positive' if a > 0 else 'negative'} and we want {op} 0.")
        print(f"  The parabola opens {'upward' if a > 0 else 'downward'}, and we want")
        print(f"  the {'positive' if op in ['>','>='] else 'negative'} region.")
        print(f"  That region is OUTSIDE the roots — the two outer intervals.")
        print(f"")
        print(f"  Solution: x ∈ (-∞, {x1:.4f}{r} ∪ {l}{x2:.4f}, +∞)")
    else:
        print(f"  NO — a is {'positive' if a > 0 else 'negative'} but we want {op} 0.")
        print(f"  The parabola opens {'upward' if a > 0 else 'downward'}, but we want")
        print(f"  the {'negative' if op in ['>','>='] else 'positive'} region.")
        print(f"  That region is BETWEEN the roots — the inner interval.")
        print(f"")
        print(f"  Solution: x ∈ {l}{x1:.4f}, {x2:.4f}{r}")


def plot_inequality(a, b, c, op, x1, x2, delta):
    if x1 is not None:
        center = (x1 + x2) / 2
        spread = max(abs(x2 - x1) * 2, 4)
    else:
        center = -b / (2*a)
        spread = 6

    x = np.linspace(center - spread, center + spread, 400)
    y = a*x**2 + b*x + c

    fig, ax = plt.subplots(figsize=(8, 5))

    if delta > 0 and x1 is not None:
        strict = op in [">", "<"]
        agrees = (a > 0 and op in [">", ">="]) or (a < 0 and op in ["<", "<="])

        if agrees:
            ax.fill_between(x, y, 0, where=(x <= x1),
                            alpha=0.25, color="steelblue", label="Solution region")
            ax.fill_between(x, y, 0, where=(x >= x2),
                            alpha=0.25, color="steelblue")
        else:
            ax.fill_between(x, y, 0, where=((x >= x1) & (x <= x2)),
                            alpha=0.25, color="steelblue", label="Solution region")

        mfc = "white" if strict else "steelblue"
        ax.plot([x1, x2], [0, 0], marker="o", markersize=8,
                color="steelblue", linestyle="none",
                markerfacecolor=mfc, markeredgecolor="steelblue", markeredgewidth=2)
        ax.annotate(f"x₁={x1:.2f}", (x1, 0), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10)
        ax.annotate(f"x₂={x2:.2f}", (x2, 0), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10)

    ax.plot(x, y, color="crimson", linewidth=2, label=f"f(x) = {a}x² + {b}x + {c}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"{a}x² + {b}x + {c}  {op}  0", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("=== Quadratic Inequality Solver ===")
    print("Enter the coefficients of ax^2 + bx + c  [op]  0\n")
    a = float(input("Enter a: "))
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))
    op = input("Enter operator (>, <, >=, <=): ")
    solve_inequality(a, b, c, op)