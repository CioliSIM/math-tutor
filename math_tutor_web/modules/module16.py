import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc"); ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")


# ── SIMPLE INTEREST ───────────────────────────────────────────────────────────

def solve_simple(C, r, t):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Simple interest — linear growth",
        """You invest C, earn r% per year, and every year you get the <em>same</em> amount.<br>
Interest never earns interest — it stays flat. Growth is a straight line.<br><br>
<span class="mf">Interest = C·r·t &nbsp;&nbsp; Final = C·(1 + r·t)</span>""",
        "warm")

    interest = C*r*t; final = C*(1+r*t)
    add("Result",
        f"Capital: {C:,.2f} &nbsp;·&nbsp; Rate: {r*100:.2f}% &nbsp;·&nbsp; Time: {t} years<br><br>"
        f"Interest = {C:g}·{r:g}·{t:g} = <strong>{interest:,.2f}</strong><br>"
        f"Final = {C:g}·(1+{r:g}·{t:g}) = <strong>{final:,.2f}</strong><br><br>"
        f"Earning {interest/t:,.2f} per year — always the same. No acceleration.",
        "sage")

    rows=""
    for yr in range(1,min(int(t)+1,11)):
        e=C*r*yr; tot=C+e
        rows+=f"Year {yr}: interest={e:,.2f}, total={tot:,.2f}<br>"
    add("Year by year", rows)

    return {"steps":steps,"C":C,"r":r,"t":t,"final":final}


# ── COMPOUND INTEREST ─────────────────────────────────────────────────────────

def solve_compound(C, r, t, n):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Compound interest — exponential growth",
        """Interest earns interest. Each period, interest is added to the principal.<br><br>
<span class="mf">A = C·(1 + r/n)^(n·t)</span><br><br>
n = compounding periods per year (1=annual, 12=monthly, 365=daily)<br>
As n→∞: continuous compounding A = C·e^(r·t) — the natural exponential from Module 10.""",
        "warm")

    A = C*(1+r/n)**(n*t); A_s = C*(1+r*t); A_c = C*math.exp(r*t)
    add("Computation",
        f"A = {C:g}·(1+{r:g}/{n})^({n}·{t:g}) = <strong>{A:,.2f}</strong><br><br>"
        f"Simple interest: {A_s:,.2f} &nbsp;·&nbsp; "
        f"Compound (n={n}): {A:,.2f} &nbsp;·&nbsp; "
        f"Continuous: {A_c:,.2f}<br><br>"
        f"Extra from compounding vs simple: <strong>{A-A_s:,.2f}</strong>")

    approx_d = 72/(r*100); exact_d = math.log(2)/math.log(1+r/n)/n
    add("Rule of 72 — years to double",
        f"72 / {r*100:.1f} = <strong>{approx_d:.1f} years</strong> (approximation)<br>"
        f"Exact: <strong>{exact_d:.2f} years</strong><br>"
        f"Gap: {abs(approx_d-exact_d):.2f} years — remarkably accurate for rates 2%–15%.",
        "sage")

    return {"steps":steps,"C":C,"r":r,"t":t,"n":n,"A":A,"A_s":A_s,"A_c":A_c}


def plot_compound_fig(C, r, t, n):
    years=np.linspace(0,t,300)
    simple=C*(1+r*years); comp=C*(1+r/n)**(n*years); cont=C*np.exp(r*years)
    fig,axes=plt.subplots(1,2,figsize=(11,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    axes[0].plot(years,simple,color="#b0a090",linewidth=2,linestyle="--",label="Simple")
    axes[0].plot(years,comp,  color="#e8602a",linewidth=2,label=f"Compound n={n}")
    axes[0].plot(years,cont,  color="#3d6b5e",linewidth=1.5,linestyle=":",label="Continuous")
    axes[0].set_xlabel("Years",color="#4a4540",fontsize=9)
    axes[0].set_ylabel("Amount",color="#4a4540",fontsize=9)
    axes[0].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[0].set_title(f"Growth of {C:,} at {r*100:.1f}%",fontsize=10,color="#4a4540")
    adv=comp-simple
    axes[1].fill_between(years,adv,color="#3d6b5e",alpha=0.4,label="Extra vs simple")
    axes[1].plot(years,adv,color="#3d6b5e",linewidth=2)
    axes[1].set_xlabel("Years",color="#4a4540",fontsize=9)
    axes[1].set_ylabel("Extra amount",color="#4a4540",fontsize=9)
    axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[1].set_title("Compounding advantage",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── PRESENT / FUTURE VALUE ────────────────────────────────────────────────────

def solve_pv_fv(mode, r, t, amount):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("The time value of money",
        """A euro today is worth more than a euro tomorrow.<br><br>
<span class="mf">FV = PV·(1+r)^t</span> &nbsp;&nbsp; (capitalizing — moving forward)<br>
<span class="mf">PV = FV/(1+r)^t</span> &nbsp;&nbsp; (discounting — moving backward)<br><br>
The factor 1/(1+r)^t is the <strong>discount factor</strong> — what one future euro is worth today.""",
        "warm")

    if mode == "fv":
        PV=amount; FV=PV*(1+r)**t; df=1/(1+r)**t
        add("Future value",
            f"FV = {PV:,.2f}·(1+{r:g})^{t:g} = <strong>{FV:,.2f}</strong><br><br>"
            f"Total gain: {FV-PV:,.2f} ({(FV/PV-1)*100:.2f}% total return)<br>"
            f"Discount factor: {df:.6f} — every euro in {t:.0f} years is worth {df:.4f}€ today.",
            "sage")
        return {"steps":steps,"PV":PV,"FV":FV,"r":r,"t":t}
    else:
        FV=amount; PV=FV/(1+r)**t
        add("Present value",
            f"PV = {FV:,.2f} / (1+{r:g})^{t:g} = <strong>{PV:,.2f}</strong><br><br>"
            f"The discount: {FV-PV:,.2f} — the price of waiting.<br>"
            f"Equivalently: invest {PV:,.2f} today at {r*100:.1f}% → exactly {FV:,.2f} in {t:.0f} years.",
            "sage")
        return {"steps":steps,"PV":PV,"FV":FV,"r":r,"t":t}


def plot_pv_fv(PV, FV, r, t):
    years=np.linspace(0,t,300); vals=PV*(1+r)**years
    fig,ax=plt.subplots(figsize=(8,4)); fig.patch.set_facecolor("#fdfaf5"); styled_ax(ax,fig)
    ax.plot(years,vals,color="#e8602a",linewidth=2.2)
    ax.plot(0,PV,"o",color="#3d6b5e",markersize=11,zorder=5,label=f"PV={PV:,.2f}")
    ax.plot(t,FV,"o",color="#c8a96e",markersize=11,zorder=5,label=f"FV={FV:,.2f}")
    ax.fill_between(years,PV,vals,alpha=0.15,color="#e8602a")
    ax.axhline(PV,color="#b0a090",linewidth=1,linestyle="--",alpha=0.5)
    ax.set_xlabel("Years",color="#4a4540",fontsize=9)
    ax.set_ylabel("Value",color="#4a4540",fontsize=9)
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout(); return fig


# ── ANNUITIES ─────────────────────────────────────────────────────────────────

def solve_annuity(R, r, n):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Annuity — series of equal payments",
        """An annuity is a series of equal payments at regular intervals.<br>
Pensions, loan repayments, insurance premiums — all annuities.<br><br>
Each payment is discounted back to today. Summing the geometric series gives:<br><br>
<span class="mf">PV = R·[1 − (1+r)^(−n)] / r</span><br><br>
This is how banks compute mortgage payments and pension funds value liabilities.""",
        "warm")

    PV=R*(1-(1+r)**(-n))/r; FV=R*((1+r)**n-1)/r
    add("Present and future value",
        f"PV = {R:g}·[1−(1+{r:g})^(−{n})] / {r:g} = <strong>{PV:,.2f}</strong><br>"
        f"FV = {R:g}·[(1+{r:g})^{n}−1] / {r:g} = <strong>{FV:,.2f}</strong><br><br>"
        f"Total paid: {R*n:,.2f} &nbsp;·&nbsp; Interest earned: {FV-R*n:,.2f}",
        "sage")

    rows=""; cum=0
    for k in range(1,min(n+1,11)):
        pv_k=R/(1+r)**k; cum+=pv_k
        rows+=f"Payment {k}: PV={pv_k:.4f}, cumulative={cum:.4f}<br>"
    if n>10: rows+=f"… (total PV = {PV:.4f})"
    add("Payment breakdown", rows)

    return {"steps":steps,"R":R,"r":r,"n":n,"PV":PV}


def plot_annuity_fig(R, r, n, PV):
    payments=list(range(1,n+1)); pv_each=[R/(1+r)**k for k in payments]
    cum=np.cumsum(pv_each)
    fig,axes=plt.subplots(1,2,figsize=(11,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    colors=plt.cm.RdYlGn_r(np.linspace(0.1,0.9,n))
    axes[0].bar(payments,pv_each,color=colors,edgecolor="none")
    axes[0].axhline(R,color="#b0a090",linewidth=1.5,linestyle="--",alpha=0.7,label=f"R={R:g}")
    axes[0].set_title("PV of each payment",fontsize=10,color="#4a4540")
    axes[0].set_xlabel("Payment #",color="#4a4540",fontsize=9)
    axes[0].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[1].plot(payments,cum,color="#e8602a",linewidth=2,marker="o",markersize=3)
    axes[1].axhline(PV,color="#3d6b5e",linewidth=1.5,linestyle="--",label=f"Total PV={PV:,.2f}")
    axes[1].axhline(R*n,color="#b0a090",linewidth=1.5,linestyle=":",label=f"Nominal={R*n:g}")
    axes[1].set_title("Cumulative PV",fontsize=10,color="#4a4540")
    axes[1].set_xlabel("Payment #",color="#4a4540",fontsize=9)
    axes[1].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout(); return fig


# ── MORTGAGE ──────────────────────────────────────────────────────────────────

def solve_mortgage(PV, r, n):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Mortgage amortization",
        """Each payment covers interest on the remaining debt plus a slice of principal.<br>
At the start, most goes to interest. Gradually more shifts to principal.<br><br>
<span class="mf">R = PV·r·(1+r)^n / [(1+r)^n − 1]</span><br><br>
<strong>The mortgage paradox:</strong> on a 30-year mortgage you can easily pay back twice the loan.""",
        "warm")

    R=PV*r*(1+r)**n/((1+r)**n-1); total=R*n; interest=total-PV
    add("Your mortgage",
        f"Monthly payment: <strong>{R:,.2f}</strong><br>"
        f"Total paid: {total:,.2f} &nbsp;·&nbsp; Total interest: {interest:,.2f}<br>"
        f"Interest as % of loan: {interest/PV*100:.1f}%<br>"
        f"For every euro borrowed you pay back {total/PV:.2f}€"
        +("<br><strong>You pay more in interest than in principal.</strong>" if interest>PV else ""),
        "sage")

    balance=PV; schedule=[]
    for mo in range(1,n+1):
        ip=balance*r; pp=R-ip; balance=max(balance-pp,0)
        schedule.append((mo,R,ip,pp,balance))

    rows=""
    for row in schedule[:5]:
        rows+=f"Month {row[0]}: payment={row[1]:,.2f}, interest={row[2]:,.2f}, principal={row[3]:,.2f}, remaining={row[4]:,.2f}<br>"
    if n>10: rows+="…<br>"
    for row in schedule[-3:]:
        rows+=f"Month {row[0]}: payment={row[1]:,.2f}, interest={row[2]:,.2f}, principal={row[3]:,.2f}, remaining={row[4]:,.2f}<br>"
    add("Amortization schedule (first 5 + last 3)", rows)

    return {"steps":steps,"PV":PV,"R":R,"n":n,"schedule":schedule}


def plot_mortgage_fig(schedule, PV, R, n):
    months=[s[0] for s in schedule]; interest=[s[2] for s in schedule]
    principal=[s[3] for s in schedule]; remaining=[s[4] for s in schedule]
    fig,axes=plt.subplots(1,2,figsize=(11,4)); fig.patch.set_facecolor("#fdfaf5")
    for ax in axes: styled_ax(ax,fig)
    axes[0].stackplot(months,interest,principal,
                      labels=["Interest","Principal"],
                      colors=["#e8602a","#3d6b5e"],alpha=0.7)
    axes[0].set_title("Payment breakdown",fontsize=10,color="#4a4540")
    axes[0].set_xlabel("Month",color="#4a4540",fontsize=9)
    axes[0].legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    axes[1].plot(months,remaining,color="#e8602a",linewidth=2)
    axes[1].fill_between(months,remaining,alpha=0.2,color="#e8602a")
    axes[1].set_title("Remaining debt",fontsize=10,color="#4a4540")
    axes[1].set_xlabel("Month",color="#4a4540",fontsize=9)
    axes[1].set_ylabel("Principal left",color="#4a4540",fontsize=9)
    plt.tight_layout(); return fig


# ── INFLATION ─────────────────────────────────────────────────────────────────

def solve_inflation(S, r, i, t):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Inflation and real returns",
        """Inflation silently erodes the value of money.<br><br>
<span class="mf">(1+r_real) = (1+r_nominal)/(1+i) &nbsp;&nbsp; r_real ≈ r_nominal − i  (Fisher)</span><br><br>
If your return is below inflation, you lose purchasing power even as the number grows.<br>
Money in a mattress loses value every year.""",
        "warm")

    nominal=S*(1+r)**t; real=S*((1+r)/(1+i))**t; purch=S/(1+i)**t
    r_real=(1+r)/(1+i)-1
    trend = ("positive ✓ — purchasing power grows." if r_real>0 else
             f"NEGATIVE ✗ — losing {abs(r_real)*100:.2f}% purchasing power per year." if r_real<0 else
             "zero — unchanged.")
    add("After " + str(int(t)) + " years",
        f"Nominal value: {nominal:,.2f}<br>"
        f"Real value (inflation-adjusted): <strong>{real:,.2f}</strong><br>"
        f"Purchasing power of S alone: {purch:,.2f}<br><br>"
        f"Real return: {r_real*100:.4f}% → {trend}",
        "sage" if r_real>0 else "error" if r_real<0 else "")

    halving=math.log(2)/math.log(1+i)
    add("Rule of 72 for inflation",
        f"At {i*100:.1f}% inflation, purchasing power halves in {halving:.2f} years.<br>"
        f"In {halving:.0f} years you need twice as much to buy the same things.")

    return {"steps":steps,"S":S,"r":r,"i":i,"t":t,
            "nominal":nominal,"real":real,"purch":purch}


def plot_inflation_fig(S, r, i, t):
    years=np.linspace(0,t,300)
    nominal=S*(1+r)**years; real=S*((1+r)/(1+i))**years; purch=S/(1+i)**years
    fig,ax=plt.subplots(figsize=(8,4)); fig.patch.set_facecolor("#fdfaf5"); styled_ax(ax,fig)
    ax.plot(years,nominal,color="#3d6b5e",linewidth=2,label=f"Nominal ({r*100:.1f}%)")
    ax.plot(years,real,   color="#e8602a",linewidth=2,label=f"Real ({((1+r)/(1+i)-1)*100:.2f}%)")
    ax.plot(years,purch,  color="#c8a96e",linewidth=2,linestyle="--",label=f"Purch. power")
    ax.axhline(S,color="#b0a090",linewidth=1,linestyle=":",alpha=0.6)
    ax.set_xlabel("Years",color="#4a4540",fontsize=9)
    ax.set_ylabel("Value",color="#4a4540",fontsize=9)
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    plt.tight_layout(); return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Simple interest","Compound interest","Present & future value",
             "Annuities","Mortgage","Inflation"],
            key="fin_topic")

        if topic == "Simple interest":
            C=st.number_input("Capital C",value=1000.0,step=100.0,key="fin_C")
            r=st.number_input("Rate r (e.g. 0.05 = 5%)",value=0.05,step=0.01,format="%.4f",key="fin_r")
            t=st.number_input("Years",value=10.0,step=1.0,key="fin_t")

        elif topic == "Compound interest":
            C=st.number_input("Capital C",value=1000.0,step=100.0,key="fin_cC")
            r=st.number_input("Annual rate r",value=0.05,step=0.01,format="%.4f",key="fin_cr")
            t=st.number_input("Years",value=20.0,step=1.0,key="fin_ct")
            n=st.selectbox("Compounding periods/year",[1,4,12,52,365],index=2,key="fin_cn")

        elif topic == "Present & future value":
            mode=st.selectbox("Direction",["Compute FV from PV","Compute PV from FV"],key="fin_pm")
            r=st.number_input("Rate r",value=0.05,step=0.01,format="%.4f",key="fin_pvr")
            t=st.number_input("Years",value=10.0,step=1.0,key="fin_pvt")
            amount=st.number_input("PV" if "PV" in mode else "FV",value=1000.0,step=100.0,key="fin_pvam")

        elif topic == "Annuities":
            R=st.number_input("Payment R",value=500.0,step=50.0,key="fin_aR")
            r=st.number_input("Rate per period r",value=0.05,step=0.01,format="%.4f",key="fin_ar")
            n_a=st.number_input("Periods n",value=10,min_value=1,step=1,key="fin_an")

        elif topic == "Mortgage":
            PV_m=st.number_input("Loan amount",value=200000.0,step=10000.0,key="fin_mPV")
            r_m=st.number_input("Monthly rate r (e.g. 0.004 = 4.8% annual)",
                                 value=0.004,step=0.0005,format="%.5f",key="fin_mr")
            n_m=st.number_input("Months",value=360,min_value=12,step=12,key="fin_mn")

        else:  # Inflation
            S=st.number_input("Initial amount",value=10000.0,step=1000.0,key="fin_iS")
            r_n=st.number_input("Nominal return r",value=0.05,step=0.01,format="%.4f",key="fin_ir")
            i_v=st.number_input("Inflation rate i",value=0.03,step=0.005,format="%.4f",key="fin_ii")
            t_i=st.number_input("Years",value=30.0,step=1.0,key="fin_it")

        solve_btn=st.button("Compute →",key="fin_solve")
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Simple: <code>C=1000, r=5%, t=10</code><br>
    Compound: <code>monthly, 20yr</code> → vs simple<br>
    Mortgage: <code>200k, 0.4%/mo, 360mo</code><br>
    Inflation: <code>r=5%, i=3%, 30yr</code><br>
    Annuity: <code>R=500, r=5%, n=10</code>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Simple interest":
                r_=solve_simple(C,r,t)
                for lbl,body,var in r_["steps"]: style.step(lbl,body,var)
                style.result_band(("Interest",f"{C*r*t:,.2f}"),("Final",f"{C*(1+r*t):,.2f}"))

            elif topic == "Compound interest":
                r_=solve_compound(C,r,t,n)
                for lbl,body,var in r_["steps"]: style.step(lbl,body,var)
                style.result_band(("Compound",f"{r_['A']:,.2f}"),
                                  ("Simple",f"{r_['A_s']:,.2f}"),
                                  ("Continuous",f"{r_['A_c']:,.2f}"))
                st.markdown('<div class="graph-label">Growth comparison</div>',unsafe_allow_html=True)
                fig=plot_compound_fig(C,r,t,n); st.pyplot(fig); plt.close(fig)

            elif topic == "Present & future value":
                pv_mode="fv" if "FV" in mode else "pv"
                r_=solve_pv_fv(pv_mode,r,t,amount)
                for lbl,body,var in r_["steps"]: style.step(lbl,body,var)
                style.result_band(("PV",f"{r_['PV']:,.2f}"),("FV",f"{r_['FV']:,.2f}"))
                st.markdown('<div class="graph-label">Time value curve</div>',unsafe_allow_html=True)
                fig=plot_pv_fv(r_["PV"],r_["FV"],r,t); st.pyplot(fig); plt.close(fig)

            elif topic == "Annuities":
                r_=solve_annuity(R,r,int(n_a))
                for lbl,body,var in r_["steps"]: style.step(lbl,body,var)
                style.result_band(("PV",f"{r_['PV']:,.2f}"),
                                  ("Total nominal",f"{R*n_a:,.2f}"))
                st.markdown('<div class="graph-label">Annuity analysis</div>',unsafe_allow_html=True)
                fig=plot_annuity_fig(R,r,int(n_a),r_["PV"]); st.pyplot(fig); plt.close(fig)

            elif topic == "Mortgage":
                r_=solve_mortgage(PV_m,r_m,int(n_m))
                for lbl,body,var in r_["steps"]: style.step(lbl,body,var)
                R_mo=PV_m*r_m*(1+r_m)**n_m/((1+r_m)**n_m-1)
                style.result_band(("Monthly payment",f"{R_mo:,.2f}"),
                                  ("Total paid",f"{R_mo*n_m:,.2f}"),
                                  ("Total interest",f"{R_mo*n_m-PV_m:,.2f}"))
                st.markdown('<div class="graph-label">Amortization</div>',unsafe_allow_html=True)
                fig=plot_mortgage_fig(r_["schedule"],PV_m,R_mo,int(n_m))
                st.pyplot(fig); plt.close(fig)

            else:
                r_=solve_inflation(S,r_n,i_v,t_i)
                for lbl,body,var in r_["steps"]: style.step(lbl,body,var)
                style.result_band(("Nominal",f"{r_['nominal']:,.2f}"),
                                  ("Real",f"{r_['real']:,.2f}"),
                                  ("Purch. power",f"{r_['purch']:,.2f}"))
                st.markdown('<div class="graph-label">Inflation vs returns</div>',unsafe_allow_html=True)
                fig=plot_inflation_fig(S,r_n,i_v,t_i); st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("€")