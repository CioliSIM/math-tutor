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


# ── TRIANGLES ─────────────────────────────────────────────────────────────────

def solve_triangle(a, b, c):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("The triangle",
        """The simplest polygon — and the most fundamental.<br>
Every other polygon decomposes into triangles.<br><br>
<strong>The one rule that never changes:</strong> interior angles always sum to 180°.<br><br>
Why? Draw a line through one vertex parallel to the opposite side.
The three angles at that vertex are alternate interior angles — they form a straight line.""",
        "warm")

    # triangle inequality
    ok = a+b>c and a+c>b and b+c>a
    if not ok:
        add("Triangle inequality", "These three lengths cannot form a triangle.", "error")
        return {"steps": steps, "valid": False}

    # classify
    if abs(a-b)<1e-9 and abs(b-c)<1e-9:
        side_type = "Equilateral — all sides equal, all angles 60°"
    elif abs(a-b)<1e-9 or abs(b-c)<1e-9 or abs(a-c)<1e-9:
        side_type = "Isosceles — two sides equal, two base angles equal"
    else:
        side_type = "Scalene — all sides different"
    add("Classification by sides", side_type)

    # angles
    cos_A = (b**2+c**2-a**2)/(2*b*c)
    cos_B = (a**2+c**2-b**2)/(2*a*c)
    cos_C = (a**2+b**2-c**2)/(2*a*b)
    A = math.degrees(math.acos(max(-1,min(1,cos_A))))
    B = math.degrees(math.acos(max(-1,min(1,cos_B))))
    C = math.degrees(math.acos(max(-1,min(1,cos_C))))

    add("Angles — law of cosines",
        f"<span class='mf'>c² = a² + b² − 2ab·cos(C) &nbsp;→&nbsp; cos(C) = (a²+b²−c²)/2ab</span><br><br>"
        f"A (opposite a={a:g}) = <strong>{A:.4f}°</strong><br>"
        f"B (opposite b={b:g}) = <strong>{B:.4f}°</strong><br>"
        f"C (opposite c={c:g}) = <strong>{C:.4f}°</strong><br>"
        f"Sum = {A+B+C:.4f}° ✓")

    max_a = max(A,B,C)
    if abs(max_a-90)<1e-5: angle_type = "Right triangle — one angle exactly 90°"
    elif max_a < 90:        angle_type = "Acute triangle — all angles &lt; 90°"
    else:                   angle_type = "Obtuse triangle — one angle &gt; 90°"
    add("Classification by angles", angle_type)

    s1,s2,hyp = sorted([a,b,c])
    diff = s1**2+s2**2-hyp**2
    pyth_body = (f"a²+b² = {s1**2+s2**2:.4f} vs c² = {hyp**2:.4f} → "
                 + ("confirmed right triangle ✓" if abs(diff)<1e-6 else
                    "a²+b² > c² → acute ✓" if diff>0 else "a²+b² < c² → obtuse ✓"))
    add("Pythagorean check", pyth_body)

    s    = (a+b+c)/2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    R    = (a*b*c)/(4*area)
    r_in = area/s

    add("Area — Heron's formula",
        f"s = (a+b+c)/2 = {s:.4f}  (semi-perimeter)<br>"
        f"Area = √(s(s−a)(s−b)(s−c)) = <strong>{area:.4f}</strong><br>"
        f"Perimeter = {a+b+c:.4f}")

    euler_body = (f"Circumradius R = abc/(4·Area) = <strong>{R:.4f}</strong><br>"
                  f"Inradius r = Area/s = <strong>{r_in:.4f}</strong><br><br>"
                  f"Euler's inequality: R ≥ 2r &nbsp;→ &nbsp;{R:.4f} ≥ {2*r_in:.4f} "
                  + ("✓" if R >= 2*r_in-1e-9 else "✗"))
    add("Circumradius and inradius", euler_body, "sage")

    return {"steps": steps, "valid": True,
            "a":a,"b":b,"c":c,"A":A,"B":B,"C":C,"area":area,"R":R,"r_in":r_in}


def plot_triangle(r):
    a,b,c = r["a"],r["b"],r["c"]
    A_rad = math.radians(r["A"])
    x0,y0 = 0,0; x1,y1 = c,0
    x2 = b*math.cos(A_rad); y2 = b*math.sin(A_rad)
    R = r["R"]; r_in = r["r_in"]; area = r["area"]

    fig, ax = plt.subplots(figsize=(7,6))
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5")
    ax.set_aspect("equal")

    tri = plt.Polygon([(x0,y0),(x1,y1),(x2,y2)],
                      facecolor="#e8602a",alpha=0.1,edgecolor="#e8602a",linewidth=2)
    ax.add_patch(tri)
    t = np.linspace(0,2*np.pi,400)
    D = 2*(x0*(y1-y2)+x1*(y2-y0)+x2*(y0-y1))
    if abs(D)>1e-10:
        ux = ((x0**2+y0**2)*(y1-y2)+(x1**2+y1**2)*(y2-y0)+(x2**2+y2**2)*(y0-y1))/D
        uy = ((x0**2+y0**2)*(x2-x1)+(x1**2+y1**2)*(x0-x2)+(x2**2+y2**2)*(x1-x0))/D
        ax.plot(ux+R*np.cos(t),uy+R*np.sin(t),
                color="#c8a96e",linewidth=1,linestyle="--",alpha=0.6,label=f"Circumcircle R={R:.2f}")
    ix=(a*x0+b*x1+c*x2)/(a+b+c); iy=(a*y0+b*y1+c*y2)/(a+b+c)
    ax.plot(ix+r_in*np.cos(t),iy+r_in*np.sin(t),
            color="#3d6b5e",linewidth=1,linestyle="--",alpha=0.6,label=f"Incircle r={r_in:.2f}")
    for (x,y),lbl in [((x0,y0),"A"),((x1,y1),"B"),((x2,y2),"C")]:
        ax.plot(x,y,"o",color="#e8602a",markersize=9,zorder=5)
        ax.annotate(f" {lbl}",(x,y),fontsize=11,fontweight="bold",color="#e8602a")
    ax.text((x0+x1)/2,-0.25,f"c={c:.2f}",ha="center",fontsize=9,color="#4a4540")
    lim = max(x1,x2,y2,R)+1
    ax.set_xlim(-lim,lim); ax.set_ylim(-1,lim)
    ax.grid(True,alpha=0.2,color="#e0d8cc")
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    ax.set_title(f"Area={area:.3f}  Perimeter={a+b+c:.3f}",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── THALES ────────────────────────────────────────────────────────────────────

def solve_thales(mode, **kw):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Thales' theorem — two versions",
        """<strong>Version 1 — Parallel segments:</strong><br>
If DE ∥ BC in triangle ABC, then AD/DB = AE/EC.<br>
The parallel line cuts both sides in the same ratio.<br><br>
<strong>Version 2 — Angle in semicircle:</strong><br>
If AB is a diameter and C is any point on the circle, then ∠ACB = 90°. Always.<br>
Proof: central angle = 180° → inscribed angle = 90° (half the central angle).""",
        "warm")

    if mode == "parallel":
        AD,DB,AE = kw["AD"],kw["DB"],kw["AE"]
        ratio = AD/DB; EC = AE/ratio; k = AD/(AD+DB)
        add("Proportional segments",
            f"AD/DB = {AD:g}/{DB:g} = <strong>{ratio:.4f}</strong><br><br>"
            f"By Thales: AE/EC = same ratio<br>"
            f"EC = AE/ratio = {AE:g}/{ratio:.4f} = <strong>{EC:.4f}</strong><br><br>"
            f"Similarity ratio k = AD/AB = {k:.4f}<br>"
            f"Triangle ADE ∼ Triangle ABC with ratio {k:.4f}<br>"
            f"Areas scale by k² = {k**2:.4f}",
            "sage")
        return {"steps":steps,"mode":"parallel",
                "AD":AD,"DB":DB,"AE":AE,"EC":EC,"k":k}

    else:  # semicircle
        r = kw["r"]; angle_deg = kw["angle"]
        if not 0<angle_deg<180:
            add("Error","Angle must be strictly between 0° and 180°.","error")
            return {"steps":steps}
        angle_rad = math.radians(angle_deg)
        Cx=r*math.cos(angle_rad); Cy=r*math.sin(angle_rad)
        Ax,Ay=-r,0; Bx,By=r,0
        vCA=(Ax-Cx,Ay-Cy); vCB=(Bx-Cx,By-Cy)
        dot=vCA[0]*vCB[0]+vCA[1]*vCB[1]
        mag=math.sqrt(vCA[0]**2+vCA[1]**2)*math.sqrt(vCB[0]**2+vCB[1]**2)
        acb=math.degrees(math.acos(dot/mag))
        add("Angle in semicircle",
            f"C is at {angle_deg}° on the circle.<br>"
            f"∠ACB = <strong>{acb:.4f}°</strong> ✓<br><br>"
            f"Try any angle 1°–179° — it is always exactly 90°.<br>"
            "This is because the diameter subtends a 180° central angle,<br>"
            "and the inscribed angle is always half the central angle.",
            "sage")
        return {"steps":steps,"mode":"circle",
                "r":r,"Cx":Cx,"Cy":Cy,"Ax":Ax,"Ay":Ay,"Bx":Bx,"By":By}


def plot_thales_circle(d):
    r=d["r"]; Cx,Cy=d["Cx"],d["Cy"]; Ax,Ay=d["Ax"],d["Ay"]; Bx,By=d["Bx"],d["By"]
    fig, ax = plt.subplots(figsize=(6,6))
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5"); ax.set_aspect("equal")
    t=np.linspace(0,2*np.pi,400)
    ax.plot(r*np.cos(t),r*np.sin(t),color="#3d6b5e",linewidth=2)
    ax.plot([Ax,Bx],[Ay,By],color="#1a1814",linewidth=2)
    tri=plt.Polygon([(Ax,Ay),(Cx,Cy),(Bx,By)],facecolor="#e8602a",alpha=0.1,
                    edgecolor="#e8602a",linewidth=1.5)
    ax.add_patch(tri)
    size=r*0.09
    vCA=np.array([Ax-Cx,Ay-Cy]); vCB=np.array([Bx-Cx,By-Cy])
    vCA=vCA/np.linalg.norm(vCA)*size; vCB=vCB/np.linalg.norm(vCB)*size
    sq=np.array([[Cx,Cy],[Cx+vCA[0],Cy+vCA[1]],
                 [Cx+vCA[0]+vCB[0],Cy+vCA[1]+vCB[1]],[Cx+vCB[0],Cy+vCB[1]]])
    ax.plot(np.append(sq[:,0],sq[0,0]),np.append(sq[:,1],sq[0,1]),
            color="#e8602a",linewidth=2)
    for (x,y),lbl in [((Ax,Ay),"A"),((Bx,By),"B"),((Cx,Cy),"C")]:
        ax.plot(x,y,"o",color="#e8602a",markersize=9,zorder=5)
        ax.annotate(f" {lbl}",(x,y),fontsize=11,fontweight="bold",color="#e8602a")
    ax.set_xlim(-r-0.6,r+0.6); ax.set_ylim(-r-0.6,r+0.6)
    ax.grid(True,alpha=0.2,color="#e0d8cc")
    ax.set_title("∠ACB = 90° always — Thales",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── CIRCLES ───────────────────────────────────────────────────────────────────

def solve_circle(r, central, PA, PB, PC):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    add("Circle geometry",
        """<strong>Inscribed Angle Theorem:</strong> the central angle is exactly twice the inscribed angle
when both subtend the same arc.<br><br>
Consequences:<br>
· All inscribed angles on the same arc are equal<br>
· Angle in semicircle = 90° (Thales)<br>
· Opposite angles of a cyclic quadrilateral sum to 180°""",
        "warm")

    inscribed = central/2
    add("Central and inscribed angle",
        f"Central angle: <strong>{central:.2f}°</strong><br>"
        f"Inscribed angle: {central:.2f}°/2 = <strong>{inscribed:.2f}°</strong><br>"
        + ("→ This is a diameter → inscribed angle = 90° (Thales) ✓"
           if abs(central-180)<1e-6 else
           f"Any inscribed angle on the same arc = {inscribed:.2f}°"))

    add("Basic measurements",
        f"Radius: {r:g} &nbsp;·&nbsp; Diameter: {2*r:g}<br>"
        f"Circumference: 2πr = {2*math.pi*r:.4f}<br>"
        f"Area: πr² = {math.pi*r**2:.4f}")

    PD = PA*PB/PC
    add("Intersecting chords theorem",
        f"PA·PB = PC·PD — always, for any two chords through P.<br><br>"
        f"PA·PB = {PA:g}·{PB:g} = {PA*PB:.4f}<br>"
        f"PD = PA·PB/PC = {PA*PB:.4f}/{PC:g} = <strong>{PD:.4f}</strong><br>"
        f"PC·PD = {PC:g}·{PD:.4f} = {PC*PD:.4f} ✓",
        "sage")

    return {"steps":steps,"r":r,"central":central}


def plot_circle_fig(r, central_deg):
    fig, ax = plt.subplots(figsize=(6,6))
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5"); ax.set_aspect("equal")
    t=np.linspace(0,2*np.pi,400)
    ax.plot(r*np.cos(t),r*np.sin(t),color="#3d6b5e",linewidth=2,alpha=0.7)
    ax.plot(0,0,"o",color="#1a1814",markersize=5)
    half=math.radians(central_deg/2)
    A=(r*math.cos(-half),r*math.sin(-half)); B=(r*math.cos(half),r*math.sin(half))
    ax.plot([0,A[0]],[0,A[1]],color="#e8602a",linewidth=2)
    ax.plot([0,B[0]],[0,B[1]],color="#e8602a",linewidth=2,label=f"Central={central_deg:.1f}°")
    C_ang=math.radians(central_deg/2+130)
    C=(r*math.cos(C_ang),r*math.sin(C_ang))
    ax.plot([C[0],A[0]],[C[1],A[1]],color="#3d6b5e",linewidth=2)
    ax.plot([C[0],B[0]],[C[1],B[1]],color="#3d6b5e",linewidth=2,label=f"Inscribed={central_deg/2:.1f}°")
    for pt,lbl in [(A,"A"),(B,"B"),(C,"C")]:
        ax.plot(pt[0],pt[1],"o",color="#e8602a",markersize=9,zorder=5)
        ax.annotate(f" {lbl}",pt,fontsize=10,fontweight="bold",color="#e8602a")
    ax.set_xlim(-r-0.6,r+0.6); ax.set_ylim(-r-0.6,r+0.6)
    ax.grid(True,alpha=0.2,color="#e0d8cc")
    ax.legend(fontsize=8.5,framealpha=0.7,facecolor="#fdfaf5",edgecolor="#e0d8cc")
    ax.set_title("Inscribed angle = Central angle / 2",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── POLYGONS ──────────────────────────────────────────────────────────────────

def solve_polygon(n, s):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    names={3:"Triangle",4:"Quadrilateral",5:"Pentagon",6:"Hexagon",
           7:"Heptagon",8:"Octagon",9:"Nonagon",10:"Decagon",12:"Dodecagon"}
    name=names.get(n,f"{n}-gon")
    angle_sum=(n-2)*180; each_int=angle_sum/n; each_ext=360/n
    diags=n*(n-3)//2

    add(f"The {name}",
        f"""Every polygon decomposes into triangles — an n-gon into (n−2) triangles.<br>
Each contributes 180°, so the interior angle sum is always <strong>(n−2)·180°</strong>.<br><br>
For a regular {name}:<br>
Interior angle sum: ({n}−2)·180° = <strong>{angle_sum}°</strong><br>
Each interior angle: <strong>{each_int:.4f}°</strong><br>
Each exterior angle: <strong>{each_ext:.4f}°</strong> &nbsp;(sum = 360° always)<br>
Number of diagonals: n(n−3)/2 = <strong>{diags}</strong>""",
        "warm")

    if s > 0:
        area=n*s**2/(4*math.tan(math.pi/n)); perim=n*s
        R_circ=s/(2*math.sin(math.pi/n))
        add("Area and perimeter",
            f"Area = (n·s²)/(4·tan(π/n)) = <strong>{area:.4f}</strong><br>"
            f"Perimeter = n·s = <strong>{perim:.4f}</strong><br>"
            f"Circumradius R = s/(2·sin(π/n)) = <strong>{R_circ:.4f}</strong><br><br>"
            f"As n → ∞, the regular polygon approaches a circle — one way to understand π.",
            "sage")
        return {"steps":steps,"n":n,"s":s,"valid":True}

    return {"steps":steps,"n":n,"s":s,"valid":s>0}


def plot_polygon_fig(n, s):
    R=s/(2*math.sin(math.pi/n))
    angles=[2*math.pi*k/n-math.pi/2 for k in range(n)]
    xs=[R*math.cos(a) for a in angles]; ys=[R*math.sin(a) for a in angles]
    fig,ax=plt.subplots(figsize=(6,6))
    fig.patch.set_facecolor("#fdfaf5"); ax.set_facecolor("#fdfaf5"); ax.set_aspect("equal")
    ax.fill(xs,ys,alpha=0.15,color="#e8602a")
    ax.plot(xs+[xs[0]],ys+[ys[0]],color="#e8602a",linewidth=2)
    for i in range(n):
        ax.plot(xs[i],ys[i],"o",color="#e8602a",markersize=7,zorder=5)
    for i in range(n):
        for j in range(i+2,n):
            if not(i==0 and j==n-1):
                ax.plot([xs[i],xs[j]],[ys[i],ys[j]],color="#b0a090",
                        linewidth=0.5,linestyle="--",alpha=0.3)
    t=np.linspace(0,2*np.pi,400)
    ax.plot(R*np.cos(t),R*np.sin(t),color="#c8a96e",linewidth=1,
            linestyle=":",alpha=0.6)
    lim=R+0.5; ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.grid(True,alpha=0.2,color="#e0d8cc")
    ax.set_title(f"Regular {n}-gon  (s={s:.2f})",fontsize=10,color="#4a4540")
    plt.tight_layout(); return fig


# ── OLYMPIAD ──────────────────────────────────────────────────────────────────

def solve_olympiad(mode, **kw):
    steps = []
    def add(l, bo, v=""): steps.append((l, bo, v))

    if mode == "ceva":
        add("Ceva's theorem",
            """A cevian is a segment from a vertex to the opposite side.<br>
Medians, altitudes, angle bisectors — all cevians.<br><br>
Three cevians AD, BE, CF are <strong>concurrent</strong> iff:<br><br>
<span class="mf">(AF/FB) · (BD/DC) · (CE/EA) = 1</span><br><br>
This single condition replaces pages of coordinate geometry.""",
            "warm")
        AF,FB,BD,DC,CE,EA = kw["AF"],kw["FB"],kw["BD"],kw["DC"],kw["CE"],kw["EA"]
        prod = (AF/FB)*(BD/DC)*(CE/EA)
        concurrent = abs(prod-1)<1e-6
        add("Result",
            f"(AF/FB)·(BD/DC)·(CE/EA) = {AF/FB:.4f}·{BD/DC:.4f}·{CE/EA:.4f} = <strong>{prod:.6f}</strong><br><br>"
            + ("= 1 ✓ — the three cevians ARE concurrent." if concurrent else
               f"≠ 1 — NOT concurrent. Distance from 1: {abs(prod-1):.6f}"),
            "sage" if concurrent else "error")

    elif mode == "menelaus":
        add("Menelaus' theorem",
            """Three points D, E, F on the sides (or extensions) of a triangle are <strong>collinear</strong> iff:<br><br>
<span class="mf">|AF/FB| · |BD/DC| · |CE/EA| = 1</span>  (with an odd number of points on extensions)<br><br>
Contrast with Ceva: same equation, but Menelaus proves collinearity, not concurrence.""",
            "warm")
        AF,FB,BD,DC,CE,EA = kw["AF"],kw["FB"],kw["BD"],kw["DC"],kw["CE"],kw["EA"]
        prod = (AF/FB)*(BD/DC)*(CE/EA)
        collinear = abs(prod-1)<1e-6
        add("Result",
            f"Product = {prod:.6f}<br><br>"
            + ("= 1 ✓ — D, E, F ARE collinear." if collinear else
               f"≠ 1 — NOT collinear. Distance from 1: {abs(prod-1):.6f}"),
            "sage" if collinear else "error")

    else:  # triangle inequality
        add("Triangle inequality",
            """For any triangle: <span class="mf">|a−b| &lt; c &lt; a+b</span><br><br>
The straight-line path is always shorter than any detour.<br>
In olympiads it appears for existence, bounding, and metric space arguments.""",
            "warm")
        a,b,c = kw["a"],kw["b"],kw["c"]
        t1,t2,t3 = a+b>c, a+c>b, b+c>a
        margins = [a+b-c, a+c-b, b+c-a]
        valid = t1 and t2 and t3
        if valid:
            s=( a+b+c)/2; area=math.sqrt(s*(s-a)*(s-b)*(s-c))
            add("Result",
                f"a+b>c: {a+b:.4f}>{c:g} {'✓' if t1 else '✗'}<br>"
                f"a+c>b: {a+c:.4f}>{b:g} {'✓' if t2 else '✗'}<br>"
                f"b+c>a: {b+c:.4f}>{a:g} {'✓' if t3 else '✗'}<br><br>"
                f"Valid triangle ✓  Area = {area:.4f}<br>"
                f"Margins: {margins[0]:.3f}, {margins[1]:.3f}, {margins[2]:.3f}"
                + ("<br>Very close to degenerate — nearly collinear." if min(margins)<0.05*max(a,b,c) else ""),
                "sage")
        else:
            add("Result","Not a valid triangle — triangle inequality violated.","error")

    return {"steps":steps}


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>', unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Triangles","Thales","Circles","Polygons","Olympiad theorems"],
            key="eg_topic")

        if topic == "Triangles":
            c1,c2,c3 = st.columns(3)
            a=c1.number_input("a",value=3.0,step=0.5,key="eg_ta")
            b=c2.number_input("b",value=4.0,step=0.5,key="eg_tb")
            cv=c3.number_input("c",value=5.0,step=0.5,key="eg_tc")

        elif topic == "Thales":
            th_mode = st.selectbox("Version",["Parallel segments","Semicircle angle"],key="eg_tm")
            if th_mode == "Parallel segments":
                AD=st.number_input("AD",value=2.0,step=0.5,key="eg_AD")
                DB=st.number_input("DB",value=3.0,step=0.5,key="eg_DB")
                AE=st.number_input("AE",value=2.0,step=0.5,key="eg_AE")
            else:
                r_th=st.number_input("Radius",value=3.0,step=0.5,key="eg_tr")
                ang_th=st.number_input("Position of C (degrees, 1–179)",value=60.0,step=10.0,key="eg_tang")

        elif topic == "Circles":
            r_c=st.number_input("Radius",value=3.0,step=0.5,key="eg_cr")
            cent=st.number_input("Central angle (degrees)",value=80.0,step=10.0,key="eg_cent")
            PA=st.number_input("PA",value=4.0,step=0.5,key="eg_PA")
            PB=st.number_input("PB",value=3.0,step=0.5,key="eg_PB")
            PC=st.number_input("PC",value=6.0,step=0.5,key="eg_PC")

        elif topic == "Polygons":
            n_p=st.number_input("Sides n",value=6,min_value=3,step=1,key="eg_np")
            s_p=st.number_input("Side length s",value=2.0,step=0.5,key="eg_sp")

        else:  # Olympiad
            ol_mode=st.selectbox("Theorem",["Ceva","Menelaus","Triangle inequality"],key="eg_ol")
            if ol_mode in ["Ceva","Menelaus"]:
                c1,c2=st.columns(2)
                AF=c1.number_input("AF",value=2.0,step=0.5,key="eg_AF")
                FB=c2.number_input("FB",value=3.0,step=0.5,key="eg_FB")
                BD=c1.number_input("BD",value=4.0,step=0.5,key="eg_BD")
                DC=c2.number_input("DC",value=2.0,step=0.5,key="eg_DC")
                CE=c1.number_input("CE",value=3.0,step=0.5,key="eg_CE")
                EA=c2.number_input("EA",value=4.0,step=0.5,key="eg_EA")
            else:
                c1,c2,c3=st.columns(3)
                ol_a=c1.number_input("a",value=3.0,step=0.5,key="eg_ola")
                ol_b=c2.number_input("b",value=4.0,step=0.5,key="eg_olb")
                ol_c=c3.number_input("c",value=5.0,step=0.5,key="eg_olc")

        solve_btn=st.button("Analyze →",key="eg_solve")
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Triangle: <code>3, 4, 5</code> → right triangle<br>
    Thales circle: <code>r=3</code>, any angle → 90°<br>
    Polygon: <code>n=6, s=2</code> → hexagon<br>
    Ceva: <code>2,3,4,2,3,4</code> → check if concurrent
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Triangles":
                r=solve_triangle(a,b,cv)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if r.get("valid"):
                    style.result_band(
                        ("Area", f"{r['area']:.4f}"),
                        ("R",    f"{r['R']:.4f}"),
                        ("r",    f"{r['r_in']:.4f}"),
                    )
                    st.markdown('<div class="graph-label">Triangle</div>',unsafe_allow_html=True)
                    fig=plot_triangle(r); st.pyplot(fig); plt.close(fig)

            elif topic == "Thales":
                if th_mode=="Parallel segments":
                    r=solve_thales("parallel",AD=AD,DB=DB,AE=AE)
                else:
                    r=solve_thales("circle",r=r_th,angle=ang_th)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if r.get("mode")=="circle":
                    st.markdown('<div class="graph-label">Thales on circle</div>',unsafe_allow_html=True)
                    fig=plot_thales_circle(r); st.pyplot(fig); plt.close(fig)

            elif topic == "Circles":
                r=solve_circle(r_c,cent,PA,PB,PC)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                st.markdown('<div class="graph-label">Circle</div>',unsafe_allow_html=True)
                fig=plot_circle_fig(r_c,cent); st.pyplot(fig); plt.close(fig)

            elif topic == "Polygons":
                r=solve_polygon(int(n_p),s_p)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
                if s_p>0:
                    st.markdown('<div class="graph-label">Regular polygon</div>',unsafe_allow_html=True)
                    fig=plot_polygon_fig(int(n_p),s_p); st.pyplot(fig); plt.close(fig)

            else:
                if ol_mode=="Ceva":
                    r=solve_olympiad("ceva",AF=AF,FB=FB,BD=BD,DC=DC,CE=CE,EA=EA)
                elif ol_mode=="Menelaus":
                    r=solve_olympiad("menelaus",AF=AF,FB=FB,BD=BD,DC=DC,CE=CE,EA=EA)
                else:
                    r=solve_olympiad("tri_ineq",a=ol_a,b=ol_b,c=ol_c)
                for lbl,body,var in r["steps"]: style.step(lbl,body,var)
        else:
            style.empty_state("△")