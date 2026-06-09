import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

n_sym = sp.Symbol('n', positive=True, integer=True)


def plot_sequence(terms, title, param1, param2, kind):
    fig, ax = plt.subplots(figsize=(8, 5))
    n_vals = list(range(1, len(terms) + 1))
    ax.stem(n_vals, terms, linefmt="crimson", markerfmt="o", basefmt="black")

    if kind == "arithmetic":
        ax.set_title(f"{title}  (a={param1}, d={param2})", fontsize=14)
    elif kind == "geometric":
        ax.set_title(f"{title}  (a={param1}, r={param2})", fontsize=14)
    else:
        ax.set_title(f"{title}", fontsize=14)

    ax.set_xlabel("n  (position)")
    ax.set_ylabel("a(n)  (value)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def compute_limit(expr_sym):
    try:
        result = sp.limit(expr_sym, n_sym, sp.oo)
        return result
    except Exception:
        return None


def arithmetic_sequence():
    print(f"\n{'='*50}")
    print(f"ARITHMETIC SEQUENCE")
    print(f"{'='*50}")
    print(f"")
    print(f"  Think of an arithmetic sequence like climbing stairs.")
    print(f"  Every step is the same height — you always add")
    print(f"  the same number d, called the common difference.")
    print(f"")
    print(f"  The general term lets you jump to any position")
    print(f"  without listing every term before it:")
    print(f"")
    print(f"      a(n) = a + (n-1)·d")
    print(f"")
    print(f"  where a is where you start and n is the step number.")
    print(f"  For example, if a = 2 and d = 3:")
    print(f"  a(1)=2, a(2)=5, a(3)=8, a(4)=11 ... and so on.")
    print(f"")

    a = float(input("  First term a: "))
    d = float(input("  Common difference d: "))
    n = int(input("  How many terms to display? "))

    print(f"\n--- Step 1: Build the sequence ---")
    print(f"  We plug n = 1, 2, ..., {n} into a(n) = {a} + (n-1)·{d}.")
    print(f"  Each term should be exactly {d} away from the previous one.")
    print(f"")

    terms = []
    for i in range(1, n + 1):
        term = a + (i - 1) * d
        terms.append(term)
        print(f"  a({i:2}) = {a} + ({i}-1)·{d} = {term}")

    print(f"\n--- Step 2: Sum of the first {n} terms ---")
    print(f"  Here's a trick attributed to Gauss at age 10 that left me shocked when I first learned about it.")
    print(f"  He noticed that pairing the first term with the last,")
    print(f"  the second with the second-to-last, and so on,")
    print(f"  gives the same sum every time.")
    print(f"")
    print(f"  First + Last = {terms[0]} + {terms[-1]} = {terms[0]+terms[-1]}")
    print(f"  Every pair has this sum, and there are n/2 pairs.")
    print(f"  So: S(n) = n/2 · (first + last)")
    print(f"")
    S = n / 2 * (terms[0] + terms[-1])
    print(f"  S({n}) = {n}/2 · ({terms[0]} + {terms[-1]}) = {S}")

    print(f"\n--- Step 3: What happens as n → ∞? ---")
    print(f"  This is where limits come in. Instead of just saying")
    print(f"  'the sequence grows forever', we write it precisely:")
    print(f"")
    print(f"      lim(n→∞) a(n) = ?")
    print(f"")
    print(f"  The general term is a(n) = {a} + (n-1)·{d}.")
    print(f"  As n gets huge, the (n-1)·{d} part takes over.")
    print(f"  The starting value {a} becomes irrelevant — it's")
    print(f"  just a drop in the ocean compared to {d}·n.")
    print(f"")

    a_sym = sp.Rational(a).limit_denominator(1000)
    d_sym = sp.Rational(d).limit_denominator(1000)
    expr_sym = a_sym + (n_sym - 1) * d_sym
    limite = compute_limit(expr_sym)

    print(f"  Computing: lim(n→∞) [{a} + (n-1)·{d}]")
    print(f"")
    if limite is None:
        print(f"  Could not compute automatically — check by hand.")
    elif limite == sp.oo:
        print(f"  Result: +∞")
        print(f"")
        print(f"  d = {d} > 0 means you keep climbing every step.")
        print(f"  There's no ceiling — the sequence diverges to +∞.")
    elif limite == -sp.oo:
        print(f"  Result: -∞")
        print(f"")
        print(f"  d = {d} < 0 means you keep descending every step.")
        print(f"  There's no floor — the sequence diverges to -∞.")
    else:
        print(f"  Result: {limite}")
        print(f"")
        print(f"  d = 0 means you never move. Every term equals {a}.")
        print(f"  The sequence converges to {limite}.")

    plot_sequence(terms, "Arithmetic Sequence", a, d, kind="arithmetic")


def geometric_sequence():
    print(f"\n{'='*50}")
    print(f"GEOMETRIC SEQUENCE")
    print(f"{'='*50}")
    print(f"")
    print(f"  Now instead of adding, we multiply. Each term")
    print(f"  is the previous one times a fixed number r,")
    print(f"  called the common ratio.")
    print(f"")
    print(f"  The general term is:")
    print(f"")
    print(f"      a(n) = a · r^(n-1)")
    print(f"")
    print(f"  The behavior depends entirely on r:")
    print(f"  · r > 1  → terms grow exponentially (think compound interest)")
    print(f"  · 0 < r < 1  → terms shrink toward zero")
    print(f"  · r < 0  → terms alternate in sign (positive, negative, ...)")
    print(f"")

    a = float(input("  First term a: "))
    r = float(input("  Common ratio r: "))
    n = int(input("  How many terms to display? "))

    print(f"\n--- Step 1: Build the sequence ---")
    print(f"  Applying a(n) = {a} · {r}^(n-1) for n = 1 to {n}.")
    print(f"  Notice how the growth is exponential, not linear —")
    print(f"  each term is {r}x the previous one, not {r} more.")
    print(f"")

    terms = []
    for i in range(1, n + 1):
        term = a * r**(i - 1)
        terms.append(term)
        print(f"  a({i:2}) = {a} · {r}^{i-1} = {term:.4f}")

    print(f"\n--- Step 2: Sum of the first {n} terms ---")
    print(f"")
    if r == 1:
        S = a * n
        print(f"  r = 1 → every term equals {a}, so the sum is just {a} · {n}.")
        print(f"  S({n}) = {S}")
    else:
        S = a * (1 - r**n) / (1 - r)
        print(f"  Formula: S(n) = a · (1 - r^n) / (1 - r)")
        print(f"  This comes from a telescoping argument —")
        print(f"  most terms cancel when you subtract r·S(n) from S(n).")
        print(f"")
        print(f"  S({n}) = {a} · (1 - {r}^{n}) / (1 - {r})")
        print(f"         = {a} · (1 - {r**n:.4f}) / {1-r:.4f}")
        print(f"         = {S:.4f}")

    print(f"\n--- Step 3: What happens as n → ∞? ---")
    print(f"  The key question: what does r^n do as n grows?")
    print(f"  That's what drives everything.")
    print(f"")
    print(f"  · If |r| < 1: r^n → 0  (shrinks to nothing)")
    print(f"  · If |r| > 1: r^n → ∞  (explodes)")
    print(f"  · If r = -1:  r^n oscillates between +1 and -1 forever")
    print(f"")
    print(f"  Computing: lim(n→∞) [{a} · {r}^(n-1)]")
    print(f"")

    a_sym = sp.Rational(a).limit_denominator(1000)
    r_sym = sp.Rational(r).limit_denominator(1000)
    expr_sym = a_sym * r_sym**(n_sym - 1)
    limite = compute_limit(expr_sym)

    if limite is None:
        print(f"  The limit does not exist.")
        print(f"  r = {r} causes the terms to oscillate without settling.")
        print(f"  They keep flipping sign — there's no single value")
        print(f"  they approach. We say the sequence has no limit.")
    elif limite == sp.oo:
        print(f"  Result: +∞")
        print(f"  |r| = {abs(r)} > 1 → r^n explodes. The sequence diverges.")
    elif limite == -sp.oo:
        print(f"  Result: -∞")
        print(f"  |r| = {abs(r)} > 1 and a < 0 → diverges to -∞.")
    else:
        print(f"  Result: {limite}")
        if limite == 0:
            print(f"  |r| = {abs(r)} < 1 → r^n shrinks exponentially to zero.")
            print(f"  The terms get smaller and smaller — converges to 0.")
            if r < 0:
                print(f"  Since r < 0, they alternate in sign while shrinking.")
                print(f"  Positive, negative, positive, negative... but always")
                print(f"  closer to zero. The limit is still 0.")
        else:
            print(f"  r = 1 → every term equals {a}. Converges to {a}.")

    plot_sequence(terms, "Geometric Sequence", a, r, kind="geometric")


def recursive_sequence():
    print(f"\n{'='*50}")
    print(f"RECURSIVE SEQUENCE")
    print(f"{'='*50}")
    print(f"")
    print(f"  A recursive sequence is defined differently from")
    print(f"  the others. Instead of a direct formula, it gives")
    print(f"  you a rule: to find the next term, look at the")
    print(f"  previous ones and apply the rule.")
    print(f"")
    print(f"  You always need a starting point — the base case.")
    print(f"  Without it, there's nothing to apply the rule to.")
    print(f"")
    print(f"  Choose a sequence:")
    print(f"  1 — Fibonacci  (a(n) = a(n-1) + a(n-2))")
    print(f"  2 — Custom     (a(n) = a(n-1) · k + c)")
    print(f"")
    choice = input("  Enter 1 or 2: ")
    n = int(input("  How many terms to display? "))

    if choice == "1":
        print(f"\n--- Fibonacci Sequence ---")
        print(f"  Base case: a(1) = 1, a(2) = 1")
        print(f"  Rule: a(n) = a(n-1) + a(n-2)")
        print(f"")
        print(f"  Each term is the sum of the two before it.")
        print(f"  Simple rule — remarkable consequences.")
        print(f"  This sequence shows up in sunflower spirals,")
        print(f"  nautilus shells, pinecones, and tree branches.")
        print(f"  Nature keeps rediscovering it independently.")
        print(f"")

        terms = [1, 1]
        print(f"  a(1) = 1  (base case)")
        print(f"  a(2) = 1  (base case)")
        for i in range(2, n):
            next_term = terms[-1] + terms[-2]
            terms.append(next_term)
            print(f"  a({i+1:2}) = a({i}) + a({i-1}) = "
                  f"{terms[-2]} + {terms[-3]} = {next_term}")

        terms = terms[:n]

        print(f"\n--- Step 2: The limit of the sequence ---")
        print(f"  The terms themselves grow without bound:")
        print(f"")
        print(f"      lim(n→∞) a(n) = +∞")
        print(f"")
        print(f"  But here's what's truly remarkable. Look at the")
        print(f"  ratio between consecutive terms: a(n+1)/a(n).")
        print(f"  As n grows, this ratio converges to a specific number.")
        print(f"")
        print(f"  That number is φ = (1+√5)/2 — the golden ratio.")
        print(f"  It appears in art, architecture, and nature.")
        print(f"  And Fibonacci leads straight to it.")
        print(f"")

        phi = (1 + math.sqrt(5)) / 2
        print(f"  φ = (1 + √5) / 2 = {phi:.10f}")
        print(f"")
        print(f"  {'n':>4}  {'ratio':>12}  {'distance from φ':>18}")
        print(f"  {'-'*38}")
        for i in range(1, len(terms)):
            ratio = terms[i] / terms[i-1]
            diff = abs(ratio - phi)
            print(f"  {i+1:>4}  {ratio:>12.8f}  {diff:>18.10f}")

        print(f"")
        print(f"  lim(n→∞) a(n+1)/a(n) = φ ≈ {phi:.6f}")
        print(f"  The ratio never reaches φ exactly.")
        print(f"  But it never stops getting closer.")
        print(f"  That's exactly what a limit means.")

        plot_sequence(terms, "Fibonacci Sequence", 1, 1, kind="recursive")

    elif choice == "2":
        print(f"\n--- Custom Recursive Sequence ---")
        print(f"  Rule: a(n) = a(n-1) · k + c")
        print(f"  You choose the starting value, the multiplier k,")
        print(f"  and the constant shift c.")
        print(f"")
        a1 = float(input("  First term a(1): "))
        k  = float(input("  Multiplier k: "))
        c  = float(input("  Constant c: "))

        print(f"\n--- Step 1: Build the sequence ---")
        print(f"  Applying a(n) = a(n-1) · {k} + {c} from a(1) = {a1}.")
        print(f"")

        terms = [a1]
        print(f"  a(1) = {a1}  (base case)")
        for i in range(1, n):
            next_term = terms[-1] * k + c
            terms.append(next_term)
            print(f"  a({i+1:2}) = {terms[-2]:.4f} · {k} + {c} = {next_term:.4f}")

        print(f"\n--- Step 2: The limit — fixed point method ---")
        print(f"  If this sequence converges to a value L,")
        print(f"  then at the limit the sequence stops changing.")
        print(f"  That means: L = L·k + c")
        print(f"  Solving for L:")
        print(f"")
        print(f"      L = L·k + c")
        print(f"      L - L·k = c")
        print(f"      L·(1-k) = c")
        print(f"      L = c / (1-k)")
        print(f"")
        print(f"  But this only works if |k| < 1.")
        print(f"  If |k| ≥ 1, the sequence never settles — it escapes.")
        print(f"")

        if k == 1:
            print(f"  k = 1 → a(n) = a(n-1) + {c} — this is arithmetic!")
            if c > 0:
                print(f"  lim(n→∞) a(n) = +∞")
            elif c < 0:
                print(f"  lim(n→∞) a(n) = -∞")
            else:
                print(f"  c = 0 too → constant sequence. lim = {a1}")
        elif k == -1:
            print(f"  k = -1 → the sequence oscillates between two values.")
            print(f"  The limit does not exist — it never settles.")
        else:
            k_sym  = sp.Rational(k).limit_denominator(1000)
            c_sym  = sp.Rational(c).limit_denominator(1000)
            a1_sym = sp.Rational(a1).limit_denominator(1000)

            closed_form = (k_sym**(n_sym - 1) * a1_sym +
                           c_sym * (1 - k_sym**(n_sym - 1)) / (1 - k_sym))
            limite = compute_limit(closed_form)

            print(f"  Closed form: a(n) = {k}^(n-1)·{a1} + "
                  f"{c}·(1-{k}^(n-1))/(1-{k})")
            print(f"")
            print(f"  lim(n→∞) a(n) = {limite}")
            print(f"")

            if limite is not None and limite not in [sp.oo, -sp.oo]:
                print(f"  |k| = {abs(k)} < 1 → converges to L = {float(limite):.6f}")
                print(f"  Let's verify: c/(1-k) = {c}/(1-{k}) = {c/(1-k):.6f}")
                print(f"")
                print(f"  Last three terms closing in on {float(limite):.6f}:")
                for t in terms[-3:]:
                    print(f"    {t:.8f}")
            else:
                print(f"  |k| = {abs(k)} > 1 → the sequence diverges.")
                print(f"  The multiplier is too large — terms escape to infinity.")

        plot_sequence(terms, "Custom Recursive Sequence", a1, k, kind="recursive")

    else:
        print(f"  Invalid choice. Please enter 1 or 2.")


def analyze_sequence():
    print(f"\n{'='*50}")
    print(f"SEQUENCE ANALYZER")
    print(f"{'='*50}")
    print(f"")
    print(f"  A sequence is just an ordered list of numbers,")
    print(f"  where each number has a position — first, second,")
    print(f"  third, and so on. But the interesting question")
    print(f"  is always: what pattern connects them?")
    print(f"")
    print(f"  Choose the type of sequence to analyze:")
    print(f"  1 — Arithmetic  (add the same value each step)")
    print(f"  2 — Geometric   (multiply by the same value each step)")
    print(f"  3 — Recursive   (each term depends on the previous ones)")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        arithmetic_sequence()
    elif choice == "2":
        geometric_sequence()
    elif choice == "3":
        recursive_sequence()
    else:
        print(f"  Invalid choice. Please enter 1, 2, or 3.")


# Input
if __name__ == "__main__":
    print("=== Sequence Analyzer ===")
    print("Explore arithmetic, geometric, and recursive sequences.")
    print("For each one we build the terms, compute the sum,")
    print("and ask the most important question: where does it go?\n")
    analyze_sequence()