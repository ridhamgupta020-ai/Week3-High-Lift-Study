
import csv
import math
import matplotlib.pyplot as plt

# ==========================================
# WEEK 3: HIGH-LIFT STUDY AND VALIDATION
# Fixed-Wing UAV
# ==========================================

# 1. DESIGN INPUTS (From Week 2)
MASS = 12.0
GRAVITY = 9.81
WING_AREA = 1.20
WING_SPAN = 3.00
ROOT_CHORD = 0.50
TIP_CHORD = 0.30
MAC = 0.4083

CRUISE_SPEED = 20.0
LOW_SPEED = 12.0

AIR_DENSITY = 1.225
DYNAMIC_VISCOSITY = 1.789e-5

# Illustrative reference value only.
# Replace with a value from a verified airfoil polar
# at the matching Reynolds number and configuration.
REFERENCE_CL_MAX = 1.20

# ==========================================
# 2. ENGINEERING CALCULATIONS
# ==========================================

def calculate_weight():
    return MASS * GRAVITY


def calculate_dynamic_pressure(speed):
    return 0.5 * AIR_DENSITY * speed ** 2


def calculate_required_cl(speed):
    weight = calculate_weight()
    q = calculate_dynamic_pressure(speed)

    return weight / (q * WING_AREA)


def calculate_reynolds(speed, chord):
    return (
        AIR_DENSITY * speed * chord
        / DYNAMIC_VISCOSITY
    )


def calculate_stall_speed(cl_max):
    if cl_max <= 0:
        raise ValueError("CLmax must be positive.")

    weight = calculate_weight()

    return math.sqrt(
        (2 * weight) /
        (AIR_DENSITY * WING_AREA * cl_max)
    )


def calculate_lift(speed, cl):
    q = calculate_dynamic_pressure(speed)

    return q * WING_AREA * cl


# ==========================================
# 3. VALIDATION
# ==========================================

def validate_design():
    weight = calculate_weight()

    cruise_q = calculate_dynamic_pressure(CRUISE_SPEED)
    low_q = calculate_dynamic_pressure(LOW_SPEED)

    cruise_cl = calculate_required_cl(CRUISE_SPEED)
    low_cl = calculate_required_cl(LOW_SPEED)

    cruise_re = calculate_reynolds(CRUISE_SPEED, MAC)
    low_re = calculate_reynolds(LOW_SPEED, MAC)

    estimated_stall = calculate_stall_speed(
        REFERENCE_CL_MAX
    )

    lift_margin = (
        (REFERENCE_CL_MAX - low_cl)
        / REFERENCE_CL_MAX
    ) * 100

    print("\nWEEK 3 HIGH-LIFT STUDY")
    print("=" * 45)

    print(f"Aircraft Weight: {weight:.2f} N")

    print("\nCRUISE CONDITION")
    print(f"Speed: {CRUISE_SPEED:.2f} m/s")
    print(f"Dynamic Pressure: {cruise_q:.2f} Pa")
    print(f"Required CL: {cruise_cl:.3f}")
    print(f"Reynolds Number: {cruise_re:.0f}")

    print("\nLOW-SPEED CONDITION")
    print(f"Speed: {LOW_SPEED:.2f} m/s")
    print(f"Dynamic Pressure: {low_q:.2f} Pa")
    print(f"Required CL: {low_cl:.3f}")
    print(f"Reynolds Number: {low_re:.0f}")

    print("\nHIGH-LIFT VALIDATION")
    print(f"Illustrative CLmax: {REFERENCE_CL_MAX:.2f}")
    print(f"Estimated Stall Speed: {estimated_stall:.2f} m/s")
    print(f"CL Margin: {lift_margin:.2f}%")

    if low_cl < REFERENCE_CL_MAX:
        print("Result: Required CL is below the illustrative reference CLmax.")
    else:
        print("Result: Required CL exceeds the illustrative reference CLmax.")

    print("\nIMPORTANT:")
    print("The CLmax value is an assumed reference for")
    print("sensitivity analysis, not a measured UAV result.")
    print("Validate it using matching NACA 2412 airfoil")
    print("data before making a flight-performance claim.")

    return {
        "weight": weight,
        "cruise_q": cruise_q,
        "low_q": low_q,
        "cruise_cl": cruise_cl,
        "low_cl": low_cl,
        "cruise_re": cruise_re,
        "low_re": low_re,
        "stall_speed": estimated_stall,
        "lift_margin": lift_margin
    }


# ==========================================
# 4. HIGH-LIFT COMPARISON GRAPH
# ==========================================

def create_cl_graph(results):
    labels = ["Cruise", "Low Speed", "Illustrative CLmax"]

    values = [
        results["cruise_cl"],
        results["low_cl"],
        REFERENCE_CL_MAX
    ]

    plt.figure(figsize=(9, 5))

    plt.bar(labels, values)

    plt.title("High-Lift Study - Lift Coefficient Comparison")
    plt.ylabel("Lift Coefficient (CL)")
    plt.xlabel("Operating Condition")

    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("week3_lift_coefficient_comparison.png", dpi=300)
    plt.close()


# ==========================================
# 5. STALL SPEED SENSITIVITY GRAPH
# ==========================================

def create_stall_graph():
    cl_values = [0.9, 1.0, 1.1, 1.2, 1.3, 1.4]

    stall_speeds = [
        calculate_stall_speed(cl)
        for cl in cl_values
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        cl_values,
        stall_speeds,
        marker="o"
    )

    plt.title("Estimated Stall Speed vs CLmax")
    plt.xlabel("Assumed Maximum Lift Coefficient")
    plt.ylabel("Estimated Stall Speed (m/s)")

    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("week3_stall_speed_analysis.png", dpi=300)
    plt.close()


# ==========================================
# 6. EXPORT CSV RESULTS
# ==========================================

def export_results(results):
    rows = [
        ["Parameter", "Value", "Unit"],
        ["Aircraft Weight", results["weight"], "N"],
        ["Cruise Dynamic Pressure", results["cruise_q"], "Pa"],
        ["Low Speed Dynamic Pressure", results["low_q"], "Pa"],
        ["Cruise Required CL", results["cruise_cl"], "-"],
        ["Low Speed Required CL", results["low_cl"], "-"],
        ["Cruise Reynolds Number", results["cruise_re"], "-"],
        ["Low Speed Reynolds Number", results["low_re"], "-"],
        ["Illustrative Reference CLmax", REFERENCE_CL_MAX, "-"],
        ["Estimated Stall Speed", results["stall_speed"], "m/s"],
        ["Illustrative Lift Margin", results["lift_margin"], "%"]
    ]

    with open(
        "week3_validation_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)
        writer.writerows(rows)


# ==========================================
# 7. ERROR AND UNCERTAINTY REPORT
# ==========================================

def export_uncertainties():
    rows = [
        ["Source", "Possible Effect", "Validation Needed"],
        [
            "Air density",
            "Changes dynamic pressure and lift",
            "Use actual operating altitude and temperature"
        ],
        [
            "Aerofoil surface roughness",
            "May change maximum lift and drag",
            "Surface inspection or wind tunnel testing"
        ],
        [
            "Reynolds number",
            "Changes boundary layer behaviour",
            "Use matching Reynolds number airfoil data"
        ],
        [
            "Three-dimensional wing effects",
            "Finite-wing lift differs from 2D airfoil data",
            "Finite-wing analysis or CFD"
        ],
        [
            "Flap installation",
            "Changes lift, drag and pitching moment",
            "Test flap geometry and deflection"
        ]
    ]

    with open(
        "week3_uncertainty_analysis.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)
        writer.writerows(rows)


# ==========================================
# 8. MAIN PROGRAM
# ==========================================

def main():
    results = validate_design()

    create_cl_graph(results)
    create_stall_graph()

    export_results(results)
    export_uncertainties()

    print("\nFILES GENERATED SUCCESSFULLY:")
    print("1. week3_validation_results.csv")
    print("2. week3_uncertainty_analysis.csv")
    print("3. week3_lift_coefficient_comparison.png")
    print("4. week3_stall_speed_analysis.png")


if __name__ == "__main__":
    main()
