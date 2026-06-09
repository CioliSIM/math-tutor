import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

x = sp.Symbol('x')


def plot_limit(expr, a):
    f_numeric = sp.lambdify(x, expr, 'numpy')

    try:
        a_float = float(a)
        x_vals  = np.linspace(a_float - 4, a_float + 4, 1000)
    except Exception:
        x_vals  = np.linspace(-10, 10, 1000)
        a_float = None

    with np.errstate(divide='ignore', invalid='ignore'):
        y_vals = f_numeric(x_vals)
        y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y_vals, color="crimson", linewidth=2,
            label=f"f(x) = {expr}")

    if a_float is not None:
        try:
            lim_val = float(sp.limit(expr, x, a))
            ax.plot(a_float, lim_val, "o", color="steelblue",
                    markersize=10, markerfacecolor="white",
                    markeredgecolor="steelblue", markeredgewidth=2,
                    label=f"lim(x→{a}) = {lim_val:.4f}")
            ax.axvline(a_float, color="gray", linewidth=0.8,
                       linestyle="--", alpha=0.6)
        except Exception:
            pass

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_ylim(-10, 10)
    ax.set_title(f"lim(x→{a})  f(x) = {expr}", fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def limit_at_point():
    print(f"\n{'='*50}")
    print(f"LIMIT AT A POINT")
    print(f"{'='*50}")
    print(f"")
    print(f"  We want to answer this question:")
    print(f"  as x gets closer and closer to a specific value a,")
    print(f"  what does f(x) approach?")
    print(f"")
    print(f"  The key insight: it doesn't matter what happens")
    print(f"  exactly AT x = a. The limit is about the journey,")
    print(f"  not the destination. f(a) might not even exist —")
    print(f"  and the limit can still be perfectly well-defined.")
    print(f"")

    expr_str = input("  Enter f(x): ")
    a_str    = input("  Enter the point a (or 'oo' for +∞, '-oo' for -∞): ")

    expr = sp.sympify(expr_str)
    a    = sp.sympify(a_str)

    print(f"\n--- Step 1: What are we working with? ---")
    print(f"  f(x) = {expr}")
    print(f"  We're watching what happens as x → {a}.")
    print(f"")

    print(f"--- Step 2: Try the simplest approach first ---")
    print(f"  The easiest thing to try is direct substitution:")
    print(f"  just plug x = {a} into f(x) and see what comes out.")
    print(f"  If the result is a normal finite number, we're done.")
    print(f"  If we get something like 0/0 or ∞/∞, we need more work.")
    print(f"")

    try:
        direct = expr.subs(x, a)
        direct_simplified = sp.simplify(direct)
        print(f"  f({a}) = {direct_simplified}")
        print(f"")

        if direct_simplified == sp.nan or not direct_simplified.is_finite:
            print(f"  We got an indeterminate form — direct substitution")
            print(f"  doesn't work here. This is actually the interesting case.")
            print(f"  It means the function has some kind of tension at x = {a}")
            print(f"  that we need to resolve algebraically.")
            indeterminate = True
        else:
            print(f"  Direct substitution works — the result is finite.")
            print(f"  No tricks needed.")
            indeterminate = False
    except Exception:
        print(f"  Direct substitution failed — indeterminate form.")
        indeterminate = True

    print(f"\n--- Step 3: Compute the limit ---")

    if indeterminate:
        print(f"  Since direct substitution failed, we hand this")
        print(f"  to sympy, which knows techniques like:")
        print(f"  · Factoring and canceling common terms")
        print(f"  · L'Hôpital's rule (differentiate top and bottom)")
        print(f"  · Known limit identities like sin(x)/x → 1")
        print(f"")

    try:
        limite = sp.limit(expr, x, a)
        print(f"  lim(x→{a}) {expr} = {limite}")
        print(f"")

        if limite == sp.oo:
            print(f"  The limit is +∞.")
            print(f"  As x gets close to {a}, the function shoots upward")
            print(f"  without any ceiling. This is a vertical asymptote.")
        elif limite == -sp.oo:
            print(f"  The limit is -∞.")
            print(f"  As x gets close to {a}, the function drops with no floor.")
            print(f"  Vertical asymptote at x = {a}.")
        else:
            print(f"  The limit exists and equals {limite}.")
            if indeterminate:
                print(f"  Even though plugging in {a} directly broke things,")
                print(f"  the function approaches {limite} smoothly from both sides.")
                print(f"  The indeterminate form was resolvable.")

    except Exception:
        print(f"  Could not compute the limit automatically.")
        print(f"  Try simplifying the expression by hand first.")

    print(f"\n--- Step 4: Is the function continuous at x = {a}? ---")
    print(f"  Continuity means the function has no breaks, jumps,")
    print(f"  or holes at this point. For that, three things must hold:")
    print(f"  1. f({a}) must exist (the function is defined there)")
    print(f"  2. lim(x→{a}) f(x) must exist")
    print(f"  3. They must be equal")
    print(f"  If any of these fail, there's a discontinuity.")
    print(f"")

    try:
        val_at_a = sp.simplify(expr.subs(x, a))
        lim_val  = sp.limit(expr, x, a)

        if not val_at_a.is_finite:
            print(f"  f({a}) doesn't exist — condition 1 fails.")
            print(f"  Not continuous at x = {a}.")
        elif val_at_a == lim_val:
            print(f"  f({a}) = {val_at_a}  and  lim = {lim_val}")
            print(f"  All three conditions hold ✓")
            print(f"  f is continuous at x = {a} — no break, no hole.")
        else:
            print(f"  f({a}) = {val_at_a}  but  lim = {lim_val}")
            print(f"  The limit exists, but it doesn't match f({a}).")
            print(f"  This is a removable discontinuity — a single")
            print(f"  misplaced point. You could 'fix' it by redefining")
            print(f"  f({a}) = {lim_val}.")
    except Exception:
        print(f"  Could not check continuity automatically.")

    plot_limit(expr, a)


def limit_at_infinity():
    print(f"\n{'='*50}")
    print(f"LIMIT AT INFINITY")
    print(f"{'='*50}")
    print(f"")
    print(f"  Instead of zooming in on a single point,")
    print(f"  we zoom out — all the way to infinity.")
    print(f"  We ask: as x grows without bound,")
    print(f"  does f(x) settle toward some fixed value?")
    print(f"  Or does it keep growing, shrinking, or oscillating?")
    print(f"")
    print(f"  If it settles, that value is a horizontal asymptote —")
    print(f"  a line the graph approaches but never quite reaches.")
    print(f"")

    expr_str = input("  Enter f(x): ")
    expr = sp.sympify(expr_str)

    print(f"\n  f(x) = {expr}")
    print(f"")

    print(f"--- Step 1: The intuition ---")
    print(f"  For large x, the highest-degree term dominates.")
    print(f"  Lower-degree terms and constants become negligible —")
    print(f"  they're a drop in the ocean compared to x^n.")
    print(f"  This is the key to understanding limits at infinity.")
    print(f"")

    print(f"--- Step 2: lim(x→+∞) ---")
    print(f"  x runs off to the right forever.")
    print(f"")
    try:
        lim_pos = sp.limit(expr, x, sp.oo)
        print(f"  lim(x→+∞) {expr} = {lim_pos}")
        print(f"")
        if lim_pos == sp.oo:
            print(f"  The function grows without bound.")
            print(f"  No horizontal asymptote on the right.")
        elif lim_pos == -sp.oo:
            print(f"  The function drops without bound.")
            print(f"  No horizontal asymptote on the right.")
        else:
            print(f"  The function settles toward {lim_pos}.")
            print(f"  Horizontal asymptote: y = {lim_pos} on the right.")
    except Exception:
        print(f"  Could not compute lim(x→+∞) automatically.")

    print(f"\n--- Step 3: lim(x→-∞) ---")
    print(f"  x runs off to the left forever.")
    print(f"")
    try:
        lim_neg = sp.limit(expr, x, -sp.oo)
        print(f"  lim(x→-∞) {expr} = {lim_neg}")
        print(f"")
        if lim_neg == sp.oo:
            print(f"  The function grows without bound.")
            print(f"  No horizontal asymptote on the left.")
        elif lim_neg == -sp.oo:
            print(f"  The function drops without bound.")
            print(f"  No horizontal asymptote on the left.")
        else:
            print(f"  The function settles toward {lim_neg}.")
            print(f"  Horizontal asymptote: y = {lim_neg} on the left.")
    except Exception:
        print(f"  Could not compute lim(x→-∞) automatically.")

    print(f"\n--- Step 4: Summary ---")
    try:
        if lim_pos == lim_neg and lim_pos not in [sp.oo, -sp.oo]:
            print(f"  Both sides settle to {lim_pos}.")
            print(f"  y = {lim_pos} is a horizontal asymptote on both sides.")
            print(f"  The function is 'sandwiched' between the two ends.")
        elif lim_pos not in [sp.oo, -sp.oo] and lim_neg not in [sp.oo, -sp.oo]:
            print(f"  The function has different behavior on each side:")
            print(f"  → as x → -∞:  f(x) → {lim_neg}")
            print(f"  → as x → +∞:  f(x) → {lim_pos}")
            print(f"  Two different horizontal asymptotes.")
        else:
            print(f"  The function diverges on at least one side.")
            print(f"  No horizontal asymptote there.")
    except Exception:
        pass

    plot_limit(expr, sp.oo)


def one_sided_limits():
    print(f"\n{'='*50}")
    print(f"ONE-SIDED LIMITS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Some functions behave differently depending on")
    print(f"  which direction you approach a point from.")
    print(f"  That's when we need one-sided limits.")
    print(f"")
    print(f"  lim(x→a⁺)  — coming from the RIGHT (x slightly > a)")
    print(f"  lim(x→a⁻)  — coming from the LEFT  (x slightly < a)")
    print(f"")
    print(f"  The full two-sided limit exists only when both")
    print(f"  one-sided limits exist and agree.")
    print(f"  If they give different values, the limit doesn't exist —")
    print(f"  the function can't decide where it's going.")
    print(f"")

    expr_str = input("  Enter f(x): ")
    a_str    = input("  Enter the point a: ")

    expr = sp.sympify(expr_str)
    a    = sp.sympify(a_str)

    print(f"\n  f(x) = {expr}")
    print(f"  Approaching x = {a} from both sides.")
    print(f"")

    print(f"--- Step 1: Right-hand limit ---")
    print(f"  We approach x = {a} from values slightly larger than {a}.")
    print(f"  Think of walking toward {a} from the right side.")
    print(f"")
    try:
        lim_right = sp.limit(expr, x, a, '+')
        print(f"  lim(x→{a}⁺) {expr} = {lim_right}")
    except Exception:
        lim_right = None
        print(f"  Could not compute the right-hand limit.")

    print(f"\n--- Step 2: Left-hand limit ---")
    print(f"  We approach x = {a} from values slightly smaller than {a}.")
    print(f"  Think of walking toward {a} from the left side.")
    print(f"")
    try:
        lim_left = sp.limit(expr, x, a, '-')
        print(f"  lim(x→{a}⁻) {expr} = {lim_left}")
    except Exception:
        lim_left = None
        print(f"  Could not compute the left-hand limit.")

    print(f"\n--- Step 3: Do they agree? ---")
    print(f"")

    if lim_right is not None and lim_left is not None:
        if lim_right == lim_left:
            print(f"  lim(x→{a}⁺) = {lim_right}")
            print(f"  lim(x→{a}⁻) = {lim_left}")
            print(f"  They match ✓")
            print(f"  The two-sided limit exists:")
            print(f"  lim(x→{a}) {expr} = {lim_right}")
        else:
            print(f"  lim(x→{a}⁺) = {lim_right}")
            print(f"  lim(x→{a}⁻) = {lim_left}")
            print(f"  They don't match.")
            print(f"  The two-sided limit does NOT exist at x = {a}.")
            print(f"  Coming from the left gives {lim_left},")
            print(f"  coming from the right gives {lim_right}.")
            print(f"  The function jumps — there's no single value it approaches.")

    print(f"\n--- Step 4: What kind of discontinuity is this? ---")
    print(f"  Three types exist, and they look very different on a graph:")
    print(f"")
    print(f"  · Removable   — limit exists, but f(a) is wrong or missing")
    print(f"                   (a single hole in the graph)")
    print(f"  · Jump        — left and right limits exist but differ")
    print(f"                   (the graph jumps to a new level)")
    print(f"  · Infinite    — at least one side goes to ±∞")
    print(f"                   (a vertical asymptote)")
    print(f"")

    try:
        val_at_a = sp.simplify(expr.subs(x, a))
        if lim_right == lim_left and lim_right is not None:
            if not val_at_a.is_finite:
                print(f"  f({a}) is undefined, but the limit = {lim_right}.")
                print(f"  This is a REMOVABLE discontinuity.")
                print(f"  There's a hole in the graph at x = {a}.")
                print(f"  Defining f({a}) = {lim_right} would fill it.")
            elif val_at_a == lim_right:
                print(f"  f({a}) = {val_at_a} = limit ✓")
                print(f"  No discontinuity at all — f is continuous here.")
            else:
                print(f"  f({a}) = {val_at_a} but limit = {lim_right}.")
                print(f"  REMOVABLE discontinuity — the limit exists")
                print(f"  but the function value is in the wrong place.")
        elif lim_right != lim_left:
            if lim_right in [sp.oo, -sp.oo] or lim_left in [sp.oo, -sp.oo]:
                print(f"  At least one side goes to ±∞.")
                print(f"  INFINITE discontinuity — vertical asymptote at x = {a}.")
            else:
                print(f"  Both limits are finite but different.")
                print(f"  JUMP discontinuity — the graph leaps at x = {a}.")
    except Exception:
        print(f"  Could not classify automatically.")

    plot_limit(expr, a)


def notable_limits():
    print(f"\n{'='*50}")
    print(f"NOTABLE LIMITS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Some limits come up so often that every mathematician")
    print(f"  memorizes them. They're not just exercises — they're")
    print(f"  the foundation of calculus. Derivatives, integrals,")
    print(f"  Taylor series — all of it traces back to these.")
    print(f"  Let's go through the six most important ones.")
    print(f"")

    notable = [
        ("sin(x)/x",        "x", 0,      "sin(x)/x"),
        ("(1 + 1/x)**x",    "x", sp.oo,  "(1 + 1/x)^x"),
        ("(1 + x)**(1/x)",  "x", 0,      "(1+x)^(1/x)"),
        ("(exp(x)-1)/x",    "x", 0,      "(e^x - 1)/x"),
        ("(log(1+x))/x",    "x", 0,      "ln(1+x)/x"),
        ("x*sin(1/x)",      "x", sp.oo,  "x·sin(1/x)"),
    ]

    explanations = {
        "sin(x)/x": (
            "The most important limit in trigonometry.\n"
            "  At x = 0, sin(0)/0 = 0/0 — looks broken.\n"
            "  But for small angles, sin(x) and x are almost\n"
            "  identical — the ratio is nearly 1.\n"
            "  As x → 0, the ratio approaches 1 exactly.\n"
            "  Without this limit, you can't differentiate sin(x)."
        ),
        "(1 + 1/x)^x": (
            "This is one way to define e ≈ 2.71828.\n"
            "  As x grows, (1+1/x) creeps toward 1 —\n"
            "  but the exponent x grows at the same time.\n"
            "  These two forces balance out and converge to e.\n"
            "  This is exactly what happens in continuous compounding:\n"
            "  interest applied infinitely often per year."
        ),
        "(1+x)^(1/x)": (
            "Another path to e, this time as x → 0.\n"
            "  The base (1+x) → 1, the exponent 1/x → ∞.\n"
            "  Same tension, same resolution: the limit is e.\n"
            "  Two different-looking expressions, same answer."
        ),
        "(e^x - 1)/x": (
            "At x = 0 this gives 0/0 — indeterminate.\n"
            "  But e^x grows at rate 1 near x = 0,\n"
            "  so e^x - 1 ≈ x for small x.\n"
            "  This limit is the derivative of e^x at x = 0.\n"
            "  It's why e is the 'natural' base for exponentials."
        ),
        "ln(1+x)/x": (
            "At x = 0 this gives 0/0 — indeterminate.\n"
            "  ln(1+x) ≈ x for small x, so the ratio → 1.\n"
            "  This limit is the derivative of ln(x) at x = 1.\n"
            "  It pairs perfectly with the previous one."
        ),
        "x·sin(1/x)": (
            "As x → ∞, sin(1/x) oscillates wildly at first.\n"
            "  But 1/x → 0, so the oscillations shrink.\n"
            "  Meanwhile x grows — the two effects cancel out.\n"
            "  x · sin(1/x) ≈ x · (1/x) = 1 as x → ∞.\n"
            "  The squeeze theorem confirms the limit is 1."
        ),
    }

    for expr_str, var, point, label in notable:
        print(f"  {'─'*46}")
        print(f"  lim(x→{point})  {label}")
        print(f"")

        expr = sp.sympify(expr_str)
        try:
            limite = sp.limit(expr, x, point)
            print(f"  Result: {limite}")
            if limite == sp.E:
                print(f"         = e ≈ {float(sp.E):.8f}")
            elif limite not in [sp.oo, -sp.oo]:
                try:
                    print(f"         ≈ {float(limite):.8f}")
                except Exception:
                    pass
        except Exception:
            print(f"  Could not compute automatically.")

        print(f"")
        if label in explanations:
            print(f"  Why does this work?")
            for line in explanations[label].split('\n'):
                print(f"  {line}")
        print(f"")

    print(f"  {'─'*46}")
    print(f"  These six are worth knowing by heart.")
    print(f"  In calculus, when you hit an indeterminate form,")
    print(f"  the first thing to ask is: does this reduce")
    print(f"  to one of these? Often the answer is yes.")


def analyze_limits():
    print(f"\n{'='*50}")
    print(f"LIMIT ANALYZER")
    print(f"{'='*50}")
    print(f"")
    print(f"  A limit asks one deceptively simple question:")
    print(f"  as x gets closer and closer to some value,")
    print(f"  what does f(x) approach?")
    print(f"")
    print(f"  It doesn't matter what happens exactly AT that point.")
    print(f"  Only what happens NEAR it.")
    print(f"  This small distinction is what makes limits powerful —")
    print(f"  and what makes calculus possible.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Limit at a point      lim(x→a) f(x)")
    print(f"  2 — Limit at infinity     lim(x→±∞) f(x)")
    print(f"  3 — One-sided limits      lim(x→a⁺) and lim(x→a⁻) f(x)")
    print(f"  4 — Notable limits        sin(x)/x, (1+1/x)^x, ...")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        limit_at_point()
    elif choice == "2":
        limit_at_infinity()
    elif choice == "3":
        one_sided_limits()
    elif choice == "4":
        notable_limits()
    else:
        print(f"  Invalid choice. Please enter 1, 2, 3, or 4.")


# Input
if __name__ == "__main__":
    print("=== Limit Analyzer ===")
    print("Explore limits of functions — at a point, at infinity,")
    print("from one side, and the classic limits every mathematician knows.\n")
    analyze_limits()