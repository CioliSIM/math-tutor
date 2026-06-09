import math
import matplotlib.pyplot as plt
import numpy as np

def solve(a, b, c):
    print(f"\n{'='*50}")
    print(f"QUADRATIC EQUATION SOLVER")
    print(f"{'='*50}")
    print(f"  {a}x² + {b}x + {c} = 0")
    print(f"")
    print(f"  We have one unknown — x — and our job is to")
    print(f"  find every value of x that makes this true.")
    print(f"  There could be 0, 1, or 2 real solutions.")
    print(f"  The discriminant will tell us which case we're in.")

    print(f"\n--- Step 1: Compute the discriminant ---")
    print(f"  The discriminant is this expression: Δ = b² - 4ac")
    print(f"  It's not magic — it comes directly from the")
    print(f"  quadratic formula. The part under the square root")
    print(f"  determines how many real solutions exist:")
    print(f"")
    print(f"    Δ > 0  →  two distinct solutions")
    print(f"    Δ = 0  →  one repeated solution")
    print(f"    Δ < 0  →  no real solutions (square root of negative)")
    print(f"")
    print(f"  Let's compute it:")
    print(f"  Δ = ({b})² - 4·({a})·({c})")
    print(f"    = {b**2} - {4*a*c}")
    delta = b**2 - 4*a*c
    print(f"    = {delta}")

    print(f"\n--- Step 2: What does Δ = {delta} tell us? ---")

    if delta > 0:
        print(f"  Δ > 0 — we have two distinct real solutions.")
        print(f"  The parabola crosses the x-axis at two points.")

        radice = math.sqrt(delta)
        x1 = (-b + radice) / (2*a)
        x2 = (-b - radice) / (2*a)

        print(f"\n--- Step 3: Apply the quadratic formula ---")
        print(f"  The formula is: x = (-b ± √Δ) / 2a")
        print(f"  The ± gives us two solutions — one with +, one with -.")
        print(f"  This is why Δ > 0 always means exactly two solutions.")
        print(f"")
        print(f"  √Δ = √{delta} = {radice:.4f}")
        print(f"")
        print(f"  x₁ = ({-b} + {radice:.4f}) / {2*a} = {x1:.4f}")
        print(f"  x₂ = ({-b} - {radice:.4f}) / {2*a} = {x2:.4f}")

        print(f"\n--- Step 4: Verify both solutions ---")
        print(f"  Always check. Plug each solution back in")
        print(f"  and confirm the result is (approximately) zero.")
        print(f"")
        for x, label in [(x1, "x₁"), (x2, "x₂")]:
            check = a*x**2 + b*x + c
            print(f"  {label} = {x:.4f}:  {a}·({x:.4f})² + {b}·({x:.4f}) + {c} = {check:.6f} ✓")
        print(f"")
        print(f"  Both work. The solutions are x₁ = {x1:.4f} and x₂ = {x2:.4f}.")
        plot_equation(a, b, c, x1, x2)

    elif delta == 0:
        print(f"  Δ = 0 — exactly one solution, called a double root.")
        print(f"  The parabola touches the x-axis at exactly one point")
        print(f"  but doesn't cross it. The ± in the formula collapses")
        print(f"  to a single value because √0 = 0.")

        x = -b / (2*a)

        print(f"\n--- Step 3: Apply the formula ---")
        print(f"  x = -b / 2a")
        print(f"    = {-b} / {2*a}")
        print(f"    = {x}")

        print(f"\n--- Step 4: Verify ---")
        check = a*x**2 + b*x + c
        print(f"  Substituting x = {x}:")
        print(f"  {a}·({x})² + {b}·({x}) + {c} = {check:.6f} ✓")
        print(f"")
        print(f"  The solution is x = {x} (double root).")
        plot_equation(a, b, c, x1=x)

    else:
        print(f"  Δ < 0 — no real solutions.")
        print(f"  We'd need to take the square root of {delta},")
        print(f"  which isn't a real number. The parabola never")
        print(f"  touches the x-axis at all.")
        print(f"")
        print(f"  There are two complex solutions, but those")
        print(f"  involve imaginary numbers — covered in the advanced module.")
        plot_equation(a, b, c)


def plot_equation(a, b, c, x1=None, x2=None):
    center = -b / (2*a)
    spread = max(abs(x1 - x2) * 2 if x1 is not None and x2 is not None else 4, 4)

    x = np.linspace(center - spread, center + spread, 400)
    y = a*x**2 + b*x + c

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="crimson", linewidth=2, label=f"f(x) = {a}x² + {b}x + {c}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    if x1 is not None and x2 is not None:
        ax.plot([x1, x2], [0, 0], "o", color="steelblue", markersize=8, label="Roots")
        ax.annotate(f"x₁={x1:.2f}", (x1, 0), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=10)
        ax.annotate(f"x₂={x2:.2f}", (x2, 0), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=10)
    elif x1 is not None:
        ax.plot([x1], [0], "o", color="steelblue", markersize=8, label=f"Double root x={x1:.2f}")
        ax.annotate(f"x={x1:.2f}", (x1, 0), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=10)

    ax.set_title(f"{a}x² + {b}x + {c} = 0", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("=== Quadratic Equation Solver ===")
    print("Enter the coefficients of ax^2 + bx + c = 0\n")
    a = float(input("Enter a: "))
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))
    solve(a, b, c)