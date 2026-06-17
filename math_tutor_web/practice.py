# practice.py — interactive practice system for all modules

import random
import sympy as sp
import streamlit as st

x = sp.Symbol('x')

# ── Feedback HTML helpers ─────────────────────────────────────────────────────

def _correct_html(answer, explanation=""):
    extra = f'<div style="font-size:0.78rem;margin-top:0.3rem;opacity:0.8;">{explanation}</div>' if explanation else ""
    return f"""
<div style="background:rgba(45,90,78,0.12);border-left:3px solid #2d5a4e;
            border-radius:0 8px 8px 0;padding:0.75rem 1rem;font-size:0.87rem;
            color:var(--ink2);margin-top:0.5rem;animation:fadeUp 0.2s ease both;">
  <strong style="color:#2d5a4e;">✓ Correct</strong> — {answer}{extra}
</div>"""

def _wrong_html(answer, explanation=""):
    extra = f'<div style="font-size:0.78rem;margin-top:0.3rem;opacity:0.85;">{explanation}</div>' if explanation else ""
    return f"""
<div style="background:rgba(200,96,42,0.08);border-left:3px solid #c8602a;
            border-radius:0 8px 8px 0;padding:0.75rem 1rem;font-size:0.87rem;
            color:var(--ink2);margin-top:0.5rem;animation:fadeUp 0.2s ease both;">
  <strong style="color:#c8602a;">✗ Not quite</strong> — answer is <strong style="color:#c8602a;">{answer}</strong>{extra}
</div>"""

def _question_label(q, hint=""):
    hint_html = f'<div style="font-family:\'DM Mono\',monospace;font-size:0.68rem;color:var(--ink2);margin-bottom:0.5rem;opacity:0.75;">{hint}</div>' if hint else ""
    return f"""
<div style="font-size:0.97rem;font-weight:400;color:var(--ink);
            line-height:1.72;margin-bottom:0.55rem;">{q}</div>{hint_html}"""


# ── Question types ─────────────────────────────────────────────────────────────

def numeric_question(q, answer, tolerance=1e-6, explanation="", key_suffix=""):
    """Numeric input — feedback appears instantly as you type."""
    key = f"prac_num_{q[:25]}_{key_suffix}"
    st.markdown(_question_label(q), unsafe_allow_html=True)
    user_ans = st.text_input("", key=key, label_visibility="collapsed",
                              placeholder="Type your answer…")
    if user_ans.strip():
        try:
            user_val = float(sp.sympify(user_ans))
            correct  = abs(user_val - float(answer)) < tolerance
            html = _correct_html(answer, explanation) if correct else _wrong_html(answer, explanation)
            st.markdown(html, unsafe_allow_html=True)
            return correct
        except Exception:
            st.markdown(
                '<div style="font-size:0.78rem;color:var(--ink2);opacity:0.7;margin-top:0.3rem;">'
                'Enter a valid number or expression (e.g. 1/3, sqrt(2))</div>',
                unsafe_allow_html=True)
    return None


def multiple_choice(q, options, correct_idx, explanation="", key_suffix=""):
    """Multiple choice — feedback appears instantly on selection."""
    key = f"prac_mc_{q[:25]}_{key_suffix}"
    st.markdown(_question_label(q), unsafe_allow_html=True)
    choice = st.radio("", options, key=key, label_visibility="collapsed", index=None)
    if choice is not None:
        correct = options.index(choice) == correct_idx
        html = (_correct_html(options[correct_idx], explanation) if correct
                else _wrong_html(options[correct_idx], explanation))
        st.markdown(html, unsafe_allow_html=True)
        return correct
    return None


def symbolic_question(q, answer_expr, var=x, explanation="", key_suffix=""):
    """Symbolic input — feedback appears instantly as you type."""
    key = f"prac_sym_{q[:25]}_{key_suffix}"
    st.markdown(_question_label(q, "Python notation: x**2, sin(x), exp(x), log(x)"),
                unsafe_allow_html=True)
    user_ans = st.text_input("", key=key, label_visibility="collapsed",
                              placeholder="e.g. 3*x**2 + cos(x)")
    if user_ans.strip():
        try:
            user_expr = sp.sympify(user_ans)
            diff      = sp.simplify(user_expr - answer_expr)
            correct   = diff == 0
            ans_str   = str(answer_expr)
            html = _correct_html(ans_str, explanation) if correct else _wrong_html(ans_str, explanation)
            st.markdown(html, unsafe_allow_html=True)
            return correct
        except Exception:
            st.markdown(
                '<div style="font-size:0.78rem;color:var(--ink2);opacity:0.7;margin-top:0.3rem;">'
                'Could not parse — check notation</div>',
                unsafe_allow_html=True)
    return None


# ── Question banks per module ──────────────────────────────────────────────────

def questions_ch1():
    """Quadratic Equations practice."""
    rng = random.Random(st.session_state.get("prac_seed_1", 42))
    a, b, c = rng.randint(1,4), rng.randint(-5,5), rng.randint(-6,6)
    disc = b**2 - 4*a*c

    return [
        {
            "type": "multiple_choice",
            "q": f"How many real solutions does {a}x²+{b}x+{c}=0 have?",
            "options": ["0", "1", "2"],
            "correct": 0 if disc<0 else 1 if disc==0 else 2,
            "explanation": f"The discriminant Δ={b}²−4·{a}·{c}={disc}. "
                          + ("Δ<0 → no real solutions." if disc<0
                             else "Δ=0 → exactly one solution." if disc==0
                             else "Δ>0 → two distinct solutions."),
        },
        {
            "type": "numeric",
            "q": "What is the discriminant of x²−5x+6=0?",
            "answer": 1,
            "explanation": "Δ = (−5)² − 4·1·6 = 25−24 = 1.",
        },
        {
            "type": "symbolic",
            "q": "Write the solutions to x²−5x+6=0 as a sum (x₁+x₂).",
            "answer": sp.sympify("5"),
            "explanation": "By Vieta's formulas, x₁+x₂ = −b/a = 5.",
        },
        {
            "type": "multiple_choice",
            "q": "The parabola y=x²−4x+4 touches the x-axis at:",
            "options": ["x=−2", "x=2", "x=0 and x=4"],
            "correct": 1,
            "explanation": "x²−4x+4=(x−2)². Δ=0, unique root at x=2.",
        },
    ]


def questions_ch2():
    """Quadratic Inequalities."""
    return [
        {
            "type": "multiple_choice",
            "q": "The solution to x²−x−6 > 0 is:",
            "options": ["x∈(−2, 3)", "x∈(−∞,−2)∪(3,+∞)", "x∈(−3, 2)"],
            "correct": 1,
            "explanation": "(x+2)(x−3)>0. Parabola opens up: positive outside roots.",
        },
        {
            "type": "numeric",
            "q": "How many integers satisfy x²−4 ≤ 0?",
            "answer": 5,
            "explanation": "x²≤4 → −2≤x≤2. Integers: −2,−1,0,1,2 → 5 values.",
        },
        {
            "type": "symbolic",
            "q": "For the inequality 2x²−3x−2 < 0, find the sum of the endpoints of the solution interval.",
            "answer": sp.Rational(3,2),
            "explanation": "Roots: x=(3±√25)/4 → x=−1/2 and x=2. Sum=−1/2+2=3/2.",
        },
    ]


def questions_ch4():
    """Polynomials."""
    return [
        {
            "type": "symbolic",
            "q": "What is the derivative of x⁴−3x²+2? (Find f'(x))",
            "answer": 4*x**3 - 6*x,
            "explanation": "Power rule: (x⁴)'=4x³, (3x²)'=6x, (2)'=0.",
        },
        {
            "type": "multiple_choice",
            "q": "If p(2)=0 for polynomial p(x), which of the following is guaranteed?",
            "options": ["p(x) is divisible by x+2",
                        "p(x) is divisible by x−2",
                        "p(x) has degree ≥ 2"],
            "correct": 1,
            "explanation": "Factor theorem: p(a)=0 ⟹ (x−a) | p(x). Here a=2.",
        },
        {
            "type": "numeric",
            "q": "Divide x³−6x²+11x−6 by (x−1). What is the remainder?",
            "answer": 0,
            "explanation": "p(1)=1−6+11−6=0. By the remainder theorem, remainder=0.",
        },
    ]


def questions_ch7():
    """Limits."""
    return [
        {
            "type": "numeric",
            "q": "Compute lim(x→2) (x²−4)/(x−2).",
            "answer": 4,
            "explanation": "(x²−4)/(x−2)=(x+2)(x−2)/(x−2)=x+2 → 4 as x→2.",
        },
        {
            "type": "numeric",
            "q": "Compute lim(x→0) sin(x)/x.",
            "answer": 1,
            "explanation": "This is a fundamental limit — equal to 1 by the squeeze theorem.",
        },
        {
            "type": "multiple_choice",
            "q": "lim(x→+∞) (3x²+1)/(x²−2) equals:",
            "options": ["0", "1", "3", "+∞"],
            "correct": 2,
            "explanation": "Divide numerator and denominator by x²: (3+1/x²)/(1−2/x²) → 3/1=3.",
        },
        {
            "type": "multiple_choice",
            "q": "lim(x→0⁺) ln(x) equals:",
            "options": ["0", "1", "−∞", "+∞"],
            "correct": 2,
            "explanation": "ln(x)→−∞ as x→0⁺. The log function has a vertical asymptote at x=0.",
        },
    ]


def questions_ch8():
    """Trigonometry."""
    return [
        {
            "type": "numeric",
            "q": "Compute sin(π/6).",
            "answer": 0.5,
            "explanation": "sin(30°)=sin(π/6)=1/2. One of the fundamental values.",
        },
        {
            "type": "numeric",
            "q": "Compute cos²(x)+sin²(x) for any x.",
            "answer": 1,
            "explanation": "Pythagorean identity: cos²x+sin²x=1 for all x.",
        },
        {
            "type": "multiple_choice",
            "q": "Which of the following equals sin(2x)?",
            "options": ["2sin(x)", "2sin(x)cos(x)", "sin²(x)−cos²(x)"],
            "correct": 1,
            "explanation": "Double angle formula: sin(2x)=2sin(x)cos(x).",
        },
        {
            "type": "numeric",
            "q": "How many solutions does sin(x)=0 have in [0, 2π]?",
            "answer": 3,
            "explanation": "sin(x)=0 at x=0, π, 2π — three solutions in [0,2π].",
        },
    ]


def questions_ch10():
    """Logarithms & Exponentials."""
    return [
        {
            "type": "numeric",
            "q": "Compute log₂(32).",
            "answer": 5,
            "explanation": "2⁵=32, so log₂(32)=5.",
        },
        {
            "type": "symbolic",
            "q": "Simplify log(x²) in terms of log(x). (Enter the simplified form)",
            "answer": 2*sp.log(x),
            "explanation": "log(x²)=2·log(x) by the power rule of logarithms.",
        },
        {
            "type": "multiple_choice",
            "q": "The function y=eˣ is:",
            "options": ["Always negative", "Always positive", "Zero at x=0"],
            "correct": 1,
            "explanation": "eˣ>0 for all x∈ℝ. At x=0: e⁰=1≠0.",
        },
        {
            "type": "numeric",
            "q": "Solve eˣ=1. What is x?",
            "answer": 0,
            "explanation": "e⁰=1, so x=0.",
        },
    ]


def questions_ch11():
    """Combinatorics."""
    return [
        {
            "type": "numeric",
            "q": "How many ways can you choose 3 books from a shelf of 7?",
            "answer": 35,
            "explanation": "C(7,3)=7!/(3!·4!)=35.",
        },
        {
            "type": "numeric",
            "q": "In how many ways can 4 people be arranged in a line?",
            "answer": 24,
            "explanation": "4!=4·3·2·1=24.",
        },
        {
            "type": "multiple_choice",
            "q": "C(n,k) = C(n, n−k) because:",
            "options": ["It's a coincidence",
                        "Choosing k to include = choosing n−k to exclude",
                        "Pascal's triangle is symmetric"],
            "correct": 1,
            "explanation": "Every subset of size k corresponds to a complement of size n−k.",
        },
        {
            "type": "numeric",
            "q": "What is C(5,0) + C(5,1) + C(5,2) + C(5,3) + C(5,4) + C(5,5)?",
            "answer": 32,
            "explanation": "Sum of a row of Pascal's triangle = 2ⁿ = 2⁵ = 32.",
        },
    ]


def questions_ch12():
    """Probability."""
    return [
        {
            "type": "numeric",
            "q": "A fair die is rolled. What is the probability of getting an even number?",
            "answer": 0.5,
            "explanation": "Even numbers: 2,4,6 → P=3/6=1/2.",
        },
        {
            "type": "multiple_choice",
            "q": "P(A∪B) = P(A)+P(B) only when:",
            "options": ["A and B are independent",
                        "A and B are mutually exclusive",
                        "Always"],
            "correct": 1,
            "explanation": "P(A∪B)=P(A)+P(B)−P(A∩B). If A∩B=∅, then P(A∩B)=0.",
        },
        {
            "type": "numeric",
            "q": "P(A)=0.4, P(B|A)=0.3. What is P(A∩B)?",
            "answer": 0.12,
            "explanation": "P(A∩B)=P(A)·P(B|A)=0.4·0.3=0.12.",
        },
    ]


def questions_ch15():
    """Number Theory."""
    return [
        {
            "type": "numeric",
            "q": "What is gcd(48, 36)?",
            "answer": 12,
            "explanation": "48=2⁴·3, 36=2²·3². GCD=2²·3=12.",
        },
        {
            "type": "multiple_choice",
            "q": "Which of the following is prime?",
            "options": ["91", "97", "99"],
            "correct": 1,
            "explanation": "91=7·13, 99=9·11. 97 has no divisors other than 1 and itself.",
        },
        {
            "type": "numeric",
            "q": "What is 7³ mod 5?",
            "answer": 3,
            "explanation": "7≡2 (mod 5), so 7³≡2³=8≡3 (mod 5).",
        },
        {
            "type": "multiple_choice",
            "q": "Fermat's Little Theorem states that for prime p and gcd(a,p)=1:",
            "options": ["aᵖ ≡ 1 (mod p)",
                        "aᵖ⁻¹ ≡ 1 (mod p)",
                        "a² ≡ 1 (mod p)"],
            "correct": 1,
            "explanation": "FLT: aᵖ⁻¹≡1 (mod p). This is one of the most used results in number theory.",
        },
    ]


def questions_ch21():
    """Derivatives."""
    return [
        {
            "type": "symbolic",
            "q": "Find f'(x) for f(x) = x³ − 4x + 1.",
            "answer": 3*x**2 - 4,
            "explanation": "Power rule: (x³)'=3x², (4x)'=4, (1)'=0.",
        },
        {
            "type": "numeric",
            "q": "What is the slope of y=sin(x) at x=0?",
            "answer": 1,
            "explanation": "(sin x)'=cos x. cos(0)=1.",
        },
        {
            "type": "multiple_choice",
            "q": "At a local maximum, f'(x) is:",
            "options": ["Positive", "Zero", "Negative"],
            "correct": 1,
            "explanation": "At any local extremum, the tangent is horizontal: f'(x)=0.",
        },
        {
            "type": "symbolic",
            "q": "Differentiate f(x) = sin(x²) using the chain rule.",
            "answer": 2*x*sp.cos(x**2),
            "explanation": "Chain rule: f'=cos(x²)·2x = 2x·cos(x²).",
        },
        {
            "type": "multiple_choice",
            "q": "f''(x)>0 at a critical point means:",
            "options": ["Local maximum", "Local minimum", "Inflection point"],
            "correct": 1,
            "explanation": "f''(x)>0 means the curve bends upward ∪ → local minimum.",
        },
        {
            "type": "numeric",
            "q": "f(x)=x³−3x. At x=1, is f'(1) positive, negative, or zero? Enter 0 for zero.",
            "answer": 0,
            "explanation": "f'(x)=3x²−3. f'(1)=3−3=0. It's a critical point.",
        },
    ]


def questions_ch22():
    """Integrals."""
    return [
        {
            "type": "numeric",
            "q": "Compute ∫₀¹ x² dx.",
            "answer": round(1/3, 6),
            "explanation": "∫x²dx=x³/3+C. [x³/3]₀¹=1/3.",
        },
        {
            "type": "symbolic",
            "q": "Find the antiderivative of f(x)=3x²+2x. (Omit the +C)",
            "answer": x**3 + x**2,
            "explanation": "∫(3x²+2x)dx=x³+x²+C.",
        },
        {
            "type": "numeric",
            "q": "Compute ∫₀^π sin(x) dx.",
            "answer": 2,
            "explanation": "[−cos x]₀^π = −cos(π)+cos(0) = 1+1 = 2.",
        },
        {
            "type": "multiple_choice",
            "q": "The Fundamental Theorem of Calculus connects:",
            "options": ["Limits and continuity",
                        "Differentiation and integration",
                        "Sequences and series"],
            "correct": 1,
            "explanation": "FTC: if F'=f, then ∫ₐᵇf(x)dx=F(b)−F(a). The two operations are inverses.",
        },
        {
            "type": "symbolic",
            "q": "Compute ∫ e^x·sin(x)dx. (Enter without +C — use the result eˣ(sinx−cosx)/2)",
            "answer": sp.exp(x)*(sp.sin(x)-sp.cos(x))/2,
            "explanation": "Integration by parts twice (circular trick): I=eˣ(sinx−cosx)/2.",
        },
    ]


def questions_ch19():
    """Mathematical Proofs."""
    return [
        {
            "type": "multiple_choice",
            "q": "To prove P→Q by contrapositive, you prove:",
            "options": ["Q→P", "¬Q→¬P", "¬P→¬Q"],
            "correct": 1,
            "explanation": "Contrapositive of P→Q is ¬Q→¬P. They are logically equivalent.",
        },
        {
            "type": "multiple_choice",
            "q": "In a proof by contradiction, you:",
            "options": ["Prove the statement directly",
                        "Assume the negation and derive a contradiction",
                        "Find a counterexample"],
            "correct": 1,
            "explanation": "Assume ¬P, derive something false, conclude P must be true.",
        },
        {
            "type": "multiple_choice",
            "q": "The inductive step of mathematical induction proves:",
            "options": ["P(1) is true",
                        "P(k)→P(k+1) for all k",
                        "P(n) is true for all specific n"],
            "correct": 1,
            "explanation": "Induction: base case P(1), then show P(k)→P(k+1). Together they prove P(n) for all n.",
        },
    ]


def questions_ch20():
    """Olympic Mathematics."""
    return [
        {
            "type": "multiple_choice",
            "q": "The Pigeonhole Principle states:",
            "options": ["n objects in n boxes → one box is empty",
                        "n+1 objects in n boxes → one box has ≥2",
                        "n objects in n+1 boxes → one box has ≥2"],
            "correct": 1,
            "explanation": "n+1 pigeons in n holes → at least one hole has ≥2 pigeons.",
        },
        {
            "type": "multiple_choice",
            "q": "An invariant in a problem is:",
            "options": ["A quantity that always increases",
                        "A quantity that never changes",
                        "A quantity that eventually reaches zero"],
            "correct": 1,
            "explanation": "Invariants are preserved under all allowed operations. If initial≠target, the target is unreachable.",
        },
        {
            "type": "numeric",
            "q": "Among any 5 integers, two must have the same remainder when divided by 4. How many possible remainders mod 4 are there?",
            "answer": 4,
            "explanation": "Remainders mod 4: 0,1,2,3 → 4 boxes. With 5 integers, Pigeonhole guarantees a collision.",
        },
    ]

def questions_ch3():
    """Systems of Equations."""
    return [
        {
            "type": "numeric",
            "q": "Solve the system: x+y=7, x−y=3. What is x?",
            "answer": 5,
            "explanation": "Add the equations: 2x=10 → x=5.",
        },
        {
            "type": "numeric",
            "q": "Solve: 2x+y=8, x+2y=7. What is x+y?",
            "answer": 5,
            "explanation": "Add equations: 3(x+y)=15 → x+y=5.",
        },
        {
            "type": "multiple_choice",
            "q": "A system of two linear equations in two unknowns can have:",
            "options": ["Only one solution",
                        "Zero, one, or infinitely many solutions",
                        "At most two solutions"],
            "correct": 1,
            "explanation": "Parallel lines → no solution. Same line → ∞ solutions. Intersecting → exactly one.",
        },
        {
            "type": "numeric",
            "q": "Find the x-coordinate of the intersection of y=2x+1 and y=x+3.",
            "answer": 2,
            "explanation": "2x+1=x+3 → x=2.",
        },
    ]


def questions_ch5():
    """Function Analysis."""
    return [
        {
            "type": "multiple_choice",
            "q": "f(x)=x² is:",
            "options": ["Odd", "Even", "Neither"],
            "correct": 1,
            "explanation": "f(−x)=(−x)²=x²=f(x) → even function.",
        },
        {
            "type": "multiple_choice",
            "q": "The domain of f(x)=√(x−3) is:",
            "options": ["x>3", "x≥3", "x∈ℝ"],
            "correct": 1,
            "explanation": "Need x−3≥0 → x≥3.",
        },
        {
            "type": "numeric",
            "q": "How many zeros does f(x)=x³−x have?",
            "answer": 3,
            "explanation": "x³−x=x(x−1)(x+1)=0 → x=0,1,−1. Three zeros.",
        },
        {
            "type": "multiple_choice",
            "q": "f(x)=x³ is monotone:",
            "options": ["Decreasing on ℝ", "Increasing on ℝ", "Neither"],
            "correct": 1,
            "explanation": "f'(x)=3x²≥0 for all x, and =0 only at x=0. So f is increasing on all of ℝ.",
        },
    ]


def questions_ch6():
    """Sequences."""
    return [
        {
            "type": "numeric",
            "q": "The arithmetic sequence has first term 3 and common difference 4. What is the 10th term?",
            "answer": 39,
            "explanation": "aₙ=a₁+(n−1)d=3+9·4=39.",
        },
        {
            "type": "numeric",
            "q": "A geometric sequence has first term 2 and ratio 3. What is the 5th term?",
            "answer": 162,
            "explanation": "a₅=2·3⁴=2·81=162.",
        },
        {
            "type": "multiple_choice",
            "q": "The series 1+1/2+1/4+1/8+… converges to:",
            "options": ["1", "2", "∞"],
            "correct": 1,
            "explanation": "Geometric series with a=1, r=1/2: S=a/(1−r)=1/(1/2)=2.",
        },
        {
            "type": "numeric",
            "q": "What is the sum of the first 5 terms of 1+2+4+8+…?",
            "answer": 31,
            "explanation": "S₅=1·(2⁵−1)/(2−1)=31.",
        },
    ]


def questions_ch9():
    """Analytic Geometry 2D."""
    return [
        {
            "type": "numeric",
            "q": "What is the distance between (0,0) and (3,4)?",
            "answer": 5,
            "explanation": "d=√(3²+4²)=√25=5.",
        },
        {
            "type": "numeric",
            "q": "What is the slope of the line through (1,2) and (3,8)?",
            "answer": 3,
            "explanation": "m=(8−2)/(3−1)=6/2=3.",
        },
        {
            "type": "multiple_choice",
            "q": "The circle x²+y²=25 has radius:",
            "options": ["5", "25", "√25=5"],
            "correct": 0,
            "explanation": "x²+y²=r² → r=5.",
        },
        {
            "type": "numeric",
            "q": "Find the y-intercept of the line 3x+2y=12.",
            "answer": 6,
            "explanation": "Set x=0: 2y=12 → y=6.",
        },
    ]


def questions_ch13():
    """Complex Numbers."""
    return [
        {
            "type": "numeric",
            "q": "Compute |3+4i|.",
            "answer": 5,
            "explanation": "|a+bi|=√(a²+b²)=√(9+16)=5.",
        },
        {
            "type": "symbolic",
            "q": "Compute (1+i)². Enter in the form a+bi → just enter the real part as a number.",
            "answer": sp.sympify("2*sp.I"),
            "explanation": "(1+i)²=1+2i+i²=1+2i−1=2i.",
        },
        {
            "type": "multiple_choice",
            "q": "i⁴ equals:",
            "options": ["i", "−1", "1"],
            "correct": 2,
            "explanation": "i¹=i, i²=−1, i³=−i, i⁴=1. The cycle repeats every 4.",
        },
        {
            "type": "numeric",
            "q": "The modulus of e^(iπ) is:",
            "answer": 1,
            "explanation": "|e^(iθ)|=1 for all real θ. Euler's formula: e^(iπ)=−1, |−1|=1.",
        },
    ]


def questions_ch14():
    """Euclidean Geometry."""
    return [
        {
            "type": "numeric",
            "q": "In a triangle, two angles are 60° and 80°. What is the third angle?",
            "answer": 40,
            "explanation": "Sum of angles = 180°. Third = 180−60−80=40°.",
        },
        {
            "type": "multiple_choice",
            "q": "An angle inscribed in a semicircle is always:",
            "options": ["45°", "90°", "180°"],
            "correct": 1,
            "explanation": "Thales' theorem: any angle inscribed in a semicircle is 90°.",
        },
        {
            "type": "numeric",
            "q": "A right triangle has legs 5 and 12. What is the hypotenuse?",
            "answer": 13,
            "explanation": "c=√(5²+12²)=√(25+144)=√169=13.",
        },
        {
            "type": "multiple_choice",
            "q": "Two tangent lines drawn from an external point to a circle have:",
            "options": ["Different lengths", "Equal lengths", "No relationship"],
            "correct": 1,
            "explanation": "Tangent segments from an external point are always equal in length.",
        },
    ]


def questions_ch16():
    """Financial Math."""
    return [
        {
            "type": "numeric",
            "q": "€1000 at 5% annual simple interest for 3 years. Total interest earned?",
            "answer": 150,
            "explanation": "I=P·r·t=1000·0.05·3=150.",
        },
        {
            "type": "multiple_choice",
            "q": "Compound interest is greater than simple interest because:",
            "options": ["The rate is higher",
                        "Interest earns interest",
                        "The principal grows faster"],
            "correct": 1,
            "explanation": "In compound interest, earned interest is added to principal and earns further interest.",
        },
        {
            "type": "numeric",
            "q": "€500 doubles at 7% compound interest. Approximately how many years? (Use rule of 72: 72/rate)",
            "answer": round(72/7, 1),
            "explanation": "Rule of 72: years≈72/7≈10.3 years.",
        },
    ]


def questions_ch17():
    """Parametric Equations."""
    return [
        {
            "type": "multiple_choice",
            "q": "The parametric curve x=cos(t), y=sin(t) traces:",
            "options": ["A parabola", "A unit circle", "An ellipse"],
            "correct": 1,
            "explanation": "cos²t+sin²t=1 → x²+y²=1: the unit circle.",
        },
        {
            "type": "numeric",
            "q": "For x=2t, y=t², eliminate the parameter. What is the power of x in y=x²/4? Enter the denominator.",
            "answer": 4,
            "explanation": "t=x/2 → y=(x/2)²=x²/4.",
        },
        {
            "type": "multiple_choice",
            "q": "The slope of a parametric curve at a point is:",
            "options": ["dy/dt", "dx/dt", "(dy/dt)/(dx/dt)"],
            "correct": 2,
            "explanation": "By the chain rule: dy/dx = (dy/dt)/(dx/dt).",
        },
    ]


def questions_ch18():
    """Analytic Geometry 3D."""
    return [
        {
            "type": "numeric",
            "q": "Compute the dot product of (1,2,3) and (4,5,6).",
            "answer": 32,
            "explanation": "1·4+2·5+3·6=4+10+18=32.",
        },
        {
            "type": "multiple_choice",
            "q": "Two vectors are perpendicular when their dot product is:",
            "options": ["1", "0", "−1"],
            "correct": 1,
            "explanation": "u·v=|u||v|cos θ=0 when θ=90°.",
        },
        {
            "type": "numeric",
            "q": "The distance from (0,0,0) to (1,2,2) is:",
            "answer": 3,
            "explanation": "d=√(1²+2²+2²)=√9=3.",
        },
        {
            "type": "multiple_choice",
            "q": "The equation of a plane in 3D has the form:",
            "options": ["ax+by=c", "ax+by+cz=d", "x²+y²+z²=r²"],
            "correct": 1,
            "explanation": "A plane in 3D: ax+by+cz=d where (a,b,c) is the normal vector.",
        },
    ]


QUESTION_BANKS = {
    1:  questions_ch1,
    2:  questions_ch2,
    3:  questions_ch3,
    4:  questions_ch4,
    5:  questions_ch5,
    6:  questions_ch6,
    7:  questions_ch7,
    8:  questions_ch8,
    9:  questions_ch9,
    10: questions_ch10,
    11: questions_ch11,
    12: questions_ch12,
    13: questions_ch13,
    14: questions_ch14,
    15: questions_ch15,
    16: questions_ch16,
    17: questions_ch17,
    18: questions_ch18,
    19: questions_ch19,
    20: questions_ch20,
    21: questions_ch21,
    22: questions_ch22,
}


# ── Practice section renderer ─────────────────────────────────────────────────

def render_practice(chapter_n, dark=False):
    """Render the practice section for a given chapter."""
    if chapter_n not in QUESTION_BANKS:
        st.markdown('<div style="font-size:0.85rem;color:var(--ink2);opacity:0.6;">No practice questions available for this chapter yet.</div>', unsafe_allow_html=True)
        return

    ink2 = "#9e9080" if dark else "#4a4540"
    bdr  = "#2a2620" if dark else "#ddd5c8"
    card = "#161410" if dark else "#ffffff"
    warm = "#d4703a" if dark else "#c8602a"
    sand = "#b89848" if dark else "#a8893e"
    sage = "#4a8070" if dark else "#2d5a4e"

    seed_key  = f"prac_seed_{chapter_n}"
    score_key = f"prac_score_{chapter_n}"
    total_key = f"prac_total_{chapter_n}"

    if seed_key  not in st.session_state: st.session_state[seed_key]  = 42
    if score_key not in st.session_state: st.session_state[score_key] = 0
    if total_key not in st.session_state: st.session_state[total_key] = 0

    questions = QUESTION_BANKS[chapter_n]()
    score = st.session_state[score_key]
    total = st.session_state[total_key]
    pct   = int(score / total * 100) if total > 0 else 0

    # Header with live score bar
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-bottom:1.2rem;flex-wrap:wrap;gap:0.5rem;">
  <div style="display:flex;align-items:center;gap:0.9rem;">
    <div style="width:6px;height:6px;border-radius:50%;background:{warm};"></div>
    <div style="font-family:'DM Mono',monospace;font-size:0.56rem;letter-spacing:0.2em;
                text-transform:uppercase;color:{sand};">Practice · Chapter {chapter_n:02d}</div>
  </div>
  <div style="display:flex;align-items:center;gap:1rem;">
    <div style="font-family:'DM Mono',monospace;font-size:0.72rem;color:{ink2};">
      {score}/{total} correct &nbsp;·&nbsp; <strong style="color:{warm if pct<60 else sage};">{pct}%</strong>
    </div>
    <div style="width:100px;height:4px;background:{bdr};border-radius:2px;overflow:hidden;">
      <div style="width:{pct}%;height:100%;background:{warm if pct<60 else sage};
                  border-radius:2px;transition:width 0.4s ease;"></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    results = []
    for i, q in enumerate(questions):
        st.markdown(f"""
<div style="background:{card};border:1px solid {bdr};border-radius:10px;
            padding:1.2rem 1.4rem;margin-bottom:0.9rem;">
  <div style="font-family:'DM Mono',monospace;font-size:0.5rem;letter-spacing:0.14em;
              text-transform:uppercase;color:{sand};margin-bottom:0.7rem;">
    Q{i+1}
  </div>
""", unsafe_allow_html=True)
        ks = f"{chapter_n}_{i}"
        if q["type"] == "multiple_choice":
            r = multiple_choice(q["q"], q["options"], q["correct"],
                                q.get("explanation",""), key_suffix=ks)
        elif q["type"] == "numeric":
            r = numeric_question(q["q"], q["answer"],
                                 explanation=q.get("explanation",""), key_suffix=ks)
        elif q["type"] == "symbolic":
            r = symbolic_question(q["q"], q["answer"],
                                  explanation=q.get("explanation",""), key_suffix=ks)
        else:
            r = None
        results.append(r)
        st.markdown("</div>", unsafe_allow_html=True)

    answered = [r for r in results if r is not None]
    if answered:
        st.session_state[score_key] = sum(1 for r in answered if r)
        st.session_state[total_key] = len(answered)

    col1, col2 = st.columns([2,3])
    with col1:
        if st.button("↻  New questions", key=f"prac_new_{chapter_n}"):
            st.session_state[seed_key]  = __import__('random').randint(0, 9999)
            st.session_state[score_key] = 0
            st.session_state[total_key] = 0
            st.rerun()
    with col2:
        if total > 0:
            msg = ("🎯 Perfect score!" if pct==100 else "✓ Good work." if pct>=70
                   else "Keep going — practice makes permanent.")
            st.markdown(f'<div style="font-size:0.8rem;color:{ink2};padding:0.4rem 0;">{msg}</div>',
                        unsafe_allow_html=True)