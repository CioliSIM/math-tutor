import math
import matplotlib.pyplot as plt
import numpy as np

def choose_method(a1, b1, a2, b2):
    """
    Looks at the coefficients and decides the cleanest method.
    Returns 'substitution' or 'elimination'.
    """
    # If any coefficient is 1 or -1, substitution is immediate
    if abs(a1) == 1 or abs(b1) == 1 or abs(a2) == 1 or abs(b2) == 1:
        return "substitution"

    # If coefficients of x or y are equal or opposite, elimination is direct
    if a1 == a2 or a1 == -a2 or b1 == b2 or b1 == -b2:
        return "elimination"

    # General case — elimination with multiplication
    return "elimination"


def solve_substitution(a1, b1, c1, a2, b2, c2):
    print(f"\n--- Why substitution? ---")
    print(f"  One of the coefficients is 1 or -1.")
    print(f"  That means we can isolate a variable immediately")
    print(f"  without any messy fractions. It's the cleanest path.")

    # Find which variable to isolate — pick coefficient = ±1
    if abs(a1) == 1:
        # isolate x from equation 1: x = (c1 - b1*y) / a1
        print(f"\n--- Step 1: Isolate x from equation 1 ---")
        print(f"  {a1}x + {b1}y = {c1}")
        print(f"  x = ({c1} - {b1}y) / {a1}")
        if a1 == 1:
            print(f"  x = {c1} - {b1}y")
        else:
            print(f"  x = {-c1} + {b1}y")

        print(f"\n--- Step 2: Substitute into equation 2 ---")
        print(f"  Replace x in:  {a2}x + {b2}y = {c2}")
        # a2*(c1 - b1*y)/a1 + b2*y = c2
        # expand: (a2*c1/a1) - (a2*b1/a1)*y + b2*y = c2
        coeff_y = b2 - (a2 * b1) / a1
        const   = c2 - (a2 * c1) / a1
        print(f"  {a2}·({c1} - {b1}y)/{a1} + {b2}y = {c2}")
        print(f"  {a2*c1/a1:.4f} - {a2*b1/a1:.4f}y + {b2}y = {c2}")
        print(f"  {const:.4f} + {coeff_y:.4f}y = ... wait, let me rearrange:")
        print(f"  {coeff_y:.4f}y = {c2} - {a2*c1/a1:.4f}")
        print(f"  {coeff_y:.4f}y = {const:.4f}")

        if coeff_y == 0:
            if const == 0:
                print(f"\n  0 = 0 — infinite solutions.")
                return None, None
            else:
                print(f"\n  {const} = 0 — no solution.")
                return None, None

        y = const / coeff_y
        x = (c1 - b1 * y) / a1

        print(f"  y = {const:.4f} / {coeff_y:.4f} = {y:.4f}")

        print(f"\n--- Step 3: Back-substitute to find x ---")
        print(f"  x = ({c1} - {b1}·{y:.4f}) / {a1}")
        print(f"  x = ({c1} - {b1*y:.4f}) / {a1}")
        print(f"  x = {x:.4f}")

    elif abs(b1) == 1:
        # isolate y from equation 1: y = (c1 - a1*x) / b1
        print(f"\n--- Step 1: Isolate y from equation 1 ---")
        print(f"  {a1}x + {b1}y = {c1}")
        print(f"  y = ({c1} - {a1}x) / {b1}")
        if b1 == 1:
            print(f"  y = {c1} - {a1}x")
        else:
            print(f"  y = {-c1} + {a1}x")

        print(f"\n--- Step 2: Substitute into equation 2 ---")
        print(f"  Replace y in:  {a2}x + {b2}y = {c2}")
        coeff_x = a2 - (b2 * a1) / b1
        const   = c2 - (b2 * c1) / b1
        print(f"  {a2}x + {b2}·({c1} - {a1}x)/{b1} = {c2}")
        print(f"  {coeff_x:.4f}x = {const:.4f}")

        if coeff_x == 0:
            if const == 0:
                print(f"\n  0 = 0 — infinite solutions.")
                return None, None
            else:
                print(f"\n  {const} = 0 — no solution.")
                return None, None

        x = const / coeff_x
        y = (c1 - a1 * x) / b1

        print(f"  x = {const:.4f} / {coeff_x:.4f} = {x:.4f}")

        print(f"\n--- Step 3: Back-substitute to find y ---")
        print(f"  y = ({c1} - {a1}·{x:.4f}) / {b1}")
        print(f"  y = ({c1} - {a1*x:.4f}) / {b1}")
        print(f"  y = {y:.4f}")

    elif abs(a2) == 1:
        # isolate x from equation 2 — swap and recurse
        return solve_substitution(a2, b2, c2, a1, b1, c1)

    else:
        # isolate y from equation 2
        return solve_substitution(a2, b2, c2, a1, b1, c1)

    return x, y


def solve_elimination(a1, b1, c1, a2, b2, c2):
    print(f"\n--- Why elimination? ---")

    # Check if direct cancellation is possible
    if b1 == -b2 or b1 == b2:
        if b1 == -b2:
            print(f"  The y-coefficients are opposite ({b1} and {b2}).")
            print(f"  Adding the two equations cancels y immediately.")
            sign = "adding"
        else:
            print(f"  The y-coefficients are equal ({b1} and {b2}).")
            print(f"  Subtracting the two equations cancels y immediately.")
            sign = "subtracting"

        print(f"\n--- Step 1: Eliminate y ---")
        if b1 == -b2:
            new_a = a1 + a2
            new_c = c1 + c2
            print(f"  ({a1}x + {b1}y = {c1})")
            print(f"+ ({a2}x + {b2}y = {c2})")
        else:
            new_a = a1 - a2
            new_c = c1 - c2
            print(f"  ({a1}x + {b1}y = {c1})")
            print(f"- ({a2}x + {b2}y = {c2})")

        print(f"  {'─'*30}")
        print(f"  {new_a}x = {new_c}")

        if new_a == 0:
            if new_c == 0:
                print(f"\n  0 = 0 — infinite solutions.")
                return None, None
            else:
                print(f"\n  {new_c} = 0 — no solution.")
                return None, None

        x = new_c / new_a
        print(f"  x = {new_c} / {new_a} = {x:.4f}")

        print(f"\n--- Step 2: Substitute x back ---")
        print(f"  Plug x = {x:.4f} into equation 1:")
        print(f"  {a1}·({x:.4f}) + {b1}y = {c1}")
        y = (c1 - a1 * x) / b1
        print(f"  {a1*x:.4f} + {b1}y = {c1}")
        print(f"  {b1}y = {c1 - a1*x:.4f}")
        print(f"  y = {y:.4f}")

    elif a1 == -a2 or a1 == a2:
        if a1 == -a2:
            print(f"  The x-coefficients are opposite ({a1} and {a2}).")
            print(f"  Adding the equations cancels x immediately.")
        else:
            print(f"  The x-coefficients are equal ({a1} and {a2}).")
            print(f"  Subtracting the equations cancels x immediately.")

        print(f"\n--- Step 1: Eliminate x ---")
        if a1 == -a2:
            new_b = b1 + b2
            new_c = c1 + c2
            print(f"  ({a1}x + {b1}y = {c1})")
            print(f"+ ({a2}x + {b2}y = {c2})")
        else:
            new_b = b1 - b2
            new_c = c1 - c2
            print(f"  ({a1}x + {b1}y = {c1})")
            print(f"- ({a2}x + {b2}y = {c2})")

        print(f"  {'─'*30}")
        print(f"  {new_b}y = {new_c}")

        if new_b == 0:
            if new_c == 0:
                print(f"\n  0 = 0 — infinite solutions.")
                return None, None
            else:
                print(f"\n  {new_c} = 0 — no solution.")
                return None, None

        y = new_c / new_b
        print(f"  y = {new_c} / {new_b} = {y:.4f}")

        print(f"\n--- Step 2: Substitute y back ---")
        print(f"  Plug y = {y:.4f} into equation 1:")
        print(f"  {a1}x + {b1}·({y:.4f}) = {c1}")
        x = (c1 - b1 * y) / a1
        print(f"  {a1}x + {b1*y:.4f} = {c1}")
        print(f"  {a1}x = {c1 - b1*y:.4f}")
        print(f"  x = {x:.4f}")

    else:
        # General case — find multipliers to cancel y
        import math
        lcm_b = abs(b1 * b2) // math.gcd(abs(int(b1)), abs(int(b2)))
        m1 = lcm_b // abs(int(b1))
        m2 = lcm_b // abs(int(b2))

        print(f"  No coefficients cancel directly.")
        print(f"  We multiply to create opposite coefficients for y.")
        print(f"  LCM of {abs(b1)} and {abs(b2)} = {lcm_b}")
        print(f"  Multiply equation 1 by {m1}, equation 2 by {m2}.")

        print(f"\n--- Step 1: Multiply both equations ---")
        na1, nb1, nc1 = a1*m1, b1*m1, c1*m1
        na2, nb2, nc2 = a2*m2, b2*m2, c2*m2

        print(f"  Eq.1 × {m1}:  {na1}x + {nb1}y = {nc1}")
        print(f"  Eq.2 × {m2}:  {na2}x + {nb2}y = {nc2}")

        print(f"\n--- Step 2: Eliminate y ---")
        if nb1 == -nb2:
            new_a = na1 + na2
            new_c = nc1 + nc2
            print(f"  Adding the two equations:")
        else:
            new_a = na1 - na2
            new_c = nc1 - nc2
            print(f"  Subtracting the two equations:")

        print(f"  {new_a}x = {new_c}")

        if new_a == 0:
            if new_c == 0:
                print(f"\n  0 = 0 — infinite solutions.")
                return None, None
            else:
                print(f"\n  {new_c} = 0 — no solution.")
                return None, None

        x = new_c / new_a
        print(f"  x = {new_c} / {new_a} = {x:.4f}")

        print(f"\n--- Step 3: Substitute x back ---")
        print(f"  Plug x = {x:.4f} into original equation 1:")
        print(f"  {a1}·({x:.4f}) + {b1}y = {c1}")
        y = (c1 - a1 * x) / b1
        print(f"  {b1}y = {c1 - a1*x:.4f}")
        print(f"  y = {y:.4f}")

    return x, y


def plot_system(a1, b1, c1, a2, b2, c2, x_sol, y_sol):
    x_vals = np.linspace(x_sol - 5, x_sol + 5, 400)
    y1 = (c1 - a1*x_vals) / b1
    y2 = (c2 - a2*x_vals) / b2

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y1, color="crimson",   linewidth=2, label=f"{a1}x + {b1}y = {c1}")
    ax.plot(x_vals, y2, color="steelblue", linewidth=2, label=f"{a2}x + {b2}y = {c2}")
    ax.plot(x_sol, y_sol, "o", color="green", markersize=10,
            label=f"Solution ({x_sol:.2f}, {y_sol:.2f})")
    ax.annotate(f"({x_sol:.2f}, {y_sol:.2f})", (x_sol, y_sol),
                textcoords="offset points", xytext=(10, 10), fontsize=10)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title("System of Equations", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def solve_system(a1, b1, c1, a2, b2, c2):
    print(f"\n{'='*50}")
    print(f"SYSTEM OF EQUATIONS SOLVER")
    print(f"{'='*50}")
    print(f"")
    print(f"  {a1}x + {b1}y = {c1}")
    print(f"  {a2}x + {b2}y = {c2}")
    print(f"")
    print(f"  We have two equations and two unknowns.")
    print(f"  Our job: find x and y that satisfy BOTH at once.")
    print(f"  The solution is the point where the two lines cross.")
    print(f"")

    method = choose_method(a1, b1, a2, b2)

    print(f"--- Choosing the best method ---")
    if method == "substitution":
        print(f"  A coefficient is 1 or -1 — substitution is cleanest.")
        x, y = solve_substitution(a1, b1, c1, a2, b2, c2)
    else:
        print(f"  Elimination will cancel a variable directly.")
        x, y = solve_elimination(a1, b1, c1, a2, b2, c2)

    if x is None:
        return

    print(f"\n--- Verify the solution ---")
    print(f"  Never skip this. Plug x = {x:.4f} and y = {y:.4f}")
    print(f"  back into both original equations.")
    print(f"")
    check1 = a1*x + b1*y
    check2 = a2*x + b2*y
    print(f"  Eq.1: {a1}·({x:.4f}) + {b1}·({y:.4f}) = {check1:.6f}  (expected {c1}) ✓")
    print(f"  Eq.2: {a2}·({x:.4f}) + {b2}·({y:.4f}) = {check2:.6f}  (expected {c2}) ✓")
    print(f"")
    print(f"  Solution: x = {x:.4f},  y = {y:.4f}")

    print(f"\n--- A note on other methods ---")
    print(f"  What we just did is how any mathematician would approach")
    print(f"  this by hand — pick the path of least resistance.")
    print(f"  For larger systems (3, 4, 10 variables) doing this")
    print(f"  manually becomes impossible. That's when matrix methods")
    print(f"  like Gaussian elimination or Cramer's rule take over —")
    print(f"  they're systematic and work for any size.")

    plot_system(a1, b1, c1, a2, b2, c2, x, y)


if __name__ == "__main__":
    print("=== System of Equations Solver ===")
    print("Enter the coefficients of the system:\n")
    a1 = float(input("Enter a1: "))
    b1 = float(input("Enter b1: "))
    c1 = float(input("Enter c1: "))
    a2 = float(input("Enter a2: "))
    b2 = float(input("Enter b2: "))
    c2 = float(input("Enter c2: "))
    solve_system(a1, b1, c1, a2, b2, c2)
    