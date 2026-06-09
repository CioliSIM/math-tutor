import math
import matplotlib.pyplot as plt
import numpy as np


def plot_interest_comparison(C, r, t):
    years      = np.linspace(0, t, 300)
    simple     = C * (1 + r*years)
    compound_a = C * (1 + r)**years
    compound_m = C * (1 + r/12)**(12*years)
    continuous = C * np.exp(r*years)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, simple,     color="gray",      linewidth=2,
            linestyle="--", label="Simple interest")
    ax.plot(years, compound_a, color="steelblue", linewidth=2,
            label="Compound (annual)")
    ax.plot(years, compound_m, color="green",     linewidth=2,
            label="Compound (monthly)")
    ax.plot(years, continuous, color="crimson",   linewidth=2,
            linestyle=":", label="Continuous  e^(rt)")
    ax.axhline(C, color="black", linewidth=0.8,
               linestyle="--", alpha=0.4)
    ax.set_title(f"Simple vs Compound Interest  (C={C:.0f}, r={r*100:.1f}%)",
                 fontsize=14)
    ax.set_xlabel("Years")
    ax.set_ylabel("Amount")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_compound(C, r, t, n):
    years      = np.linspace(0, t, 300)
    simple     = C * (1 + r*years)
    compound   = C * (1 + r/n)**(n*years)
    continuous = C * np.exp(r*years)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(years, simple,     color="gray",      linewidth=2,
                 linestyle="--", label="Simple")
    axes[0].plot(years, compound,   color="crimson",   linewidth=2,
                 label=f"Compound n={n}")
    axes[0].plot(years, continuous, color="steelblue", linewidth=1.5,
                 linestyle=":", label="Continuous e^(rt)")
    axes[0].set_title(f"Growth of {C:.0f} at {r*100:.1f}%", fontsize=12)
    axes[0].set_xlabel("Years")
    axes[0].set_ylabel("Amount")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    advantage = compound - simple
    axes[1].fill_between(years, advantage,
                         color="steelblue", alpha=0.4,
                         label="Extra from compounding")
    axes[1].plot(years, advantage, color="steelblue", linewidth=2)
    axes[1].set_title("Extra earned: compound vs simple", fontsize=12)
    axes[1].set_xlabel("Years")
    axes[1].set_ylabel("Extra amount")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Compound Interest", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_present_future(PV, FV, r, t):
    years  = np.linspace(0, t, 300)
    values = PV * (1+r)**years

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(years, values, color="crimson", linewidth=2.5)
    ax.plot(0, PV, "o", color="steelblue", markersize=12,
            label=f"PV = {PV:.2f}  (today)")
    ax.plot(t, FV, "o", color="green",     markersize=12,
            label=f"FV = {FV:.2f}  (in {t:.0f} years)")
    ax.annotate(f"PV = {PV:.2f}", (0, PV),
                textcoords="offset points", xytext=(10, 10), fontsize=11)
    ax.annotate(f"FV = {FV:.2f}", (t, FV),
                textcoords="offset points", xytext=(-80, 10), fontsize=11)
    ax.fill_between(years, PV, values,
                    alpha=0.15, color="steelblue", label="Growth")
    ax.axhline(PV, color="gray", linewidth=1,
               linestyle="--", alpha=0.5)
    ax.set_title(f"Present Value and Future Value  (r={r*100:.1f}%)", fontsize=14)
    ax.set_xlabel("Years")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_annuity(R, r, n, PV):
    payments = list(range(1, n+1))
    pv_each  = [R / (1+r)**k for k in payments]
    cum_pv   = np.cumsum(pv_each)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    colors = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, n))
    axes[0].bar(payments, pv_each, color=colors, edgecolor="none")
    axes[0].axhline(R, color="gray", linewidth=1.5,
                    linestyle="--", alpha=0.7,
                    label=f"Nominal R={R:.2f}")
    axes[0].set_title("Present value of each payment\n"
                      "(earlier payments worth more)", fontsize=11)
    axes[0].set_xlabel("Payment number")
    axes[0].set_ylabel("Present value")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis="y")

    axes[1].plot(payments, cum_pv, color="crimson",
                 linewidth=2, marker="o", markersize=4)
    axes[1].axhline(PV, color="steelblue", linewidth=1.5,
                    linestyle="--", label=f"Total PV = {PV:.2f}")
    axes[1].axhline(R*n, color="gray", linewidth=1.5,
                    linestyle=":", label=f"Total nominal = {R*n:.2f}")
    axes[1].set_title("Cumulative present value", fontsize=11)
    axes[1].set_xlabel("Payment number")
    axes[1].set_ylabel("Cumulative PV")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Annuity Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_mortgage(schedule, PV, R, n):
    months    = [s[0] for s in schedule]
    interest  = [s[2] for s in schedule]
    principal = [s[3] for s in schedule]
    remaining = [s[4] for s in schedule]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].stackplot(months, interest, principal,
                      labels=["Interest portion", "Principal portion"],
                      colors=["crimson", "steelblue"], alpha=0.7)
    axes[0].axhline(R, color="black", linewidth=1,
                    linestyle="--", alpha=0.5,
                    label=f"Total payment {R:.2f}")
    axes[0].set_title("Payment breakdown — interest vs principal",
                      fontsize=12)
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Amount")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(months, remaining, color="crimson", linewidth=2)
    axes[1].fill_between(months, remaining,
                         alpha=0.2, color="crimson")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("Remaining debt over time", fontsize=12)
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Remaining principal")
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(
        f"Mortgage Amortization  "
        f"(Loan={PV:.0f}, Payment={R:.2f}/month)",
        fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_inflation(S, r, i, t):
    years   = np.linspace(0, t, 300)
    nominal = S * (1+r)**years
    real    = S * ((1+r)/(1+i))**years
    purch   = S / (1+i)**years

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, nominal, color="steelblue", linewidth=2,
            label=f"Nominal value  (r={r*100:.1f}%)")
    ax.plot(years, real,    color="green",     linewidth=2,
            label=f"Real value  "
                  f"(r_real={(((1+r)/(1+i))-1)*100:.2f}%)")
    ax.plot(years, purch,   color="crimson",   linewidth=2,
            linestyle="--",
            label=f"Purchasing power  (inflation={i*100:.1f}%)")
    ax.axhline(S, color="gray", linewidth=1,
               linestyle=":", alpha=0.6,
               label=f"Initial S={S:.2f}")
    ax.set_title(
        f"Inflation vs Return  "
        f"(S={S:.0f}, r={r*100:.1f}%, i={i*100:.1f}%)",
        fontsize=13)
    ax.set_xlabel("Years")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def simple_interest():
    print(f"\n{'='*50}")
    print(f"SIMPLE INTEREST")
    print(f"{'='*50}")
    print(f"")
    print(f"  Simple interest is the most basic form of return.")
    print(f"  You put in a capital C, earn r% per year,")
    print(f"  and every year you get exactly the same amount.")
    print(f"  The interest never earns interest — it stays flat.")
    print(f"")
    print(f"  Formula:")
    print(f"      Interest = C · r · t")
    print(f"      Final amount = C · (1 + r·t)")
    print(f"")
    print(f"  It grows in a straight line — linear, not exponential.")
    print(f"  Useful for short-term loans and simple bonds.")
    print(f"  For long-term savings it's far less powerful than")
    print(f"  compound interest — and banks know it.")
    print(f"")

    C = float(input("  Initial capital C: "))
    r = float(input("  Annual rate r (e.g. 0.05 for 5%): "))
    t = float(input("  Time in years t: "))

    interest = C * r * t
    final    = C * (1 + r*t)

    print(f"\n--- Computing simple interest ---")
    print(f"  Capital:  {C:.2f}")
    print(f"  Rate:     {r*100:.2f}% per year")
    print(f"  Time:     {t} years")
    print(f"")
    print(f"  Interest = {C} · {r} · {t} = {interest:.2f}")
    print(f"  Final    = {C} · (1 + {r}·{t}) = {final:.2f}")
    print(f"")
    print(f"  You earn {interest:.2f} over {t} years.")
    print(f"  That's {interest/t:.2f} per year — always the same.")
    print(f"  No acceleration, no compounding. Just a straight line.")

    print(f"\n--- Year by year ---")
    print(f"  {'Year':>6}  {'Interest so far':>16}  {'Total':>12}")
    print(f"  {'─'*37}")
    for year in range(1, min(int(t)+1, 21)):
        earned = C * r * year
        total  = C + earned
        print(f"  {year:>6}  {earned:>16.2f}  {total:>12.2f}")

    plot_interest_comparison(C, r, t)


def compound_interest():
    print(f"\n{'='*50}")
    print(f"COMPOUND INTEREST")
    print(f"{'='*50}")
    print(f"")
    print(f"  Here's where it gets interesting.")
    print(f"  With compound interest, the interest you earn")
    print(f"  also starts earning interest.")
    print(f"  Interest on interest on interest — exponential growth.")
    print(f"")
    print(f"  Einstein allegedly called it 'the eighth wonder of the world.'")
    print(f"  Whether he really said it or not, the math is extraordinary.")
    print(f"  A small difference in rate, over decades,")
    print(f"  produces enormous differences in outcome.")
    print(f"")
    print(f"  Formula:")
    print(f"      A = C · (1 + r/n)^(n·t)")
    print(f"")
    print(f"  n = compounding periods per year:")
    print(f"  n = 1    annual     n = 12   monthly")
    print(f"  n = 4    quarterly  n = 365  daily")
    print(f"  n → ∞   continuous compounding:  A = C · e^(r·t)")
    print(f"")
    print(f"  The continuous case connects to Module 10 —")
    print(f"  as n → ∞, (1+r/n)^n → e^r.")
    print(f"  The natural exponential emerges from finance.")
    print(f"")

    C = float(input("  Initial capital C: "))
    r = float(input("  Annual rate r (e.g. 0.05 for 5%): "))
    t = float(input("  Time in years t: "))
    n = int(input("  Compounding periods per year n: "))

    A_compound   = C * (1 + r/n)**(n*t)
    A_simple     = C * (1 + r*t)
    A_continuous = C * math.exp(r*t)

    print(f"\n--- Computing compound interest ---")
    print(f"  Capital:      {C:.2f}")
    print(f"  Rate:         {r*100:.2f}% per year")
    print(f"  Time:         {t} years")
    print(f"  Compounding:  {n}x per year")
    print(f"")
    print(f"  A = {C} · (1 + {r}/{n})^({n}·{t})")
    print(f"    = {C} · {(1+r/n):.8f}^{n*t:.1f}")
    print(f"    = {A_compound:.2f}")
    print(f"")
    print(f"  Comparison:")
    print(f"  Simple interest:      {A_simple:.2f}   "
          f"(interest: {A_simple-C:.2f})")
    print(f"  Compound (n={n}): {A_compound:.2f}   "
          f"(interest: {A_compound-C:.2f})")
    print(f"  Continuous:           {A_continuous:.2f}   "
          f"(interest: {A_continuous-C:.2f})")
    print(f"")
    print(f"  Extra from compounding vs simple: {A_compound-A_simple:.2f}")
    print(f"  This gap grows enormously over time.")

    print(f"\n--- The Rule of 72 ---")
    print(f"  How long to double your money?")
    print(f"  Quick estimate: 72 / rate(%) = years to double.")
    print(f"")
    approx_double = 72 / (r*100)
    exact_double  = math.log(2) / math.log(1 + r/n) / n
    print(f"  Rule of 72:   72 / {r*100:.1f} = {approx_double:.1f} years")
    print(f"  Exact answer: {exact_double:.2f} years")
    print(f"  Gap:          {abs(approx_double-exact_double):.2f} years")
    print(f"")
    print(f"  Remarkably accurate for rates between 2% and 15%.")
    print(f"  Mental arithmetic shortcut used by every banker.")

    print(f"\n--- Year by year breakdown ---")
    print(f"  {'Year':>6}  {'Amount':>12}  "
          f"{'Interest this year':>20}  {'Total interest':>15}")
    print(f"  {'─'*57}")
    prev = C
    for year in range(1, min(int(t)+1, 21)):
        amount   = C * (1 + r/n)**(n*year)
        int_year = amount - prev
        tot_int  = amount - C
        print(f"  {year:>6}  {amount:>12.2f}  "
              f"{int_year:>20.2f}  {tot_int:>15.2f}")
        prev = amount

    plot_compound(C, r, t, n)


def present_future_value():
    print(f"\n{'='*50}")
    print(f"PRESENT VALUE AND FUTURE VALUE")
    print(f"{'='*50}")
    print(f"")
    print(f"  The central question of financial mathematics:")
    print(f"  how much is a future payment worth TODAY?")
    print(f"")
    print(f"  If someone promises you 1000€ in 5 years,")
    print(f"  that's worth LESS than 1000€ today.")
    print(f"  Why? Because 1000€ today, invested at 5%,")
    print(f"  grows to more than 1000€ in 5 years.")
    print(f"  So the present value of that future 1000€ must be less.")
    print(f"")
    print(f"  Two directions, one formula:")
    print(f"      FV = PV · (1+r)^t      capitalizing (moving forward)")
    print(f"      PV = FV / (1+r)^t      discounting  (moving backward)")
    print(f"")
    print(f"  The factor 1/(1+r)^t is the discount factor.")
    print(f"  It answers: for every euro I'll receive in t years,")
    print(f"  how many euros is that worth today?")
    print(f"")
    print(f"  What do you want to compute?")
    print(f"  1 — Future value   (I have money today, what will it be?)")
    print(f"  2 — Present value  (I'll receive money later, what's it worth now?)")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    r = float(input("  Annual discount rate r (e.g. 0.05 for 5%): "))
    t = float(input("  Time in years t: "))

    if choice == "1":
        PV = float(input("  Present value PV: "))
        FV = PV * (1+r)**t

        print(f"\n--- Capitalizing PV forward ---")
        print(f"  FV = PV · (1+r)^t")
        print(f"     = {PV} · (1+{r})^{t}")
        print(f"     = {PV} · {(1+r)**t:.6f}")
        print(f"     = {FV:.2f}")
        print(f"")
        print(f"  {PV:.2f} today becomes {FV:.2f} in {t:.0f} years.")
        print(f"  Total gain: {FV-PV:.2f}  ({(FV/PV-1)*100:.2f}% total return)")
        print(f"")
        df = 1 / (1+r)**t
        print(f"  Discount factor: {df:.6f}")
        print(f"  Every euro in {t:.0f} years is worth {df:.4f}€ today.")

        plot_present_future(PV, FV, r, t)

    elif choice == "2":
        FV = float(input("  Future value FV: "))
        PV = FV / (1+r)**t

        print(f"\n--- Discounting FV back to today ---")
        print(f"  PV = FV / (1+r)^t")
        print(f"     = {FV} / (1+{r})^{t}")
        print(f"     = {FV} / {(1+r)**t:.6f}")
        print(f"     = {PV:.2f}")
        print(f"")
        print(f"  {FV:.2f} in {t:.0f} years is worth {PV:.2f} today.")
        print(f"  The discount: {FV-PV:.2f} — the price of waiting.")
        print(f"")
        print(f"  Equivalently: invest {PV:.2f} today at {r*100:.1f}%")
        print(f"  and you'll have exactly {FV:.2f} in {t:.0f} years.")

        plot_present_future(PV, FV, r, t)

    else:
        print(f"  Invalid choice.")


def annuities():
    print(f"\n{'='*50}")
    print(f"ANNUITIES")
    print(f"{'='*50}")
    print(f"")
    print(f"  An annuity is a series of equal payments made")
    print(f"  at regular intervals — every month, every year.")
    print(f"  Pensions, insurance premiums, loan repayments —")
    print(f"  all of these are annuities.")
    print(f"")
    print(f"  The key question: what is the total present value")
    print(f"  of ALL these future payments combined?")
    print(f"")
    print(f"  Each payment must be discounted back to today.")
    print(f"  Payment 1 (in 1 year) is worth R/(1+r).")
    print(f"  Payment 2 (in 2 years) is worth R/(1+r)².")
    print(f"  And so on — a geometric series.")
    print(f"  Summing it gives the annuity formula:")
    print(f"")
    print(f"      PV = R · [1 - (1+r)^(-n)] / r")
    print(f"")
    print(f"  This single formula is how banks compute mortgage payments,")
    print(f"  how pension funds value their liabilities, and how you")
    print(f"  decide whether a lump sum beats a stream of payments.")
    print(f"")

    R = float(input("  Periodic payment R: "))
    r = float(input("  Periodic interest rate r (e.g. 0.05 for 5%): "))
    n = int(input("  Number of payments n: "))

    PV = R * (1 - (1+r)**(-n)) / r
    FV = R * ((1+r)**n - 1) / r

    print(f"\n--- Present value of the annuity ---")
    print(f"  PV = R · [1 - (1+r)^(-n)] / r")
    print(f"     = {R} · [1 - (1+{r})^(-{n})] / {r}")
    print(f"     = {R} · [1 - {(1+r)**(-n):.6f}] / {r}")
    print(f"     = {R} · {(1-(1+r)**(-n)):.6f} / {r}")
    print(f"     = {PV:.2f}")
    print(f"")
    print(f"  Meaning: {PV:.2f} invested today at {r*100:.2f}%")
    print(f"  is EXACTLY equivalent to receiving {R:.2f}")
    print(f"  every period for {n} periods.")
    print(f"  The two options are financially identical.")

    print(f"\n--- Future value ---")
    print(f"  FV = R · [(1+r)^n - 1] / r = {FV:.2f}")
    print(f"  Total paid in:   {R*n:.2f}")
    print(f"  Interest earned: {FV - R*n:.2f}")

    print(f"\n--- Payment by payment breakdown ---")
    print(f"  {'#':>4}  {'Payment':>10}  {'PV of payment':>15}  "
          f"{'Cumulative PV':>14}")
    print(f"  {'─'*46}")
    cum = 0
    for k in range(1, min(n+1, 21)):
        pv_k = R / (1+r)**k
        cum += pv_k
        print(f"  {k:>4}  {R:>10.2f}  {pv_k:>15.4f}  {cum:>14.4f}")
    if n > 20:
        print(f"  ... ({n-20} more)")
        print(f"  Total PV = {PV:.4f}")

    plot_annuity(R, r, n, PV)


def mortgage():
    print(f"\n{'='*50}")
    print(f"MORTGAGE AMORTIZATION")
    print(f"{'='*50}")
    print(f"")
    print(f"  A mortgage is a loan repaid through equal monthly payments.")
    print(f"  Each payment covers two things:")
    print(f"  · Interest on the remaining debt")
    print(f"  · A slice of the actual debt (principal)")
    print(f"")
    print(f"  At the start, most of each payment goes to interest.")
    print(f"  Month after month, as the debt shrinks,")
    print(f"  more goes to principal and less to interest.")
    print(f"  This gradual shift is called amortization.")
    print(f"")
    print(f"  The monthly payment formula:")
    print(f"      R = PV · r · (1+r)^n / [(1+r)^n - 1]")
    print(f"  (This is the annuity formula solved for R.)")
    print(f"")
    print(f"  The mortgage paradox:")
    print(f"  On a 30-year mortgage, you can easily pay back")
    print(f"  more than TWICE the amount you borrowed.")
    print(f"  The program will show you exactly where your money goes.")
    print(f"")

    PV = float(input("  Loan amount: "))
    r  = float(input("  Monthly interest rate (e.g. 0.004 for 4.8% annual): "))
    n  = int(input("  Number of monthly payments (e.g. 360 for 30 years): "))

    R              = PV * r * (1+r)**n / ((1+r)**n - 1)
    total_paid     = R * n
    total_interest = total_paid - PV

    print(f"\n--- Your mortgage ---")
    print(f"  Loan amount:      {PV:>12.2f}")
    print(f"  Monthly rate:     {r*100:.4f}%  ({r*12*100:.2f}% annual)")
    print(f"  Duration:         {n} months  ({n//12} years)")
    print(f"")
    print(f"  Monthly payment:  {R:>12.2f}")
    print(f"  Total paid:       {total_paid:>12.2f}")
    print(f"  Total interest:   {total_interest:>12.2f}")
    print(f"  Interest as % of loan: {total_interest/PV*100:.1f}%")
    print(f"")
    print(f"  For every euro borrowed, you pay back {total_paid/PV:.2f}€.")
    if total_interest > PV:
        print(f"  You pay more in interest than in principal.")
        print(f"  This is the mortgage paradox — and it's real.")
    print(f"")
    print(f"  This is why paying even a little extra each month")
    print(f"  (toward the principal) saves enormous amounts of interest.")

    print(f"\n--- Amortization schedule ---")
    print(f"  (First 5 and last 5 payments shown)")
    print(f"")
    print(f"  {'Month':>6}  {'Payment':>10}  {'Interest':>10}  "
          f"{'Principal':>10}  {'Remaining':>12}")
    print(f"  {'─'*52}")

    balance  = PV
    schedule = []
    for month in range(1, n+1):
        int_paid  = balance * r
        prin_paid = R - int_paid
        balance  -= prin_paid
        schedule.append((month, R, int_paid, prin_paid, max(balance, 0)))

    for row in schedule[:5]:
        print(f"  {row[0]:>6}  {row[1]:>10.2f}  {row[2]:>10.2f}  "
              f"{row[3]:>10.2f}  {row[4]:>12.2f}")
    if n > 10:
        print(f"  {'...':>6}")
    for row in schedule[-5:]:
        print(f"  {row[0]:>6}  {row[1]:>10.2f}  {row[2]:>10.2f}  "
              f"{row[3]:>10.2f}  {row[4]:>12.2f}")

    print(f"")
    print(f"  Notice: in the first payment, {schedule[0][2]:.2f} is interest")
    print(f"  and only {schedule[0][3]:.2f} reduces the debt.")
    print(f"  In the last payment, {schedule[-1][2]:.2f} is interest")
    print(f"  and {schedule[-1][3]:.2f} goes to principal.")
    print(f"  The shift happens gradually over {n//12} years.")

    plot_mortgage(schedule, PV, R, n)


def inflation():
    print(f"\n{'='*50}")
    print(f"INFLATION AND PURCHASING POWER")
    print(f"{'='*50}")
    print(f"")
    print(f"  Inflation is the rate at which prices rise.")
    print(f"  It silently erodes the value of money.")
    print(f"  100€ today buys less than 100€ did 10 years ago.")
    print(f"  And 100€ in 10 years will buy less than 100€ today.")
    print(f"")
    print(f"  The real interest rate — what you actually earn")
    print(f"  after accounting for inflation:")
    print(f"")
    print(f"      (1 + r_real) = (1 + r_nominal) / (1 + i)")
    print(f"      r_real ≈ r_nominal - i  (Fisher approximation)")
    print(f"")
    print(f"  Example: 5% return, 3% inflation → ~2% real return.")
    print(f"  Your account balance grows — but your purchasing power")
    print(f"  grows much less.")
    print(f"")
    print(f"  The dangerous case: if your return is below inflation,")
    print(f"  you're losing purchasing power even as the number grows.")
    print(f"  Money in a mattress loses value every year.")
    print(f"")

    S = float(input("  Initial amount S: "))
    i = float(input("  Annual inflation rate i (e.g. 0.03 for 3%): "))
    r = float(input("  Annual nominal return r (e.g. 0.05 for 5%): "))
    t = float(input("  Years t: "))

    nominal = S * (1+r)**t
    real    = S * ((1+r)/(1+i))**t
    purch   = S / (1+i)**t
    r_real  = (1+r)/(1+i) - 1
    r_approx = r - i

    print(f"\n--- After {t:.0f} years ---")
    print(f"  Nominal value (ignoring inflation):  {nominal:.2f}")
    print(f"  Real value (inflation-adjusted):     {real:.2f}")
    print(f"  Purchasing power of S alone:         {purch:.2f}")
    print(f"")
    print(f"  Nominal return:       {r*100:.2f}%")
    print(f"  Inflation rate:       {i*100:.2f}%")
    print(f"  Real return (exact):  {r_real*100:.4f}%")
    print(f"  Real return (approx): {r_approx*100:.4f}%")
    print(f"")

    if r_real > 0:
        print(f"  Real return is positive ✓")
        print(f"  Your purchasing power grows at {r_real*100:.2f}% per year.")
        print(f"  You're genuinely getting richer.")
    elif r_real < 0:
        print(f"  Real return is NEGATIVE ✗")
        print(f"  Your nominal value grows, but your purchasing power shrinks.")
        print(f"  You lose {abs(r_real)*100:.2f}% purchasing power per year.")
        print(f"  This is the hidden cost of low-return investments")
        print(f"  in high-inflation environments.")
    else:
        print(f"  Real return = 0 — purchasing power is unchanged.")

    print(f"\n--- Rule of 72 for inflation ---")
    halving   = 72 / (i*100)
    halving_e = math.log(2) / math.log(1+i)
    print(f"  At {i*100:.1f}% inflation, purchasing power halves in:")
    print(f"  Rule of 72: {halving:.1f} years")
    print(f"  Exact:      {halving_e:.2f} years")
    print(f"")
    print(f"  This means: in {halving_e:.0f} years, you need twice")
    print(f"  as much money to buy the same things as today.")

    plot_inflation(S, r, i, t)


def financial_math():
    print(f"\n{'='*50}")
    print(f"FINANCIAL MATHEMATICS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Financial mathematics is the language of money over time.")
    print(f"  One principle drives everything:")
    print(f"")
    print(f"      A euro today is worth more than a euro tomorrow.")
    print(f"")
    print(f"  From this single idea you can understand:")
    print(f"  how savings grow, how mortgages work, how pensions")
    print(f"  are valued, how inflation erodes wealth, and how to")
    print(f"  compare any two financial options rationally.")
    print(f"")
    print(f"  These aren't just formulas for exams.")
    print(f"  A 30-year mortgage at 5% costs you nearly twice")
    print(f"  the loan amount in total. Knowing why — and knowing")
    print(f"  what to do about it — is genuinely valuable.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Simple interest       linear growth")
    print(f"  2 — Compound interest     exponential growth + Rule of 72")
    print(f"  3 — Present & future value  the time value of money")
    print(f"  4 — Annuities             streams of equal payments")
    print(f"  5 — Mortgage              amortization and the true cost")
    print(f"  6 — Inflation             real vs nominal returns")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, 5, or 6: ")

    if choice == "1":
        simple_interest()
    elif choice == "2":
        compound_interest()
    elif choice == "3":
        present_future_value()
    elif choice == "4":
        annuities()
    elif choice == "5":
        mortgage()
    elif choice == "6":
        inflation()
    else:
        print(f"  Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    financial_math()
    