import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def fmt(z):
    r, i = z.real, z.imag
    if abs(i) < 1e-10:
        return f"{r:.4f}"
    elif abs(r) < 1e-10:
        return f"{i:.4f}i"
    elif i >= 0:
        return f"{r:.4f} + {i:.4f}i"
    else:
        return f"{r:.4f} - {abs(i):.4f}i"


def plot_complex_plane(numbers, labels, title="Complex Plane"):
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ["crimson", "steelblue", "green", "orange",
              "purple", "brown", "pink", "teal"]
    max_val = max(max(abs(z.real), abs(z.imag))
                  for z in numbers if z != 0) + 1

    for z, label, color in zip(numbers, labels, colors):
        ax.plot(z.real, z.imag, "o", color=color, markersize=10)
        ax.annotate(f"  {label} = {fmt(z)}",
                    (z.real, z.imag), fontsize=10, color=color)
        ax.plot([0, z.real], [0, z.imag], color=color,
                linewidth=1, linestyle="--", alpha=0.4)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_aspect("equal")
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imaginary axis")
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_polar(z, r, theta):
    fig, ax = plt.subplots(figsize=(8, 8))

    t = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(t), np.sin(t), color="gray",
            linewidth=0.8, linestyle="--", alpha=0.5,
            label="Unit circle")
    ax.plot(r*np.cos(t), r*np.sin(t), color="steelblue",
            linewidth=0.8, linestyle="--", alpha=0.4,
            label=f"Circle r={r:.2f}")

    ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->",
                                color="crimson", lw=2))
    ax.plot(z.real, z.imag, "o", color="crimson", markersize=10)
    ax.annotate(f"  z = {fmt(z)}\n"
                f"  r={r:.2f}, θ={math.degrees(theta):.1f}°",
                (z.real, z.imag), fontsize=10, color="crimson")

    arc_t = np.linspace(0, theta if theta >= 0 else theta + 2*math.pi, 100)
    arc_r = r * 0.3
    ax.plot(arc_r*np.cos(arc_t), arc_r*np.sin(arc_t),
            color="green", linewidth=1.5)
    ax.annotate(f"θ={math.degrees(theta):.1f}°",
                (arc_r*0.6*math.cos(theta/2),
                 arc_r*0.6*math.sin(theta/2)),
                fontsize=10, color="green")

    ax.plot([z.real, z.real], [0, z.imag],
            color="gray", linewidth=1, linestyle=":")
    ax.plot([0, z.real], [z.imag, z.imag],
            color="gray", linewidth=1, linestyle=":")
    ax.text(z.real/2, -0.25, f"a={z.real:.2f}",
            ha="center", fontsize=9, color="gray")
    ax.text(-0.4, z.imag/2, f"b={z.imag:.2f}",
            ha="right", fontsize=9, color="gray")

    lim = max(r + 1, 2.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imaginary axis")
    ax.set_title(f"Polar form: z = {r:.2f}·e^(i·{theta:.3f})", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_nth_roots(roots, labels, r_root, n, original):
    fig, ax = plt.subplots(figsize=(8, 8))

    t = np.linspace(0, 2*np.pi, 400)
    ax.plot(r_root*np.cos(t), r_root*np.sin(t),
            color="steelblue", linewidth=1.5, linestyle="--",
            alpha=0.6, label=f"Circle r={r_root:.3f}")

    coords = [(z.real, z.imag) for z in roots]
    coords.append(coords[0])
    ax.plot([c[0] for c in coords], [c[1] for c in coords],
            color="green", linewidth=1, linestyle="-", alpha=0.4)

    colors = plt.cm.tab10(np.linspace(0, 1, len(roots)))
    for z, label, color in zip(roots, labels, colors):
        ax.plot(z.real, z.imag, "o", color=color, markersize=12)
        ax.annotate(f"  {label}\n  {fmt(z)}",
                    (z.real, z.imag), fontsize=9, color=color)

    ax.plot(original.real, original.imag, "*",
            color="crimson", markersize=15,
            label=f"z = {fmt(original)}")

    lim = max(r_root + 1, abs(original) + 1, 2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imaginary axis")
    ax.set_title(f"The {n} roots of z = {fmt(original)}\n"
                 f"— vertices of a regular {n}-gon", fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def complex_operations():
    print(f"\n{'='*50}")
    print(f"COMPLEX NUMBERS — BASIC OPERATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A complex number is written as  z = a + bi")
    print(f"  where a is the real part and b is the imaginary part.")
    print(f"  i is defined by one single rule:  i² = -1")
    print(f"")
    print(f"  That one rule — i² = -1 — is all you need.")
    print(f"  Everything else follows from normal algebra.")
    print(f"  Whenever i² appears, replace it with -1. That's it.")
    print(f"")
    print(f"  The operations work exactly like polynomials in i,")
    print(f"  with the substitution i² = -1 applied at the end.")
    print(f"")

    a = float(input("  z₁ real part a: "))
    b = float(input("  z₁ imaginary part b: "))
    c = float(input("  z₂ real part c: "))
    d = float(input("  z₂ imaginary part d: "))

    z1 = complex(a, b)
    z2 = complex(c, d)

    print(f"\n  z₁ = {fmt(z1)}")
    print(f"  z₂ = {fmt(z2)}")

    print(f"\n--- Addition ---")
    print(f"  Add real parts together, imaginary parts together.")
    print(f"  Nothing surprising here — just component-wise addition.")
    print(f"  z₁ + z₂ = ({a} + {c}) + ({b} + {d})i")
    s = z1 + z2
    print(f"         = {fmt(s)}")

    print(f"\n--- Subtraction ---")
    print(f"  Same logic — subtract component by component.")
    print(f"  z₁ - z₂ = ({a} - {c}) + ({b} - {d})i")
    diff = z1 - z2
    print(f"         = {fmt(diff)}")

    print(f"\n--- Multiplication ---")
    print(f"  Expand like a binomial, then replace i² with -1.")
    print(f"  This is where the definition i² = -1 actually does work.")
    print(f"")
    print(f"  z₁ · z₂ = ({a} + {b}i)({c} + {d}i)")
    print(f"           = {a*c} + {a*d}i + {b*c}i + {b*d}i²")
    print(f"           = {a*c} + {a*d}i + {b*c}i + {b*d}·(-1)")
    print(f"           = ({a*c} - {b*d}) + ({a*d} + {b*c})i")
    prod = z1 * z2
    print(f"           = {fmt(prod)}")

    print(f"\n--- Complex conjugate ---")
    print(f"  The conjugate of z = a + bi is z̄ = a - bi.")
    print(f"  Just flip the sign of the imaginary part.")
    print(f"")
    print(f"  Why does it matter?")
    print(f"  z · z̄ = (a + bi)(a - bi) = a² + b²")
    print(f"  The product is always real — no imaginary part.")
    print(f"  This is the trick that makes division possible.")
    print(f"")
    z1c = z1.conjugate()
    print(f"  z̄₁ = {fmt(z1c)}")
    print(f"  z₁ · z̄₁ = {a}² + {b}² = {a**2 + b**2:.4f}  (real ✓)")

    print(f"\n--- Division ---")
    print(f"  You can't divide by a complex number directly.")
    print(f"  The trick: multiply top and bottom by the conjugate of z₂.")
    print(f"  The denominator becomes real — then divide normally.")
    print(f"")
    if abs(z2) < 1e-12:
        print(f"  z₂ = 0 — division undefined.")
    else:
        print(f"  z₁/z₂ = (z₁ · z̄₂) / (z₂ · z̄₂)")
        print(f"        = (z₁ · z̄₂) / (c² + d²)")
        print(f"        = (z₁ · z̄₂) / {c**2 + d**2:.4f}")
        quot = z1 / z2
        print(f"        = {fmt(quot)}")

    print(f"\n--- Modulus ---")
    print(f"  The modulus |z| is the distance from z to the origin.")
    print(f"  It's the Pythagorean theorem on the complex plane:")
    print(f"  |z| = √(a² + b²)")
    print(f"")
    print(f"  |z₁| = √({a}² + {b}²) = {abs(z1):.4f}")
    print(f"  |z₂| = √({c}² + {d}²) = {abs(z2):.4f}")
    print(f"")
    print(f"  A beautiful property: |z₁ · z₂| = |z₁| · |z₂|")
    print(f"  {abs(z1):.4f} · {abs(z2):.4f} = {abs(z1)*abs(z2):.4f}")
    print(f"  |z₁ · z₂| = {abs(prod):.4f}  ✓")

    plot_complex_plane([z1, z2, s, prod],
                       ["z₁", "z₂", "z₁+z₂", "z₁·z₂"])


def polar_form():
    print(f"\n{'='*50}")
    print(f"POLAR FORM AND EULER'S FORMULA")
    print(f"{'='*50}")
    print(f"")
    print(f"  Every complex number lives at a point in the plane.")
    print(f"  Instead of describing it with coordinates (a, b),")
    print(f"  you can describe it with distance and angle:")
    print(f"")
    print(f"      z = r · (cos θ + i·sin θ)")
    print(f"")
    print(f"  · r = |z| = √(a²+b²)    the modulus — distance from origin")
    print(f"  · θ = arg(z)              the argument — angle with real axis")
    print(f"")
    print(f"  The connection to trigonometry is direct:")
    print(f"  a = r·cos θ  and  b = r·sin θ")
    print(f"  exactly like the unit circle, but scaled by r.")
    print(f"")
    print(f"  Now here's where it gets extraordinary.")
    print(f"  Euler's formula says:")
    print(f"")
    print(f"      e^(iθ) = cos θ + i·sin θ")
    print(f"")
    print(f"  So the polar form becomes simply:  z = r·e^(iθ)")
    print(f"")
    print(f"  This connects three seemingly unrelated things:")
    print(f"  the exponential function, trigonometry, and complex numbers.")
    print(f"  They turn out to be the same thing in disguise.")
    print(f"")
    print(f"  The most famous special case: set θ = π")
    print(f"  e^(iπ) = cos π + i·sin π = -1")
    print(f"  e^(iπ) + 1 = 0")
    print(f"")
    print(f"  Five of the most important constants in mathematics —")
    print(f"  e, i, π, 1, 0 — in one equation.")
    print(f"  This is why mathematicians call it the most beautiful")
    print(f"  formula ever written.")
    print(f"")

    a = float(input("  Real part a: "))
    b = float(input("  Imaginary part b: "))

    z     = complex(a, b)
    r     = abs(z)
    theta = math.atan2(b, a)

    print(f"\n  z = {fmt(z)}")

    print(f"\n--- Step 1: Modulus ---")
    print(f"  r = √({a}² + {b}²) = √{a**2+b**2:.4f} = {r:.4f}")

    print(f"\n--- Step 2: Argument ---")
    print(f"  θ = atan2({b}, {a}) = {theta:.4f} rad = {math.degrees(theta):.2f}°")
    print(f"")
    print(f"  We use atan2 instead of arctan(b/a) because arctan")
    print(f"  can't tell apart angles in opposite quadrants.")
    print(f"  atan2 uses the signs of both a and b to get the right quadrant.")

    print(f"\n--- Step 3: Polar form ---")
    print(f"  z = {r:.4f} · (cos({theta:.4f}) + i·sin({theta:.4f}))")
    print(f"    = {r:.4f} · e^(i·{theta:.4f})")
    print(f"")
    print(f"  Verify:")
    print(f"  r·cos θ = {r:.4f}·{math.cos(theta):.4f} = {r*math.cos(theta):.4f}  (expected {a}) ✓")
    print(f"  r·sin θ = {r:.4f}·{math.sin(theta):.4f} = {r*math.sin(theta):.4f}  (expected {b}) ✓")

    print(f"\n--- Why polar form is powerful ---")
    print(f"  In polar form, multiplication becomes elegant:")
    print(f"  z₁·z₂ = r₁·r₂ · e^(i(θ₁+θ₂))")
    print(f"  Multiply the moduli. Add the arguments.")
    print(f"  Geometrically: scale by r₂ and rotate by θ₂.")
    print(f"  Much cleaner than expanding (a+bi)(c+di) every time.")

    plot_polar(z, r, theta)


def de_moivre():
    print(f"\n{'='*50}")
    print(f"DE MOIVRE'S THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  De Moivre's theorem is what you get when you apply")
    print(f"  Euler's formula to integer powers:")
    print(f"")
    print(f"      (cos θ + i·sin θ)^n = cos(nθ) + i·sin(nθ)")
    print(f"")
    print(f"  In polar form this is just the exponent rule:")
    print(f"  (e^(iθ))^n = e^(inθ)  — obvious.")
    print(f"  But the consequence is powerful.")
    print(f"")
    print(f"  Raising a complex number to the n-th power:")
    print(f"  · Multiplies the argument by n  (rotates)")
    print(f"  · Raises the modulus to the n-th power  (scales)")
    print(f"  Geometrically: every power is a rotation and a scaling.")
    print(f"")
    print(f"  A beautiful application — double angle formulas:")
    print(f"  (cos θ + i·sin θ)² = cos(2θ) + i·sin(2θ)")
    print(f"  But also = cos²θ - sin²θ + 2i·sinθ·cosθ")
    print(f"  Comparing real and imaginary parts:")
    print(f"  · cos(2θ) = cos²θ - sin²θ")
    print(f"  · sin(2θ) = 2·sinθ·cosθ")
    print(f"  The same formulas from Module 8 — derived in two lines.")
    print(f"")

    a = float(input("  Real part a: "))
    b = float(input("  Imaginary part b: "))
    n = int(input("  Power n: "))

    z     = complex(a, b)
    r     = abs(z)
    theta = math.atan2(b, a)

    print(f"\n  z = {fmt(z)}")
    print(f"  r = {r:.4f},  θ = {math.degrees(theta):.2f}°")

    print(f"\n--- Computing z^{n} using De Moivre ---")
    print(f"  z^{n} = r^{n} · (cos({n}θ) + i·sin({n}θ))")
    print(f"")

    r_n     = r**n
    theta_n = n * theta

    print(f"  r^{n}  = {r:.4f}^{n} = {r_n:.4f}")
    print(f"  {n}·θ  = {n} · {math.degrees(theta):.2f}° = {math.degrees(theta_n):.2f}°")
    print(f"")
    print(f"  cos({math.degrees(theta_n):.2f}°) = {math.cos(theta_n):.4f}")
    print(f"  sin({math.degrees(theta_n):.2f}°) = {math.sin(theta_n):.4f}")
    print(f"")

    result = complex(r_n*math.cos(theta_n), r_n*math.sin(theta_n))
    direct = z**n

    print(f"  z^{n} = {r_n:.4f} · ({math.cos(theta_n):.4f} + {math.sin(theta_n):.4f}i)")
    print(f"       = {fmt(result)}")
    print(f"")
    print(f"  Direct computation: {fmt(direct)}  ✓")

    print(f"\n--- Geometric interpretation ---")
    print(f"  Starting angle:   {math.degrees(theta):.2f}°")
    print(f"  After power {n}:    {math.degrees(theta_n):.2f}°  (×{n})")
    print(f"  Starting modulus: {r:.4f}")
    print(f"  After power {n}:    {r_n:.4f}  (^{n})")

    print(f"\n--- All powers z^1 to z^{abs(n)} ---")
    powers = []
    labels = []
    for k in range(1, abs(n)+1):
        zk = z**k
        powers.append(zk)
        labels.append(f"z^{k}")
        print(f"  z^{k} = {fmt(zk)}"
              f"  (r={abs(zk):.3f}, θ={math.degrees(math.atan2(zk.imag,zk.real)):.1f}°)")

    plot_complex_plane(powers, labels,
                       title=f"Powers of z={fmt(z)} — De Moivre")


def nth_roots():
    print(f"\n{'='*50}")
    print(f"N-TH ROOTS OF COMPLEX NUMBERS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Every complex number has exactly n distinct n-th roots.")
    print(f"  Not one, not sometimes n — always exactly n.")
    print(f"")
    print(f"  If z = r·e^(iθ), the n roots are:")
    print(f"")
    print(f"      zₖ = r^(1/n) · e^(i(θ+2πk)/n)   k = 0, 1, ..., n-1")
    print(f"")
    print(f"  Three things to notice:")
    print(f"  · All roots have the same modulus r^(1/n)")
    print(f"  · They are equally spaced around a circle")
    print(f"  · The gap between consecutive roots is 360°/n")
    print(f"")
    print(f"  Geometrically: the n roots are the vertices of a regular")
    print(f"  n-gon inscribed in a circle of radius r^(1/n).")
    print(f"  This is one of the most beautiful results in complex analysis.")
    print(f"")
    print(f"  The n-th roots of 1 (called roots of unity)")
    print(f"  always form a perfect regular polygon centered at the origin.")
    print(f"  Try n=3 with z=1 — you get an equilateral triangle.")
    print(f"  n=4 gives a square. n=6 gives a regular hexagon.")
    print(f"")
    print(f"  This connects to the Fundamental Theorem of Algebra:")
    print(f"  every polynomial of degree n has exactly n roots")
    print(f"  in the complex numbers — no exceptions, no special cases.")
    print(f"")

    a = float(input("  Real part a: "))
    b = float(input("  Imaginary part b: "))
    n = int(input("  Root degree n: "))

    if n <= 0:
        print(f"  n must be a positive integer.")
        return

    z      = complex(a, b)
    r      = abs(z)
    theta  = math.atan2(b, a)
    r_root = r**(1/n)

    print(f"\n  z = {fmt(z)}")
    print(f"  r = {r:.4f},  θ = {math.degrees(theta):.2f}°")

    print(f"\n--- The {n} roots ---")
    print(f"  Each root has modulus: r^(1/{n}) = {r:.4f}^(1/{n}) = {r_root:.4f}")
    print(f"  Angular spacing: 360°/{n} = {360/n:.2f}°")
    print(f"")

    roots  = []
    labels = []

    for k in range(n):
        theta_k = (theta + 2*math.pi*k) / n
        zk      = complex(r_root*math.cos(theta_k),
                          r_root*math.sin(theta_k))
        roots.append(zk)
        labels.append(f"z{k}")
        print(f"  Root {k}:")
        print(f"    angle = ({math.degrees(theta):.2f}° + {k}·360°) / {n}"
              f" = {math.degrees(theta_k):.2f}°")
        print(f"    zₖ = {fmt(zk)}")
        check = zk**n
        print(f"    zₖ^{n} = {fmt(check)}  (expected {fmt(z)}) ✓")
        print(f"")

    print(f"--- Why exactly n roots and not more? ---")
    print(f"  e^(iθ) = e^(i(θ+2πk)) for any integer k.")
    print(f"  So there are infinitely many angles that work.")
    print(f"  But for k=n the angle becomes (θ+2πn)/n = θ/n + 2π,")
    print(f"  which is the same as k=0 — we've gone full circle.")
    print(f"  So k=0,1,...,n-1 give exactly n distinct roots.")
    print(f"  Any further k just repeats one we already have.")

    plot_nth_roots(roots, labels, r_root, n, z)


def complex_equations():
    print(f"\n{'='*50}")
    print(f"EQUATIONS IN THE COMPLEX FIELD")
    print(f"{'='*50}")
    print(f"")
    print(f"  In Module 1 we left something unresolved.")
    print(f"  When Δ < 0, we said 'no real solutions' and moved on.")
    print(f"  In the complex field, those equations DO have solutions —")
    print(f"  two complex conjugate roots, always.")
    print(f"")
    print(f"  The Fundamental Theorem of Algebra says:")
    print(f"  every polynomial of degree n has exactly n roots")
    print(f"  in the complex numbers.")
    print(f"  Real numbers left gaps. Complex numbers fill them all.")
    print(f"")
    print(f"  Which equation?")
    print(f"  1 — Quadratic ax²+bx+c=0  (the Δ<0 case we left open)")
    print(f"  2 — z^n = w               (roots using De Moivre)")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    if choice == "1":
        a = float(input("  a: "))
        b = float(input("  b: "))
        c = float(input("  c: "))

        delta = b**2 - 4*a*c
        print(f"\n  Δ = {b}² - 4·{a}·{c} = {delta:.4f}")
        print(f"")

        if delta >= 0:
            print(f"  Δ ≥ 0 — the roots are real.")
            print(f"  You've already solved these in Module 1.")
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            print(f"  x₁ = {x1:.4f}")
            print(f"  x₂ = {x2:.4f}")
        else:
            print(f"  Δ < 0 — no real roots.")
            print(f"  But √Δ exists in the complex field.")
            print(f"  √({delta:.4f}) = √({-delta:.4f}) · √(-1) = {math.sqrt(-delta):.4f}i")
            print(f"")
            sqrt_d = math.sqrt(-delta)
            re     = -b / (2*a)
            im     = sqrt_d / (2*a)
            z1     = complex(re,  im)
            z2     = complex(re, -im)

            print(f"  x = (-b ± √Δ) / 2a")
            print(f"    = ({-b} ± {sqrt_d:.4f}i) / {2*a}")
            print(f"")
            print(f"  z₁ = {fmt(z1)}")
            print(f"  z₂ = {fmt(z2)}")
            print(f"")
            print(f"  Notice: z₁ and z₂ are complex conjugates.")
            print(f"  This always happens when the coefficients are real.")
            print(f"  Complex roots of real polynomials always come in pairs.")
            print(f"")
            print(f"--- Verify ---")
            for z, label in [(z1,"z₁"), (z2,"z₂")]:
                check = a*z**2 + b*z + c
                print(f"  {label}: result = {fmt(check)} ≈ 0 ✓")

            plot_complex_plane([z1, z2],
                               ["z₁", "z₂"],
                               title=f"Complex roots of {a}x²+{b}x+{c}=0")

    elif choice == "2":
        a = float(input("  w real part: "))
        b = float(input("  w imaginary part: "))
        n = int(input("  Degree n: "))

        z      = complex(a, b)
        r      = abs(z)
        theta  = math.atan2(b, a)
        r_root = r**(1/n)
        roots  = []
        labels = []

        print(f"\n  Finding all solutions to z^{n} = {fmt(z)}")
        print(f"")

        for k in range(n):
            theta_k = (theta + 2*math.pi*k) / n
            zk      = complex(r_root*math.cos(theta_k),
                              r_root*math.sin(theta_k))
            roots.append(zk)
            labels.append(f"z{k}")
            print(f"  z{k} = {fmt(zk)}")

        plot_nth_roots(roots, labels, r_root, n, z)

    else:
        print(f"  Invalid choice.")


def complex_numbers():
    print(f"\n{'='*50}")
    print(f"COMPLEX NUMBERS")
    print(f"{'='*50}")
    print(f"")
    print(f"  For centuries, mathematicians refused to accept √(-1).")
    print(f"  It seemed absurd — no real number squared gives negative.")
    print(f"  Then in the 1500s Cardano noticed something unsettling:")
    print(f"  if you allow √(-1) in intermediate steps of cubic equations,")
    print(f"  you get correct real answers at the end.")
    print(f"  The 'impossible' numbers were somehow useful.")
    print(f"")
    print(f"  It took two more centuries to understand why.")
    print(f"  Complex numbers are not fake — they're points on a plane.")
    print(f"  The real numbers are just one line through that plane.")
    print(f"  Extending to the plane completes algebra perfectly:")
    print(f"  every polynomial of degree n has exactly n roots.")
    print(f"  No exceptions. No leftover cases. Always.")
    print(f"")
    print(f"  And they appear in physics constantly —")
    print(f"  quantum mechanics, electrical engineering, signal processing.")
    print(f"  Schrödinger's equation, the equation that describes")
    print(f"  how particles behave, is fundamentally complex-valued.")
    print(f"  The universe itself seems to prefer complex numbers.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Basic operations      sum, product, division, modulus")
    print(f"  2 — Polar form            Euler's formula, e^(iπ)+1=0")
    print(f"  3 — De Moivre's theorem   powers as rotations")
    print(f"  4 — N-th roots            the regular polygon result")
    print(f"  5 — Equations             closing the gaps real numbers left")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        complex_operations()
    elif choice == "2":
        polar_form()
    elif choice == "3":
        de_moivre()
    elif choice == "4":
        nth_roots()
    elif choice == "5":
        complex_equations()
    else:
        print(f"  Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    complex_numbers()
    