import math
import streamlit as st

import style


# ── Content data ──────────────────────────────────────────────────────────────

CONNECTIVES = """
<strong>NOT (¬)</strong><br>
¬P is true exactly when P is false.<br>
"n is NOT even" = "n is odd"<br><br>

<strong>AND (∧)</strong><br>
P��Q is true only when BOTH P and Q are true.<br>
"n is even AND n>10" — both conditions required.<br><br>

<strong>OR (∨)</strong><br>
P��Q is true when at least one holds. In mathematics, OR is always INCLUSIVE.<br><br>

<strong>IF-THEN (→) — the most important connective in proofs</strong><br>
P��Q means: whenever P is true, Q must be true.<br>
FALSE only in ONE case: P true but Q false.<br><br>

Truth table for P→Q:<br>
<code>P=T, Q=T → T &nbsp; P=T, Q=F → F (only failure!)</code><br>
<code>P=F, Q=T → T &nbsp; P=F, Q=F → T (vacuous truth)</code><br><br>

<strong>Vacuous truth:</strong> when P is false, P→Q is always true.<br>
"If 1=2 then I am a dinosaur" — technically true.<br>
The promise was never triggered.<br><br>

<strong>IFF (↔)</strong><br>
P��Q is true when P and Q always have the same truth value.<br><br>

<strong>Four forms of P→Q:</strong><br>
Original: P→Q &nbsp;&nbsp; Converse: Q→P<br>
Contrapositive: ¬Q→¬P &nbsp;&nbsp; Inverse: ¬P→¬Q<br><br>

<strong>CRUCIAL:</strong> P→Q ≡ ¬Q→¬P (contrapositive). They say the same thing.<br>
The CONVERSE is NOT equivalent. Confusing these is a very common error.
"""

QUANTIFIERS_CONTENT = """
<strong>∀ (for all, for every)</strong><br>
∀x P(x): P(x) is true for EVERY possible x.<br><br>
To <strong>prove</strong> ∀x P(x): introduce an ARBITRARY x. Prove P(x).<br>
To <strong>disprove</strong>: find ONE counterexample where P(x) fails.<br><br>

Example: ∀n∈ℤ, n²≥0<br>
Let n be any integer. If n≥0: n²=n·n≥0. If n&lt;0: n²=(-n)(-n)≥0. □<br><br>

<strong>∃ (there exists)</strong><br>
∃x P(x): at least ONE x satisfies P(x).<br><br>
To <strong>prove</strong>: exhibit a specific x₀ and verify P(x₀).<br>
To <strong>disprove</strong>: show P(x) is false for ALL x (harder).<br><br>

Example: ∃n∈ℤ, n²=n<br>
Take n=1. Then n²=1=n. □ (n=0 also works)<br><br>

<strong>Negating quantifiers (De Morgan for quantifiers):</strong><br>
¬(∀x P(x)) ≡ ∃x ¬P(x) — "Not everyone passed" = "Someone failed"<br>
¬(∃x P(x)) ≡ ∀x ¬P(x) — "Nobody passed" = "Everyone failed"<br><br>

<strong>Order matters:</strong><br>
∀x ∃y (y>x): TRUE — for any x, take y=x+1.<br>
∃y ∀x (y>x): FALSE — no largest number exists.<br>
Same words, completely different meaning.<br><br>

<strong>Unique existence ∃!</strong><br>
∃!x P(x): exactly ONE x satisfies P(x).<br>
Prove: (1) existence — find one x. (2) uniqueness — if P(x) and P(y), then x=y.
"""

GOAL_TABLE = [
    ("P ∧ Q (AND)", "Split into two subgoals. Prove P, then prove Q.",
     "We show two things:\n(i)  P: [proof]\n(ii) Q: [proof]\nTherefore P∧Q. □"),
    ("P ∨ Q (OR)", "Either prove P directly, or assume ¬P and prove Q.",
     "Suppose ¬P.\n[derive Q from ¬P and givens]\nTherefore P∨Q. □"),
    ("P → Q (IF-THEN)", "Assume P. Add to givens. Prove Q.",
     "Suppose P.\n[steps using P]\nTherefore Q. □"),
    ("P ↔ Q (IFF)", "Prove P→Q, then prove Q→P. Two separate proofs.",
     "(→) Suppose P. [steps] Therefore Q.\n(←) Suppose Q. [steps] Therefore P. □"),
    ("∀x P(x) (FOR ALL)", "Let x be an arbitrary element. Prove P(x).",
     "Let x be arbitrary.\n[prove P(x)]\nSince x was arbitrary, ∀x P(x). □"),
    ("∃x P(x) (THERE EXISTS)", "Exhibit a specific x₀. Verify P(x₀).",
     "Let x₀ = [value].\nThen P(x₀): [verification]. □"),
    ("¬P (NEGATION)", "Assume P and derive a contradiction.",
     "Suppose for contradiction that P.\n[steps leading to contradiction]\nContradiction. Therefore ¬P. □"),
]

TECHNIQUES = {
    "Direct proof": {
        "when": "The most natural strategy. Try this first.",
        "template": "Suppose P.\n[steps]\nTherefore Q. □",
        "examples": [
            ("If n is even, then n² is even.",
             "Suppose n is even. Then n=2k for some k.\nn²=(2k)²=4k²=2(2k²). Since 2k²∈ℤ, n² is even. □"),
        ]
    },
    "Contrapositive": {
        "when": "When ¬Q gives more to work with than P. When direct proof feels stuck.",
        "template": "We prove the contrapositive.\nSuppose ¬Q.\n[steps]\nTherefore ¬P. □",
        "examples": [
            ("If n² is odd, then n is odd.",
             "Contrapositive: if n is even, then n² is even.\nSuppose n=2k. Then n²=4k²=2(2k²) is even. □"),
        ]
    },
    "Contradiction": {
        "when": "Proving non-existence, irrationality, or infinitely many things.",
        "template": "Suppose for contradiction that ¬P.\n[steps]\nBut this contradicts [something].\nTherefore P. □",
        "examples": [
            ("√2 is irrational.",
             "Suppose √2=p/q in lowest terms (gcd(p,q)=1).\nThen p²=2q² → p even → p=2k → q²=2k² → q even.\nBut 2|p and 2|q contradicts gcd(p,q)=1. □"),
            ("There are infinitely many primes.",
             "Suppose finitely many: p₁,...,pₙ.\nN=p₁·...·pₙ+1 has a prime factor p=pᵢ.\npᵢ|N and pᵢ|p₁·...·pₙ → pᵢ|1. Impossible. □"),
        ]
    },
    "Cases": {
        "when": "The situation naturally breaks into scenarios.",
        "template": "We consider [n] cases.\nCase 1: ...\n  [proof]\nCase 2: ...\n  [proof]\nIn all cases, [conclusion]. □",
        "examples": [
            ("For all n∈ℤ, n²+n is even.",
             "Case 1: n=2k. n²+n=4k²+2k=2(2k²+k). Even.\nCase 2: n=2k+1. n²+n=4k²+6k+2=2(2k²+3k+1). Even. □"),
        ]
    },
    "Induction": {
        "when": "Proving ∀n∈ℕ P(n) — universal over natural numbers.",
        "template": "Base case: [prove P(0)]\nInductive step:\n  Suppose P(k). [inductive hypothesis]\n  [prove P(k+1) using P(k)]\nBy induction, ∀n P(n). □",
        "examples": [
            ("1+2+...+n = n(n+1)/2.",
             "Base: n=1: left=1, right=1·2/2=1. ✓\nStep: assume 1+...+k=k(k+1)/2.\n1+...+k+(k+1)=k(k+1)/2+(k+1)=(k+1)(k+2)/2. □"),
            ("For all n≥0, 3|(n³−n).",
             "Base: 0³−0=0=3·0. ✓\nStep: (k+1)³−(k+1)=(k³−k)+3k(k+1).\n3|(k³−k) by IH. 3|3k(k+1) obviously. □"),
        ]
    },
}

OLYMPIAD_PROBLEMS = [
    {
        "title": "6 | n³−n for all n∈ℤ",
        "analysis": "Factor: n³−n=(n−1)n(n+1) — product of three consecutive integers.\nAmong three consecutive: at least one divisible by 2, exactly one by 3.\nSo the product is divisible by both 2 and 3, hence by 6.",
        "proof": "Let n be arbitrary. Note n³−n=(n−1)n(n+1).\n\n2|(n−1)n(n+1): among n−1 and n (consecutive), one is even. ✓\n\n3|(n−1)n(n+1): every integer ≡ 0,1, or 2 (mod 3).\n  n≡0 → 3|n. n≡1 → 3|(n−1). n≡2 → 3|(n+1). ✓\n\nSince 2 and 3 both divide (n−1)n(n+1) and gcd(2,3)=1,\nwe have 6|(n³−n). □",
        "reflection": "Key: FACTOR before choosing a technique.\nOnce you see (n−1)n(n+1), the proof is obvious."
    },
    {
        "title": "√2 is irrational",
        "analysis": "Goal: √2 ∉ ℚ. Form: negation → contradiction.\nAssume √2=p/q in lowest terms (gcd(p,q)=1).\nSquare: p²=2q² → p even → p=2k → q even → contradicts gcd=1.",
        "proof": "Suppose √2=p/q with gcd(p,q)=1.\nSquaring: p²=2q², so p² is even, so p is even.\nWrite p=2k. Then 4k²=2q², so q²=2k², so q is even.\nBut 2|p and 2|q contradicts gcd(p,q)=1.\nTherefore √2 is irrational. □",
        "reflection": "Builds on: n² even → n even (proved separately).\nGeneralizes: same proof shows √p is irrational for any prime p."
    },
    {
        "title": "1²+2²+...+n² = n(n+1)(2n+1)/6",
        "analysis": "Goal: ∀n≥1, formula. Form: universal over ℕ → induction.\nKey algebraic step: k(k+1)(2k+1)/6 + (k+1)² = (k+1)(k+2)(2k+3)/6.",
        "proof": "Base (n=1): left=1, right=1·2·3/6=1. ✓\n\nInductive step: suppose 1²+...+k²=k(k+1)(2k+1)/6.\n1²+...+k²+(k+1)²\n  = k(k+1)(2k+1)/6 + (k+1)²            [by IH]\n  = (k+1)[k(2k+1)/6 + (k+1)]\n  = (k+1)[2k²+7k+6]/6\n  = (k+1)(k+2)(2k+3)/6 ✓\n\nBy induction, the formula holds for all n≥1. □",
        "reflection": "Factor out (k+1) first — that's the key move.\nInduction proves but doesn't explain where the formula came from."
    },
    {
        "title": "Infinitely many primes (Euclid ~300 BC)",
        "analysis": "Goal: infinite primes. Form: negation → contradiction.\nAssume finitely many p₁,...,pₙ. Build N=p₁·...·pₙ+1.\nN has a prime factor p=pᵢ, but pᵢ|N and pᵢ|p₁·...·pₙ → pᵢ|1. Impossible.",
        "proof": "Suppose finitely many primes: p₁,...,pₙ.\nLet N=p₁·p₂·...·pₙ+1.\nN>1 has a prime factor p=pᵢ for some i.\npᵢ|N and pᵢ|p₁·...·pₙ → pᵢ|(N−p₁·...·pₙ)=1.\nNo prime divides 1 — contradiction.\nTherefore there are infinitely many primes. □",
        "reflection": "Common mistake: N is not necessarily prime (e.g. 2·3·5·7·11·13+1=30031=59·509).\nThe proof says N has a prime factor NOT on the list — not that N itself is prime."
    },
    {
        "title": "Pigeonhole: among 5 integers, two share remainder mod 4",
        "analysis": "Objects: 5 integers. Boxes: remainders mod 4 = {0,1,2,3} — 4 boxes.\n5 objects, 4 boxes → at least one box has ≥2 objects.\nTwo integers in the same box = same remainder mod 4.",
        "proof": "Let a₁,...,a₅ be any five integers.\nEach has remainder 0,1,2, or 3 when divided by 4.\nThere are 5 integers but only 4 possible remainders.\nBy the Pigeonhole Principle, at least two integers share a remainder. □",
        "reflection": "The proof is three sentences once you identify objects and boxes.\nSkill: recognizing when to apply Pigeonhole."
    },
    {
        "title": "Pascal's identity: C(n,k) = C(n-1,k-1) + C(n-1,k)",
        "analysis": "Double counting: C(n,k) = subsets of size k from {1,...,n}.\nSplit by whether n is included:\n  n in → C(n-1,k-1). n out → C(n-1,k). Total = C(n,k).",
        "proof": "Count k-element subsets of {1,...,n}.\nSubsets containing n: choose k−1 from {1,...,n−1} → C(n−1,k−1).\nSubsets not containing n: choose k from {1,...,n−1} → C(n−1,k).\nMutually exclusive and exhaustive.\nTherefore C(n,k) = C(n−1,k−1) + C(n−1,k). □",
        "reflection": "Combinatorial proof is shorter AND more insightful than algebra.\nWhen you see a combinatorial identity, ask: can I count the same thing two ways?"
    },
]


# ── Render helpers ─────────────────────────────────────────────────────────────

def render_content_block(label, body):
    style.step(label, body.replace("\n","<br>"))

def render_code_block(text):
    st.markdown(
        f'<pre style="background:var(--bg2);border:1px solid var(--border);'
        f'border-radius:6px;padding:1rem;font-family:\'DM Mono\',monospace;'
        f'font-size:0.82rem;color:var(--ink2);white-space:pre-wrap;">{text}</pre>',
        unsafe_allow_html=True)


# ── Section renderers ─────────────────────────────────────────────────────────

def render_logic():
    style.step("Propositions and Connectives",
        """A <strong>proposition</strong> is a sentence that is either TRUE or FALSE.
Not a question, not an opinion — a precise claim.<br><br>""" + CONNECTIVES,
        "warm")

    style.step("Truth table for P→Q",
        """<table style="border-collapse:collapse;font-family:'DM Mono',monospace;font-size:0.82rem;">
<tr style="border-bottom:1px solid var(--border);color:var(--sand);">
<td style="padding:0.25rem 0.8rem;">P</td><td style="padding:0.25rem 0.8rem;">Q</td>
<td style="padding:0.25rem 0.8rem;">P→Q</td><td style="padding:0.25rem 0.8rem;">Note</td></tr>
<tr><td style="padding:0.2rem 0.8rem;">T</td><td>T</td><td>T</td><td>Promise kept</td></tr>
<tr style="background:#fff3f0;"><td style="padding:0.2rem 0.8rem;">T</td><td>F</td><td><strong>F</strong></td><td>Promise broken — only failure!</td></tr>
<tr><td style="padding:0.2rem 0.8rem;">F</td><td>T</td><td>T</td><td>Vacuous truth</td></tr>
<tr><td style="padding:0.2rem 0.8rem;">F</td><td>F</td><td>T</td><td>Vacuous truth</td></tr>
</table>""")

    style.step("Quantifiers", QUANTIFIERS_CONTENT.replace("\n","<br>"))

    style.step("Logical equivalences to know",
        """<strong>Double negation:</strong> ¬¬P ≡ P<br>
<strong>De Morgan 1:</strong> ¬(P∧Q) ≡ ¬P∨¬Q — negate AND → flip to OR<br>
<strong>De Morgan 2:</strong> ¬(P∨Q) ≡ ¬P∧¬Q — negate OR → flip to AND<br>
<strong>Contrapositive:</strong> P→Q ≡ ¬Q→¬P<br>
<strong>Implication as OR:</strong> P→Q ≡ ¬P∨Q<br>
<strong>Biconditional split:</strong> P↔Q ≡ (P→Q)∧(Q→P)<br><br>
The three you'll use constantly: De Morgan, Contrapositive, Biconditional split.""",
        "sage")


def render_structure():
    style.step("Velleman's method — the core idea",
        """Every proof has two lists:<br><br>
<strong>GIVENS</strong> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>GOAL</strong><br>
What you already know &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; What you need to show<br><br>
A proof moves from givens to goal.<br>
The KEY INSIGHT: the <strong>form of the goal</strong> tells you what to do first.<br>
You don't need to be clever — you need to read carefully.""",
        "warm")

    style.step("Goal form → proof strategy (Velleman's lookup table)",
        "<br>".join(
            f"<strong>{form}:</strong><br>&emsp;{move}<br>"
            f"<code style='font-size:0.78rem;'>{template.replace(chr(10), ' | ')}</code><br>"
            for form, move, template in GOAL_TABLE
        ))

    style.step("Full example: a | b and a | c → a | (b+c)",
        """<strong>GIVEN:</strong> a,b,c integers; a|b; a|c<br>
<strong>GOAL:</strong> a|(b+c)<br>
<strong>FORM:</strong> existential (∃) — find m with b+c=am<br><br>
<strong>Unpack:</strong> b=aj, c=ak for some j,k∈ℤ<br>
<strong>Scratch:</strong> b+c=aj+ak=a(j+k) → m=j+k<br><br>
<strong>Proof:</strong><br>
Let a,b,c be arbitrary integers. Suppose a|b and a|c.<br>
Then b=aj and c=ak for some j,k∈ℤ.<br>
Therefore b+c=aj+ak=a(j+k).<br>
Since j+k is an integer, a|(b+c). □""",
        "sage")

    style.step("Working forward and backward",
        """<strong>Forward</strong> — from givens: "From P, I can derive..."<br>
<strong>Backward</strong> — from goal: "To prove Q, it suffices to show..."<br><br>
In practice: work BOTH directions in scratch work. Meet in the middle.<br><br>
<strong>Important rule:</strong> in the FINAL written proof, always go FORWARD.<br>
The backward reasoning was scratch work — don't show it.""")


def render_techniques(choice):
    if choice not in TECHNIQUES:
        return
    t = TECHNIQUES[choice]
    style.step(choice + " — when to use",
        t["when"], "warm")
    style.step("Template",
        t["template"].replace("\n","<br>"))
    for title, proof in t["examples"]:
        style.step(f"Example: {title}",
            proof.replace("\n","<br>"), "sage")


def render_functions():
    style.step("Injective, Surjective, Bijective",
        """<strong>INJECTIVE</strong> (one-to-one): different inputs → different outputs.<br>
∀a₁,a₂: f(a₁)=f(a₂) → a₁=a₂<br><br>
<strong>SURJECTIVE</strong> (onto): every element of B is an output.<br>
∀b∈B, ∃a∈A: f(a)=b<br><br>
<strong>BIJECTIVE</strong>: injective AND surjective. Has an inverse.<br><br>
f(x)=2x+1 on ℝ: injective ✓, surjective ✓, bijective ✓<br>
g(x)=x² on ℝ: NOT injective (g(2)=g(-2)), NOT surjective (-1 has no preimage)""",
        "warm")

    style.step("How to prove injective",
        """Goal: f(a₁)=f(a₂) → a₁=a₂<br>
<strong>Template:</strong> Suppose f(a₁)=f(a₂). [algebra] Therefore a₁=a₂. □<br><br>
<strong>Example:</strong> f(x)=3x−5<br>
Suppose f(x₁)=f(x₂). Then 3x₁−5=3x₂−5 → 3x₁=3x₂ → x₁=x₂. □""")

    style.step("How to prove surjective",
        """Goal: ∀b∈B, ∃a: f(a)=b<br>
<strong>Template:</strong> Let b be arbitrary. Let a=[formula]. Then f(a)=[verify]=b. □<br><br>
<strong>Example:</strong> f(x)=3x−5<br>
Let y∈ℝ. Let x=(y+5)/3. Then f(x)=3(y+5)/3−5=y+5−5=y. □""")

    style.step("Equivalence relations",
        """A relation ~ is an <strong>equivalence relation</strong> if:<br>
· <strong>Reflexive:</strong> a~a for all a<br>
· <strong>Symmetric:</strong> a~b → b~a<br>
· <strong>Transitive:</strong> a~b and b~c → a~c<br><br>
<strong>Example: a≡b (mod n)</strong><br>
Reflexive: n|(a−a)=0 ✓<br>
Symmetric: n|(a−b) → a−b=nk → b−a=n(−k) ✓<br>
Transitive: a−b=nj and b−c=nk → a−c=n(j+k) ✓<br>
All three hold. □""",
        "sage")


def render_olympiad(idx):
    if idx >= len(OLYMPIAD_PROBLEMS): return
    p = OLYMPIAD_PROBLEMS[idx]
    style.step(f"Problem: {p['title']}", "", "warm")
    style.step("Analysis — how to find the approach",
        p["analysis"].replace("\n","<br>"))
    style.step("Complete proof",
        f'<pre style="font-family:\'DM Mono\',monospace;font-size:0.82rem;'
        f'background:var(--bg2);border-radius:4px;padding:0.5rem;white-space:pre-wrap;">'
        f'{p["proof"]}</pre>')
    style.step("Reflection", p["reflection"].replace("\n","<br>"), "sage")

    # verification for specific problems
    if idx == 0:  # 6 | n³-n
        rows="".join(
            f"n={n}: n³−n={n**3-n}, ÷6={( n**3-n)//6} {'✓' if (n**3-n)%6==0 else '✗'}<br>"
            for n in range(-4,6))
        style.step("Numerical verification", rows)
    elif idx == 2:  # sum of squares
        s=0; rows=""
        for n in range(1,11):
            s+=n**2; f=n*(n+1)*(2*n+1)//6
            rows+=f"n={n}: sum={s}, formula={f} {'✓' if s==f else '✗'}<br>"
        style.step("Numerical verification", rows)
    elif idx == 4:  # pigeonhole
        style.step("Examples of Pigeonhole",
            "5 integers → 4 remainders mod 4 → two must coincide.<br>"
            "13 people → 12 months → two share a birth month.<br>"
            "367 people → 366 possible birthdays → two share a birthday.")


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose section</div>',
                    unsafe_allow_html=True)

        section = st.selectbox("Section",
            ["1 — Logic & Language",
             "2 — Proof Structure (Velleman's method)",
             "3 — Proof Techniques",
             "4 — Relations & Functions",
             "5 — Olympiad Problems"],
            key="prf_section")

        if section.startswith("3"):
            technique = st.selectbox("Technique",
                list(TECHNIQUES.keys()), key="prf_tech")

        if section.startswith("5"):
            problem_idx = st.selectbox("Problem",
                [f"{i+1}. {p['title']}" for i,p in enumerate(OLYMPIAD_PROBLEMS)],
                key="prf_prob")
            pidx = int(problem_idx.split(".")[0]) - 1

        go_btn = st.button("Read →", key="prf_go")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Recommended order</div>
  <div class="hint-body">
    1 → Logic & language first<br>
    2 → Velleman's method<br>
    3 → Techniques (direct first)<br>
    4 → Relations & functions<br>
    5 → Olympiad problems last<br><br>
    Based on Velleman's<br><em>How to Prove It</em>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if go_btn:
            if section.startswith("1"):
                render_logic()
            elif section.startswith("2"):
                render_structure()
            elif section.startswith("3"):
                render_techniques(technique)
            elif section.startswith("4"):
                render_functions()
            else:
                render_olympiad(pidx)
        else:
            style.step("Mathematical Proofs",
                """A proof is an argument that convinces any reader,
beyond any doubt, that a statement is true.<br><br>
Most students think proofs require special talent.<br>
<strong>Velleman's insight:</strong> proofs have structure. The structure can be learned.<br><br>
The form of the goal tells you what to do first.<br>
You don't need to be brilliant — you need to read carefully.<br><br>
Choose a section on the left and press Read →""",
                "warm")