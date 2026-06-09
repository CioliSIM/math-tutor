import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot_vectors(v, w, cross):
    fig = plt.figure(figsize=(9, 8))
    ax  = fig.add_subplot(111, projection='3d')

    def draw(vec, color, label):
        ax.quiver(0, 0, 0, vec[0], vec[1], vec[2],
                  color=color, linewidth=2,
                  arrow_length_ratio=0.15, label=label)

    draw(v,     "crimson",   f"v = {tuple(np.round(v,2))}")
    draw(w,     "steelblue", f"w = {tuple(np.round(w,2))}")
    draw(cross, "green",
         f"v×w = ({cross[0]:.2f},{cross[1]:.2f},{cross[2]:.2f})")

    corners = np.array([np.zeros(3), v, v+w, w, np.zeros(3)])
    ax.plot(corners[:,0], corners[:,1], corners[:,2],
            color="gray", linewidth=1, linestyle="--", alpha=0.5)

    lim = max(np.max(np.abs(v)), np.max(np.abs(w)),
              np.max(np.abs(cross))*0.5, 1) + 0.5
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("Vectors in 3D Space", fontsize=13)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_lines_space(p1, d1, p2, d2):
    fig = plt.figure(figsize=(9, 8))
    ax  = fig.add_subplot(111, projection='3d')

    t   = np.linspace(-3, 3, 100)
    l1  = np.array([p1 + ti*d1 for ti in t])
    l2  = np.array([p2 + ti*d2 for ti in t])

    ax.plot(l1[:,0], l1[:,1], l1[:,2],
            color="crimson",   linewidth=2, label="Line 1")
    ax.plot(l2[:,0], l2[:,1], l2[:,2],
            color="steelblue", linewidth=2, label="Line 2")
    ax.scatter(*p1, color="crimson",   s=60, zorder=5)
    ax.scatter(*p2, color="steelblue", s=60, zorder=5)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("Lines in 3D Space", fontsize=13)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_plane(a, b, c, d, points=None):
    fig = plt.figure(figsize=(9, 8))
    ax  = fig.add_subplot(111, projection='3d')

    xx, yy = np.meshgrid(np.linspace(-3, 3, 20),
                         np.linspace(-3, 3, 20))
    if abs(c) > 1e-10:
        zz = (-a*xx - b*yy - d) / c
    else:
        zz = np.zeros_like(xx)

    ax.plot_surface(xx, yy, zz, alpha=0.25, color="steelblue")

    z0 = float(-d/c) if abs(c) > 1e-10 else 0
    ax.quiver(0, 0, z0, a, b, c,
              color="crimson", linewidth=2,
              arrow_length_ratio=0.15, label="Normal n")

    if points:
        for pt in points:
            ax.scatter(*pt, color="green", s=80, zorder=5)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(f"Plane: {a:.2f}x+{b:.2f}y+{c:.2f}z+{d:.2f}=0",
                 fontsize=12)
    ax.legend()
    plt.tight_layout()
    plt.show()


def vector_operations():
    print(f"\n{'='*50}")
    print(f"VECTORS IN SPACE")
    print(f"{'='*50}")
    print(f"")
    print(f"  A vector in 3D space has three components —")
    print(f"  one for each axis: x, y, z.")
    print(f"  It represents a direction and a magnitude.")
    print(f"  Written as v = (x, y, z).")
    print(f"")
    print(f"  Vectors are the natural language of 3D geometry.")
    print(f"  Forces, velocities, electric fields — all vectors.")
    print(f"  And every geometric relationship in space can be")
    print(f"  expressed through a few vector operations.")
    print(f"")
    print(f"  Enter two vectors v and w:")
    print(f"")

    vx = float(input("  v → x: "))
    vy = float(input("       y: "))
    vz = float(input("       z: "))
    wx = float(input("  w → x: "))
    wy = float(input("       y: "))
    wz = float(input("       z: "))

    v = np.array([vx, vy, vz])
    w = np.array([wx, wy, wz])

    print(f"\n  v = ({vx}, {vy}, {vz})")
    print(f"  w = ({wx}, {wy}, {wz})")

    print(f"\n--- Addition and subtraction ---")
    print(f"  Add component by component — nothing complicated here.")
    s = v + w
    d = v - w
    print(f"  v + w = ({s[0]}, {s[1]}, {s[2]})")
    print(f"  v - w = ({d[0]}, {d[1]}, {d[2]})")

    print(f"\n--- Modulus (length) ---")
    print(f"  The modulus is the length of the vector arrow.")
    print(f"  It's the Pythagorean theorem extended to 3D:")
    print(f"  |v| = √(x² + y² + z²)")
    print(f"")
    mod_v = np.linalg.norm(v)
    mod_w = np.linalg.norm(w)
    print(f"  |v| = √({vx}²+{vy}²+{vz}²) = {mod_v:.4f}")
    print(f"  |w| = √({wx}²+{wy}²+{wz}²) = {mod_w:.4f}")

    print(f"\n--- Unit vector ---")
    print(f"  A unit vector has length exactly 1.")
    print(f"  It carries only direction — no magnitude.")
    print(f"  v̂ = v / |v|")
    print(f"")
    if mod_v > 1e-10:
        uv = v / mod_v
        print(f"  v̂ = ({uv[0]:.4f}, {uv[1]:.4f}, {uv[2]:.4f})")
        print(f"  |v̂| = {np.linalg.norm(uv):.8f} ✓")
    else:
        print(f"  v is the zero vector — unit vector undefined.")

    print(f"\n--- Dot product ---")
    print(f"  v · w = vx·wx + vy·wy + vz·wz")
    print(f"")
    print(f"  Geometric meaning: v · w = |v|·|w|·cos(θ)")
    print(f"  where θ is the angle between the two vectors.")
    print(f"  The most important consequence:")
    print(f"  v · w = 0  if and only if  v ⊥ w")
    print(f"  Perpendicularity reduces to a single number check.")
    print(f"")
    dot = np.dot(v, w)
    print(f"  v · w = {vx}·{wx} + {vy}·{wy} + {vz}·{wz}")
    print(f"        = {vx*wx:.4f} + {vy*wy:.4f} + {vz*wz:.4f}")
    print(f"        = {dot:.4f}")
    print(f"")

    if mod_v > 1e-10 and mod_w > 1e-10:
        cos_t = max(-1, min(1, dot/(mod_v*mod_w)))
        theta = math.degrees(math.acos(cos_t))
        print(f"  Angle: cos(θ) = {dot:.4f} / ({mod_v:.4f}·{mod_w:.4f}) = {cos_t:.6f}")
        print(f"  θ = {theta:.4f}°")
        print(f"")
        if abs(dot) < 1e-10:
            print(f"  v · w = 0 → v and w are PERPENDICULAR ✓")
        elif theta < 90:
            print(f"  θ < 90° → vectors point in roughly the same direction.")
        else:
            print(f"  θ > 90° → vectors point in roughly opposite directions.")

    print(f"\n--- Cross product ---")
    print(f"  v × w gives a NEW vector perpendicular to both v and w.")
    print(f"  Its direction follows the right-hand rule.")
    print(f"  Its magnitude equals the AREA of the parallelogram")
    print(f"  formed by v and w — a beautiful geometric fact.")
    print(f"")
    print(f"  Computed via the determinant:")
    print(f"  v × w = |i   j   k |")
    print(f"          |{vx}  {vy}  {vz}|")
    print(f"          |{wx}  {wy}  {wz}|")
    print(f"")
    cross = np.cross(v, w)
    print(f"  v × w = ({vy*wz-vz*wy:.4f},  {vz*wx-vx*wz:.4f},  {vx*wy-vy*wx:.4f})")
    print(f"        = ({cross[0]:.4f}, {cross[1]:.4f}, {cross[2]:.4f})")
    print(f"")
    area = np.linalg.norm(cross)
    print(f"  |v × w| = {area:.4f}")
    print(f"  → Area of parallelogram = {area:.4f}")
    print(f"  → Area of triangle      = {area/2:.4f}")
    print(f"")
    if mod_v > 1e-10 and mod_w > 1e-10:
        print(f"  Verify perpendicularity:")
        print(f"  (v×w)·v = {np.dot(cross,v):.8f} ≈ 0 ✓")
        print(f"  (v×w)·w = {np.dot(cross,w):.8f} ≈ 0 ✓")

    print(f"\n--- Triple product ---")
    print(f"  v · (w × u) gives the VOLUME of the parallelepiped")
    print(f"  formed by three vectors.")
    print(f"  If it equals zero, the three vectors are coplanar —")
    print(f"  they all lie in the same plane.")
    print(f"  This is the 3D equivalent of collinearity.")
    print(f"")
    ux = float(input("  Third vector u → x: "))
    uy = float(input("                   y: "))
    uz = float(input("                   z: "))
    u  = np.array([ux, uy, uz])

    triple = np.dot(v, np.cross(w, u))
    print(f"  u = ({ux}, {uy}, {uz})")
    print(f"  v · (w × u) = {triple:.6f}")
    print(f"")
    if abs(triple) < 1e-10:
        print(f"  = 0 → v, w, u are COPLANAR.")
        print(f"  All three lie in the same plane.")
        print(f"  One is a linear combination of the other two.")
    else:
        print(f"  ≠ 0 → v, w, u are NOT coplanar.")
        print(f"  Volume of parallelepiped = |{triple:.4f}| = {abs(triple):.4f}")

    plot_vectors(v, w, cross)


def lines_in_space():
    print(f"\n{'='*50}")
    print(f"LINES IN SPACE")
    print(f"{'='*50}")
    print(f"")
    print(f"  A line in 3D needs two ingredients:")
    print(f"  a point it passes through, and a direction.")
    print(f"")
    print(f"  Parametric form:")
    print(f"      x = x₀ + a·t")
    print(f"      y = y₀ + b·t")
    print(f"      z = z₀ + c·t")
    print(f"")
    print(f"  At t=0 you're at (x₀,y₀,z₀).")
    print(f"  (a,b,c) is where you're headed.")
    print(f"  t moves you forward or backward along the line.")
    print(f"")
    print(f"  Cartesian form (when a,b,c all ≠ 0):")
    print(f"  (x-x₀)/a = (y-y₀)/b = (z-z₀)/c = t")
    print(f"")
    print(f"  In 3D, two lines can relate in four ways:")
    print(f"  · Coincident   — exactly the same line")
    print(f"  · Parallel     — same direction, never meet")
    print(f"  · Intersecting — meet at exactly one point")
    print(f"  · Skew         — not parallel, never meet")
    print(f"    This last case is impossible in 2D — unique to 3D.")
    print(f"")

    print(f"  Line 1 — point:")
    x1 = float(input("  x₀: "))
    y1 = float(input("  y₀: "))
    z1 = float(input("  z₀: "))
    print(f"  Line 1 — direction:")
    a1 = float(input("  a: "))
    b1 = float(input("  b: "))
    c1 = float(input("  c: "))

    print(f"  Line 2 — point:")
    x2 = float(input("  x₀: "))
    y2 = float(input("  y₀: "))
    z2 = float(input("  z₀: "))
    print(f"  Line 2 — direction:")
    a2 = float(input("  a: "))
    b2 = float(input("  b: "))
    c2 = float(input("  c: "))

    p1 = np.array([x1, y1, z1])
    d1 = np.array([a1, b1, c1])
    p2 = np.array([x2, y2, z2])
    d2 = np.array([a2, b2, c2])

    print(f"\n  Line 1: ({x1},{y1},{z1}) + t·({a1},{b1},{c1})")
    print(f"  Line 2: ({x2},{y2},{z2}) + s·({a2},{b2},{c2})")

    print(f"\n--- Step 1: Are they parallel? ---")
    print(f"  Two lines are parallel if d1 × d2 = 0.")
    print(f"  The cross product is zero exactly when the")
    print(f"  two vectors are proportional — same direction.")
    print(f"")
    cross_d  = np.cross(d1, d2)
    parallel = np.linalg.norm(cross_d) < 1e-10
    print(f"  d1 × d2 = ({cross_d[0]:.4f}, {cross_d[1]:.4f}, {cross_d[2]:.4f})")
    print(f"  |d1×d2| = {np.linalg.norm(cross_d):.6f}")
    print(f"")

    if parallel:
        print(f"  = 0 → lines are parallel (or coincident).")
        diff  = p2 - p1
        check = np.cross(diff, d1)
        if np.linalg.norm(check) < 1e-10:
            print(f"  p2 lies on line 1 → lines are COINCIDENT.")
        else:
            dist = np.linalg.norm(check) / np.linalg.norm(d1)
            print(f"  p2 does NOT lie on line 1 → lines are PARALLEL.")
            print(f"  Distance between them: {dist:.4f}")
    else:
        print(f"  ≠ 0 → lines are NOT parallel.")
        print(f"  They could be intersecting or skew.")

        print(f"\n--- Step 2: Do they intersect? ---")
        print(f"  If they meet: p1 + t·d1 = p2 + s·d2 for some t,s.")
        print(f"  This system of 3 equations in 2 unknowns has a solution")
        print(f"  only if a compatibility condition holds.")
        print(f"  The condition: (p2-p1) · (d1×d2) = 0")
        print(f"")
        diff   = p2 - p1
        triple = np.dot(diff, cross_d)
        print(f"  (p2-p1) · (d1×d2) = {triple:.6f}")
        print(f"")

        if abs(triple) < 1e-10:
            print(f"  = 0 → lines INTERSECT.")
            A_mat = np.array([[a1, -a2],
                              [b1, -b2],
                              [c1, -c2]])
            b_vec = p2 - p1
            ts    = np.linalg.lstsq(A_mat, b_vec, rcond=None)[0]
            pt    = p1 + ts[0]*d1
            print(f"  Intersection: ({pt[0]:.4f}, {pt[1]:.4f}, {pt[2]:.4f})")
        else:
            dist = abs(triple) / np.linalg.norm(cross_d)
            print(f"  ≠ 0 → lines are SKEW.")
            print(f"  They don't intersect and aren't parallel.")
            print(f"  Only possible in 3D — never in 2D.")
            print(f"")
            print(f"  Distance between the skew lines:")
            print(f"  d = |(p2-p1)·(d1×d2)| / |d1×d2|")
            print(f"    = |{triple:.4f}| / {np.linalg.norm(cross_d):.4f}")
            print(f"    = {dist:.4f}")
            print(f"")
            print(f"  This is the length of the common perpendicular —")
            print(f"  the unique segment that meets both lines at 90°.")

    plot_lines_space(p1, d1, p2, d2)


def planes_in_space():
    print(f"\n{'='*50}")
    print(f"PLANES IN SPACE")
    print(f"{'='*50}")
    print(f"")
    print(f"  A plane in 3D is completely determined by:")
    print(f"  a point it passes through and a normal vector —")
    print(f"  a vector perpendicular to the entire plane.")
    print(f"")
    print(f"  Equation: a(x-x₀) + b(y-y₀) + c(z-z₀) = 0")
    print(f"  Or equivalently: ax + by + cz + d = 0")
    print(f"")
    print(f"  (a,b,c) is the normal vector.")
    print(f"  Every vector lying in the plane is perpendicular to (a,b,c).")
    print(f"  This is why the normal vector controls everything —")
    print(f"  angles between planes, distances, parallelism.")
    print(f"")
    print(f"  What do you want to do?")
    print(f"  1 — Define plane from point and normal")
    print(f"  2 — Define plane through three points")
    print(f"  3 — Angle between two planes")
    print(f"  4 — Distance from point to plane")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        print(f"\n  Point on the plane:")
        x0 = float(input("  x₀: "))
        y0 = float(input("  y₀: "))
        z0 = float(input("  z₀: "))
        print(f"  Normal vector:")
        a = float(input("  a: "))
        b = float(input("  b: "))
        c = float(input("  c: "))

        d = -(a*x0 + b*y0 + c*z0)

        print(f"\n--- The plane ---")
        print(f"  Point: ({x0}, {y0}, {z0})")
        print(f"  Normal: ({a}, {b}, {c})")
        print(f"")
        print(f"  Equation: {a}(x-{x0}) + {b}(y-{y0}) + {c}(z-{z0}) = 0")
        print(f"  Expanded: {a}x + {b}y + {c}z + {d:.4f} = 0")
        print(f"")
        print(f"  Any point (x,y,z) satisfies this if and only if")
        print(f"  the vector from ({x0},{y0},{z0}) to (x,y,z)")
        print(f"  is perpendicular to the normal — i.e. lies in the plane.")

        plot_plane(a, b, c, d)

    elif choice == "2":
        print(f"\n  Three non-collinear points determine a unique plane.")
        print(f"  Strategy:")
        print(f"  1. Build two vectors lying in the plane (AB and AC)")
        print(f"  2. Their cross product is perpendicular to both")
        print(f"     → it's the normal vector")
        print(f"  3. Use any of the three points to write the equation")
        print(f"")
        print(f"  Point A:")
        ax = float(input("  x: "))
        ay = float(input("  y: "))
        az = float(input("  z: "))
        print(f"  Point B:")
        bx = float(input("  x: "))
        by = float(input("  y: "))
        bz = float(input("  z: "))
        print(f"  Point C:")
        cx = float(input("  x: "))
        cy = float(input("  y: "))
        cz = float(input("  z: "))

        A  = np.array([ax, ay, az])
        B  = np.array([bx, by, bz])
        C  = np.array([cx, cy, cz])
        AB = B - A
        AC = C - A

        print(f"\n--- Step 1: Vectors in the plane ---")
        print(f"  AB = B - A = ({AB[0]}, {AB[1]}, {AB[2]})")
        print(f"  AC = C - A = ({AC[0]}, {AC[1]}, {AC[2]})")

        print(f"\n--- Step 2: Normal = AB × AC ---")
        n = np.cross(AB, AC)
        if np.linalg.norm(n) < 1e-10:
            print(f"  AB × AC = 0 → the three points are collinear.")
            print(f"  Three collinear points don't define a unique plane.")
            return
        print(f"  n = AB × AC = ({n[0]:.4f}, {n[1]:.4f}, {n[2]:.4f})")
        print(f"  This vector is perpendicular to AB and AC,")
        print(f"  so it's perpendicular to every vector in the plane.")

        print(f"\n--- Step 3: Plane equation ---")
        d = -(n[0]*ax + n[1]*ay + n[2]*az)
        print(f"  Using point A = ({ax},{ay},{az}):")
        print(f"  {n[0]:.4f}(x-{ax}) + {n[1]:.4f}(y-{ay}) + {n[2]:.4f}(z-{az}) = 0")
        print(f"  {n[0]:.4f}x + {n[1]:.4f}y + {n[2]:.4f}z + {d:.4f} = 0")

        print(f"\n--- Verify: all three points on the plane ---")
        for pt, lbl in [(A,"A"), (B,"B"), (C,"C")]:
            val = n[0]*pt[0] + n[1]*pt[1] + n[2]*pt[2] + d
            print(f"  {lbl}: {val:.8f} ≈ 0 ✓")

        plot_plane(n[0], n[1], n[2], d, points=[A,B,C])

    elif choice == "3":
        print(f"\n  The angle between two planes equals the angle")
        print(f"  between their normal vectors.")
        print(f"  We always take the acute angle (≤ 90°).")
        print(f"  Why? Because two planes form two supplementary angles —")
        print(f"  we report the smaller one by convention.")
        print(f"")
        print(f"  Plane 1 — ax+by+cz+d=0:")
        a1 = float(input("  a: "))
        b1 = float(input("  b: "))
        c1 = float(input("  c: "))
        print(f"  Plane 2 — ax+by+cz+d=0:")
        a2 = float(input("  a: "))
        b2 = float(input("  b: "))
        c2 = float(input("  c: "))

        n1        = np.array([a1, b1, c1])
        n2        = np.array([a2, b2, c2])
        dot       = np.dot(n1, n2)
        cos_theta = min(1, abs(dot) / (np.linalg.norm(n1)*np.linalg.norm(n2)))
        theta     = math.degrees(math.acos(cos_theta))

        print(f"\n--- Angle between the planes ---")
        print(f"  n1 = ({a1}, {b1}, {c1}),  |n1| = {np.linalg.norm(n1):.4f}")
        print(f"  n2 = ({a2}, {b2}, {c2}),  |n2| = {np.linalg.norm(n2):.4f}")
        print(f"  n1·n2 = {dot:.4f}")
        print(f"  cos θ = |n1·n2| / (|n1|·|n2|) = {cos_theta:.6f}")
        print(f"  θ = {theta:.4f}°")
        print(f"")
        if theta < 1e-6:
            print(f"  θ ≈ 0° → planes are PARALLEL.")
            print(f"  Their normals point in the same direction.")
        elif abs(theta - 90) < 1e-4:
            print(f"  θ = 90° → planes are PERPENDICULAR.")
            print(f"  Their normals are perpendicular → planes meet at a right angle.")
        else:
            print(f"  The planes meet at {theta:.4f}°.")
            print(f"  Their intersection is a line.")

    elif choice == "4":
        print(f"\n  Distance from a point to a plane:")
        print(f"")
        print(f"      d = |ax₀ + by₀ + cz₀ + D| / √(a²+b²+c²)")
        print(f"")
        print(f"  Where does this come from?")
        print(f"  The numerator is how much the point 'violates'")
        print(f"  the plane equation. The denominator normalizes by")
        print(f"  the length of the normal — so the result is the")
        print(f"  actual perpendicular distance, not a scaled version.")
        print(f"")
        print(f"  Plane ax+by+cz+D=0:")
        a = float(input("  a: "))
        b = float(input("  b: "))
        c = float(input("  c: "))
        D = float(input("  D: "))
        print(f"  Point P:")
        px = float(input("  x: "))
        py = float(input("  y: "))
        pz = float(input("  z: "))

        num  = abs(a*px + b*py + c*pz + D)
        den  = math.sqrt(a**2 + b**2 + c**2)
        dist = num / den

        print(f"\n--- Distance from ({px},{py},{pz}) to the plane ---")
        print(f"  Numerator:   |{a}·{px} + {b}·{py} + {c}·{pz} + {D}|")
        print(f"             = |{a*px+b*py+c*pz+D:.4f}|")
        print(f"             = {num:.4f}")
        print(f"  Denominator: √({a}²+{b}²+{c}²) = √{a**2+b**2+c**2:.4f} = {den:.4f}")
        print(f"")
        print(f"  d = {num:.4f} / {den:.4f} = {dist:.4f}")
        print(f"")
        if dist < 1e-10:
            print(f"  d = 0 → the point lies ON the plane.")
        else:
            print(f"  The point is {dist:.4f} units from the plane.")

    else:
        print(f"  Invalid choice.")


def intersections_3d():
    print(f"\n{'='*50}")
    print(f"INTERSECTIONS IN 3D")
    print(f"{'='*50}")
    print(f"")
    print(f"  What do you want to compute?")
    print(f"  1 — Line-plane intersection")
    print(f"  2 — Plane-plane intersection  (gives a line)")
    print(f"  3 — Distance from point to line")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        print(f"\n  LINE-PLANE INTERSECTION")
        print(f"")
        print(f"  Strategy: substitute the parametric line into")
        print(f"  the plane equation and solve for t.")
        print(f"  Then plug t back in to get the point.")
        print(f"")
        print(f"  Three cases can arise:")
        print(f"  · One solution  → line crosses the plane at one point")
        print(f"  · No solution   → line is parallel to the plane")
        print(f"  · Infinite solutions → line lies entirely in the plane")
        print(f"")
        print(f"  Line — point:")
        px = float(input("  x: "))
        py = float(input("  y: "))
        pz = float(input("  z: "))
        print(f"  Line — direction:")
        dx = float(input("  a: "))
        dy = float(input("  b: "))
        dz = float(input("  c: "))
        print(f"  Plane ax+by+cz+D=0:")
        a = float(input("  a: "))
        b = float(input("  b: "))
        c = float(input("  c: "))
        D = float(input("  D: "))

        P  = np.array([px, py, pz])
        dv = np.array([dx, dy, dz])
        n  = np.array([a, b, c])
        nd = np.dot(n, dv)

        print(f"\n--- Substituting into the plane equation ---")
        print(f"  x={px}+{dx}t,  y={py}+{dy}t,  z={pz}+{dz}t")
        print(f"  {a}({px}+{dx}t) + {b}({py}+{dy}t) + {c}({pz}+{dz}t) + {D} = 0")
        const = np.dot(n, P) + D
        print(f"  {const:.4f} + {nd:.4f}·t = 0")
        print(f"")

        if abs(nd) < 1e-10:
            if abs(const) < 1e-10:
                print(f"  0 = 0 → line lies INSIDE the plane.")
                print(f"  Infinitely many intersection points.")
            else:
                print(f"  {const:.4f} = 0 → impossible.")
                print(f"  Line is PARALLEL to the plane — no intersection.")
                dist = abs(const) / np.linalg.norm(n)
                print(f"  Distance from line to plane: {dist:.4f}")
        else:
            t  = -const / nd
            pt = P + t*dv
            print(f"  t = -{const:.4f} / {nd:.4f} = {t:.4f}")
            print(f"")
            print(f"  Intersection point:")
            print(f"  x = {px}+{dx}·{t:.4f} = {pt[0]:.4f}")
            print(f"  y = {py}+{dy}·{t:.4f} = {pt[1]:.4f}")
            print(f"  z = {pz}+{dz}·{t:.4f} = {pt[2]:.4f}")
            print(f"  Point: ({pt[0]:.4f}, {pt[1]:.4f}, {pt[2]:.4f})")
            print(f"")
            check = a*pt[0]+b*pt[1]+c*pt[2]+D
            print(f"  Verify on plane: {check:.8f} ≈ 0 ✓")

    elif choice == "2":
        print(f"\n  PLANE-PLANE INTERSECTION")
        print(f"")
        print(f"  Two non-parallel planes always intersect in a line.")
        print(f"  The direction of that line = n1 × n2.")
        print(f"  Why? Because the intersection line lies in both planes,")
        print(f"  so it must be perpendicular to both normals.")
        print(f"  The cross product gives exactly that direction.")
        print(f"")
        print(f"  Plane 1:")
        a1 = float(input("  a₁: "))
        b1 = float(input("  b₁: "))
        c1 = float(input("  c₁: "))
        d1 = float(input("  d₁: "))
        print(f"  Plane 2:")
        a2 = float(input("  a₂: "))
        b2 = float(input("  b₂: "))
        c2 = float(input("  c₂: "))
        d2 = float(input("  d₂: "))

        n1   = np.array([a1, b1, c1])
        n2   = np.array([a2, b2, c2])
        dirn = np.cross(n1, n2)

        print(f"\n--- Direction of intersection line ---")
        print(f"  d = n1 × n2 = ({dirn[0]:.4f}, {dirn[1]:.4f}, {dirn[2]:.4f})")
        print(f"")

        if np.linalg.norm(dirn) < 1e-10:
            print(f"  |d| = 0 → planes are PARALLEL.")
            check = abs(d1/np.linalg.norm(n1) - d2/np.linalg.norm(n2))
            if check < 1e-10:
                print(f"  And coincident — the same plane.")
            else:
                print(f"  Parallel but distinct — they never meet.")
        else:
            print(f"--- A point on the intersection line ---")
            print(f"  Set z=0 and solve the 2×2 system:")
            A_mat = np.array([[a1, b1], [a2, b2]])
            b_vec = np.array([-d1, -d2])
            try:
                xy = np.linalg.solve(A_mat, b_vec)
                pt = np.array([xy[0], xy[1], 0.0])
                print(f"  Point: ({pt[0]:.4f}, {pt[1]:.4f}, 0)")
                print(f"")
                print(f"  Intersection line:")
                print(f"  x = {pt[0]:.4f} + {dirn[0]:.4f}·t")
                print(f"  y = {pt[1]:.4f} + {dirn[1]:.4f}·t")
                print(f"  z = 0 + {dirn[2]:.4f}·t")
            except np.linalg.LinAlgError:
                print(f"  System singular at z=0 — try a different fixed coordinate.")

    elif choice == "3":
        print(f"\n  DISTANCE FROM POINT TO LINE IN 3D")
        print(f"")
        print(f"  Formula: d = |AP × v| / |v|")
        print(f"")
        print(f"  Where this comes from:")
        print(f"  |AP × v| = area of the parallelogram formed by AP and v")
        print(f"  Area = base × height = |v| × distance")
        print(f"  So: distance = |AP × v| / |v|")
        print(f"  The cross product gives us the area — dividing by")
        print(f"  the base gives the perpendicular height, which is")
        print(f"  exactly the distance we want.")
        print(f"")
        print(f"  Point A on the line:")
        ax = float(input("  x: "))
        ay = float(input("  y: "))
        az = float(input("  z: "))
        print(f"  Line direction v:")
        vx = float(input("  x: "))
        vy = float(input("  y: "))
        vz = float(input("  z: "))
        print(f"  External point P:")
        px = float(input("  x: "))
        py = float(input("  y: "))
        pz = float(input("  z: "))

        A     = np.array([ax, ay, az])
        v     = np.array([vx, vy, vz])
        P     = np.array([px, py, pz])
        AP    = P - A
        cross = np.cross(AP, v)
        dist  = np.linalg.norm(cross) / np.linalg.norm(v)

        print(f"\n--- Distance from P to the line ---")
        print(f"  AP = P - A = ({AP[0]}, {AP[1]}, {AP[2]})")
        print(f"  AP × v = ({cross[0]:.4f}, {cross[1]:.4f}, {cross[2]:.4f})")
        print(f"  |AP × v| = {np.linalg.norm(cross):.4f}")
        print(f"  |v|      = {np.linalg.norm(v):.4f}")
        print(f"  d = {np.linalg.norm(cross):.4f} / {np.linalg.norm(v):.4f} = {dist:.4f}")

    else:
        print(f"  Invalid choice.")


def analytic_geometry_3d():
    print(f"\n{'='*50}")
    print(f"ANALYTIC GEOMETRY IN SPACE")
    print(f"{'='*50}")
    print(f"")
    print(f"  In 2D, coordinates let you describe geometry algebraically.")
    print(f"  In 3D, the same idea applies — but the geometry is richer.")
    print(f"  Lines can pass each other without meeting (skew).")
    print(f"  Planes intersect in lines, not points.")
    print(f"  And vectors become the central tool for everything.")
    print(f"")
    print(f"  The normal vector is the key idea.")
    print(f"  A plane is completely determined by its normal and one point.")
    print(f"  Two planes are parallel if their normals are parallel.")
    print(f"  The angle between planes is the angle between normals.")
    print(f"  Distance from a point to a plane comes from projecting")
    print(f"  onto the normal direction.")
    print(f"  Everything connects through the normal vector.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Vectors          dot product, cross product, triple product")
    print(f"  2 — Lines in space   parallel, intersecting, skew")
    print(f"  3 — Planes           equations, angles, distances")
    print(f"  4 — Intersections    line-plane, plane-plane, point-line distance")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        vector_operations()
    elif choice == "2":
        lines_in_space()
    elif choice == "3":
        planes_in_space()
    elif choice == "4":
        intersections_3d()
    else:
        print(f"  Invalid choice. Please enter 1 to 4.")


if __name__ == "__main__":
    analytic_geometry_3d()