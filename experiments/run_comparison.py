from seatlab.scenario import Scenario, FareClass
from seatlab.simulate import simulate_flight
from seatlab.policies.fcfs import FCFSPolicy
from seatlab.policies.nested import NestedProtectionPolicy
import numpy as np
from scipy import stats

def run_comparison(scenario, n_simulations=1000, base_seed=42):

    if n_simulations < 2:
        raise ValueError("At least 2 simulations are required")

    fcfs_revenues = []
    nested_revenues = []

    fcfs_policy = FCFSPolicy()

    nested_policy = NestedProtectionPolicy(
        scenario.fare_classes[0],
        scenario.fare_classes[1]
    )

    for i in range(n_simulations):

        seed = base_seed + i

        fcfs_result = simulate_flight(
            scenario,
            fcfs_policy,
            seed=seed
        )

        nested_result = simulate_flight(
            scenario,
            nested_policy,
            seed=seed
        )

        fcfs_revenues.append(fcfs_result["revenue"])
        nested_revenues.append(nested_result["revenue"])

    revenue_differences = [
        nested - fcfs
        for nested, fcfs in zip(nested_revenues, fcfs_revenues)
    ]

    average_difference = np.mean(revenue_differences)

    std_difference = np.std(revenue_differences, ddof=1)

    standard_error = std_difference / np.sqrt(n_simulations)

    t_critical = stats.t.ppf(0.975, df=n_simulations - 1)

    margin_of_error = t_critical * standard_error

    confidence_interval = (
        average_difference - margin_of_error,
        average_difference + margin_of_error
    )

    return {
        "fcfs_mean": np.mean(fcfs_revenues),
        "nested_mean": np.mean(nested_revenues),
        "average_difference": average_difference,
        "std_difference": std_difference,
        "confidence_interval": confidence_interval
    }

if __name__ == "__main__":

    scenario = Scenario(
        route="JFK-LAX",
        capacity=180,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 180),
            FareClass("High", 400, 75)
        ]
    )

    results = run_comparison(scenario, n_simulations=1000)

    print(results)

    nested_policy = NestedProtectionPolicy(
        scenario.fare_classes[0],
        scenario.fare_classes[1]
    )

    print("Protection level:", nested_policy.protection_level)

    print("FCFS, seed 42:", simulate_flight(
        scenario, FCFSPolicy(), seed=42
    ))

    print("Nested, seed 42:", simulate_flight(
        scenario, nested_policy, seed=42
    ))