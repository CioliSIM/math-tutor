# matches.py — problem bank for the Matches section

PROBLEMS = [
    # ── ROOKIE ──────────────────────────────────────────────────────────────
    {
        "id": 1, "level": "Rookie",
        "statement": "Find all integers n such that n² − n is divisible by 6.",
        "hint": "Try small values first. Then ask: what are the possible remainders of n when divided by 6?",
        "solution": "n²−n = n(n−1), the product of two consecutive integers. One is always even (divisible by 2) and among any two consecutive integers one is divisible by... wait — we need 6 = 2·3. Among three consecutive integers n−1, n, n+1, one is divisible by 3. But here we only have two. Try: n(n−1) mod 2 = 0 always. For divisibility by 3: check n ≡ 0,1,2 mod 3. In all cases 3 | n(n−1). Therefore 6 | n(n−1) for all integers n.",
        "answer": "All integers n.",
        "topics": ["Number Theory", "Modular arithmetic"],
    },
    {
        "id": 2, "level": "Rookie",
        "statement": "A function f satisfies f(x+1) = f(x) + 2x + 1 for all real x, and f(0) = 0. Find f(n) for positive integers n.",
        "hint": "Compute f(1), f(2), f(3) by applying the rule repeatedly. Look for a pattern.",
        "solution": "f(1)=f(0)+1=1, f(2)=f(1)+3=4, f(3)=f(2)+5=9, f(4)=16. The pattern is f(n)=n². Proof by induction: f(n+1)=f(n)+2n+1=n²+2n+1=(n+1)².",
        "answer": "f(n) = n²",
        "topics": ["Sequences", "Induction"],
    },
    {
        "id": 3, "level": "Rookie",
        "statement": "Prove that for any real number x, the value of x² − x + 1 is always positive.",
        "hint": "Can you write x²−x+1 in a form that makes its sign obvious?",
        "solution": "Complete the square: x²−x+1 = (x−½)² + ¾. Since (x−½)² ≥ 0 for all real x, we have x²−x+1 ≥ ¾ > 0.",
        "answer": "x²−x+1 = (x−½)²+¾ > 0 for all x∈ℝ.",
        "topics": ["Quadratic Equations", "Proofs"],
    },
    {
        "id": 4, "level": "Rookie",
        "statement": "In a class of 30 students, each student shakes hands with every other student exactly once. How many handshakes occur in total?",
        "hint": "Think about how many handshakes each student makes. Be careful not to count each handshake twice.",
        "solution": "Each of the 30 students shakes hands with 29 others: 30·29 = 870. But each handshake is counted twice (once for each participant), so the total is 870/2 = 435. Equivalently: C(30,2) = 30!/(2!·28!) = 435.",
        "answer": "435 handshakes.",
        "topics": ["Combinatorics"],
    },
    {
        "id": 5, "level": "Rookie",
        "statement": "The sum of three consecutive integers is 99. What are they?",
        "hint": "Call the middle integer n. What are the other two?",
        "solution": "Let the integers be n−1, n, n+1. Their sum: (n−1)+n+(n+1) = 3n = 99, so n = 33. The integers are 32, 33, 34.",
        "answer": "32, 33, 34.",
        "topics": ["Algebra", "Systems"],
    },

    # ── COMPETITIVE ──────────────────────────────────────────────────────────
    {
        "id": 6, "level": "Competitive",
        "statement": "Find all pairs of positive integers (a, b) such that a² + b² = a²b².",
        "hint": "Divide both sides by a²b². What familiar identity do you see?",
        "solution": "Divide by a²b²: 1/b² + 1/a² = 1. Let x=1/a², y=1/b². Then x+y=1 with x,y>0 and x=1/a²≤1, y=1/b²≤1. Since a,b are positive integers, a,b≥1, so 1/a²≤1. For x+y=1 with x=1/a²: 1/a²+1/b²=1. If a=1: 1+1/b²=1 → 1/b²=0, impossible. If a=2: 1/4+1/b²=1 → 1/b²=3/4 → b²=4/3, not integer. No solution exists for a,b≥2 since 1/a²+1/b²≤1/4+1/4=1/2<1. Therefore there are no pairs.",
        "answer": "No pairs of positive integers satisfy the equation.",
        "topics": ["Number Theory", "Algebra"],
    },
    {
        "id": 7, "level": "Competitive",
        "statement": "Prove that among any 5 integers, there exist two whose difference is divisible by 4.",
        "hint": "What are the possible remainders when an integer is divided by 4? How many are there?",
        "solution": "Every integer has remainder 0, 1, 2, or 3 when divided by 4 — only 4 possibilities. With 5 integers and 4 boxes (by pigeonhole), at least two integers aᵢ, aⱼ fall in the same box, meaning aᵢ ≡ aⱼ (mod 4). Therefore 4 | (aᵢ−aⱼ).",
        "answer": "By the Pigeonhole Principle, two of the 5 integers share a remainder mod 4.",
        "topics": ["Number Theory", "Pigeonhole", "Proofs"],
    },
    {
        "id": 8, "level": "Competitive",
        "statement": "A ball is dropped from height h = 100 m. Each time it bounces, it reaches 2/3 of its previous height. What is the total distance traveled by the ball?",
        "hint": "The ball travels down, then up, then down, then up... Write the total as a sum. Recognize the type of series.",
        "solution": "First fall: 100 m. Then up 200/3, down 200/3, up 400/9, down 400/9, … Total after first fall: 100 + 2·(100·2/3 + 100·(2/3)² + …) = 100 + 2·(100·2/3)/(1−2/3) = 100 + 2·(200/3)/(1/3) = 100 + 2·200 = 100 + 400 = 500 m.",
        "answer": "500 metres.",
        "topics": ["Sequences", "Geometric series"],
    },
    {
        "id": 9, "level": "Competitive",
        "statement": "For which real values of k does the equation x² + kx + 1 = 0 have two distinct real roots, both negative?",
        "hint": "Two conditions must hold simultaneously. What does the discriminant tell you? What does the sum and product of roots tell you?",
        "solution": "For two distinct real roots: Δ = k²−4 > 0 → k>2 or k<−2. For both roots negative: sum = −k < 0 → k > 0; product = 1 > 0 ✓ (already satisfied). Combining: k>2 and k>0 → k>2. Or k<−2 and k>0 → impossible. Answer: k>2.",
        "answer": "k > 2.",
        "topics": ["Quadratic Equations", "Proofs"],
    },
    {
        "id": 10, "level": "Competitive",
        "statement": "Let f(x) = x³ − 3x. Find all local maxima and minima, and determine on which intervals f is increasing.",
        "hint": "You need the derivative. Then analyze its sign. This combines two techniques.",
        "solution": "f'(x) = 3x²−3 = 3(x−1)(x+1). Critical points: x=−1 (f'changes + to −, local max, f(−1)=2) and x=1 (f' changes − to +, local min, f(1)=−2). Increasing on (−∞,−1) and (1,+∞). Decreasing on (−1,1).",
        "answer": "Local max at (−1, 2). Local min at (1, −2). Increasing for x<−1 and x>1.",
        "topics": ["Derivatives", "Function Analysis"],
    },

    # ── OLYMPIC ──────────────────────────────────────────────────────────────
    {
        "id": 11, "level": "Olympic",
        "statement": "Prove that for every integer n ≥ 1, the number n⁵ − n is divisible by 30.",
        "hint": "30 = 2·3·5. Can you show divisibility by each prime separately? For the prime 5, there is a very elegant one-line argument.",
        "solution": "30=2·3·5. Factor: n⁵−n=n(n⁴−1)=n(n²−1)(n²+1)=(n−1)n(n+1)(n²+1). Div by 2: (n−1)n is a product of consecutive integers, one even. Div by 3: among n−1,n,n+1, one is div by 3. Div by 5: by Fermat's Little Theorem, n⁵≡n (mod 5) for all n, so 5|n⁵−n. Since gcd(2,3,5)=1 pairwise, 30|n⁵−n.",
        "answer": "30 | n⁵−n for all integers n.",
        "topics": ["Number Theory", "Proofs", "Olympic Mathematics"],
    },
    {
        "id": 12, "level": "Olympic",
        "statement": "Find all functions f: ℝ→ℝ such that f(x+y) = f(x) + f(y) for all real x, y, and f(1) = 1.",
        "hint": "Start with specific values: f(0), f(2), f(n) for integers. Then extend to rationals. What can you say about f(x) for any rational x?",
        "solution": "f(0): f(0+0)=f(0)+f(0)→f(0)=0. f(n) for n∈ℕ: by induction f(n)=nf(1)=n. f(−1): f(1)+f(−1)=f(0)=0→f(−1)=−1. So f(n)=n for all integers. f(p/q): qf(p/q)=f(p)=p→f(p/q)=p/q. For rationals: f(x)=x. Without continuity, other solutions exist (using axiom of choice). With continuity (or monotonicity): f(x)=x for all x∈ℝ.",
        "answer": "f(x) = x for all x∈ℝ (assuming continuity or monotonicity).",
        "topics": ["Functions", "Proofs", "Olympic Mathematics"],
    },
    {
        "id": 13, "level": "Olympic",
        "statement": "In a tournament with n players where each pair plays exactly once (no draws), prove that there always exists a player who beat at least half of the remaining players.",
        "hint": "Consider the player with the most wins. What can you say about their win count?",
        "solution": "Let wₘₐₓ be the maximum number of wins. Total games = C(n,2). Total wins = C(n,2). Average wins per player = (n−1)/2. The player with the most wins has wₘₐₓ ≥ average = (n−1)/2. So wₘₐₓ ≥ ⌈(n−1)/2⌉ ≥ (n−1)/2. This player beat at least (n−1)/2 opponents, which is at least half of the remaining n−1 players.",
        "answer": "The player with the most wins beat at least ⌊(n−1)/2⌋ opponents.",
        "topics": ["Combinatorics", "Proofs", "Olympic Mathematics"],
    },
    {
        "id": 14, "level": "Olympic",
        "statement": "Prove that √2 + √3 is irrational.",
        "hint": "Suppose it is rational. Square it. Use what you know about √6.",
        "solution": "Suppose √2+√3=r∈ℚ. Square: 2+2√6+3=r²→√6=(r²−5)/2∈ℚ. But √6 is irrational (proof: if √6=p/q reduced, then 6q²=p²→2|p→p=2k→6q²=4k²→3q²=2k²→2|q, contradicting gcd(p,q)=1). Contradiction. Therefore √2+√3 is irrational.",
        "answer": "√2+√3 is irrational.",
        "topics": ["Number Theory", "Proofs", "Olympic Mathematics"],
    },
    {
        "id": 15, "level": "Olympic",
        "statement": "Let p be a prime and a an integer not divisible by p. Prove that the sequence a, a², a³, … (mod p) is eventually periodic, and find the period.",
        "hint": "There are only p−1 non-zero residues mod p. What does this force?",
        "solution": "The sequence aᵏ mod p takes values in {1,2,…,p−1} (since gcd(a,p)=1 means aᵏ≢0). There are only p−1 possible values. By pigeonhole, aⁱ≡aʲ (mod p) for some i<j≤p. Since gcd(a,p)=1, we can cancel: aʲ⁻ⁱ≡1 (mod p). So the sequence is periodic. The period is ord_p(a), the smallest d≥1 with aᵈ≡1 (mod p). By Fermat's Little Theorem, d | p−1.",
        "answer": "The sequence is periodic with period ord_p(a), which divides p−1.",
        "topics": ["Number Theory", "Proofs", "Olympic Mathematics"],
    },
]

LEVEL_ORDER = ["Rookie", "Competitive", "Olympic"]
LEVEL_COLORS = {
    "Rookie":      "#2d5a4e",
    "Competitive": "#a8893e",
    "Olympic":     "#c8602a",
}