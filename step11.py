import math
import matplotlib.pyplot as plt
import numpy as np


def factorial_explained():
    print(f"\n{'='*50}")
    print(f"FACTORIAL")
    print(f"{'='*50}")
    print(f"")
    print(f"  Before we can count arrangements and selections,")
    print(f"  we need one fundamental operation: the factorial.")
    print(f"")
    print(f"  n! is simply the product of all integers from 1 to n:")
    print(f"      n! = 1 · 2 · 3 · ... · n")
    print(f"")
    print(f"  The intuition: if you have n distinct objects,")
    print(f"  n! is the number of ways to arrange them in a line.")
    print(f"  Three objects A, B, C give 3! = 6 arrangements:")
    print(f"  ABC, ACB, BAC, BCA, CAB, CBA — count them, exactly 6.")
    print(f"")
    print(f"  One thing that surprises everyone at first: 0! = 1.")
    print(f"  It's defined this way, not derived.")
    print(f"  The reason: there is exactly one way to arrange nothing.")
    print(f"  And it makes every formula work cleanly — you'll see why.")
    print(f"")

    n = int(input("  Enter n: "))

    if n < 0:
        print(f"  Factorial is not defined for negative numbers.")
        return

    print(f"\n--- Step 1: Expand ---")
    if n == 0:
        print(f"  0! = 1  by definition.")
        result = 1
    else:
        factors = list(range(1, n+1))
        print(f"  {n}! = " + " · ".join(str(f) for f in factors))

        print(f"\n--- Step 2: Compute step by step ---")
        result = 1
        for f in factors:
            result *= f
            print(f"  × {f}  →  running product = {result}")

    print(f"")
    print(f"  {n}! = {result}")

    print(f"\n--- How fast does factorial grow? ---")
    print(f"  This is worth seeing directly.")
    print(f"  Factorials grow faster than exponentials — much faster.")
    print(f"")
    print(f"  {'n':>5}  {'n!':>25}")
    print(f"  {'─'*33}")
    for i in [1, 2, 3, 4, 5, 10, 15, 20]:
        print(f"  {i:>5}  {math.factorial(i):>25}")
    print(f"")
    digits = len(str(math.factorial(20)))
    print(f"  20! has {digits} digits.")
    print(f"  That's why counting arrangements of large sets")
    print(f"  produces numbers that seem impossibly large.")


def dispositions():
    print(f"\n{'='*50}")
    print(f"DISPOSITIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A disposition is an ordered selection of k objects")
    print(f"  from n distinct objects.")
    print(f"  The key word: ORDERED.")
    print(f"  (A, B) and (B, A) are two different dispositions.")
    print(f"")
    print(f"  Two versions depending on whether you can reuse objects:")
    print(f"")
    print(f"  Without repetition — each object used at most once:")
    print(f"      D(n,k) = n! / (n-k)!  =  n · (n-1) · ... · (n-k+1)")
    print(f"  Why? First slot has n choices, second has n-1, and so on.")
    print(f"  k slots total → multiply k consecutive values starting from n.")
    print(f"")
    print(f"  With repetition — same object can appear multiple times:")
    print(f"      D'(n,k) = n^k")
    print(f"  Why? Each of the k slots has n choices independently.")
    print(f"  k independent choices of n → n multiplied k times.")
    print(f"")
    print(f"  Which type?")
    print(f"  1 — Without repetition")
    print(f"  2 — With repetition")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    n = int(input("  Total objects n: "))
    k = int(input("  Objects to select k: "))

    if n < 0 or k < 0:
        print(f"  n and k must be non-negative.")
        return

    if choice == "1":
        if k > n:
            print(f"  k > n — impossible without repetition.")
            print(f"  You can't pick {k} distinct objects from only {n}.")
            return

        print(f"\n--- Computing D({n},{k}) ---")
        print(f"  D({n},{k}) = {n} · {n-1} · ... · {n-k+1}")
        print(f"  We multiply {k} consecutive integers starting from {n}.")
        print(f"")

        factors = list(range(n, n-k, -1))
        result  = 1
        for f in factors:
            result *= f
            print(f"  × {f}  →  {result}")

        print(f"")
        print(f"  D({n},{k}) = {result}")
        print(f"")
        print(f"  There are {result} ordered ways to pick {k} objects from {n}.")

    elif choice == "2":
        result = n**k
        print(f"\n--- Computing D'({n},{k}) ---")
        print(f"  D'({n},{k}) = {n}^{k}")
        print(f"")
        print(f"  Each of the {k} slots has {n} independent choices:")
        for i in range(1, k+1):
            print(f"  Slot {i}: {n} choices")
        print(f"")
        print(f"  Total: {n}^{k} = {result}")
        print(f"")
        print(f"  There are {result} ordered sequences of length {k}")
        print(f"  from {n} objects, with repetition allowed.")

    else:
        print(f"  Invalid choice.")


def permutations():
    print(f"\n{'='*50}")
    print(f"PERMUTATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A permutation is a disposition where you use ALL n objects.")
    print(f"  It's the special case k = n.")
    print(f"")
    print(f"      P(n) = n!")
    print(f"")
    print(f"  But what if some objects are identical?")
    print(f"  Swapping two identical objects gives the same arrangement —")
    print(f"  so we're overcounting. We correct this by dividing.")
    print(f"")
    print(f"  Permutations with repeated objects:")
    print(f"      P(n; n₁, n₂, ...) = n! / (n₁! · n₂! · ...)")
    print(f"  where n₁, n₂, ... are the counts of each repeated group.")
    print(f"")
    print(f"  Classic example: MISSISSIPPI has 11 letters.")
    print(f"  M=1, I=4, S=4, P=2")
    print(f"  Arrangements = 11! / (1!·4!·4!·2!) = 34650")
    print(f"  Not 11! = 39916800 — because many are identical.")
    print(f"")
    print(f"  Which type?")
    print(f"  1 — All objects distinct")
    print(f"  2 — Some objects are identical")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    if choice == "1":
        n = int(input("  Number of objects n: "))

        if n < 0:
            print(f"  n must be non-negative.")
            return

        result = math.factorial(n)

        print(f"\n--- Computing P({n}) = {n}! ---")
        print(f"")
        if n <= 12:
            factors = list(range(1, n+1))
            print(f"  {n}! = " + " · ".join(str(f) for f in factors))
        print(f"     = {result}")
        print(f"")
        print(f"  There are {result} ways to arrange {n} distinct objects.")

    elif choice == "2":
        n = int(input("  Total objects n: "))
        print(f"  Enter the size of each group of identical objects.")
        print(f"  They must add up to {n}.")
        print(f"")

        groups = []
        total  = 0
        while total < n:
            g = int(input(f"  Size of next group (remaining: {n-total}): "))
            if g <= 0:
                print(f"  Must be positive.")
                continue
            if total + g > n:
                print(f"  Too large. Maximum allowed here: {n-total}")
                continue
            groups.append(g)
            total += g

        print(f"\n--- Computing P({n}; {', '.join(map(str,groups))}) ---")
        print(f"")
        print(f"  P = {n}! / ({' · '.join(str(g)+'!' for g in groups)})")
        print(f"")

        numerator   = math.factorial(n)
        denominator = 1
        for g in groups:
            denominator *= math.factorial(g)

        result = numerator // denominator

        print(f"  Numerator:   {n}! = {numerator}")
        denom_str = " · ".join(f"{g}!={math.factorial(g)}" for g in groups)
        print(f"  Denominator: {denom_str}")
        print(f"             = {denominator}")
        print(f"")
        print(f"  P = {numerator} / {denominator} = {result}")
        print(f"")
        print(f"  There are {result} distinct arrangements.")

    else:
        print(f"  Invalid choice.")


def combinations():
    print(f"\n{'='*50}")
    print(f"COMBINATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A combination is a selection of k objects from n")
    print(f"  where ORDER DOES NOT MATTER.")
    print(f"  (A,B) and (B,A) are the same combination.")
    print(f"")
    print(f"  This single difference — order matters vs doesn't —")
    print(f"  changes the count dramatically.")
    print(f"")
    print(f"      C(n,k) = n! / (k! · (n-k)!)")
    print(f"")
    print(f"  Also written as (n choose k), or as the binomial coefficient.")
    print(f"")
    print(f"  Where does it come from?")
    print(f"  Start with D(n,k) ordered selections.")
    print(f"  Each group of k objects appears k! times in that count —")
    print(f"  once for each way to order those k objects.")
    print(f"  Since we don't care about order, divide by k!:")
    print(f"  C(n,k) = D(n,k) / k! = n! / (k! · (n-k)!)")
    print(f"")
    print(f"  A beautiful symmetry: C(n,k) = C(n, n-k)")
    print(f"  Choosing k objects to include is the same as")
    print(f"  choosing n-k objects to leave out.")
    print(f"")

    n = int(input("  Total objects n: "))
    k = int(input("  Objects to choose k: "))

    if n < 0 or k < 0:
        print(f"  n and k must be non-negative.")
        return
    if k > n:
        print(f"  k > n — C({n},{k}) = 0.")
        print(f"  You can't choose more objects than you have.")
        return

    print(f"\n--- Computing C({n},{k}) ---")
    print(f"  C({n},{k}) = {n}! / ({k}! · {n-k}!)")
    print(f"")

    num    = math.factorial(n)
    den_k  = math.factorial(k)
    den_r  = math.factorial(n-k)
    den    = den_k * den_r
    result = num // den

    print(f"  {n}!     = {num}")
    print(f"  {k}!     = {den_k}")
    print(f"  {n-k}!   = {den_r}")
    print(f"  {k}! · {n-k}! = {den}")
    print(f"")
    print(f"  C({n},{k}) = {num} / {den} = {result}")
    print(f"")
    print(f"  Symmetry: C({n},{n-k}) = {math.comb(n,n-k)}"
          f"  {'✓' if result == math.comb(n,n-k) else '✗'}")
    print(f"")
    print(f"  There are {result} ways to choose {k} objects from {n}")
    print(f"  when order does not matter.")

    print(f"\n--- Comparing dispositions and combinations ---")
    disp = math.factorial(n) // math.factorial(n-k)
    print(f"  D({n},{k}) = {disp}   ordered selections")
    print(f"  C({n},{k}) = {result}   unordered selections")
    print(f"  {disp} / {result} = {disp//result} = {k}! = {math.factorial(k)}")
    print(f"  Exactly k! — each combination maps to k! dispositions. ✓")


def pascal_triangle():
    print(f"\n{'='*50}")
    print(f"PASCAL'S TRIANGLE  —  Triangolo di Tartaglia")
    print(f"{'='*50}")
    print(f"")
    print(f"  In Italy this is rightly called Tartaglia's triangle,")
    print(f"  after Niccolò Tartaglia who studied it in the 1500s.")
    print(f"  Pascal rediscovered it a century later in France.")
    print(f"  In reality it was already known in China, Persia,")
    print(f"  and India centuries before either of them.")
    print(f"  Some mathematical ideas are too natural not to find.")
    print(f"")
    print(f"  The construction rule couldn't be simpler:")
    print(f"  · Start with 1 at the top")
    print(f"  · Each number = sum of the two directly above it")
    print(f"  · The edges are always 1")
    print(f"")
    print(f"  What makes it extraordinary is what's hidden inside.")
    print(f"  Every number at row n, position k is exactly C(n,k).")
    print(f"  The triangle is the complete table of binomial coefficients,")
    print(f"  disguised as a simple addition pattern.")
    print(f"")

    rows = int(input("  How many rows to display? (e.g. 10): "))

    if rows <= 0:
        print(f"  Enter a positive number.")
        return

    triangle = [[math.comb(n, k) for k in range(n+1)]
                for n in range(rows)]

    print(f"\n--- The triangle ---")
    print(f"")
    width = len(str(max(math.comb(rows-1, rows//2), 1))) + 1
    for n, row in enumerate(triangle):
        spaces = " " * ((rows - n - 1) * (width // 2 + 1))
        nums   = "  ".join(str(x).center(width) for x in row)
        print(f"  {spaces}{nums}")

    print(f"")
    print(f"--- Five hidden patterns worth knowing ---")
    print(f"")

    print(f"  1. ROW SUMS — always a power of 2:")
    for n in range(min(rows, 8)):
        print(f"     Row {n}: {sum(triangle[n])} = 2^{n}")

    print(f"")
    print(f"  2. SYMMETRY — every row reads the same forwards and back.")
    print(f"     C(n,k) = C(n,n-k)")
    print(f"     Choosing k to include = choosing n-k to exclude.")

    print(f"")
    print(f"  3. HOCKEY STICK IDENTITY:")
    print(f"     C(r,r) + C(r+1,r) + ... + C(n,r) = C(n+1, r+1)")
    print(f"     Sum any diagonal — it equals one step down and right.")
    r     = 2
    n_demo = min(rows-1, 6)
    lhs   = sum(math.comb(i, r) for i in range(r, n_demo+1))
    rhs   = math.comb(n_demo+1, r+1)
    print(f"     C(2,2)+C(3,2)+...+C({n_demo},2) = {lhs}")
    print(f"     C({n_demo+1},{r+1}) = {rhs}  {'✓' if lhs==rhs else '✗'}")

    print(f"")
    print(f"  4. FIBONACCI IN THE DIAGONALS:")
    print(f"     Add up the shallow diagonals of the triangle.")
    print(f"     The sums are exactly the Fibonacci numbers.")
    fib_sums = []
    for d in range(min(rows, 10)):
        s = sum(math.comb(d-k, k) for k in range(d//2+1) if d-k >= k)
        fib_sums.append(s)
    print(f"     Diagonal sums: {fib_sums}")
    print(f"     Fibonacci:      1, 1, 2, 3, 5, 8, 13, 21, 34, 55")
    print(f"     Triangolo di Tartaglia and Fibonacci — connected.")

    print(f"")
    print(f"  5. SIERPINSKI FRACTAL:")
    print(f"     Color odd numbers black and even numbers white.")
    print(f"     The pattern that emerges is the Sierpinski triangle —")
    print(f"     one of the most famous fractals in all of mathematics.")
    print(f"     A fractal hidden inside a simple arithmetic triangle.")
    print(f"     Here's the preview (█=odd, ·=even):")
    print(f"")
    for n in range(min(rows, 16)):
        row    = triangle[n]
        spaces = " " * (min(rows,16) - n - 1)
        chars  = "  ".join("█" if x%2==1 else "·" for x in row)
        print(f"  {spaces}{chars}")

    plot_pascal(triangle, rows)


def plot_pascal(triangle, rows):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    max_val = max(max(row) for row in triangle)
    matrix  = np.zeros((rows, rows))
    for n, row in enumerate(triangle):
        for k, val in enumerate(row):
            matrix[n][k] = val

    im = axes[0].imshow(matrix, cmap="YlOrRd", aspect="auto")
    axes[0].set_title("Pascal's Triangle — value heatmap", fontsize=12)
    axes[0].set_xlabel("k  (position)")
    axes[0].set_ylabel("n  (row)")
    plt.colorbar(im, ax=axes[0])

    for n in range(min(rows, 10)):
        for k in range(n+1):
            axes[0].text(k, n, str(triangle[n][k]),
                        ha="center", va="center",
                        fontsize=max(6, 10-rows//3),
                        color="black" if triangle[n][k] < max_val*0.6
                        else "white")

    size = min(rows, 32)
    tri2 = [[math.comb(n, k) for k in range(n+1)] for n in range(size)]
    sier = np.zeros((size, size))
    for n in range(size):
        for k in range(n+1):
            sier[n][k] = tri2[n][k] % 2

    axes[1].imshow(sier, cmap="binary", aspect="auto")
    axes[1].set_title("Sierpinski Triangle\n(odd=black, even=white)",
                      fontsize=12)
    axes[1].set_xlabel("k  (position)")
    axes[1].set_ylabel("n  (row)")

    plt.suptitle("Pascal's Triangle  —  Triangolo di Tartaglia",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def binomial_theorem():
    print(f"\n{'='*50}")
    print(f"BINOMIAL THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  How do you expand (a+b)^n without multiplying n times?")
    print(f"  The binomial theorem gives you the answer directly:")
    print(f"")
    print(f"      (a+b)^n = Σ C(n,k) · a^(n-k) · b^k   k=0..n")
    print(f"")
    print(f"  The coefficients are exactly row n of Pascal's triangle.")
    print(f"  This is the deep link between combinatorics and algebra.")
    print(f"")
    print(f"  Why does it work?")
    print(f"  When you expand (a+b)·(a+b)·...·(a+b)  [n times],")
    print(f"  each term comes from choosing a or b from each factor.")
    print(f"  The term a^(n-k)·b^k appears whenever you choose b")
    print(f"  from exactly k of the n factors.")
    print(f"  There are C(n,k) ways to make that choice.")
    print(f"  That's where the coefficients come from.")
    print(f"")
    print(f"  Quick examples:")
    print(f"  (a+b)^2 = 1·a² + 2·ab + 1·b²       row 2: 1,2,1")
    print(f"  (a+b)^3 = 1·a³ + 3·a²b + 3·ab² + 1·b³  row 3: 1,3,3,1")
    print(f"")

    n = int(input("  Enter the exponent n: "))

    if n < 0:
        print(f"  n must be non-negative.")
        return

    print(f"\n--- Expanding (a+b)^{n} term by term ---")
    print(f"")

    terms = []
    for k in range(n+1):
        coeff = math.comb(n, k)
        a_exp = n - k
        b_exp = k

        c_str = "" if (coeff == 1 and a_exp > 0 and b_exp > 0) else str(coeff)
        a_str = "" if a_exp == 0 else ("a" if a_exp == 1 else f"a^{a_exp}")
        b_str = "" if b_exp == 0 else ("b" if b_exp == 1 else f"b^{b_exp}")
        term  = (c_str + a_str + b_str) or "1"

        terms.append(term)
        a_disp = a_str if a_str else "1"
        b_disp = b_str if b_str else "1"
        print(f"  k={k}: C({n},{k}) · {a_disp} · {b_disp}  =  {coeff}·{a_disp}·{b_disp}")

    print(f"")
    print(f"  (a+b)^{n} = " + " + ".join(terms))

    coeffs = [math.comb(n, k) for k in range(n+1)]
    print(f"\n--- Row {n} of Pascal's triangle ---")
    print(f"  {coeffs}")
    print(f"  Exactly the coefficients above. ✓")

    print(f"\n--- Two quick verifications ---")
    print(f"  a=1, b=1:  (1+1)^{n} = 2^{n} = {2**n}")
    print(f"  Sum of coefficients = {sum(coeffs)}")
    print(f"  {'✓' if sum(coeffs)==2**n else '✗'}  — confirms row sum = 2^n")
    print(f"")
    alt = sum((-1)**k * math.comb(n,k) for k in range(n+1))
    print(f"  a=1, b=-1: (1-1)^{n} = 0^{n} = {0**n if n>0 else 1}")
    print(f"  Alternating sum = {alt}")
    if n > 0:
        print(f"  {'✓' if alt==0 else '✗'}  — positive and negative coefficients balance.")


def combinatorics():
    print(f"\n{'='*50}")
    print(f"COMBINATORICS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Combinatorics is the art of counting — precisely.")
    print(f"  Not just 'how many objects' but 'how many ways'.")
    print(f"  How many arrangements? How many selections?")
    print(f"  How many ways to distribute, group, or order?")
    print(f"")
    print(f"  The same situation can give completely different answers")
    print(f"  depending on two questions:")
    print(f"  · Does order matter?")
    print(f"  · Is repetition allowed?")
    print(f"  Getting these right is the whole skill.")
    print(f"")
    print(f"  Combinatorics also underpins probability —")
    print(f"  you can't compute chances without counting outcomes.")
    print(f"  And it connects to algebra through the binomial theorem")
    print(f"  and the hidden structure of Pascal's triangle.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Factorial")
    print(f"  2 — Dispositions    (ordered selections)")
    print(f"  3 — Permutations    (arrange all objects)")
    print(f"  4 — Combinations    (unordered selections)")
    print(f"  5 — Pascal's Triangle   (Triangolo di Tartaglia)")
    print(f"  6 — Binomial Theorem")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, 5, or 6: ")

    if choice == "1":
        factorial_explained()
    elif choice == "2":
        dispositions()
    elif choice == "3":
        permutations()
    elif choice == "4":
        combinations()
    elif choice == "5":
        pascal_triangle()
    elif choice == "6":
        binomial_theorem()
    else:
        print(f"  Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    combinatorics()
    