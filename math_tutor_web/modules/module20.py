import math
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from itertools import combinations

import style


# ── Content ───────────────────────────────────────────────────────────────────

TECHNIQUE_CONTENT = {
    "Invariants & Monovariants": {
        "intro": """An <strong>invariant</strong> is a quantity that never changes under any allowed operation.<br><br>
If the initial state has invariant value X and the target has Y ≠ X → target is <strong>unreachable</strong>.<br><br>
A <strong>monovariant</strong> only moves in one direction (always increases or always decreases).
If it is bounded and always changes by ≥1, the process must terminate.""",
        "example": {
            "title": "Numbers on a board (1, 2, …, 2023): replace a,b with |a−b|. What remains?",
            "steps": [
                "Track the parity of the count of odd numbers.",
                "odd+odd→even: count −2 (parity preserved). odd+even→odd: count unchanged. even+even→even: count unchanged.",
                "Initial odd count = 1012 (odd numbers 1,3,5,…,2023). Parity: EVEN.",
                "One number remains → count is 1 (ODD) or 0 (EVEN). Since parity is EVEN, count = 0 → final number is EVEN.",
            ],
            "key": "Parity of the odd-count is invariant. One parity argument decides the result."
        }
    },
    "Parity & Colorings": {
        "intro": """<strong>Parity</strong> = the simplest invariant. Even/odd determines possibility.<br><br>
<strong>Colorings</strong> generalize parity: assign colors to elements so every valid operation
changes the color-count predictably.""",
        "example": {
            "title": "Can an 8×8 chessboard with two opposite corners removed be tiled by 31 dominoes?",
            "steps": [
                "Color the board like a chessboard (32 black, 32 white).",
                "Every domino covers exactly 1 black and 1 white square.",
                "31 dominoes need 31 black and 31 white squares.",
                "The two opposite corners have the SAME color → 30 of one, 32 of the other.",
                "30 ≠ 32 → tiling is IMPOSSIBLE. □",
            ],
            "key": "The coloring revealed a parity obstruction invisible to direct analysis."
        }
    },
    "Pigeonhole (advanced)": {
        "intro": """<strong>Basic:</strong> n+1 objects in n boxes → one box has ≥ 2.<br>
<strong>Generalized:</strong> m objects in n boxes → one box has ≥ ⌈m/n⌉.<br><br>
The hard part is <em>always</em>: identifying the correct objects and boxes.""",
        "example": {
            "title": "Among any n integers, some non-empty subset has sum divisible by n.",
            "steps": [
                "Consider partial sums S₁=a₁, S₂=a₁+a₂, …, Sₙ=a₁+…+aₙ.",
                "Case 1: some Sₖ ≡ 0 (mod n) → done.",
                "Case 2: all Sₖ have remainders in {1,…,n−1} — only n−1 boxes, n objects.",
                "By Pigeonhole: Sᵢ ≡ Sⱼ (mod n) for some i<j → aᵢ₊₁+…+aⱼ ≡ 0 (mod n). □",
            ],
            "key": "The partial sums were the objects. The boxes were residues mod n."
        }
    },
    "Infinite Descent": {
        "intro": """Suppose a solution exists. Show any solution generates a <strong>strictly smaller</strong> solution.
This creates an infinite decreasing sequence of positive integers — impossible.<br><br>
Used to prove equations have NO solutions, or only (0,0,…,0).""",
        "example": {
            "title": "√2 is irrational (descent version).",
            "steps": [
                "Suppose p²=2q² for positive integers p,q. Take p minimal.",
                "p²=2q² → p even → p=2k → 4k²=2q² → q²=2k² → q even.",
                "(k,m) with k=p/2 is a smaller solution → contradicts minimality. □",
            ],
            "key": "Any solution generates a smaller one → no solution exists."
        }
    },
    "Double Counting": {
        "intro": """Count the same set in two different ways.<br>
Both counts equal the same number → setting them equal gives a non-trivial identity or bound.""",
        "example": {
            "title": "Prove Σ C(n,k)² = C(2n,n).",
            "steps": [
                "Count n-element subsets of {1,…,2n}.",
                "Split into A={1,…,n} and B={n+1,…,2n}.",
                "Every subset has k from A and n−k from B: count C(n,k)·C(n,n−k) = C(n,k)².",
                "Summing over k: C(2n,n) = Σ C(n,k)². □",
            ],
            "key": "Counting the same set two ways gave a beautiful identity."
        }
    },
    "Extremal Principle": {
        "intro": """Consider the object that <strong>maximizes or minimizes</strong> some quantity.<br>
Extreme objects have special properties: if they could be 'improved', they wouldn't be extreme.<br>
This extra constraint often makes the proof work.""",
        "example": {
            "title": "Every graph with min degree ≥ 2 has a cycle.",
            "steps": [
                "Take the LONGEST PATH P = v₁−v₂−…−vₖ.",
                "v₁ has degree ≥ 2, so it has a neighbor besides v₂.",
                "That neighbor must be ON the path (otherwise we could extend P — contradicting maximality).",
                "Say v₁ connects to vⱼ, j>2 → v₁−v₂−…−vⱼ−v₁ is a cycle. □",
            ],
            "key": "The longest path cannot be extended → any extra neighbor creates a cycle."
        }
    },
}

OLYMPIAD_PROBLEMS = [
    {
        "title": "5 | n⁵−n for all n∈ℤ",
        "analysis": "Fermat's Little Theorem: n⁵≡n (mod 5) for all n.<br>Or: cases mod 5, or factor n⁵−n=n(n−1)(n+1)(n²+1).",
        "proof": "Version 1 (FLT): By Fermat's Little Theorem, n⁵≡n (mod 5). Therefore 5|n⁵−n. □\n\nVersion 2 (cases): n≡0,1,2,3,4 (mod 5). Check each: 0,0,0,0,0. All ≡0. □\n\nVersion 3 (factor): n⁵−n=n(n−1)(n+1)(n²+1). If none of n−1,n,n+1 is divisible by 5, then n≡2 or 3 (mod 5), so n²+1≡0 (mod 5). □",
        "reflection": "FLT gives a one-line proof. Cases give elementary verification. Both are valid."
    },
    {
        "title": "√n + √(n+1) is irrational for n≥1",
        "analysis": "Suppose the sum is rational r. The conjugate (√(n+1)−√n) = 1/r is also rational. Then both √n and √(n+1) are rational. Two consecutive integers can't both be perfect squares for n≥1.",
        "proof": "Suppose √n+√(n+1)=r∈ℚ.\n(√(n+1)−√n)(√(n+1)+√n)=1 → √(n+1)−√n=1/r∈ℚ.\nAdding: 2√(n+1)=r+1/r → √(n+1)∈ℚ → n+1 is a perfect square.\nSubtracting: 2√n=r−1/r → √n∈ℚ → n is a perfect square.\nSo n=a², n+1=b² → b²−a²=1 → (b−a)(b+a)=1 → a=0, n=0. Contradicts n≥1. □",
        "reflection": "Key trick: multiply by conjugate √(n+1)−√n to get 1/(√n+√(n+1))."
    },
    {
        "title": "6 | n³−n for all n∈ℤ",
        "analysis": "Factor: n³−n=(n−1)n(n+1) — three consecutive integers. Among three consecutive: at least one divisible by 2, exactly one by 3.",
        "proof": "n³−n=(n−1)n(n+1).\n2|(n−1)n(n+1): among n−1 and n (consecutive), one is even. ✓\n3|(n−1)n(n+1): remainders mod 3 are 0,1,2 in some order → one is 0. ✓\ngcd(2,3)=1 → 6|(n−1)n(n+1). □",
        "reflection": "Always factor before choosing a technique. Once you see three consecutive integers, the proof writes itself."
    },
    {
        "title": "Tournament: among 100 players, transitive triples exist",
        "analysis": "Let wᵢ=wins of player i. Σwᵢ=C(100,2)=4950. Count transitive triples by double counting: player i is top of C(wᵢ,2) triples. Show Σ C(wᵢ,2)>0.",
        "proof": "Total transitive triples = Σ C(wᵢ,2) (player i beats the other two).\nΣwᵢ=4950, average=49.5. By convexity of C(·,2):\nΣ C(wᵢ,2) ≥ 100·C(49,2) = 100·1176 = 117600 > 0. □",
        "reflection": "Double counting turned 'do they exist?' into 'is this sum positive?' — much easier."
    },
    {
        "title": "Pigeonhole: subset sum divisible by n",
        "analysis": "Objects: partial sums S₁,...,Sₙ. Boxes: residues mod n (only n−1 if none is 0). Two sums with same residue → their difference is a subset sum ≡0.",
        "proof": "Let a₁,...,aₙ∈ℤ. Partial sums Sₖ=a₁+...+aₖ.\nIf some Sₖ≡0: done.\nOtherwise: n partial sums, n−1 possible non-zero residues → Sᵢ≡Sⱼ (mod n), i<j → aᵢ₊₁+...+aⱼ≡0 (mod n). □",
        "reflection": "Pigeonhole on partial sums — a standard but non-obvious trick."
    },
]

def verify_problems():
    """Compute numerical verifications"""
    results = {}
    # 5 | n^5-n
    results["5_div"] = [(n, n**5-n, (n**5-n)%5==0) for n in range(-3,6)]
    # 6 | n^3-n
    results["6_div"] = [(n, n**3-n, (n**3-n)%6==0) for n in range(-4,6)]
    # tournament
    results["tournament"] = (100*math.comb(49,2), math.comb(100,3))
    # sqrt irrationality
    results["sqrt"] = [(n, math.sqrt(n)+math.sqrt(n+1)) for n in range(1,6)]
    return results


# ── Section renderers ─────────────────────────────────────────────────────────

def render_method():
    style.step("How to read a problem — three passes", """
<strong>FIRST READ</strong> — understand what's happening. Don't think about the solution yet.
What objects are involved? What are the rules? What does a typical instance look like?<br><br>

<strong>SECOND READ</strong> — extract structure:<br>
· GIVEN: what is fixed / assumed<br>
· GOAL: what must be proved or found<br>
· TYPE: 'prove that', 'find all', or 'find the maximum'?<br><br>

<strong>THIRD READ</strong> — look for hidden structure. Symmetries? Extreme cases?
What happens with the simplest input?<br><br>

<strong>Problem types → strategies:</strong><br>
'Prove ∀n' → induction or invariant. 'Find all integers' → mod arithmetic then check.
'Among n objects, two share P' → pigeonhole. 'Max/min value' → prove bound + show it's achievable (both parts!).
'Does X exist?' → construct one, or assume it exists and derive contradiction.
    """, "warm")

    style.step("From conjecture to proof — three steps", """
<strong>Step 1:</strong> State the conjecture precisely.<br>
Vague: 'the expression seems divisible by 6'<br>
Precise: 'for all integers n, 6 | n³−n'<br><br>

<strong>Step 2:</strong> Identify the logical form (Module 19 tools).<br>
'For all n' → introduce arbitrary n, or induction.<br>
'There exists' → exhibit one.<br>
'Iff' → prove both directions.<br><br>

<strong>Step 3:</strong> Extract the key insight from small cases.<br>
Ask: WHY does this work for n=3? The common reason across all cases IS the proof.""")

    style.step("How to write an olympiad solution", """
<strong>Structure every solution:</strong><br>
1. <strong>CLAIM</strong> — state what you will prove<br>
2. <strong>SETUP</strong> — define notation<br>
3. <strong>PROOF</strong> — each sentence follows from the previous<br>
4. <strong>CONCLUSION</strong> — 'Therefore [claim]. □' Never trail off.<br><br>

<strong>Five fatal mistakes:</strong><br>
1. Examples instead of proof ('For n=1: works...' → 0 points)<br>
2. 'Clearly' and 'obviously' — if it were obvious, it wouldn't be in the problem<br>
3. Assuming what you want to prove (circular reasoning)<br>
4. Proving the converse instead of the statement<br>
5. Missing cases — graders look specifically for these""", "warm")

    # Small cases demo
    style.step("Small cases for 6|n³−n", "")
    rows="".join(
        f"n={n}: n³−n={n**3-n}, ÷6={( n**3-n)//6 if (n**3-n)%6==0 else 'not exact'} {'✓' if (n**3-n)%6==0 else '✗'}<br>"
        for n in range(-4,6))
    style.step("Numerical verification", rows, "sage")


def render_technique(name):
    if name not in TECHNIQUE_CONTENT:
        return
    t = TECHNIQUE_CONTENT[name]
    style.step(name, t["intro"], "warm")
    ex = t["example"]
    style.step(f"Example: {ex['title']}", "")
    for i,s in enumerate(ex["steps"]):
        style.step(f"Step {i+1}", s)
    style.step("Key insight", ex["key"], "sage")


def render_number_theory():
    style.step("Modular arithmetic — key tools", """
<strong>Choosing the right modulus:</strong><br>
mod 2 → parity · mod 4 → squares are 0 or 1 · mod 8 → squares are 0,1,4<br>
mod 3 → digit sum · mod 9 → n² mod 9 ∈ {0,1,4,7}<br><br>
<strong>Fermat's Little Theorem:</strong> if p prime, gcd(a,p)=1 → a^(p−1)≡1 (mod p)<br>
→ p|n⁵−n for p=5 (one-line proof)<br><br>
<strong>Order of a mod p:</strong> smallest d with aᵈ≡1 (mod p); always divides p−1<br>
→ aᵏ≡1 (mod p) iff ord(a)|k<br><br>
<strong>Wilson's theorem:</strong> (p−1)!≡−1 (mod p) for any prime p""", "warm")

    # Squares mod table
    rows = ""
    for r in range(5):
        mods = " &nbsp;·&nbsp; ".join(f"mod {m}: {r**2%m}" for m in [4,8,9,5,7])
        rows += f"r={r}: {mods}<br>"
    style.step("Squares mod small numbers", rows)

    style.step("Diophantine equations — strategies", """
1. <strong>Modular arithmetic</strong> — eliminate impossible cases<br>
2. <strong>Factoring</strong> — write as product of two factors<br>
3. <strong>Bounding</strong> — show solutions must be small, then check<br>
4. <strong>Infinite descent</strong> — any solution gives a smaller one<br><br>
<strong>Example:</strong> x²−y²=2023<br>
Factor: (x+y)(x−y)=2023=7·17²<br>
Enumerate factor pairs with same parity: x=(a+b)/2, y=(b−a)/2 for each a·b=2023""", "sage")


def render_combinatorics():
    style.step("Inclusion-Exclusion", """
|A∪B| = |A|+|B|−|A∩B|<br>
|A∪B∪C| = |A|+|B|+|C|−|A∩B|−|A∩C|−|B∩C|+|A∩B∩C|<br><br>
Pattern: +individuals −pairs +triples −quadruples ...<br><br>
<strong>Derangements:</strong> D(n) = n!·Σ(−1)ᵏ/k! ≈ n!/e<br>
About 1/e ≈ 36.8% of all permutations have no fixed points.""", "warm")

    # verify derangements
    rows=""
    inv_e=1/math.e
    for n in range(1,8):
        fact=math.factorial(n)
        dn=sum((-1)**k*fact//math.factorial(k) for k in range(n+1))
        rows+=f"n={n}: D(n)={dn}, n!={fact}, D(n)/n!={dn/fact:.4f} ≈ 1/e={inv_e:.4f}<br>"
    style.step("Derangement table", rows)

    style.step("Graph theory basics", """
<strong>Handshake lemma:</strong> Σdeg(v) = 2|E| → odd-degree vertices always even in number.<br><br>
<strong>Trees:</strong> connected, no cycles, n vertices → exactly n−1 edges.<br><br>
<strong>Bipartite:</strong> 2-colorable iff no odd cycles.<br><br>
<strong>Tournaments:</strong> every tournament on n vertices has a Hamiltonian path.<br>
Proof by induction: insert each new vertex at the right position in the existing path.""", "sage")

    # combinatorial identities
    style.step("Key combinatorial identities", """
<strong>Pascal:</strong> C(n,k) = C(n−1,k−1)+C(n−1,k) — count by whether n is included<br>
<strong>Vandermonde:</strong> C(m+n,r) = ΣC(m,k)·C(n,r−k)<br>
<strong>Row sum:</strong> Σ C(n,k) = 2ⁿ — all subsets<br>
<strong>Alternating:</strong> Σ(−1)ᵏC(n,k) = 0 for n≥1<br>
<strong>Hockey stick:</strong> ΣC(r+k,k) k=0..n = C(r+n+1,n)""")


def render_olympiad(idx):
    if idx >= len(OLYMPIAD_PROBLEMS):
        return
    p = OLYMPIAD_PROBLEMS[idx]
    style.step(f"Problem: {p['title']}", "", "warm")
    style.step("Analysis — how to find the approach",
               p["analysis"].replace("\n","<br>"))
    style.step("Complete proof",
        f'<pre style="font-family:\'DM Mono\',monospace;font-size:0.8rem;'
        f'background:var(--bg2);border-radius:4px;padding:0.5rem;white-space:pre-wrap;">'
        f'{p["proof"]}</pre>')
    style.step("Reflection", p["reflection"].replace("\n","<br>"), "sage")

    # Numerical verification where applicable
    v = verify_problems()
    if idx == 0:  # 5|n^5-n
        rows="".join(f"n={n}: n⁵−n={val} {'✓' if ok else '✗'}<br>" for n,val,ok in v["5_div"])
        style.step("Verify", rows)
    elif idx == 2:  # 6|n^3-n
        rows="".join(f"n={n}: n³−n={val} {'✓' if ok else '✗'}<br>" for n,val,ok in v["6_div"])
        style.step("Verify", rows)
    elif idx == 3:  # tournament
        total, triples = v["tournament"]
        style.step("Verify",
            f"Min transitive triples = 100·C(49,2) = {total:,}<br>"
            f"Total triples C(100,3) = {triples:,}<br>"
            f"At least {total/triples*100:.1f}% of triples are transitive!")
    elif idx == 1:  # sqrt irrational
        rows="".join(f"n={n}: √n+√(n+1) = {val:.8f} (irrational ✓)<br>" for n,val in v["sqrt"])
        style.step("Verify", rows)


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose section</div>',
                    unsafe_allow_html=True)

        section = st.selectbox("Section",
            ["1 — The Olympic Method",
             "2 — Olympic Techniques",
             "3 — Olympic Number Theory",
             "4 — Olympic Combinatorics",
             "5 — Solved Problems"],
            key="ol_section")

        if section.startswith("2"):
            tech = st.selectbox("Technique",
                list(TECHNIQUE_CONTENT.keys()), key="ol_tech")

        if section.startswith("5"):
            prob = st.selectbox("Problem",
                [f"{i+1}. {p['title']}" for i,p in enumerate(OLYMPIAD_PROBLEMS)],
                key="ol_prob")
            pidx = int(prob.split(".")[0]) - 1

        go_btn = st.button("Read →", key="ol_go")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">About this module</div>
  <div class="hint-body">
    Olympic math is about thinking,<br>not just knowing formulas.<br><br>
    The gap between 'I'm sure it's true'<br>and 'I can write a proof'<br>is where olympiad scores are decided.<br><br>
    This module bridges that gap.
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if go_btn:
            if section.startswith("1"):
                render_method()
            elif section.startswith("2"):
                render_technique(tech)
            elif section.startswith("3"):
                render_number_theory()
            elif section.startswith("4"):
                render_combinatorics()
            else:
                render_olympiad(pidx)
        else:
            style.step("Olympic Mathematics",
                """Olympic mathematics is a different game from school math.<br>
At school you know the topic before you start.<br>
At olympiads you face problems you've never seen.<br><br>
The question isn't 'do you know the formula?'<br>
It's 'can you think?'<br><br>
Choose a section on the left and press Read →""",
                "warm")