import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import streamlit as st

import style


# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")


def sieve(limit):
    is_p = [True]*(limit+1); is_p[0]=is_p[1]=False
    for i in range(2,int(limit**0.5)+1):
        if is_p[i]:
            for j in range(i*i,limit+1,i): is_p[j]=False
    return is_p


# ── GCD / LCM ─────────────────────────────────────────────────────────────────

def solve_gcd_lcm(a, b):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("GCD — Euclid's algorithm",
        """The GCD is the largest number dividing both a and b.<br><br>
Euclid's key insight: GCD(a,b) = GCD(b, a mod b)<br>
Why? Any common divisor of a and b also divides the remainder.<br>
Keep replacing until the remainder is 0 — the last non-zero value is the GCD.<br><br>
This algorithm is 2 300 years old — and still the fastest.""",
        "warm")

    x,y = a,b; euclid_steps=[]
    while y!=0:
        r=x%y
        euclid_steps.append(f"GCD({x},{y}): {x} = {x//y}·{y} + {r} → GCD({y},{r})")
        x,y=y,r
    g=x
    add("Step by step", "<br>".join(euclid_steps)+f"<br><br>GCD({a},{b}) = <strong>{g}</strong>",
        "sage")

    lcm = a*b//g
    add("LCM — via GCD",
        f"LCM(a,b) = a·b / GCD(a,b)<br><br>"
        f"LCM({a},{b}) = {a}·{b} / {g} = {a*b} / {g} = <strong>{lcm}</strong><br><br>"
        f"Verify: {lcm}÷{a}={lcm//a} ✓ &nbsp;·&nbsp; {lcm}÷{b}={lcm//b} ✓<br><br>"
        f"Beautiful identity: GCD·LCM = a·b &nbsp;→ &nbsp;{g}·{lcm} = {g*lcm} = {a}·{b} = {a*b} ✓")

    return {"steps":steps, "gcd":g, "lcm":lcm}


# ── PRIME FACTORIZATION ───────────────────────────────────────────────────────

def solve_factorization(n):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Fundamental Theorem of Arithmetic",
        """Every integer &gt; 1 factors into primes in <strong>exactly one way</strong>.<br><br>
Two parts: existence (always possible) and uniqueness (only one way).<br>
The uniqueness is the surprising part — without it, arithmetic wouldn't work as we expect.<br><br>
Algorithm: trial division. Only need to try up to √n —
if n had a factor &gt; √n, its cofactor would be &lt; √n (already found).""",
        "warm")

    factors=[]; temp=n; d=2; div_lines=[]
    while d*d<=temp:
        while temp%d==0:
            div_lines.append(f"{temp} ÷ {d} = {temp//d}")
            factors.append(d); temp//=d
        d+=1
    if temp>1:
        div_lines.append(f"{temp} is prime — no more factors")
        factors.append(temp)

    counts=Counter(factors)
    factored=" · ".join(f"{p}^{e}" if e>1 else str(p) for p,e in sorted(counts.items()))
    num_div=1
    for e in counts.values(): num_div*=(e+1)

    add("Trial division",
        "<br>".join(div_lines)+f"<br><br>"
        f"{n} = <span class='mf'>{factored}</span><br><br>"
        f"Number of divisors = "+" · ".join(f"({e}+1)" for e in counts.values())
        +f" = <strong>{num_div}</strong>",
        "sage")

    return {"steps":steps,"factors":factors,"counts":counts,"factored":factored}


# ── SIEVE ─────────────────────────────────────────────────────────────────────

def solve_sieve(limit):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Sieve of Eratosthenes — 240 BC",
        """Write all numbers 2…n. Mark 2 as prime, cross out every multiple of 2.<br>
The next unmarked number is always prime. Cross out its multiples. Repeat until √n.<br><br>
<strong>Why stop at √n?</strong> Any composite ≤ n has a prime factor ≤ √n.
If all factors were &gt; √n, their product would exceed n.""",
        "warm")

    is_p=sieve(limit)
    primes=[i for i in range(2,limit+1) if is_p[i]]
    approx=limit/math.log(limit)

    add("Results",
        f"Primes up to {limit}: <strong>{len(primes)}</strong><br><br>"
        f"<strong>Prime Number Theorem:</strong> π(n) ≈ n/ln(n)<br>"
        f"Approximation: {limit}/ln({limit}) = {approx:.1f}<br>"
        f"Actual: {len(primes)}<br>"
        f"Ratio: {len(primes)/approx:.4f} (→1 as n→∞)<br><br>"
        +("Primes: "+", ".join(str(p) for p in primes[:30])
          +("…" if len(primes)>30 else "")),
        "sage")

    return {"steps":steps,"primes":primes,"limit":limit,"is_p":is_p}


def plot_sieve(primes, limit, is_p):
    ns=list(range(2,limit+1))
    fig,axes=plt.subplots(1,2,figsize=(11,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    axes[0].scatter(primes,[1]*len(primes),color="#e8602a",s=12,alpha=0.8)
    axes[0].set_title(f"Prime distribution up to {limit}",fontsize=10,color="#4a4540")
    axes[0].set_xlabel("n",color="#4a4540",fontsize=9); axes[0].set_yticks([])
    counts=[]; approx=[]; c=0
    for n in ns:
        if is_p[n]: c+=1
        counts.append(c); approx.append(n/math.log(n))
    axes[1].plot(ns,counts,color="#e8602a",linewidth=2,label="π(n) actual")
    axes[1].plot(ns,approx,color="#3d6b5e",linewidth=1.5,linestyle="--",label="n/ln(n)")
    axes[1].set_title("Prime Number Theorem",fontsize=10,color="#4a4540")
    axes[1].set_xlabel("n",color="#4a4540",fontsize=9)
    axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout(); return fig


# ── FERMAT ────────────────────────────────────────────────────────────────────

def solve_fermat(p, a, exp):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Fermat's Little Theorem — 1640",
        """If p is prime and gcd(a,p)=1:<br><br>
<span class="mf">a^(p−1) ≡ 1  (mod p)</span><br><br>
Powers: lets you reduce huge exponents instantly.<br>
Primality test: if a^(n−1) mod n ≠ 1, n is definitely NOT prime.<br>
RSA encryption (every https website) is built directly on this theorem.""",
        "warm")

    if a%p==0:
        add("Error",f"{a} is a multiple of {p} — theorem doesn't apply.","error")
        return {"steps":steps}

    res=pow(a,p-1,p)
    add("Verify a^(p−1) mod p",
        f"{a}^({p}−1) = {a}^{p-1} mod {p} = <strong>{res}</strong>"
        +(" = 1 ✓ Fermat confirmed." if res==1 else " ≠ 1 — check that p is prime."),
        "sage" if res==1 else "error")

    bases=[2,3,5,7,11,13]; rows=""
    for base in bases:
        if base>=p: break
        r=pow(base,p-1,p)
        rows+=f"{base}^{p-1} mod {p} = {r} {'✓' if r==1 else '✗ NOT PRIME'}<br>"
    add("Primality test — multiple bases", rows)

    reduced=exp%(p-1) or p-1
    r1=pow(a,reduced,p); r2=pow(a,exp,p)
    add("Power reduction",
        f"Goal: {a}^{exp} mod {p}<br>"
        f"By Fermat: reduce exponent mod (p−1) = mod {p-1}<br>"
        f"{exp} mod {p-1} = {reduced}<br>"
        f"{a}^{exp} ≡ {a}^{reduced} ≡ <strong>{r1}</strong> (mod {p})<br>"
        f"Direct check: {r2} ✓",
        "sage")

    return {"steps":steps}


# ── PERFECT NUMBERS ───────────────────────────────────────────────────────────

def solve_perfect(limit):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Perfect numbers — the oldest open problem",
        """A perfect number equals the sum of all its proper divisors.<br><br>
6 = 1+2+3 ✓ &nbsp;·&nbsp; 28 = 1+2+4+7+14 ✓<br><br>
Only 51 perfect numbers are known. Largest: over 49 million digits.<br>
<strong>Nobody knows if there are infinitely many.</strong><br>
<strong>Nobody knows if any ODD perfect number exists.</strong><br><br>
Euler: every even perfect number = 2^(p−1)·(2^p−1) where 2^p−1 is a Mersenne prime.""",
        "warm")

    found=[]
    for n in range(2,limit+1):
        divs=[i for i in range(1,n) if n%i==0]
        if sum(divs)==n:
            found.append((n,divs))

    if found:
        lines=[]
        for n,divs in found:
            lines.append(f"{n}: divisors={divs}, sum={sum(divs)} ✓")
        add("Found","\n<br>".join(lines),"sage")
    else:
        add("No perfect numbers found",
            f"None up to {limit}. Try up to 500 to find 6, 28, and 496.")

    add("Three categories",
        "Every integer is exactly one of:<br>"
        "· <strong>Perfect</strong>: sum = n<br>"
        "· <strong>Abundant</strong>: sum &gt; n (e.g. 12 → 1+2+3+4+6=16)<br>"
        "· <strong>Deficient</strong>: sum &lt; n (e.g. 8 → 1+2+4=7)<br><br>"
        "Every prime is deficient (only proper divisor is 1).")

    return {"steps":steps,"found":found,"limit":limit}


def plot_perfect(found, limit):
    ns=list(range(2,min(limit+1,300)))
    sums=[sum(i for i in range(1,n) if n%i==0) for n in ns]
    colors=["#c8a96e" if s==n else "#3d6b5e" if s>n else "#e0d8cc" for n,s in zip(ns,sums)]
    fig,ax=plt.subplots(figsize=(10,4)); fig.patch.set_facecolor("#fdfaf5")
    styled_ax(ax,fig)
    ax.bar(ns,sums,color=colors,edgecolor="none",width=0.8)
    ax.plot(ns,ns,color="#e8602a",linewidth=1.5,linestyle="--",label="y=n (perfect line)")
    perfect_ns=[n for n,_ in found if n<300]
    for p in perfect_ns:
        ax.annotate(f" {p}\n PERFECT",(p,p),fontsize=8,color="#8b6914",fontweight="bold")
    ax.set_xlabel("n",color="#4a4540",fontsize=9)
    ax.set_ylabel("Sum of proper divisors",color="#4a4540",fontsize=9)
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    ax.set_title("Perfect (gold) · Abundant (green) · Deficient (gray)",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── GOLDBACH ──────────────────────────────────────────────────────────────────

def solve_goldbach(limit):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Goldbach's conjecture — 1742",
        """'Every even integer &gt; 2 is the sum of two primes.'<br><br>
4=2+2, 6=3+3, 8=3+5, 10=3+7=5+5, ...<br><br>
Verified computationally up to 4·10^18.<br>
<strong>Never proven. Never disproven. 280 years — still open.</strong><br><br>
Best result: Chen's theorem (1973) — every large even number = prime + (prime or prime·prime).""",
        "warm")

    is_p=sieve(limit); primes_set={i for i in range(2,limit+1) if is_p[i]}
    failed=[]; decomps={}
    for n in range(4,limit+1,2):
        ways=[(p,n-p) for p in primes_set if p<=n//2 and (n-p) in primes_set]
        if not ways: failed.append(n)
        decomps[n]=len(ways)

    if failed:
        add("Counterexample found!",f"Goldbach fails at: {failed}","error")
    else:
        examples=[]
        for n in [4,6,10,20,50,100]:
            if n<=limit:
                ways=[(p,n-p) for p in primes_set if p<=n//2 and (n-p) in primes_set]
                examples.append(f"{n} = "+" or ".join(f"{a}+{b}" for a,b in ways[:3]))
        max_n=max(decomps,key=decomps.get)
        add("Verified",
            f"All even numbers 4…{limit} satisfy Goldbach ✓<br><br>"
            +"<br>".join(examples)+f"<br><br>"
            f"Most decompositions: {max_n} can be written {decomps[max_n]} ways.",
            "sage")

    return {"steps":steps,"decomps":decomps,"limit":limit}


def plot_goldbach(decomps):
    ns=list(decomps.keys()); ways=list(decomps.values())
    fig,ax=plt.subplots(figsize=(9,4)); fig.patch.set_facecolor("#fdfaf5"); styled_ax(ax,fig)
    ax.bar(ns,ways,color="#e8602a",alpha=0.7,width=1.5,edgecolor="none")
    ax.set_xlabel("Even n",color="#4a4540",fontsize=9)
    ax.set_ylabel("Ways as sum of two primes",color="#4a4540",fontsize=9)
    ax.set_title("Goldbach — decomposition count",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── TWIN PRIMES ───────────────────────────────────────────────────────────────

def solve_twin_primes(limit):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Twin primes — Zhang's breakthrough",
        """Twin primes differ by 2: (3,5),(5,7),(11,13),(17,19),...<br><br>
<strong>Conjecture:</strong> infinitely many twin prime pairs. Unproven.<br><br>
<strong>Zhang (2013):</strong> proved there are infinitely many prime pairs differing by ≤ 70 000 000.<br>
First finite bound ever — then Polymath8 reduced it to 246 in under a year.<br>
Getting it to 2 is still open.<br><br>
Pattern: except (3,5), every twin prime pair has the form (6k−1, 6k+1).""",
        "warm")

    is_p=sieve(limit)
    twins=[(p,p+2) for p in range(3,limit-1) if is_p[p] and is_p[p+2]]

    lines=[]
    for p,q in twins[:20]:
        k=(p+1)//6
        form=f" = (6·{k}−1, 6·{k}+1)" if p>5 else ""
        lines.append(f"({p}, {q}){form}")
    if len(twins)>20: lines.append(f"… ({len(twins)} pairs total)")

    brun=sum(1/p+1/(p+2) for p,_ in twins) if twins else 0
    add("Twin prime pairs",
        "<br>".join(lines)+f"<br><br>"
        f"Found <strong>{len(twins)}</strong> pairs up to {limit}.<br><br>"
        f"<strong>Brun's constant:</strong> B₂ ≈ 1.9021975…<br>"
        f"Unlike the sum of 1/p over all primes (which diverges),<br>"
        f"the sum of 1/p over twin primes <em>converges</em>.<br>"
        f"Partial sum here: {brun:.6f}",
        "sage")

    return {"steps":steps,"twins":twins,"limit":limit,"is_p":is_p}


def plot_twin_primes(twins, limit, is_p):
    primes=[i for i in range(2,limit+1) if is_p[i]]
    twin_set={p for pair in twins for p in pair}
    fig,axes=plt.subplots(1,2,figsize=(11,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    colors=["#c8a96e" if p in twin_set else "#3d6b5e" for p in primes]
    axes[0].scatter(primes,[1]*len(primes),c=colors,s=20,alpha=0.9)
    axes[0].set_title(f"Twin (gold) among primes up to {limit}",fontsize=10,color="#4a4540")
    axes[0].set_xlabel("n",color="#4a4540",fontsize=9); axes[0].set_yticks([])
    if len(twins)>1:
        firsts=[p for p,_ in twins]
        gaps=[firsts[i+1]-firsts[i] for i in range(len(firsts)-1)]
        axes[1].plot(range(1,len(gaps)+1),gaps,color="#e8602a",linewidth=1.5,
                     marker="o",markersize=3,alpha=0.8)
        axes[1].set_title("Gaps between consecutive twin prime pairs",fontsize=10,color="#4a4540")
        axes[1].set_xlabel("Index",color="#4a4540",fontsize=9)
        axes[1].set_ylabel("Gap",color="#4a4540",fontsize=9)
    plt.tight_layout(); return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["GCD & LCM","Prime factorization","Sieve of Eratosthenes",
             "Fermat's Little Theorem","Perfect numbers",
             "Goldbach's conjecture","Twin primes"],
            key="nt_topic")

        if topic == "GCD & LCM":
            a=st.number_input("a",value=48,step=1,key="nt_a")
            b=st.number_input("b",value=18,step=1,key="nt_b")

        elif topic == "Prime factorization":
            nv=st.number_input("n",value=360,min_value=2,step=1,key="nt_n")

        elif topic == "Sieve of Eratosthenes":
            lim=st.number_input("Find primes up to",value=100,min_value=10,
                                max_value=5000,step=10,key="nt_lim")

        elif topic == "Fermat's Little Theorem":
            pv=st.number_input("Prime p",value=17,min_value=2,step=1,key="nt_p")
            av=st.number_input("Base a",value=3,min_value=1,step=1,key="nt_av")
            ev=st.number_input("Large exponent e",value=1000,min_value=1,step=100,key="nt_ev")

        elif topic == "Perfect numbers":
            lim_p=st.number_input("Search up to",value=500,min_value=10,
                                   max_value=10000,step=50,key="nt_lp")

        elif topic == "Goldbach's conjecture":
            lim_g=st.number_input("Verify up to",value=100,min_value=4,
                                   max_value=2000,step=10,key="nt_lg")

        else:  # Twin primes
            lim_t=st.number_input("Find up to",value=200,min_value=10,
                                   max_value=5000,step=50,key="nt_lt")

        solve_btn=st.button("Compute →",key="nt_solve")
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    GCD: <code>48, 18</code> → GCD=6, LCM=144<br>
    Factorize: <code>360</code> → 2³·3²·5<br>
    Sieve: <code>100</code> → 25 primes<br>
    Fermat: <code>p=17, a=3</code> → verify 3^16≡1<br>
    Perfect: up to <code>500</code> → 6, 28, 496<br>
    Goldbach: up to <code>100</code> → all verified
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "GCD & LCM":
                r=solve_gcd_lcm(int(a),int(b))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                style.result_band(("GCD",str(r["gcd"])),("LCM",str(r["lcm"])))

            elif topic == "Prime factorization":
                r=solve_factorization(int(nv))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Sieve of Eratosthenes":
                r=solve_sieve(int(lim))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                style.result_band(("Primes found",str(len(r["primes"]))),
                                  ("Up to",str(int(lim))))
                st.markdown('<div class="graph-label">Distribution</div>',unsafe_allow_html=True)
                fig=plot_sieve(r["primes"],r["limit"],r["is_p"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Fermat's Little Theorem":
                r=solve_fermat(int(pv),int(av),int(ev))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)

            elif topic == "Perfect numbers":
                r=solve_perfect(int(lim_p))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if r["found"]:
                    st.markdown('<div class="graph-label">Divisor sums</div>',unsafe_allow_html=True)
                    fig=plot_perfect(r["found"],r["limit"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Goldbach's conjecture":
                r=solve_goldbach(int(lim_g))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if "decomps" in r:
                    st.markdown('<div class="graph-label">Decompositions</div>',unsafe_allow_html=True)
                    fig=plot_goldbach(r["decomps"]); st.pyplot(fig); plt.close(fig)

            else:
                r=solve_twin_primes(int(lim_t))
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if r["twins"]:
                    st.markdown('<div class="graph-label">Twin prime distribution</div>',unsafe_allow_html=True)
                    fig=plot_twin_primes(r["twins"],r["limit"],r["is_p"])
                    st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("p")