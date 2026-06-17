# matches.py — problem bank, 55 problems across all 22 chapters

PROBLEMS = [

    # ── QUADRATIC EQUATIONS (ch.1) ───────────────────────────────────────────
    {
        "id": 1, "level": "Rookie", "chapter": 1,
        "statement": "Prove that for any real x, the expression x² − x + 1 is always positive.",
        "hint": "Complete the square.",
        "solution": "x²−x+1 = (x−½)²+¾. Since (x−½)²≥0, the expression is always ≥¾>0.",
        "answer": "x²−x+1 ≥ ¾ > 0 for all x∈ℝ.",
        "topics": ["Quadratic Equations"],
    },
    {
        "id": 2, "level": "Competitive", "chapter": 1,
        "statement": "Find all real k such that x²+kx+1=0 has two distinct negative roots.",
        "hint": "Three conditions: discriminant > 0, sum of roots < 0, product of roots > 0.",
        "solution": "Δ=k²−4>0→|k|>2. Sum=−k<0→k>0. Product=1>0 always. Combined: k>2.",
        "answer": "k > 2.",
        "topics": ["Quadratic Equations"],
    },

    # ── QUADRATIC INEQUALITIES (ch.2) ────────────────────────────────────────
    {
        "id": 3, "level": "Rookie", "chapter": 2,
        "statement": "Solve x²−5x+6 < 0.",
        "hint": "Factor the quadratic. The parabola opens upward — where is it below the x-axis?",
        "solution": "x²−5x+6=(x−2)(x−3). Since parabola opens up, it is negative between the roots: 2<x<3.",
        "answer": "x ∈ (2, 3).",
        "topics": ["Quadratic Inequalities"],
    },
    {
        "id": 4, "level": "Competitive", "chapter": 2,
        "statement": "Find all integers n such that n²−7n+10 ≤ 0.",
        "hint": "Solve the inequality over the reals first, then restrict to integers.",
        "solution": "n²−7n+10=(n−2)(n−5)≤0 → 2≤n≤5. Integer solutions: n=2,3,4,5.",
        "answer": "n ∈ {2, 3, 4, 5}.",
        "topics": ["Quadratic Inequalities"],
    },

    # ── SYSTEMS (ch.3) ───────────────────────────────────────────────────────
    {
        "id": 5, "level": "Rookie", "chapter": 3,
        "statement": "Find all pairs (x,y) satisfying x+y=10 and xy=21.",
        "hint": "These are the sum and product of two numbers. What equation do they satisfy?",
        "solution": "x and y are roots of t²−10t+21=0 → (t−3)(t−7)=0. Solutions: (3,7) and (7,3).",
        "answer": "(x,y) = (3,7) or (7,3).",
        "topics": ["Systems of Equations"],
    },

    # ── POLYNOMIALS (ch.4) ───────────────────────────────────────────────────
    {
        "id": 6, "level": "Competitive", "chapter": 4,
        "statement": "Prove that if p(x) is a polynomial and p(a)=0, then (x−a) divides p(x).",
        "hint": "Write p(x) = (x−a)·q(x) + r using polynomial division. What must r be?",
        "solution": "By the division algorithm: p(x)=(x−a)q(x)+r for some constant r. Setting x=a: p(a)=0·q(a)+r=r=0. So r=0 and (x−a)|p(x).",
        "answer": "The remainder theorem: p(a)=0 implies (x−a) | p(x).",
        "topics": ["Polynomials", "Proofs"],
    },
    {
        "id": 7, "level": "Olympic", "chapter": 4,
        "statement": "Let p(x) be a polynomial with integer coefficients. Prove that if p(0) and p(1) are both odd, then p has no integer roots.",
        "hint": "Consider any integer root r. It must be even or odd. Derive a contradiction in both cases.",
        "solution": "Suppose r is an integer root. If r is even: p(r)≡p(0) (mod 2)≡1 (mod 2)≠0, contradiction. If r is odd: p(r)≡p(1) (mod 2)≡1 (mod 2)≠0, contradiction. (This uses the fact that for integer-coefficient polynomials, a≡b (mod 2) implies p(a)≡p(b) (mod 2).) Therefore p has no integer roots.",
        "answer": "No integer roots exist.",
        "topics": ["Polynomials", "Number Theory", "Proofs"],
    },

    # ── FUNCTION ANALYSIS (ch.5) ─────────────────────────────────────────────
    {
        "id": 8, "level": "Rookie", "chapter": 5,
        "statement": "Determine whether f(x) = x³ is even, odd, or neither. Then find its domain and range.",
        "hint": "Check f(−x). What is the natural domain of a polynomial?",
        "solution": "f(−x)=(−x)³=−x³=−f(x) → odd function. Domain: ℝ. Range: ℝ (every cubic is surjective).",
        "answer": "Odd. Domain = ℝ, Range = ℝ.",
        "topics": ["Function Analysis"],
    },
    {
        "id": 9, "level": "Competitive", "chapter": 5,
        "statement": "Find all functions f: ℝ→ℝ satisfying f(x+y) = f(x)+f(y) for all x,y∈ℝ and f(1)=1.",
        "hint": "Compute f(0), f(n) for integers, f(p/q) for rationals. Assume continuity for the final step.",
        "solution": "f(0)=0 (set x=y=0). f(n)=n by induction. f(p/q)=p/q since q·f(p/q)=f(p)=p. For all rationals f=id. With continuity: f(x)=x for all x∈ℝ.",
        "answer": "f(x) = x (assuming continuity).",
        "topics": ["Function Analysis", "Proofs"],
    },

    # ── SEQUENCES (ch.6) ─────────────────────────────────────────────────────
    {
        "id": 10, "level": "Rookie", "chapter": 6,
        "statement": "The sum of the first n terms of an arithmetic sequence is Sₙ=3n²+2n. Find the first term and the common difference.",
        "hint": "Use a₁=S₁ and d=S₂−2S₁ or aₙ=Sₙ−Sₙ₋₁.",
        "solution": "a₁=S₁=5. aₙ=Sₙ−Sₙ₋₁=3n²+2n−3(n−1)²−2(n−1)=6n−1. So a₁=5✓, d=a₂−a₁=11−5=6.",
        "answer": "First term = 5, common difference = 6.",
        "topics": ["Sequences"],
    },
    {
        "id": 11, "level": "Competitive", "chapter": 6,
        "statement": "A ball dropped from 100m bounces to 2/3 of its previous height each time. Find the total distance traveled.",
        "hint": "After the first fall, the ball travels up and down infinitely. Recognize the geometric series.",
        "solution": "First fall: 100m. Then up+down: 2·(100·2/3)·1/(1−2/3)=2·200=400m. Total=500m.",
        "answer": "500 metres.",
        "topics": ["Sequences", "Geometric series"],
    },

    # ── LIMITS (ch.7) ────────────────────────────────────────────────────────
    {
        "id": 12, "level": "Rookie", "chapter": 7,
        "statement": "Compute lim(x→2) (x²−4)/(x−2).",
        "hint": "Direct substitution gives 0/0. Factor the numerator.",
        "solution": "(x²−4)/(x−2)=(x+2)(x−2)/(x−2)=x+2 for x≠2. Limit=2+2=4.",
        "answer": "4.",
        "topics": ["Limits"],
    },
    {
        "id": 13, "level": "Competitive", "chapter": 7,
        "statement": "Compute lim(x→0) (1−cos x)/x².",
        "hint": "Apply L'Hôpital's rule twice, or use the known limit sin(x)/x=1 and a trigonometric identity.",
        "solution": "Using L'Hôpital: (sin x)/(2x)→(cos x)/2→1/2 as x→0. Alternatively: (1−cosx)/x²=(2sin²(x/2))/x²=½·(sin(x/2)/(x/2))²→½·1=½.",
        "answer": "1/2.",
        "topics": ["Limits", "L'Hôpital"],
    },
    {
        "id": 14, "level": "Olympic", "chapter": 7,
        "statement": "Prove that lim(x→0) sin(x)/x = 1 using the squeeze theorem.",
        "hint": "Compare the areas of a triangle, a circular sector, and another triangle for 0<x<π/2.",
        "solution": "For 0<x<π/2: sin x < x < tan x. Divide by sin x: 1 < x/sin x < 1/cos x. Invert: cos x < sin x/x < 1. As x→0⁺, cos x→1, so by squeeze theorem sin x/x→1. By symmetry the limit from the left is also 1.",
        "answer": "lim(x→0) sin(x)/x = 1. □",
        "topics": ["Limits", "Proofs"],
    },

    # ── TRIGONOMETRY (ch.8) ──────────────────────────────────────────────────
    {
        "id": 15, "level": "Rookie", "chapter": 8,
        "statement": "Simplify sin²x + sin²(x+π/2).",
        "hint": "What is sin(x+π/2)?",
        "solution": "sin(x+π/2)=cosx. So sin²x+cos²x=1.",
        "answer": "1.",
        "topics": ["Trigonometry"],
    },
    {
        "id": 16, "level": "Competitive", "chapter": 8,
        "statement": "Find all x∈[0,2π] satisfying 2sin²x − sinx − 1 = 0.",
        "hint": "Treat sinx as an unknown. Factor the quadratic.",
        "solution": "Let t=sinx: 2t²−t−1=(2t+1)(t−1)=0 → t=−½ or t=1. t=1: x=π/2. t=−½: x=7π/6 or 11π/6.",
        "answer": "x = π/2, 7π/6, 11π/6.",
        "topics": ["Trigonometry"],
    },

    # ── ANALYTIC GEOMETRY 2D (ch.9) ──────────────────────────────────────────
    {
        "id": 17, "level": "Rookie", "chapter": 9,
        "statement": "Find the distance from the point (3,4) to the line 3x+4y−25=0.",
        "hint": "Use the point-to-line distance formula.",
        "solution": "d=|3·3+4·4−25|/√(9+16)=|9+16−25|/5=|0|/5=0. The point is ON the line.",
        "answer": "Distance = 0. The point lies on the line.",
        "topics": ["Analytic Geometry 2D"],
    },
    {
        "id": 18, "level": "Competitive", "chapter": 9,
        "statement": "Find the points of intersection of the circle x²+y²=25 and the line y=x+1.",
        "hint": "Substitute y=x+1 into the circle equation.",
        "solution": "x²+(x+1)²=25 → 2x²+2x−24=0 → x²+x−12=0 → (x+4)(x−3)=0. x=−4→y=−3; x=3→y=4.",
        "answer": "(−4, −3) and (3, 4).",
        "topics": ["Analytic Geometry 2D", "Systems"],
    },

    # ── LOGARITHMS & EXPONENTIALS (ch.10) ────────────────────────────────────
    {
        "id": 19, "level": "Rookie", "chapter": 10,
        "statement": "Solve for x: 2^(x+1) = 8^(x−1).",
        "hint": "Write both sides as powers of 2.",
        "solution": "8=2³, so 8^(x−1)=2^(3x−3). Therefore x+1=3x−3 → 2x=4 → x=2.",
        "answer": "x = 2.",
        "topics": ["Logarithms & Exponentials"],
    },
    {
        "id": 20, "level": "Competitive", "chapter": 10,
        "statement": "Prove that log₂3 is irrational.",
        "hint": "Suppose it equals p/q in lowest terms. Derive a contradiction.",
        "solution": "Suppose log₂3=p/q with p,q positive integers, gcd(p,q)=1. Then 2^(p/q)=3 → 2^p=3^q. The left side is even, the right side is odd — contradiction.",
        "answer": "log₂3 is irrational. □",
        "topics": ["Logarithms & Exponentials", "Proofs", "Number Theory"],
    },

    # ── COMBINATORICS (ch.11) ────────────────────────────────────────────────
    {
        "id": 21, "level": "Rookie", "chapter": 11,
        "statement": "In how many ways can 5 people be seated around a circular table?",
        "hint": "Fix one person's seat to eliminate rotational symmetry.",
        "solution": "Fix one person. Arrange the remaining 4 in 4!=24 ways.",
        "answer": "24.",
        "topics": ["Combinatorics"],
    },
    {
        "id": 22, "level": "Competitive", "chapter": 11,
        "statement": "Prove Pascal's identity: C(n,k) = C(n−1,k−1) + C(n−1,k).",
        "hint": "Count n-element subsets of {1,…,n} by whether element n is included or not.",
        "solution": "Count k-subsets of {1,…,n}. Either n is included (choose k−1 from {1,…,n−1}: C(n−1,k−1) ways) or not (choose k from {1,…,n−1}: C(n−1,k) ways). Total: C(n−1,k−1)+C(n−1,k)=C(n,k). □",
        "answer": "C(n,k) = C(n−1,k−1) + C(n−1,k). □",
        "topics": ["Combinatorics", "Proofs"],
    },
    {
        "id": 23, "level": "Olympic", "chapter": 11,
        "statement": "Prove that among any n+1 positive integers chosen from {1, 2, …, 2n}, at least one divides another.",
        "hint": "Write each integer as 2^k·m where m is odd. How many distinct odd parts are possible?",
        "solution": "Write each integer as 2^k·m with m odd. The odd part m lies in {1,3,5,…,2n−1} — only n values. With n+1 integers, by pigeonhole two share the same odd part m: say a=2^j·m and b=2^k·m with j<k. Then a|b. □",
        "answer": "At least one divides another. □",
        "topics": ["Combinatorics", "Number Theory", "Pigeonhole"],
    },

    # ── PROBABILITY (ch.12) ──────────────────────────────────────────────────
    {
        "id": 24, "level": "Rookie", "chapter": 12,
        "statement": "A bag contains 4 red and 6 blue balls. Two are drawn without replacement. What is the probability both are red?",
        "hint": "Multiply conditional probabilities.",
        "solution": "P(first red)=4/10. P(second red | first red)=3/9. P(both red)=4/10·3/9=12/90=2/15.",
        "answer": "2/15.",
        "topics": ["Probability"],
    },
    {
        "id": 25, "level": "Competitive", "chapter": 12,
        "statement": "A test for a disease has 99% sensitivity and 95% specificity. The disease affects 1% of the population. Given a positive test, what is the probability of actually having the disease?",
        "hint": "Use Bayes' theorem. Define events D=disease, T=positive test.",
        "solution": "P(D)=0.01, P(T|D)=0.99, P(T|¬D)=0.05. P(T)=0.99·0.01+0.05·0.99=0.0099+0.0495=0.0594. P(D|T)=0.0099/0.0594≈16.7%.",
        "answer": "≈ 16.7%. A surprisingly low number — this is why medical testing requires context.",
        "topics": ["Probability", "Bayes"],
    },
    {
        "id": 26, "level": "Olympic", "chapter": 12,
        "statement": "In a room of 23 people, what is the probability that at least two share a birthday? Prove that this exceeds 50%.",
        "hint": "Compute the complementary probability that all birthdays are distinct.",
        "solution": "P(all distinct)=365/365·364/365·…·343/365=∏(k=0 to 22)(365−k)/365. Computing: P(all distinct)≈0.4927. So P(shared)≈0.5073>50%. □",
        "answer": "≈ 50.7% — the famous birthday paradox.",
        "topics": ["Probability", "Combinatorics"],
    },

    # ── COMPLEX NUMBERS (ch.13) ──────────────────────────────────────────────
    {
        "id": 27, "level": "Rookie", "chapter": 13,
        "statement": "Compute (1+i)⁸.",
        "hint": "Convert to polar form first.",
        "solution": "1+i=√2·e^(iπ/4). (1+i)⁸=(√2)⁸·e^(i·2π)=16·1=16.",
        "answer": "16.",
        "topics": ["Complex Numbers"],
    },
    {
        "id": 28, "level": "Competitive", "chapter": 13,
        "statement": "Find all complex z such that z²=−5+12i.",
        "hint": "Write z=a+bi and expand. Solve the system for a and b.",
        "solution": "z=a+bi: a²−b²=−5 and 2ab=12→ab=6→b=6/a. a²−36/a²=−5→a⁴+5a²−36=0→(a²+9)(a²−4)=0→a=±2. Solutions: z=2+3i or z=−2−3i.",
        "answer": "z = 2+3i or z = −2−3i.",
        "topics": ["Complex Numbers"],
    },
    {
        "id": 29, "level": "Olympic", "chapter": 13,
        "statement": "Prove Euler's formula: e^(iθ) = cosθ + i·sinθ.",
        "hint": "Expand e^(iθ) as a power series. Separate real and imaginary parts.",
        "solution": "e^(iθ)=Σ(iθ)ⁿ/n!=Σ(iθ)²ᵏ/(2k)! + Σ(iθ)^(2k+1)/(2k+1)!=Σ(−1)ᵏθ²ᵏ/(2k)! + i·Σ(−1)ᵏθ^(2k+1)/(2k+1)!=cosθ+i·sinθ. □",
        "answer": "e^(iθ) = cosθ + i·sinθ. □",
        "topics": ["Complex Numbers", "Sequences", "Proofs"],
    },

    # ── EUCLIDEAN GEOMETRY (ch.14) ───────────────────────────────────────────
    {
        "id": 30, "level": "Rookie", "chapter": 14,
        "statement": "In triangle ABC, angle A=60°, angle B=70°. A point D lies on BC. The bisector of angle A meets BC at D. Find angle ADB.",
        "hint": "Use the fact that angles in a triangle sum to 180°. The bisector divides angle A.",
        "solution": "Angle C=180−60−70=50°. Angle DAB=30° (bisector). In triangle ABD: angle ADB=180−70−30=80°.",
        "answer": "∠ADB = 80°.",
        "topics": ["Euclidean Geometry"],
    },
    {
        "id": 31, "level": "Competitive", "chapter": 14,
        "statement": "Prove that the angle inscribed in a semicircle is always 90°.",
        "hint": "Let the diameter be AB and the inscribed point C. Draw the radius to C. Use isosceles triangles.",
        "solution": "Let O be center, radius r. OA=OB=OC=r. Triangle OAC is isosceles: ∠OAC=∠OCA=α. Triangle OBC is isosceles: ∠OBC=∠OCB=β. In triangle ABC: α+β+(α+β)=180° → 2(α+β)=180° → ∠ACB=α+β=90°. □",
        "answer": "∠ACB = 90°. □",
        "topics": ["Euclidean Geometry", "Proofs"],
    },

    # ── NUMBER THEORY (ch.15) ────────────────────────────────────────────────
    {
        "id": 32, "level": "Rookie", "chapter": 15,
        "statement": "Find all integers n such that n²−n is divisible by 6.",
        "hint": "Factor: n²−n = n(n−1). What do you know about consecutive integers?",
        "solution": "n(n−1) is always divisible by 2 (consecutive integers). For divisibility by 3: n≡0,1,2 (mod 3). In each case 3|n(n−1). Therefore 6|n(n−1) for all integers n.",
        "answer": "All integers n.",
        "topics": ["Number Theory"],
    },
    {
        "id": 33, "level": "Competitive", "chapter": 15,
        "statement": "Prove that there are infinitely many prime numbers.",
        "hint": "Assume finitely many. Construct a number that can't be divisible by any of them.",
        "solution": "Suppose p₁,…,pₙ are all primes. Let N=p₁·p₂·…·pₙ+1. N is not divisible by any pᵢ (remainder 1). So N is either prime or has a prime factor not in our list — contradiction. □",
        "answer": "There are infinitely many primes. □",
        "topics": ["Number Theory", "Proofs"],
    },
    {
        "id": 34, "level": "Olympic", "chapter": 15,
        "statement": "Prove that for every prime p≥5, p²−1 is divisible by 24.",
        "hint": "Write p²−1=(p−1)(p+1). What can you say about three consecutive integers around p?",
        "solution": "p≥5 prime → p is odd → p−1 and p+1 are consecutive even numbers → one divisible by 4, one by 2 → 8|(p−1)(p+1). Also p not divisible by 3 → p≡1 or 2 (mod 3) → p−1 or p+1 divisible by 3 → 3|(p−1)(p+1). gcd(8,3)=1 → 24|p²−1. □",
        "answer": "24 | p²−1 for all primes p≥5. □",
        "topics": ["Number Theory", "Proofs"],
    },

    # ── FINANCIAL MATH (ch.16) ───────────────────────────────────────────────
    {
        "id": 35, "level": "Rookie", "chapter": 16,
        "statement": "€1000 is invested at 5% annual compound interest. How much is it worth after 10 years?",
        "hint": "Use the compound interest formula A=P(1+r)^n.",
        "solution": "A=1000·(1.05)^10=1000·1.6289=€1628.89.",
        "answer": "€1628.89.",
        "topics": ["Financial Math"],
    },
    {
        "id": 36, "level": "Competitive", "chapter": 16,
        "statement": "At what annual interest rate does money double in 10 years with continuous compounding?",
        "hint": "For continuous compounding: A=Pe^(rt). Set A=2P.",
        "solution": "2P=Pe^(10r) → e^(10r)=2 → 10r=ln2 → r=ln2/10≈6.93%.",
        "answer": "r = ln2/10 ≈ 6.93%.",
        "topics": ["Financial Math", "Logarithms & Exponentials"],
    },

    # ── PARAMETRIC EQUATIONS (ch.17) ─────────────────────────────────────────
    {
        "id": 37, "level": "Competitive", "chapter": 17,
        "statement": "A curve is given by x=t²−1, y=t³−t. Find all points where the curve crosses itself.",
        "hint": "A self-intersection occurs when two different t-values give the same (x,y). Set up equations.",
        "solution": "Need t₁≠t₂ with t₁²−1=t₂²−1 and t₁³−t₁=t₂³−t₂. First: t₁²=t₂²→t₂=−t₁. Second: t₁³−t₁=−t₁³+t₁→2t₁³=2t₁→t₁(t₁²−1)=0→t₁=0,±1. t₁=1,t₂=−1: x=0,y=0. Self-intersection at (0,0).",
        "answer": "The curve crosses itself at (0, 0), when t=1 and t=−1.",
        "topics": ["Parametric Equations"],
    },

    # ── ANALYTIC GEOMETRY 3D (ch.18) ─────────────────────────────────────────
    {
        "id": 38, "level": "Competitive", "chapter": 18,
        "statement": "Find the distance from the point P=(1,2,3) to the plane 2x+y−2z+3=0.",
        "hint": "Use the 3D point-to-plane distance formula.",
        "solution": "d=|2·1+1·2−2·3+3|/√(4+1+4)=|2+2−6+3|/3=|1|/3=1/3.",
        "answer": "1/3.",
        "topics": ["Analytic Geometry 3D"],
    },

    # ── MATHEMATICAL PROOFS (ch.19) ──────────────────────────────────────────
    {
        "id": 39, "level": "Competitive", "chapter": 19,
        "statement": "Prove by induction: 1+2+3+…+n = n(n+1)/2 for all n≥1.",
        "hint": "Base case n=1. Inductive step: assume true for n, prove for n+1.",
        "solution": "Base: n=1: 1=1·2/2=1 ✓. Step: assume 1+…+n=n(n+1)/2. Then 1+…+n+(n+1)=n(n+1)/2+(n+1)=(n+1)(n/2+1)=(n+1)(n+2)/2. □",
        "answer": "1+2+…+n = n(n+1)/2. □",
        "topics": ["Mathematical Proofs", "Sequences"],
    },
    {
        "id": 40, "level": "Olympic", "chapter": 19,
        "statement": "Prove that √2 is irrational.",
        "hint": "Suppose √2=p/q in lowest terms. Square both sides and derive a contradiction about the parity of p and q.",
        "solution": "Suppose √2=p/q with gcd(p,q)=1. Then 2q²=p² → 2|p → p=2k → 2q²=4k² → q²=2k² → 2|q. But then 2|gcd(p,q)=1, contradiction. □",
        "answer": "√2 is irrational. □",
        "topics": ["Mathematical Proofs", "Number Theory"],
    },

    # ── OLYMPIC MATHEMATICS (ch.20) ──────────────────────────────────────────
    {
        "id": 41, "level": "Olympic", "chapter": 20,
        "statement": "Prove that for every integer n≥1, n⁵−n is divisible by 30.",
        "hint": "30=2·3·5. Show divisibility by each prime separately. For p=5 use Fermat's Little Theorem.",
        "solution": "n⁵−n=n(n⁴−1)=(n−1)n(n+1)(n²+1). Div by 2: (n−1)n consecutive → one even. Div by 3: among n−1,n,n+1 one divisible by 3. Div by 5: by FLT n⁵≡n (mod 5). All primes distinct → 30|n⁵−n. □",
        "answer": "30 | n⁵−n for all n≥1. □",
        "topics": ["Olympic Mathematics", "Number Theory"],
    },
    {
        "id": 42, "level": "Olympic", "chapter": 20,
        "statement": "Among any 5 integers, prove that two have a difference divisible by 4.",
        "hint": "Pigeonhole. How many residues mod 4 are there?",
        "solution": "Each integer has residue 0,1,2, or 3 (mod 4) — only 4 options. With 5 integers and 4 boxes, two share a residue aᵢ≡aⱼ (mod 4), so 4|(aᵢ−aⱼ). □",
        "answer": "Two of the five integers have difference divisible by 4. □",
        "topics": ["Olympic Mathematics", "Number Theory", "Pigeonhole"],
    },
    {
        "id": 43, "level": "Olympic", "chapter": 20,
        "statement": "Prove that √2+√3 is irrational.",
        "hint": "Suppose it's rational. Square it. What must √6 be?",
        "solution": "Suppose r=√2+√3∈ℚ. Then r²=5+2√6∈ℚ → √6=(r²−5)/2∈ℚ. But √6 irrational (proof: 6q²=p² → 2|p → 2|q, contradicts gcd(p,q)=1). Contradiction. □",
        "answer": "√2+√3 is irrational. □",
        "topics": ["Olympic Mathematics", "Number Theory", "Proofs"],
    },

    # ── DERIVATIVES (ch.21) ──────────────────────────────────────────────────
    {
        "id": 44, "level": "Rookie", "chapter": 21,
        "statement": "Find the equation of the tangent to y=x³−3x at x=2.",
        "hint": "You need the point (2, f(2)) and the slope f'(2).",
        "solution": "f(2)=8−6=2. f'(x)=3x²−3. f'(2)=9. Tangent: y−2=9(x−2) → y=9x−16.",
        "answer": "y = 9x − 16.",
        "topics": ["Derivatives"],
    },
    {
        "id": 45, "level": "Competitive", "chapter": 21,
        "statement": "Apply Lagrange's theorem to f(x)=√x on [1,4]. Find the point c guaranteed by the theorem.",
        "hint": "Lagrange says f'(c)=[f(4)−f(1)]/(4−1). Solve for c.",
        "solution": "f'(c)=1/(2√c). [f(4)−f(1)]/3=(2−1)/3=1/3. So 1/(2√c)=1/3 → 2√c=3 → c=9/4.",
        "answer": "c = 9/4.",
        "topics": ["Derivatives", "Lagrange"],
    },
    {
        "id": 46, "level": "Competitive", "chapter": 21,
        "statement": "Let f be differentiable on ℝ with f(0)=0 and |f'(x)|≤1 for all x. Prove |f(x)|≤|x| for all x.",
        "hint": "Apply Lagrange's theorem on the interval [0,x] (or [x,0]).",
        "solution": "For x>0: by Lagrange ∃c∈(0,x) with f(x)−f(0)=f'(c)·x → |f(x)|=|f'(c)|·x≤1·x=x=|x|. Similarly for x<0. □",
        "answer": "|f(x)| ≤ |x| for all x. □",
        "topics": ["Derivatives", "Lagrange", "Proofs"],
    },
    {
        "id": 47, "level": "Olympic", "chapter": 21,
        "statement": "Prove that if f is twice differentiable, f(a)=f(b)=0 and f(c)>0 for some c∈(a,b), then there exists ξ∈(a,b) with f''(ξ)<0.",
        "hint": "Use Rolle's theorem twice.",
        "solution": "f(a)=f(c): by Rolle ∃ξ₁∈(a,c) with f'(ξ₁)=0. f(c)>f(b)=0: Rolle gives ∃ξ₂∈(c,b) with f'(ξ₂)=0 (actually apply to f on [c,b]... more carefully: by MVT ∃d∈(c,b) with f'(d)=(f(b)−f(c))/(b−c)<0, and f'(ξ₁)=0>f'(d) → by Rolle on f' ∃ξ∈(ξ₁,d)⊂(a,b) with f''(ξ)=0... apply MVT to f' on [ξ₁,d]: f''(ξ)=(f'(d)−0)/(d−ξ₁)<0. □",
        "answer": "∃ξ∈(a,b) with f''(ξ)<0. □",
        "topics": ["Derivatives", "Rolle", "Proofs"],
    },

    # ── INTEGRALS (ch.22) ────────────────────────────────────────────────────
    {
        "id": 48, "level": "Rookie", "chapter": 22,
        "statement": "Compute ∫₀^π sin(x) dx.",
        "hint": "Find the antiderivative of sin(x). Apply the fundamental theorem.",
        "solution": "∫sin x dx = −cos x + C. [−cos x]₀^π = −cos π + cos 0 = 1+1=2.",
        "answer": "2.",
        "topics": ["Integrals"],
    },
    {
        "id": 49, "level": "Competitive", "chapter": 22,
        "statement": "Compute ∫₀¹ x·e^x dx.",
        "hint": "Integration by parts. Choose u=x, dv=eˣdx.",
        "solution": "u=x, dv=eˣdx → du=dx, v=eˣ. ∫xeˣdx = xeˣ−∫eˣdx = xeˣ−eˣ+C = eˣ(x−1)+C. [eˣ(x−1)]₀¹ = e·0−1·(−1) = 0+1=1.",
        "answer": "1.",
        "topics": ["Integrals", "Integration by parts"],
    },
    {
        "id": 50, "level": "Competitive", "chapter": 22,
        "statement": "Find the area enclosed between y=x² and y=x+2.",
        "hint": "Find where they intersect. The area is ∫|upper−lower|dx.",
        "solution": "Intersections: x²=x+2 → x²−x−2=0 → (x−2)(x+1)=0 → x=−1,2. Area=∫₋₁²(x+2−x²)dx=[x²/2+2x−x³/3]₋₁²=(2+4−8/3)−(1/2−2+1/3)=10/3+7/6=9/2.",
        "answer": "9/2.",
        "topics": ["Integrals", "Function Analysis"],
    },
    {
        "id": 51, "level": "Olympic", "chapter": 22,
        "statement": "Prove that ∫₀^∞ e^(−x²) dx = √π/2 using the standard squaring trick.",
        "hint": "Let I=∫₀^∞ e^(−x²)dx. Compute I² by converting to a double integral in polar coordinates.",
        "solution": "I²=(∫₀^∞ e^(−x²)dx)(∫₀^∞ e^(−y²)dy)=∫₀^∞∫₀^∞ e^(−(x²+y²))dxdy. Switch to polar (r,θ) with r≥0, θ∈[0,π/2]: I²=∫₀^(π/2)∫₀^∞ e^(−r²)r dr dθ=(π/2)·[−e^(−r²)/2]₀^∞=(π/2)·(1/2)=π/4. So I=√π/2. □",
        "answer": "∫₀^∞ e^(−x²)dx = √π/2. □",
        "topics": ["Integrals", "Proofs"],
    },
    {
        "id": 52, "level": "Olympic", "chapter": 22,
        "statement": "Compute ∫₀^(π/2) ln(sin x) dx.",
        "hint": "This is a classic result. Use the symmetry of sin and cos on [0,π/2] and the identity sin(2x)=2sin(x)cos(x).",
        "solution": "Let I=∫₀^(π/2) ln(sin x)dx = ∫₀^(π/2) ln(cos x)dx (by substitution x→π/2−x). So 2I=∫₀^(π/2) ln(sin x·cos x)dx=∫₀^(π/2) ln(sin(2x)/2)dx=∫₀^(π/2) ln(sin(2x))dx − (π/2)ln2. Substituting u=2x: ∫₀^π ln(sin u)du/2 = I − (π/2)ln2 (since ∫₀^π ln(sin u)du=2I). So 2I=I−(π/2)ln2 → I=−(π/2)ln2.",
        "answer": "∫₀^(π/2) ln(sin x)dx = −(π/2)ln2.",
        "topics": ["Integrals", "Trigonometry"],
    },

    # ── CROSS-CHAPTER (mixed) ─────────────────────────────────────────────────
    {
        "id": 53, "level": "Competitive",
        "chapter": None,
        "statement": "A sequence is defined by a₁=1, aₙ₊₁=aₙ+1/aₙ. Prove that a₂₀₂₃>63.",
        "hint": "Show that aₙ²≥2(n−1)+1=2n−1. Use induction.",
        "solution": "Claim: aₙ²≥2n−1. Base: a₁²=1=2·1−1 ✓. Step: aₙ₊₁²=(aₙ+1/aₙ)²=aₙ²+2+1/aₙ²≥aₙ²+2≥(2n−1)+2=2(n+1)−1 ✓. So a₂₀₂₃²≥2·2023−1=4045>3969=63². Thus a₂₀₂₃>63. □",
        "answer": "a₂₀₂₃ > 63. □",
        "topics": ["Sequences", "Mathematical Proofs"],
    },
    {
        "id": 54, "level": "Olympic",
        "chapter": None,
        "statement": "Prove that for any n≥1, the sum 1+1/2+1/3+…+1/n is never an integer (for n>1).",
        "hint": "Find the largest power of 2 not exceeding n. Show it divides the denominator of every term except one.",
        "solution": "Let 2^k be the largest power of 2 with 2^k≤n. Every term 1/m with m≠2^k has 2^(k+1)∤m or m<2^k, so when we write the sum over LCM, 2^k divides all denominators except for the term 1/2^k. The numerator of the sum would need 2^k to divide n!·Σ(1/m)−n!/2^k, but the latter term is odd, giving a half-integer sum. Formally this is done via 2-adic valuations. □",
        "answer": "Hₙ is not an integer for any n>1. □",
        "topics": ["Number Theory", "Sequences", "Proofs"],
    },
    {
        "id": 55, "level": "Olympic",
        "chapter": None,
        "statement": "Let f be continuous on [0,1] with ∫₀¹ f(x)dx=0. Prove that there exists c∈(0,1) with f(c)=0 OR there exist a,b∈(0,1) with a≠b and f(a)+f(b)=0.",
        "hint": "If f has no zero, it is either always positive or always negative. But then the integral cannot be zero.",
        "solution": "If f(c)=0 for some c, done. Otherwise f has constant sign on [0,1]. WLOG f>0 everywhere. Then ∫₀¹ f(x)dx>0, contradicting the assumption. So f must change sign — by IVT (Bolzano) there exists c with f(c)=0. Actually the problem as stated: the first condition already suffices by Bolzano. □",
        "answer": "By Bolzano's theorem applied to a sign-changing continuous function. □",
        "topics": ["Integrals", "Limits", "Mathematical Proofs"],
    },
]

LEVEL_ORDER = ["Rookie", "Competitive", "Olympic"]
LEVEL_COLORS = {
    "Rookie":      "#2d5a4e",
    "Competitive": "#a8893e",
    "Olympic":     "#c8602a",
}