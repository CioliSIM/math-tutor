import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

x = sp.Symbol('x')


def compute_logarithm():
    print(f"\n{'='*50}")
    print(f"COMPUTE A LOGARITHM")
    print(f"{'='*50}")
    print(f"")
    print(f"  We want to find log_b(x) — the exponent y such that b^y = x.")
    print(f"  Before we compute, let's make sure the inputs are valid.")
    print(f"")

    b     = float(input("  Base b (e.g. 10, 2, or 2.718 for e): "))
    x_val = float(input("  Argument x: "))

    print(f"\n--- Step 1: Check the inputs ---")
    print(f"  Two rules for logarithms to exist:")
    print(f"  · The base must be positive and not equal to 1")
    print(f"    (b=1 would mean 1^y=x, but 1^y=1 always — useless)")
    print(f"  · The argument must be strictly positive")
    print(f"    (no real exponent gives b^y ≤ 0 for b>0)")
    print(f"")

    if b <= 0 or b == 1:
        print(f"  Base b = {b} is not valid.")
        print(f"  Choose a positive number different from 1.")
        return
    if x_val <= 0:
        print(f"  Argument x = {x_val} is not valid.")
        print(f"  Logarithms are only defined for positive numbers.")
        print(f"  Think about it: what power of {b} gives {x_val}? None.")
        return

    print(f"  b = {b} ✓")
    print(f"  x = {x_val} ✓")

    print(f"\n--- Step 2: Compute log_{b}({x_val}) ---")
    print(f"  We use the change of base formula:")
    print(f"  log_b(x) = ln(x) / ln(b)")
    print(f"  This works because every logarithm can be expressed")
    print(f"  in terms of the natural logarithm.")
    print(f"")

    result = math.log(x_val) / math.log(b)

    print(f"  ln({x_val}) = {math.log(x_val):.6f}")
    print(f"  ln({b})     = {math.log(b):.6f}")
    print(f"")
    print(f"  log_{b}({x_val}) = {math.log(x_val):.6f} / {math.log(b):.6f}")
    print(f"               = {result:.6f}")

    print(f"\n--- Step 3: Verify ---")
    print(f"  If log_{b}({x_val}) = {result:.6f},")
    print(f"  then {b}^{result:.6f} should give back {x_val}.")
    check = b**result
    print(f"  {b}^{result:.6f} = {check:.8f}  ✓")

    print(f"\n--- Step 4: What does the result tell us? ---")
    if result > 0:
        print(f"  result = {result:.4f} > 0")
        print(f"  This means {x_val} > 1.")
        print(f"  Makes sense: you need a positive exponent to get above 1.")
    elif result < 0:
        print(f"  result = {result:.4f} < 0")
        print(f"  This means {x_val} is between 0 and 1.")
        print(f"  A negative exponent gives a fraction.")
    else:
        print(f"  result = 0 → x = 1.")
        print(f"  b^0 = 1 for any base — always.")


def logarithm_properties():
    print(f"\n{'='*50}")
    print(f"PROPERTIES OF LOGARITHMS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Three properties — that's all you need.")
    print(f"  Every logarithm manipulation in existence comes back")
    print(f"  to one of these three. Learn them deeply, not by heart.")
    print(f"")

    print(f"--- Property 1: Product rule ---")
    print(f"  log_b(a · c) = log_b(a) + log_b(c)")
    print(f"")
    print(f"  Where does it come from?")
    print(f"  Exponents add when you multiply: b^m · b^n = b^(m+n)")
    print(f"  So if a = b^m and c = b^n, then a·c = b^(m+n)")
    print(f"  → log_b(a·c) = m+n = log_b(a) + log_b(c)")
    print(f"")
    print(f"  In plain terms: the log of a product is the sum of the logs.")
    print(f"  This is exactly why logarithms were invented —")
    print(f"  multiplication becomes addition, which is much easier.")
    print(f"")
    val  = math.log10(6)
    val2 = math.log10(2) + math.log10(3)
    print(f"  Example: log(6) = log(2·3) = log(2) + log(3)")
    print(f"  log(6)          = {val:.6f}")
    print(f"  log(2) + log(3) = {val2:.6f}  ✓")

    print(f"\n--- Property 2: Quotient rule ---")
    print(f"  log_b(a / c) = log_b(a) - log_b(c)")
    print(f"")
    print(f"  Same logic: exponents subtract when you divide.")
    print(f"  b^m / b^n = b^(m-n)")
    print(f"  → log_b(a/c) = m-n = log_b(a) - log_b(c)")
    print(f"")
    val  = math.log10(5)
    val2 = math.log10(10) - math.log10(2)
    print(f"  Example: log(5) = log(10/2) = log(10) - log(2)")
    print(f"  log(5)          = {val:.6f}")
    print(f"  log(10)-log(2)  = {val2:.6f}  ✓")

    print(f"\n--- Property 3: Power rule ---")
    print(f"  log_b(a^n) = n · log_b(a)")
    print(f"")
    print(f"  This is the most powerful one.")
    print(f"  It drags the exponent out of the log and turns it")
    print(f"  into a simple multiplier — suddenly solvable.")
    print(f"  a^n = (b^m)^n = b^(m·n) → log_b(a^n) = m·n = n·log_b(a)")
    print(f"")
    val  = math.log10(8)
    val2 = 3 * math.log10(2)
    print(f"  Example: log(8) = log(2³) = 3·log(2)")
    print(f"  log(8)    = {val:.6f}")
    print(f"  3·log(2)  = {val2:.6f}  ✓")

    print(f"\n--- Special values to know by heart ---")
    print(f"  log_b(1)   = 0    always  — because b^0 = 1")
    print(f"  log_b(b)   = 1    always  — because b^1 = b")
    print(f"  log_b(b^n) = n    always  — direct consequence")
    print(f"  ln(e)      = 1    because e^1 = e")
    print(f"  ln(1)      = 0    because e^0 = 1")
    print(f"  log(10)    = 1    because 10^1 = 10")
    print(f"  log(1)     = 0    because 10^0 = 1")

    print(f"\n--- Verify with your own numbers ---")
    a = float(input("  Enter a: "))
    c = float(input("  Enter c: "))
    b = float(input("  Enter base b: "))

    if a <= 0 or c <= 0 or b <= 0 or b == 1:
        print(f"  Invalid inputs — all values must be positive, b ≠ 1.")
        return

    log_a   = math.log(a)   / math.log(b)
    log_c   = math.log(c)   / math.log(b)
    log_ac  = math.log(a*c) / math.log(b)
    log_div = math.log(a/c) / math.log(b)
    log_pow = math.log(a**3) / math.log(b)

    print(f"")
    print(f"  log_{b}({a}) = {log_a:.6f}")
    print(f"  log_{b}({c}) = {log_c:.6f}")
    print(f"")
    print(f"  Product:   log_{b}({a}·{c}) = log_{b}({a*c})")
    print(f"             = {log_ac:.6f}")
    print(f"             log_{b}({a}) + log_{b}({c}) = {log_a+log_c:.6f}  ✓")
    print(f"")
    print(f"  Quotient:  log_{b}({a}/{c}) = log_{b}({a/c:.4f})")
    print(f"             = {log_div:.6f}")
    print(f"             log_{b}({a}) - log_{b}({c}) = {log_a-log_c:.6f}  ✓")
    print(f"")
    print(f"  Power:     log_{b}({a}³) = log_{b}({a**3})")
    print(f"             = {log_pow:.6f}")
    print(f"             3·log_{b}({a}) = {3*log_a:.6f}  ✓")


def change_of_base():
    print(f"\n{'='*50}")
    print(f"CHANGE OF BASE FORMULA")
    print(f"{'='*50}")
    print(f"")
    print(f"  Your calculator has log (base 10) and ln (base e).")
    print(f"  But what about log_2(x) or log_7(x)?")
    print(f"  The change of base formula lets you compute any")
    print(f"  logarithm using whichever base you have available.")
    print(f"")
    print(f"      log_b(x) = ln(x) / ln(b) = log(x) / log(b)")
    print(f"")
    print(f"  The proof is clean:")
    print(f"  Let y = log_b(x), so b^y = x.")
    print(f"  Take ln of both sides: ln(b^y) = ln(x)")
    print(f"  Power rule:            y·ln(b) = ln(x)")
    print(f"  Solve for y:           y = ln(x)/ln(b)  ✓")
    print(f"")
    print(f"  The key point: any base works in the denominator,")
    print(f"  as long as you use the same base top and bottom.")
    print(f"")

    x_val = float(input("  Argument x: "))
    b     = float(input("  Base b: "))

    if x_val <= 0 or b <= 0 or b == 1:
        print(f"  Invalid inputs.")
        return

    result = math.log(x_val) / math.log(b)

    print(f"\n  log_{b}({x_val})")
    print(f"  = ln({x_val}) / ln({b})")
    print(f"  = {math.log(x_val):.6f} / {math.log(b):.6f}")
    print(f"  = {result:.6f}")
    print(f"")
    print(f"  Same result using base 10:")
    result2 = math.log10(x_val) / math.log10(b)
    print(f"  = log({x_val}) / log({b})")
    print(f"  = {math.log10(x_val):.6f} / {math.log10(b):.6f}")
    print(f"  = {result2:.6f}  ✓")
    print(f"")
    print(f"  Both give the same answer — the base in the denominator")
    print(f"  doesn't matter. Beautiful consistency.")


def logarithmic_equations():
    print(f"\n{'='*50}")
    print(f"LOGARITHMIC EQUATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A logarithmic equation has the unknown inside a log.")
    print(f"  The plan is always the same:")
    print(f"  isolate the log, then exponentiate to undo it.")
    print(f"")
    print(f"  The key moves:")
    print(f"  · log_b(A) = k   →   A = b^k   (exponentiate both sides)")
    print(f"  · log_b(A) = log_b(B)   →   A = B   (same log, same argument)")
    print(f"")
    print(f"  One rule you can never forget:")
    print(f"  ALWAYS check your solutions at the end.")
    print(f"  The argument of a log must be strictly positive.")
    print(f"  Algebra can produce solutions that look valid but aren't.")
    print(f"  These are called extraneous solutions — discard them.")
    print(f"")
    print(f"  Enter an equation of the form: log_b(expression) = k")
    print(f"")

    b        = float(input("  Base b: "))
    expr_str = input("  Expression inside log (e.g. 2*x+1): ")
    k        = float(input("  Right-hand side k: "))

    expr  = sp.sympify(expr_str)
    x_sym = sp.Symbol('x')

    print(f"\n--- Step 1: Write the equation ---")
    print(f"  log_{b}({expr}) = {k}")

    print(f"\n--- Step 2: Exponentiate both sides ---")
    print(f"  b^(log_b(expr)) = b^k  →  the log disappears")
    print(f"  {expr} = {b}^{k} = {b**k:.6f}")

    print(f"\n--- Step 3: Solve the resulting equation ---")
    rhs       = sp.Rational(b**k).limit_denominator(10000)
    solutions = sp.solve(expr - rhs, x_sym)

    if not solutions:
        print(f"  No solution found.")
        return

    print(f"  {expr} = {b**k:.6f}")
    print(f"  Raw solutions from algebra: {solutions}")

    print(f"\n--- Step 4: Check validity ---")
    print(f"  For each solution, we substitute back and check")
    print(f"  that the argument of the log is positive.")
    print(f"")

    valid = []
    for sol in solutions:
        val = float(expr.subs(x_sym, sol))
        if val > 0:
            print(f"  x = {sol}:")
            print(f"    argument = {val:.6f} > 0 ✓  — valid solution")
            print(f"    check: log_{b}({val:.6f}) = {math.log(val)/math.log(b):.6f}"
                  f"  (expected {k})")
            valid.append(sol)
        else:
            print(f"  x = {sol}:")
            print(f"    argument = {val:.6f} ≤ 0 ✗  — extraneous, rejected")

    print(f"")
    if valid:
        print(f"  Final answer: x = {valid}")
    else:
        print(f"  No valid solutions — all were extraneous.")
        print(f"  This equation has no solution in the real numbers.")


def plot_logarithms():
    print(f"\n{'='*50}")
    print(f"GRAPHS OF LOGARITHMIC FUNCTIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  The graph of y = log_b(x) has a shape that encodes")
    print(f"  everything we know about logarithms:")
    print(f"")
    print(f"  · Domain: x > 0 only  — no log of zero or negatives")
    print(f"  · Always passes through (1, 0)  — log_b(1) = 0 always")
    print(f"  · Always passes through (b, 1)  — log_b(b) = 1 always")
    print(f"  · Grows forever, but incredibly slowly")
    print(f"    (log grows slower than any root, which grows slower")
    print(f"     than any polynomial)")
    print(f"")
    print(f"  · b > 1   → increasing curve  (the usual case)")
    print(f"  · 0<b<1  → decreasing curve  (mirror about x-axis)")
    print(f"")
    print(f"  The logarithm and the exponential are exact mirror")
    print(f"  images across the line y = x — that's what inverse")
    print(f"  functions look like geometrically. One undoes the other.")
    print(f"")

    x_vals = np.linspace(0.01, 10, 1000)

    bases  = [math.e, 10, 2, 0.5]
    colors = ["crimson", "steelblue", "green", "orange"]
    labels = ["ln(x) — base e ≈ 2.718",
              "log(x) — base 10",
              "log₂(x) — base 2",
              "log₀.₅(x) — decaying base"]

    fig, ax = plt.subplots(figsize=(9, 6))

    for b, col, lab in zip(bases, colors, labels):
        y_vals = np.log(x_vals) / np.log(b)
        ax.plot(x_vals, y_vals, color=col, linewidth=2, label=lab)

    ax.plot([0, 10], [0, 10], color="gray", linewidth=1,
            linestyle="--", alpha=0.5, label="y = x (mirror line)")

    x_exp = np.linspace(-2, math.log(10), 400)
    ax.plot(np.exp(x_exp), x_exp, color="crimson", linewidth=1.5,
            linestyle=":", alpha=0.7, label="eˣ — mirror of ln(x)")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.axhline(1, color="gray", linewidth=0.5, linestyle="--", alpha=0.4)
    ax.axvline(1, color="gray", linewidth=0.5, linestyle="--", alpha=0.4)

    ax.plot(1, 0, "o", color="black", markersize=8)
    ax.annotate("  (1, 0) — all logs pass here", (1, 0), fontsize=9)

    ax.set_xlim(-1, 10)
    ax.set_ylim(-4, 4)
    ax.set_title("Logarithmic functions — different bases", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("log_b(x)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def explain_logarithms():
    print(f"\n{'='*50}")
    print(f"LOGARITHMS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A logarithm answers one question:")
    print(f"  'To what power must I raise b to get x?'")
    print(f"")
    print(f"      log_b(x) = y   means exactly   b^y = x")
    print(f"")
    print(f"  So log_2(8) = 3 because 2³ = 8.")
    print(f"  And log_10(1000) = 3 because 10³ = 1000.")
    print(f"  The logarithm IS the exponent — nothing more.")
    print(f"")
    print(f"  Logarithm and exponential are inverse functions.")
    print(f"  One perfectly undoes the other:")
    print(f"  b^(log_b(x)) = x   and   log_b(b^x) = x")
    print(f"")
    print(f"  The three bases you'll meet most often:")
    print(f"  · base 10  → log(x)    the common logarithm")
    print(f"                          used in pH, decibels, Richter scale")
    print(f"  · base e   → ln(x)     the natural logarithm")
    print(f"                          essential in calculus and physics")
    print(f"  · base 2   → log₂(x)   the binary logarithm")
    print(f"                          used in computer science and information theory")
    print(f"")
    print(f"  Historical note: logarithms were invented in 1614")
    print(f"  by John Napier to help astronomers multiply huge numbers.")
    print(f"  log(a·b) = log(a) + log(b) turned multiplication into")
    print(f"  addition — a massive computational shortcut before calculators.")
    print(f"  For 300 years, logarithm tables were the most important")
    print(f"  tool in science and engineering.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Compute a logarithm")
    print(f"  2 — Properties  (product, quotient, power rule)")
    print(f"  3 — Change of base formula")
    print(f"  4 — Logarithmic equations")
    print(f"  5 — Graphs")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        compute_logarithm()
    elif choice == "2":
        logarithm_properties()
    elif choice == "3":
        change_of_base()
    elif choice == "4":
        logarithmic_equations()
    elif choice == "5":
        plot_logarithms()
    else:
        print(f"  Invalid choice.")


def compute_exponential():
    print(f"\n{'='*50}")
    print(f"COMPUTE b^x")
    print(f"{'='*50}")
    print(f"")
    b   = float(input("  Base b: "))
    exp = float(input("  Exponent x: "))

    if b <= 0:
        print(f"  Base must be positive.")
        return

    result = b**exp

    print(f"\n  Computing {b}^{exp}:")
    print(f"")

    if exp == int(exp) and abs(exp) < 10:
        print(f"--- Direct computation ---")
        if exp > 0:
            print(f"  {b}^{int(exp)} means multiplying {b} by itself {int(exp)} times.")
            print(f"  = {result:.6f}")
        elif exp < 0:
            print(f"  A negative exponent means: 1 / b^|exp|")
            print(f"  {b}^{int(exp)} = 1 / {b}^{int(-exp)} = 1 / {b**(-exp):.6f}")
            print(f"  = {result:.6f}")
        else:
            print(f"  Any non-zero number to the power 0 equals 1.")
            print(f"  {b}^0 = 1")
    else:
        print(f"--- Using the natural exponential ---")
        print(f"  For non-integer exponents, we use: b^x = e^(x·ln(b))")
        print(f"  = e^({exp}·{math.log(b):.6f})")
        print(f"  = e^{exp*math.log(b):.6f}")
        print(f"  = {result:.6f}")

    print(f"")
    print(f"  Result: {b}^{exp} = {result:.6f}")


def exponential_equations():
    print(f"\n{'='*50}")
    print(f"EXPONENTIAL EQUATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  An exponential equation has the unknown in the exponent.")
    print(f"  You can't isolate x by normal algebra — the exponent")
    print(f"  is out of reach. The solution: take the log of both sides.")
    print(f"")
    print(f"  log(b^x) = x·log(b)  — the power rule brings x down.")
    print(f"  Once x is no longer in an exponent, it's just algebra.")
    print(f"")
    print(f"  Enter an equation of the form: b^(expression) = k")
    print(f"")

    b        = float(input("  Base b: "))
    expr_str = input("  Exponent (in terms of x, e.g. 2*x+1): ")
    k        = float(input("  Right-hand side k: "))

    if b <= 0 or b == 1:
        print(f"  Invalid base.")
        return
    if k <= 0:
        print(f"  k must be positive.")
        print(f"  Exponentials are always positive — b^x > 0 for any x.")
        print(f"  So b^(something) = k has no solution if k ≤ 0.")
        return

    expr  = sp.sympify(expr_str)
    x_sym = sp.Symbol('x')

    print(f"\n--- Step 1: Write the equation ---")
    print(f"  {b}^({expr}) = {k}")

    print(f"\n--- Step 2: Take log_{b} of both sides ---")
    print(f"  log_{b}({b}^({expr})) = log_{b}({k})")
    print(f"  The left side simplifies: log_{b}(b^y) = y always.")
    rhs = math.log(k) / math.log(b)
    print(f"  {expr} = log_{b}({k}) = {rhs:.6f}")

    print(f"\n--- Step 3: Solve for x ---")
    solutions = sp.solve(expr - rhs, x_sym)

    if not solutions:
        print(f"  No solution found.")
        return

    print(f"  {expr} = {rhs:.6f}")
    print(f"  x = {solutions}")

    print(f"\n--- Step 4: Verify ---")
    for sol in solutions:
        exp_val = float(expr.subs(x_sym, sol))
        check   = b**exp_val
        print(f"  x = {sol}:")
        print(f"  exponent = {exp_val:.4f}")
        print(f"  {b}^{exp_val:.4f} = {check:.6f}  (expected {k}) "
              f"{'✓' if abs(check-k) < 1e-6 else '✗'}")


def plot_exponentials():
    print(f"\n{'='*50}")
    print(f"GRAPHS OF EXPONENTIAL FUNCTIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Every exponential f(x) = b^x shares these properties:")
    print(f"  · always passes through (0, 1)  — because b^0 = 1")
    print(f"  · always positive  — b^x > 0 for all real x")
    print(f"  · one side approaches 0 (asymptote), the other explodes")
    print(f"  · grows faster than any polynomial — eventually")
    print(f"    2^x overtakes x^1000. Always. That's exponential growth.")
    print(f"")
    print(f"  The natural exponential e^x is uniquely special:")
    print(f"  it is the only function that equals its own derivative.")
    print(f"  d/dx(e^x) = e^x — it doesn't change under differentiation.")
    print(f"  This is why e appears in every corner of physics and math.")
    print(f"")

    x_vals = np.linspace(-3, 3, 400)
    bases  = [math.e, 2, 3, 0.5]
    colors = ["crimson", "steelblue", "green", "orange"]
    labels = ["eˣ  (base e ≈ 2.718 — the natural exponential)",
              "2ˣ",
              "3ˣ",
              "(0.5)ˣ — exponential decay"]

    fig, ax = plt.subplots(figsize=(9, 6))
    for b, col, lab in zip(bases, colors, labels):
        ax.plot(x_vals, b**x_vals, color=col, linewidth=2, label=lab)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axhline(1, color="gray",  linewidth=0.5, linestyle="--", alpha=0.5)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.plot(0, 1, "o", color="black", markersize=8)
    ax.annotate("  (0,1) — all exponentials pass here", (0, 1), fontsize=9)

    ax.set_ylim(-0.5, 10)
    ax.set_title("Exponential functions — different bases", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("b^x")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def growth_decay_model():
    print(f"\n{'='*50}")
    print(f"EXPONENTIAL GROWTH AND DECAY")
    print(f"{'='*50}")
    print(f"")
    print(f"  This is where exponentials meet the real world.")
    print(f"  The rule: whenever a quantity grows or shrinks")
    print(f"  proportionally to its current size, the result")
    print(f"  is always exponential.")
    print(f"")
    print(f"  The model:   A(t) = A₀ · e^(k·t)")
    print(f"")
    print(f"  A₀ = starting amount")
    print(f"  k  = rate constant  (k > 0 → growth, k < 0 → decay)")
    print(f"  t  = time")
    print(f"  A(t) = amount at time t")
    print(f"")
    print(f"  Where you see this in real life:")
    print(f"  · Compound interest  — money grows proportionally")
    print(f"  · Radioactive decay  — atoms decay proportionally")
    print(f"  · Bacterial growth   — more bacteria → more reproduction")
    print(f"  · Newton's cooling   — temperature difference decays proportionally")
    print(f"  · Viral spread       — more infected → more transmission")
    print(f"")

    A0    = float(input("  Initial amount A₀: "))
    k     = float(input("  Rate k (negative for decay): "))
    t_end = float(input("  Time span to model (e.g. 10): "))

    print(f"\n--- The model: A(t) = {A0} · e^({k}·t) ---")
    print(f"")

    print(f"--- Values at key moments ---")
    for t in [0, t_end/4, t_end/2, 3*t_end/4, t_end]:
        val = A0 * math.exp(k * t)
        print(f"  A({t:6.2f}) = {A0} · e^({k}·{t:.2f}) = {val:.4f}")

    print(f"")
    if k > 0:
        doubling = math.log(2) / k
        print(f"--- Doubling time ---")
        print(f"  How long until the amount doubles?")
        print(f"  Solve: 2·A₀ = A₀·e^(k·t)  →  2 = e^(k·t)")
        print(f"  → t = ln(2)/k = {math.log(2):.4f}/{k} = {doubling:.4f}")
        print(f"  Every {doubling:.4f} units of time, the amount doubles.")
    elif k < 0:
        half_life = math.log(2) / (-k)
        print(f"--- Half-life ---")
        print(f"  How long until the amount halves?")
        print(f"  Solve: A₀/2 = A₀·e^(k·t)  →  1/2 = e^(k·t)")
        print(f"  → t = ln(2)/|k| = {math.log(2):.4f}/{-k} = {half_life:.4f}")
        print(f"  Every {half_life:.4f} units of time, the amount halves.")

    t_vals = np.linspace(0, t_end, 400)
    A_vals = A0 * np.exp(k * t_vals)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t_vals, A_vals, color="crimson", linewidth=2,
            label=f"A(t) = {A0}·e^({k}t)")
    ax.axhline(A0, color="gray", linewidth=1, linestyle="--",
               alpha=0.6, label=f"A₀ = {A0}")
    ax.plot(0, A0, "o", color="steelblue", markersize=10)
    ax.annotate(f"  A₀ = {A0}", (0, A0), fontsize=10)

    if k > 0:
        doubling = math.log(2) / k
        if doubling <= t_end:
            ax.axvline(doubling, color="green", linewidth=1.5,
                       linestyle="--",
                       label=f"Doubling time = {doubling:.2f}")
    elif k < 0:
        half_life = math.log(2) / (-k)
        if half_life <= t_end:
            ax.axvline(half_life, color="green", linewidth=1.5,
                       linestyle="--",
                       label=f"Half-life = {half_life:.2f}")

    ax.set_title(f"{'Exponential growth' if k>0 else 'Exponential decay'}: "
                 f"A(t) = {A0}·e^({k}t)", fontsize=13)
    ax.set_xlabel("t (time)")
    ax.set_ylabel("A(t)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def explain_exponentials():
    print(f"\n{'='*50}")
    print(f"EXPONENTIAL FUNCTIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  An exponential function puts the variable in the exponent:")
    print(f"      f(x) = b^x")
    print(f"")
    print(f"  Don't confuse it with a power function like x² —")
    print(f"  there the variable is the base, not the exponent.")
    print(f"  The difference in behavior is enormous.")
    print(f"")
    print(f"  The behavior depends entirely on b:")
    print(f"  · b > 1    → exponential growth — faster than any polynomial")
    print(f"  · 0 < b < 1 → exponential decay  — toward zero, never reaching it")
    print(f"  · b = 1    → constant 1 — boring but valid")
    print(f"  · b = e    → the natural exponential — special in every way")
    print(f"")
    print(f"  Why is exponential growth so dramatic?")
    print(f"  Doubling. Start with 1. Double 30 times: 2^30 = 1,073,741,824.")
    print(f"  That's a billion from 30 doublings. That's exponential.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Compute b^x")
    print(f"  2 — Exponential equations")
    print(f"  3 — Graphs of exponential functions")
    print(f"  4 — Growth and decay models")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        compute_exponential()
    elif choice == "2":
        exponential_equations()
    elif choice == "3":
        plot_exponentials()
    elif choice == "4":
        growth_decay_model()
    else:
        print(f"  Invalid choice.")


def logs_and_exponentials():
    print(f"\n{'='*50}")
    print(f"LOGARITHMS AND EXPONENTIALS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Two functions. One relationship.")
    print(f"")
    print(f"  The exponential b^x and the logarithm log_b(x)")
    print(f"  are inverse functions — mirror images across y = x.")
    print(f"  Understanding one deeply means understanding the other.")
    print(f"")
    print(f"  Together they appear everywhere you need to describe")
    print(f"  something that grows, shrinks, compounds, or scales:")
    print(f"  · Earthquake magnitude  — Richter scale is logarithmic")
    print(f"  · Sound intensity       — decibels are logarithmic")
    print(f"  · Acidity               — pH is a logarithm")
    print(f"  · Compound interest     — exponential growth")
    print(f"  · Radioactive decay     — exponential decay")
    print(f"  · Information theory    — entropy uses log base 2")
    print(f"")
    print(f"  The reason logarithms compress huge ranges:")
    print(f"  the difference between a magnitude 5 and magnitude 8")
    print(f"  earthquake is not 3 — it's 10³ = 1000 times the energy.")
    print(f"  Logarithms make such ranges human-readable.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Logarithms")
    print(f"  2 — Exponentials")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    if choice == "1":
        explain_logarithms()
    elif choice == "2":
        explain_exponentials()
    else:
        print(f"  Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    logs_and_exponentials()
    