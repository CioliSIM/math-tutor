import math
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def gcd_explained(a, b):
    print(f"\n{'='*50}")
    print(f"GREATEST COMMON DIVISOR  (GCD)")
    print(f"{'='*50}")
    print(f"")
    print(f"  The GCD of two numbers is the largest number")
    print(f"  that divides both of them without remainder.")
    print(f"")
    print(f"  The algorithm to compute it efficiently is 2300 years old.")
    print(f"  Euclid described it in his Elements around 300 BC.")
    print(f"  It's still one of the most elegant algorithms ever written.")
    print(f"")
    print(f"  Euclid's key insight:")
    print(f"  GCD(a, b) = GCD(b, a mod b)")
    print(f"")
    print(f"  Why? Any common divisor of a and b also divides")
    print(f"  the remainder when a is divided by b.")
    print(f"  So the set of common divisors doesn't change.")
    print(f"  Keep replacing (a, b) with (b, a mod b) until b = 0.")
    print(f"  The last non-zero value is the GCD.")
    print(f"")

    print(f"--- Computing GCD({a}, {b}) step by step ---")
    print(f"")
    x, y  = a, b
    steps = 0
    while y != 0:
        r = x % y
        print(f"  GCD({x}, {y}):")
        print(f"    {x} = {x//y} · {y} + {r}")
        print(f"    → replace with GCD({y}, {r})")
        x, y   = y, r
        steps += 1

    print(f"")
    print(f"  GCD({a}, {b}) = {x}")
    print(f"  Computed in {steps} steps.")
    print(f"  Trial division would need up to {min(a,b)} steps.")
    print(f"  Euclid's algorithm is dramatically faster.")
    return x


def lcm_explained(a, b):
    print(f"\n{'='*50}")
    print(f"LEAST COMMON MULTIPLE  (LCM)")
    print(f"{'='*50}")
    print(f"")
    print(f"  The LCM is the smallest positive number divisible")
    print(f"  by both a and b.")
    print(f"")
    print(f"  The elegant connection to GCD:")
    print(f"      LCM(a, b) = a · b / GCD(a, b)")
    print(f"")
    print(f"  Why? The prime factors of a and b together")
    print(f"  can be split into shared factors (GCD) and")
    print(f"  combined factors (LCM). Their product is a·b.")
    print(f"  So: GCD · LCM = a · b — always.")
    print(f"")

    g   = math.gcd(a, b)
    lcm = a * b // g

    print(f"--- Computing LCM({a}, {b}) ---")
    print(f"  GCD({a}, {b}) = {g}")
    print(f"  LCM({a}, {b}) = {a} · {b} / {g} = {a*b} / {g} = {lcm}")
    print(f"")
    print(f"  Check:")
    print(f"  {lcm} ÷ {a} = {lcm//a}  ✓")
    print(f"  {lcm} ÷ {b} = {lcm//b}  ✓")
    print(f"  Both divide evenly — confirmed.")
    return lcm


def prime_factorization(n):
    print(f"\n{'='*50}")
    print(f"PRIME FACTORIZATION")
    print(f"{'='*50}")
    print(f"")
    print(f"  The Fundamental Theorem of Arithmetic:")
    print(f"  Every integer greater than 1 factors into primes")
    print(f"  in exactly one way — up to the order of the factors.")
    print(f"")
    print(f"  This seems obvious. It isn't.")
    print(f"  The theorem has two parts that both need proof:")
    print(f"  · Existence  — a factorization always exists")
    print(f"  · Uniqueness — there's only one way to do it")
    print(f"  The uniqueness part is the surprising one.")
    print(f"  Without it, arithmetic wouldn't work the way we expect.")
    print(f"")
    print(f"  Algorithm: trial division.")
    print(f"  Try dividing by 2, then 3, then 5, 7, 11, ...")
    print(f"  We only need to go up to √n.")
    print(f"  Why? If n had a factor larger than √n, it would need")
    print(f"  a cofactor smaller than √n — which we'd already have found.")
    print(f"")

    print(f"--- Factorizing {n} ---")
    print(f"")

    factors = []
    temp    = n
    d       = 2

    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            print(f"  {temp} ÷ {d} = {temp//d}")
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
        print(f"  {temp} is prime — no more factors")

    counts   = Counter(factors)
    factored = " · ".join(
        f"{p}^{e}" if e > 1 else str(p)
        for p, e in sorted(counts.items())
    )

    print(f"")
    print(f"  {n} = {factored}")
    print(f"")
    print(f"  This is the unique prime factorization of {n}.")
    print(f"  No other combination of primes multiplies to {n}.")
    print(f"  That's the Fundamental Theorem of Arithmetic.")

    num_divisors = 1
    for e in counts.values():
        num_divisors *= (e + 1)
    print(f"")
    print(f"  Bonus: the number of divisors of {n} = {num_divisors}")
    print(f"  Formula: multiply (exponent+1) for each prime.")
    print(f"  " + " · ".join(f"({e}+1)" for e in counts.values())
          + f" = {num_divisors}")

    return counts


def sieve_of_eratosthenes(limit):
    print(f"\n{'='*50}")
    print(f"SIEVE OF ERATOSTHENES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Eratosthenes of Cyrene, around 240 BC.")
    print(f"  The same man who measured the circumference of the Earth")
    print(f"  using just a stick, the sun, and geometry.")
    print(f"  His prime-finding algorithm is still unbeaten for")
    print(f"  finding all primes up to a given limit.")
    print(f"")
    print(f"  The idea:")
    print(f"  Write all numbers from 2 to n.")
    print(f"  2 is prime — cross out every multiple of 2.")
    print(f"  The next uncrossed number is always prime.")
    print(f"  Cross out its multiples. Repeat.")
    print(f"  Stop when you reach √n — everything left is prime.")
    print(f"")
    print(f"  Why stop at √n?")
    print(f"  Any composite number ≤ n has a prime factor ≤ √n.")
    print(f"  If all its factors were > √n, their product would exceed n.")
    print(f"  So once we've crossed out multiples of all primes ≤ √n,")
    print(f"  every remaining number must be prime.")
    print(f"")

    is_prime        = [True] * (limit+1)
    is_prime[0]     = is_prime[1] = False
    sqrt_limit      = int(limit**0.5)

    p = 2
    while p <= sqrt_limit:
        if is_prime[p]:
            print(f"  {p} is prime → crossing out {2*p}, {3*p}, {4*p}, ...")
            for multiple in range(p*p, limit+1, p):
                is_prime[multiple] = False
        p += 1

    primes = [i for i in range(2, limit+1) if is_prime[i]]

    print(f"")
    print(f"--- Primes up to {limit} ---")
    print(f"  {primes}")
    print(f"")
    print(f"  Count: {len(primes)} primes")
    print(f"")
    print(f"--- Prime Number Theorem ---")
    print(f"  The theorem predicts the number of primes ≤ n ≈ n/ln(n).")
    approx = limit / math.log(limit)
    print(f"  Approximation: {limit}/ln({limit}) = {approx:.1f}")
    print(f"  Actual count:  {len(primes)}")
    print(f"  Ratio actual/approximation = {len(primes)/approx:.4f}")
    print(f"  This ratio approaches 1 as n → ∞.")
    print(f"  The primes thin out, but in a predictable way.")

    plot_sieve(primes, limit, is_prime)
    return primes


def plot_sieve(primes, limit, is_prime):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].scatter(primes, [1]*len(primes),
                    color="crimson", s=12, alpha=0.7)
    axes[0].set_title(f"Prime distribution up to {limit}", fontsize=12)
    axes[0].set_xlabel("n")
    axes[0].set_yticks([])
    axes[0].grid(True, alpha=0.3, axis="x")

    ns     = list(range(2, limit+1))
    counts = []
    approx = []
    count  = 0
    for n in ns:
        if is_prime[n]:
            count += 1
        counts.append(count)
        approx.append(n / math.log(n))

    axes[1].plot(ns, counts, color="crimson", linewidth=2,
                 label="π(n) — actual count")
    axes[1].plot(ns, approx, color="steelblue", linewidth=1.5,
                 linestyle="--", label="n/ln(n) — approximation")
    axes[1].set_title("Prime Number Theorem", fontsize=12)
    axes[1].set_xlabel("n")
    axes[1].set_ylabel("Primes ≤ n")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Sieve of Eratosthenes", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def fermat_little_theorem():
    print(f"\n{'='*50}")
    print(f"FERMAT'S LITTLE THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  Pierre de Fermat, 1640.")
    print(f"  380 years old — and the foundation of modern cryptography.")
    print(f"")
    print(f"  If p is prime and a is not a multiple of p:")
    print(f"")
    print(f"      a^(p-1) ≡ 1  (mod p)")
    print(f"")
    print(f"  The ≡ symbol means congruent modulo p —")
    print(f"  in plain terms: a^(p-1) leaves remainder 1 when divided by p.")
    print(f"")
    print(f"  Why it's powerful:")
    print(f"  · It lets you compute huge powers modulo p instantly")
    print(f"    without calculating the full power")
    print(f"  · It gives a fast primality test:")
    print(f"    if a^(n-1) mod n ≠ 1, then n is definitely NOT prime")
    print(f"  · RSA encryption — used by every https website —")
    print(f"    is built directly on this theorem.")
    print(f"    Every secure connection you make uses Fermat's result.")
    print(f"")

    p = int(input("  Enter a prime p: "))
    a = int(input("  Enter a (not a multiple of p): "))

    if a % p == 0:
        print(f"  {a} is a multiple of {p} — Fermat's theorem doesn't apply here.")
        return

    print(f"\n--- Verifying a^(p-1) ≡ 1 (mod p) ---")
    print(f"")
    result = pow(a, p-1, p)
    print(f"  {a}^({p-1}) mod {p} = {result}")
    if result == 1:
        print(f"  = 1 ✓  Fermat confirmed.")
    else:
        print(f"  ≠ 1  — check that {p} is really prime.")

    print(f"\n--- Fermat as a primality test ---")
    print(f"  We test several values of a.")
    print(f"  A true prime always passes every test.")
    print(f"  A composite almost always fails at least one.")
    print(f"")
    bases    = [2, 3, 5, 7, 11, 13]
    all_pass = True
    for base in bases:
        if base >= p:
            break
        r      = pow(base, p-1, p)
        passed = r == 1
        print(f"  {base}^{p-1} mod {p} = {r}  {'✓' if passed else '✗ — NOT PRIME'}")
        if not passed:
            all_pass = False

    print(f"")
    if all_pass:
        print(f"  All tests passed → {p} is very likely prime.")
        print(f"  (There exist rare composite numbers called Carmichael")
        print(f"   numbers that pass all Fermat tests — but they're")
        print(f"   extremely rare and easy to catch with other methods.)")
    else:
        print(f"  At least one test failed → {p} is definitely NOT prime.")

    print(f"\n--- The power of modular reduction ---")
    exp = int(input("  Enter a large exponent e to compute: "))
    print(f"")
    print(f"  Goal: {a}^{exp} mod {p}")
    print(f"  By Fermat: {a}^{p-1} ≡ 1 (mod {p})")
    print(f"  So we only need {exp} mod {p-1} = {exp%(p-1)}")
    reduced = exp % (p-1)
    if reduced == 0:
        reduced = p-1
    result_r = pow(a, reduced, p)
    result_d = pow(a, exp, p)
    print(f"  {a}^{exp} ≡ {a}^{reduced} (mod {p})")
    print(f"           ≡ {result_r} (mod {p})")
    print(f"  Direct:  {result_d}  ✓")
    print(f"")
    print(f"  We turned a {len(str(a**exp))}-digit number")
    print(f"  into a simple one-step computation.")


def perfect_numbers():
    print(f"\n{'='*50}")
    print(f"PERFECT NUMBERS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A perfect number equals the sum of all its")
    print(f"  proper divisors — every divisor except itself.")
    print(f"")
    print(f"  6  = 1 + 2 + 3  ✓")
    print(f"  28 = 1 + 2 + 4 + 7 + 14  ✓")
    print(f"  496, 8128, 33550336 ...")
    print(f"")
    print(f"  Only 51 perfect numbers are known.")
    print(f"  The largest has over 49 million digits.")
    print(f"  Nobody knows if there are infinitely many.")
    print(f"  Nobody knows if any ODD perfect number exists —")
    print(f"  none found, none proven impossible.")
    print(f"  It's one of the oldest open problems in all of mathematics.")
    print(f"")
    print(f"  Euler proved (1772): every even perfect number has the form")
    print(f"      2^(p-1) · (2^p - 1)")
    print(f"  where 2^p - 1 is a Mersenne prime.")
    print(f"  So finding even perfect numbers = finding Mersenne primes.")
    print(f"  GIMPS (Great Internet Mersenne Prime Search) has been")
    print(f"  running since 1996 — distributed computing on home computers")
    print(f"  searching for the next one.")
    print(f"")

    limit = int(input("  Search for perfect numbers up to: "))

    print(f"\n--- Searching up to {limit} ---")
    print(f"")

    found = []
    for n in range(2, limit+1):
        divs    = [i for i in range(1, n) if n % i == 0]
        div_sum = sum(divs)
        if div_sum == n:
            found.append(n)
            print(f"  {n} is PERFECT ✓")
            print(f"  Divisors: {divs}")
            print(f"  Sum: {' + '.join(map(str,divs))} = {div_sum}")
            print(f"")

    if not found:
        print(f"  No perfect numbers found up to {limit}.")
        print(f"  Try searching up to at least 500 to find 6, 28, and 496.")
    else:
        print(f"  Found: {found}")

    print(f"\n--- Three categories of numbers ---")
    print(f"  Every number falls into exactly one:")
    print(f"  · Perfect:   sum of divisors = n")
    print(f"  · Abundant:  sum of divisors > n  (e.g. 12 → 1+2+3+4+6=16)")
    print(f"  · Deficient: sum of divisors < n  (e.g. 8  → 1+2+4=7)")
    print(f"")
    print(f"  Every prime is deficient — its only proper divisor is 1.")
    print(f"  Powers of 2 are deficient. Most numbers are deficient.")
    print(f"  Abundant numbers become more common as n grows.")

    if found:
        plot_perfect(found, limit)


def plot_perfect(perfect_nums, limit):
    ns       = list(range(2, min(limit+1, 300)))
    div_sums = [sum(i for i in range(1, n) if n % i == 0) for n in ns]

    colors = []
    for n, s in zip(ns, div_sums):
        if s == n:
            colors.append("gold")
        elif s > n:
            colors.append("steelblue")
        else:
            colors.append("lightgray")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(ns, div_sums, color=colors, edgecolor="none", width=0.8)
    ax.plot(ns, ns, color="crimson", linewidth=1.5,
            linestyle="--", label="y = n  (perfect line)")

    for p in perfect_nums:
        if p < 300:
            ax.annotate(f"  {p}\n  PERFECT",
                        (p, p), fontsize=9,
                        color="darkgoldenrod", fontweight="bold")

    ax.set_title("Divisor sums — perfect (gold), abundant (blue), deficient (gray)",
                 fontsize=12)
    ax.set_xlabel("n")
    ax.set_ylabel("Sum of proper divisors")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.show()


def goldbach_conjecture():
    print(f"\n{'='*50}")
    print(f"GOLDBACH'S CONJECTURE")
    print(f"{'='*50}")
    print(f"")
    print(f"  Christian Goldbach, 1742 — a letter to Euler:")
    print(f"  'Every even integer greater than 2 is the sum of two primes.'")
    print(f"")
    print(f"  4  = 2+2")
    print(f"  6  = 3+3")
    print(f"  8  = 3+5")
    print(f"  10 = 3+7 = 5+5")
    print(f"  100 = 3+97 = 11+89 = 17+83 = ...")
    print(f"")
    print(f"  Verified computationally up to 4·10^18.")
    print(f"  Never proven. Never disproven.")
    print(f"  After 280 years — still open.")
    print(f"")
    print(f"  Best partial result: Chen's theorem (1973).")
    print(f"  Every sufficiently large even number = prime + (prime or prime·prime).")
    print(f"  Almost Goldbach — but not quite.")
    print(f"")
    print(f"  The interesting pattern: as n grows, the number of")
    print(f"  ways to write n as a sum of two primes generally grows too.")
    print(f"  The conjecture gets 'more and more true' — but that's not a proof.")
    print(f"")

    limit = int(input("  Verify Goldbach up to: "))

    is_prime    = [True] * (limit+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, limit+1, i):
                is_prime[j] = False
    primes_set = set(i for i in range(2, limit+1) if is_prime[i])

    failed  = []
    decomps = {}
    max_ways = 0
    max_n    = 0

    for n in range(4, limit+1, 2):
        ways = [(p, n-p) for p in primes_set
                if p <= n//2 and (n-p) in primes_set]
        if not ways:
            failed.append(n)
        decomps[n] = len(ways)
        if len(ways) > max_ways:
            max_ways = len(ways)
            max_n    = n

    print(f"\n--- Results ---")
    print(f"")
    if failed:
        print(f"  COUNTEREXAMPLE FOUND: {failed}")
        print(f"  The conjecture is FALSE — extremely unexpected!")
    else:
        print(f"  All even numbers from 4 to {limit} satisfy Goldbach ✓")
        print(f"")
        print(f"  Examples:")
        for n in [4, 6, 10, 20, 50, 100]:
            if n <= limit:
                ways = [(p, n-p) for p in primes_set
                        if p <= n//2 and (n-p) in primes_set]
                print(f"  {n:4} = " + "  or  ".join(
                    f"{a}+{b}" for a,b in ways[:3]))
        print(f"")
        print(f"  Most decompositions: {max_n} can be written {max_ways} ways.")

    plot_goldbach(decomps, limit)


def plot_goldbach(decomps, limit):
    ns   = list(decomps.keys())
    ways = list(decomps.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(ns, ways, color="steelblue", alpha=0.7, width=1.5)
    ax.set_title("Goldbach — number of ways to write n as sum of two primes",
                 fontsize=12)
    ax.set_xlabel("Even number n")
    ax.set_ylabel("Number of decompositions")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.show()


def twin_primes():
    print(f"\n{'='*50}")
    print(f"TWIN PRIMES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Twin primes are pairs of primes that differ by 2.")
    print(f"  (3,5)  (5,7)  (11,13)  (17,19)  (29,31)  (41,43) ...")
    print(f"")
    print(f"  The twin prime conjecture:")
    print(f"  There are infinitely many twin prime pairs.")
    print(f"  Proposed in the 1800s. Still unproven.")
    print(f"")
    print(f"  A landmark result: Yitang Zhang, 2013.")
    print(f"  He proved there are infinitely many prime pairs")
    print(f"  differing by at most 70,000,000.")
    print(f"  Not 2 — but the first finite bound ever proven.")
    print(f"  Within a year, a collaborative effort (Polymath8)")
    print(f"  reduced the bound from 70 million to 246.")
    print(f"  Getting it down to 2 is still open.")
    print(f"")
    print(f"  A nice pattern: except for (3,5), every twin prime")
    print(f"  pair has the form (6k-1, 6k+1).")
    print(f"  Why? Every prime > 3 is either 6k-1 or 6k+1.")
    print(f"  All other residues mod 6 are divisible by 2 or 3.")
    print(f"  So twin primes must straddle a multiple of 6.")
    print(f"")

    limit = int(input("  Find twin primes up to: "))

    is_prime    = [True] * (limit+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, limit+1, i):
                is_prime[j] = False

    twins = [(p, p+2) for p in range(3, limit-1)
             if is_prime[p] and is_prime[p+2]]

    print(f"\n--- Twin prime pairs up to {limit} ---")
    print(f"")
    for p, q in twins:
        k    = (p+1)//6
        form = f"  = (6·{k}-1, 6·{k}+1)" if p > 5 else ""
        print(f"  ({p}, {q}){form}")

    print(f"")
    print(f"  Found {len(twins)} twin prime pairs up to {limit}.")
    print(f"")

    if twins:
        brun = sum(1/p + 1/(p+2) for p, _ in twins)
        print(f"--- Brun's constant ---")
        print(f"  The sum of 1/p over all primes diverges (harmonic-like).")
        print(f"  But the sum of 1/p over twin primes CONVERGES.")
        print(f"  It converges to Brun's constant B₂ ≈ 1.9021975...")
        print(f"  Sum for our pairs: {brun:.6f}")
        print(f"  Even if there are infinitely many twin primes,")
        print(f"  they're sparse enough that the sum of their reciprocals")
        print(f"  is finite. Sparse infinity — beautiful.")

    plot_twin_primes(twins, limit, is_prime)


def plot_twin_primes(twins, limit, is_prime):
    primes   = [i for i in range(2, limit+1) if is_prime[i]]
    twin_set = set(p for pair in twins for p in pair)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    colors = ["gold" if p in twin_set else "steelblue" for p in primes]
    axes[0].scatter(primes, [1]*len(primes),
                    c=colors, s=25, alpha=0.8)
    axes[0].set_title(f"Twin primes (gold) among all primes up to {limit}",
                      fontsize=12)
    axes[0].set_xlabel("n")
    axes[0].set_yticks([])
    axes[0].grid(True, alpha=0.3, axis="x")

    if len(twins) > 1:
        firsts = [p for p, _ in twins]
        gaps   = [firsts[i+1]-firsts[i] for i in range(len(firsts)-1)]
        axes[1].plot(range(1, len(gaps)+1), gaps,
                     color="crimson", linewidth=1.5,
                     marker="o", markersize=4, alpha=0.7)
        axes[1].set_title("Gaps between consecutive twin prime pairs",
                          fontsize=12)
        axes[1].set_xlabel("Twin prime pair index")
        axes[1].set_ylabel("Gap to next pair")
        axes[1].grid(True, alpha=0.3)

    plt.suptitle("Twin Primes", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def number_theory():
    print(f"\n{'='*50}")
    print(f"NUMBER THEORY")
    print(f"{'='*50}")
    print(f"")
    print(f"  Number theory is the study of integers.")
    print(f"  It asks questions a child could understand")
    print(f"  but that have resisted mathematicians for centuries.")
    print(f"")
    print(f"  Are there infinitely many twin primes?")
    print(f"  Is every even number the sum of two primes?")
    print(f"  Do odd perfect numbers exist?")
    print(f"  Nobody knows.")
    print(f"")
    print(f"  Gauss called it 'the queen of mathematics'.")
    print(f"  The simplest questions lead to the deepest mathematics.")
    print(f"  And it's surprisingly practical — RSA encryption,")
    print(f"  used by every secure website on the internet,")
    print(f"  is built entirely on prime numbers and modular arithmetic.")
    print(f"  Your bank account is protected by number theory.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — GCD and LCM             Euclid's 2300-year-old algorithm")
    print(f"  2 — Prime factorization     the Fundamental Theorem")
    print(f"  3 — Sieve of Eratosthenes   find all primes up to n")
    print(f"  4 — Fermat's Little Theorem the key to cryptography")
    print(f"  5 — Perfect numbers         the oldest open problem")
    print(f"  6 — Goldbach's conjecture   280 years, still unproven")
    print(f"  7 — Twin primes             sparse infinity")
    print(f"")
    choice = input("  Enter 1 to 7: ")

    if choice == "1":
        a = int(input("  Enter a: "))
        b = int(input("  Enter b: "))
        gcd_explained(a, b)
        lcm_explained(a, b)
    elif choice == "2":
        n = int(input("  Enter n: "))
        prime_factorization(n)
    elif choice == "3":
        limit = int(input("  Find primes up to: "))
        sieve_of_eratosthenes(limit)
    elif choice == "4":
        fermat_little_theorem()
    elif choice == "5":
        perfect_numbers()
    elif choice == "6":
        goldbach_conjecture()
    elif choice == "7":
        twin_primes()
    else:
        print(f"  Invalid choice. Please enter 1 to 7.")


if __name__ == "__main__":
    number_theory()
    