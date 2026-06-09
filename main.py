def main():
    while True:
        print(f"\n{'='*50}")
        print(f"MATH TUTOR")
        print(f"{'='*50}")
        print(f"")
        print(f"  Welcome to the Math Tutor.")
        print(f"  Every concept explained step by step.")
        print(f"  Not just the answer — the reasoning behind it.")
        print(f"")
        print(f"  1  — Quadratic Equations       discriminant, formula, graph")
        print(f"  2  — Quadratic Inequalities     sign analysis, parabola")
        print(f"  3  — Systems of Equations       substitution, elimination")
        print(f"  4  — Polynomials                Ruffini, factorization")
        print(f"  5  — Function Analysis          domain, parity, monotonicity")
        print(f"  6  — Sequences                  arithmetic, geometric, limits")
        print(f"  7  — Limits                     at a point, infinity, continuity")
        print(f"  8  — Trigonometry               unit circle, identities, equations")
        print(f"  9  — Analytic Geometry 2D       lines, circles, parabolas")
        print(f"  10 — Logarithms & Exponentials  properties, equations, models")
        print(f"  11 — Combinatorics              factorials, combinations, Pascal")
        print(f"  12 — Probability                classical, conditional, Bayes")
        print(f"  13 — Complex Numbers            operations, polar, De Moivre")
        print(f"  14 — Euclidean Geometry         triangles, circles, polygons")
        print(f"  15 — Number Theory              GCD, primes, Fermat, Goldbach")
        print(f"  16 — Financial Math             interest, mortgages, inflation")
        print(f"  17 — Parametric Equations       lines, circles, cycloids")
        print(f"  18 — Analytic Geometry 3D       vectors, lines, planes")
        print(f"  19 — Mathematical Proofs        logic, structure, techniques")
        print(f"  20 — Olympic Mathematics        method, techniques, problems")
        print(f"")
        print(f"  0  — Exit")
        print(f"")
        choice = input("  Enter a number: ").strip()

        if choice == "0":
            print(f"")
            print(f"  See you next time.")
            print(f"")
            break
        elif choice == "1":
            import step1
            step1.quadratic_equations()
        elif choice == "2":
            import step2
            step2.quadratic_inequalities()
        elif choice == "3":
            import step3
            step3.systems_of_equations()
        elif choice == "4":
            import step4
            step4.polynomials()
        elif choice == "5":
            import step5
            step5.function_analysis()
        elif choice == "6":
            import step6
            step6.sequences()
        elif choice == "7":
            import step7
            step7.limits()
        elif choice == "8":
            import step8
            step8.trigonometry()
        elif choice == "9":
            import step9
            step9.analytic_geometry()
        elif choice == "10":
            import step10
            step10.logarithms_and_exponentials()
        elif choice == "11":
            import step11
            step11.combinatorics()
        elif choice == "12":
            import step12
            step12.probability()
        elif choice == "13":
            import step13
            step13.complex_numbers()
        elif choice == "14":
            import step14
            step14.euclidean_geometry()
        elif choice == "15":
            import step15
            step15.number_theory()
        elif choice == "16":
            import step16
            step16.financial_math()
        elif choice == "17":
            import step17
            step17.parametric_equations()
        elif choice == "18":
            import step18
            step18.analytic_geometry_3d()
        elif choice == "19":
            import step19
            step19.mathematical_proofs()
        elif choice == "20":
            import step20
            step20.olympic_math()
        else:
            print(f"  Invalid choice. Please enter a number from 0 to 20.")


if __name__ == "__main__":
    main()