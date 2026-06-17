# prerequisites.py — prerequisite graph for all 22 chapters

PREREQUISITES = {
    1:  [],                  # Quadratic Equations — no prerequisites
    2:  [1],                 # Quadratic Inequalities ← Quadratic Equations
    3:  [1],                 # Systems ← Quadratic Equations
    4:  [1, 3],              # Polynomials ← Quadratic Equations, Systems
    5:  [1, 4],              # Function Analysis ← Quadratic Equations, Polynomials
    6:  [5],                 # Sequences ← Function Analysis
    7:  [5, 6],              # Limits ← Function Analysis, Sequences
    8:  [1],                 # Trigonometry ← Quadratic Equations
    9:  [1, 8],              # Analytic Geometry 2D ← Quadratic Equations, Trigonometry
    10: [5, 7],              # Logarithms & Exponentials ← Function Analysis, Limits
    11: [],                  # Combinatorics — no prerequisites
    12: [11],                # Probability ← Combinatorics
    13: [1, 8],              # Complex Numbers ← Quadratic Equations, Trigonometry
    14: [8, 9],              # Euclidean Geometry ← Trigonometry, Analytic Geometry 2D
    15: [4, 11],             # Number Theory ← Polynomials, Combinatorics
    16: [7, 10],             # Financial Math ← Limits, Logarithms & Exponentials
    17: [8, 9],              # Parametric Equations ← Trigonometry, Analytic Geometry 2D
    18: [9, 14],             # Analytic Geometry 3D ← Analytic Geometry 2D, Euclidean Geometry
    19: [5, 11, 15],         # Mathematical Proofs ← Function Analysis, Combinatorics, Number Theory
    20: [15, 19, 12],        # Olympic Mathematics ← Number Theory, Proofs, Probability
    21: [7, 10],             # Derivatives ← Limits, Logarithms & Exponentials
    22: [21],                # Integrals ← Derivatives
}

MODULE_NAMES = {
    1:  "Quadratic Equations",
    2:  "Quadratic Inequalities",
    3:  "Systems of Equations",
    4:  "Polynomials",
    5:  "Function Analysis",
    6:  "Sequences",
    7:  "Limits",
    8:  "Trigonometry",
    9:  "Analytic Geometry 2D",
    10: "Logarithms & Exponentials",
    11: "Combinatorics",
    12: "Probability",
    13: "Complex Numbers",
    14: "Euclidean Geometry",
    15: "Number Theory",
    16: "Financial Math",
    17: "Parametric Equations",
    18: "Analytic Geometry 3D",
    19: "Mathematical Proofs",
    20: "Olympic Mathematics",
    21: "Derivatives",
    22: "Integrals",
}

def get_missing(n, visited):
    """Return list of prerequisite module numbers not yet visited."""
    return [p for p in PREREQUISITES.get(n, []) if p not in visited]

def get_prereq_names(n):
    """Return names of all prerequisites for module n."""
    return [MODULE_NAMES[p] for p in PREREQUISITES.get(n, [])]