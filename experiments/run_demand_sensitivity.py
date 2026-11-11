
import numpy as np
import matplotlib.pyplot as plt

from seatlab.scenario import Scenario, FareClass
from run_comparison import run_comparison


if __name__ == "__main__":

    # Demand scenarios
    demand_multipliers = [
        1.42, 1.43, 1.44, 1.45,
        1.46, 1.47, 1.48, 1.49, 1.50
    ]

    sensitivity_results = []

    # Run Monte Carlo simulations
    for multiplier in demand_multipliers:

        scenario = Scenario(
            route="JFK-LAX",
            capacity=180,
            booking_horizon_days=30,
            fare_classes=[
                FareClass("Low", 150, 120 * multiplier),
                FareClass("High", 400, 50 * multiplier)
            ]
        )

        results = run_comparison(
            scenario,
            n_simulations=1000,
            base_seed=42
        )

        sensitivity_results.append({
            "multiplier": multiplier,
            "total_demand": 170 * multiplier,
            "fcfs_mean": results["fcfs_mean"],
            "nested_mean": results["nested_mean"],
            "difference": results["average_difference"],
            "confidence_interval": results["confidence_interval"]
        })

    # Display results
    print("\nDEMAND SENSITIVITY RESULTS")
    print("-" * 125)

    print(
        f"{'Multiplier':<12}"
        f"{'Total Demand':<15}"
        f"{'FCFS Revenue':<17}"
        f"{'Nested Revenue':<18}"
        f"{'Difference':<15}"
        f"{'95% Confidence Interval':<30}"
    )

    print("-" * 125)

    for result in sensitivity_results:

        lower, upper = result["confidence_interval"]

        print(
            f"{result['multiplier']:<12.2f}"
            f"{result['total_demand']:<15.1f}"
            f"{result['fcfs_mean']:<17.2f}"
            f"{result['nested_mean']:<18.2f}"
            f"{result['difference']:<15.2f}"
            f"[{lower:.2f}, {upper:.2f}]"
        )

    # Prepare graph data
    multipliers = [
        result["multiplier"]
        for result in sensitivity_results
    ]

    differences = [
        result["difference"]
        for result in sensitivity_results
    ]

    lower_errors = [
        result["difference"] - result["confidence_interval"][0]
        for result in sensitivity_results
    ]

    upper_errors = [
        result["confidence_interval"][1] - result["difference"]
        for result in sensitivity_results
    ]

    # Plot revenue differences with 95% confidence intervals
    plt.figure(figsize=(11, 6))

    plt.errorbar(
        multipliers,
        differences,
        yerr=[lower_errors, upper_errors],
        marker="o",
        capsize=4,
        label="Nested Protection - FCFS"
    )

    plt.axhline(
        y=0,
        linestyle="--",
        label="Equal revenue"
    )

    plt.xlabel("Demand Multiplier")
    plt.ylabel("Average Revenue Difference ($)")
    plt.title("Demand Sensitivity: Nested Protection vs FCFS")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()
