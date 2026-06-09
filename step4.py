import math
import matplotlib.pyplot as plt
import numpy as np


def get_divisors(n):
    n = abs(int(n))
    if n == 0:
        return []
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
            divisors.append(-i)
    return divisors


def plot_polynomial(coeffs, roots):
    p = np.poly1d(coeffs)

    if roots:
        center = sum(roots) / len(roots)
        spread = max(max(roots) - min(roots), 2) * 2
    else:
        center = 0
        spread = 6

    x = np.linspace(center - spread, center + spread, 400)
    y = p(x)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="crimson", linewidth=2, label=f"p(x)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    for r in roots:
        ax.plot(r, 0, "o", color="steelblue", markersize=8)
        ax.annotate(f"x={r:.2f}", (r, 0), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10)

    ax.set_title(f"Polynomial of degree {len(coeffs)-1}", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("p(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def solve_polynomial(coeffs):
    print(f"\n{'='*50}")
    print(f"POLYNOMIAL EQUATION SOLVER")
    print(f"{'='*50}")
    p = np.poly1d(coeffs)
    print(f"\nYour polynomial:")
    print(p)
    print(f"")
    print(f"  Degree: {len(coeffs) - 1}")
    print(f"  Constant term: {coeffs[-1]}")
    print(f"")
    print(f"  Here's the plan: we'll use the Rational Root Theorem")
    print(f"  to find candidates, test each one, and every time")
    print(f"  we find a root we'll use Ruffini to peel off a layer")
    print(f"  and reduce the degree. Keep going until we hit")
    print(f"  something we can solve directly.")

    print(f"\n--- Step 1: Find the candidate roots ---")
    print(f"  The Rational Root Theorem says: if this polynomial")
    print(f"  has any integer roots, they must be divisors of the")
    print(f"  constant term, which is {coeffs[-1]}.")
    print(f"  So instead of guessing randomly, we only need to")
    print(f"  try a finite list of numbers.")
    print(f"")
    candidates = get_divisors(coeffs[-1])
    print(f"  Candidates: {sorted(set(candidates))}")
    print(f"  That's {len(set(candidates))} numbers to check — let's go.")

    print(f"\n--- Step 2: Test each candidate ---")
    print(f"  We plug each candidate into the polynomial.")
    print(f"  The Remainder Theorem tells us: if p(r) = 0,")
    print(f"  then (x - r) divides the polynomial exactly,")
    print(f"  which means r is a root. Simple as that.")
    print(f"")

    current_coeffs = list(coeffs)
    roots_found = []

    for r in sorted(set(candidates)):
        current_p = np.poly1d(current_coeffs)
        value = round(current_p(r), 10)
        if value == 0:
            print(f"  p({r}) = 0 ✓  →  x = {r} is a root!")
            roots_found.append(r)
        else:
            print(f"  p({r}) = {value:.4f} ✗")

    if not roots_found:
        print(f"")
        print(f"  No integer roots found. The roots of this polynomial")
        print(f"  are either irrational or complex.")
        plot_polynomial(coeffs, [])
        return

    print(f"")
    print(f"  Roots found so far: {roots_found}")

    print(f"\n--- Step 3: Apply Ruffini's method ---")
    print(f"  For each root r we found, we divide the polynomial")
    print(f"  by (x - r) using Ruffini's scheme. This drops the")
    print(f"  degree by 1 each time. Here's how it works:")
    print(f"  · Bring down the first coefficient")
    print(f"  · Multiply it by r, add to the next coefficient")
    print(f"  · Repeat until the end — the last number is the remainder")
    print(f"  · If remainder = 0, we confirmed r is a root")
    print(f"")

    all_roots = []

    for r in roots_found:
        print(f"  Dividing by (x - {r}):")
        print(f"")

        header = f"  {r}  |  " + "   ".join(
            str(int(x)) if x == int(x) else str(x)
            for x in current_coeffs
        )
        print(f"  {'-'*50}")
        print(header)
        print(f"  {'-'*50}")

        new_coeffs = [current_coeffs[0]]
        ruffini_row = [0]
        for i in range(1, len(current_coeffs)):
            carry = new_coeffs[-1] * r
            ruffini_row.append(carry)
            new_coeffs.append(current_coeffs[i] + carry)

        carry_str = "       |  " + "   ".join(
            str(int(x)) if x == int(x) else f"{x:.2f}"
            for x in ruffini_row
        )
        print(carry_str)

        result_str = "       |  " + "   ".join(
            str(int(x)) if x == int(x) else f"{x:.2f}"
            for x in new_coeffs
        )
        print(f"  {'-'*50}")
        print(result_str)
        print(f"")

        remainder = new_coeffs[-1]
        new_coeffs = new_coeffs[:-1]

        if abs(remainder) < 1e-9:
            print(f"  Remainder = 0 ✓ — clean division confirmed.")
            print(f"  Polynomial is now degree {len(new_coeffs)-1}.")
            print(f"  New coefficients: {[int(x) if x == int(x) else x for x in new_coeffs]}")
        else:
            print(f"  Remainder = {remainder:.4f} — unexpected. Check your input.")

        all_roots.append(r)
        current_coeffs = new_coeffs
        print(f"")

    print(f"--- Step 4: Solve the reduced polynomial ---")
    print(f"  We're down to degree {len(current_coeffs)-1} — let's finish this.")
    print(f"")

    if len(current_coeffs) == 2:
        a, b = current_coeffs
        print(f"  Linear equation: {a}x + {b} = 0")
        print(f"  Isolate x: x = -{b} / {a}")
        x = -b / a
        print(f"  x = {x:.4f}")
        all_roots.append(x)

    elif len(current_coeffs) == 3:
        a, b, c = current_coeffs
        print(f"  Quadratic equation: {a}x² + {b}x + {c} = 0")
        print(f"  Back to the quadratic formula.")
        delta = b**2 - 4*a*c
        print(f"  Δ = ({b})² - 4·({a})·({c}) = {delta:.4f}")
        if delta > 0:
            radice = math.sqrt(delta)
            x1 = (-b + radice) / (2*a)
            x2 = (-b - radice) / (2*a)
            print(f"  Δ > 0 → two more roots.")
            print(f"  x₁ = {x1:.4f}")
            print(f"  x₂ = {x2:.4f}")
            all_roots.extend([x1, x2])
        elif delta == 0:
            x = -b / (2*a)
            print(f"  Δ = 0 → one repeated root: x = {x:.4f}")
            all_roots.append(x)
        else:
            print(f"  Δ < 0 → no further real roots.")
            print(f"  The remaining two roots are complex.")

    print(f"\n{'='*50}")
    print(f"FINAL RESULT")
    print(f"{'='*50}")
    print(f"  All real roots: {[round(r, 4) for r in all_roots]}")
    print(f"")
    print(f"  Factored form:")
    factors = " · ".join([f"(x - {round(r, 4)})" for r in all_roots])
    leading = int(coeffs[0]) if coeffs[0] == int(coeffs[0]) else coeffs[0]
    print(f"  p(x) = {leading} · {factors}")
    print(f"")
    print(f"  Always worth double-checking: substitute each root")
    print(f"  back into the original polynomial and confirm p(r) = 0.")

    plot_polynomial(coeffs, all_roots)


if __name__ == "__main__":
    print("=== Polynomial Equation Solver ===")
    print("Enter your polynomial from highest to lowest degree.\n")
    degree = int(input("Enter the degree of the polynomial: "))
    coeffs = []
    for i in range(degree, -1, -1):
        c = float(input(f"Enter coefficient for x^{i}: "))
        coeffs.append(c)
    solve_polynomial(coeffs)