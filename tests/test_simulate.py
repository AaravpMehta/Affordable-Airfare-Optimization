import pytest

from seatlab.scenario import Scenario, FareClass
from seatlab.policies.fcfs import FCFSPolicy
from seatlab.simulate import simulate_flight
from seatlab.policies.nested import NestedProtectionPolicy

def test_simulation_never_exceeds_capacity():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=10,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    result = simulate_flight(scenario, FCFSPolicy(), seed=42)

    total_bookings = sum(result["bookings"].values())

    assert total_bookings <= scenario.capacity
    assert result["remaining_capacity"] >= 0
    assert total_bookings + result["remaining_capacity"] == scenario.capacity

def test_revenue_matches_accepted_bookings():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=10,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    result = simulate_flight(scenario, FCFSPolicy(), seed=42)

    expected_revenue = (
        result["bookings"]["Low"] * 150
        + result["bookings"]["High"] * 400
    )

    assert result["revenue"] == expected_revenue

def test_bookings_do_not_exceed_expected_arrivals():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=10,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    result = simulate_flight(scenario, FCFSPolicy(), seed=42)

    assert result["bookings"]["Low"] >= 0
    assert result["bookings"]["High"] >= 0

    assert sum(result["bookings"].values()) <= 10

def test_simulation_tracks_rejected_bookings():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=10,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    result = simulate_flight(scenario, FCFSPolicy(), seed=42)

    assert result["rejected_bookings"] > 0
    assert result["remaining_capacity"] == 0

def test_simulation_is_deterministic():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=10,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    result1 = simulate_flight(scenario, FCFSPolicy(), seed=42)
    result2 = simulate_flight(scenario, FCFSPolicy(), seed=42)

    assert result1 == result2

def test_low_fare_bookings_do_not_increase_with_protection():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=100,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    policy_20 = NestedProtectionPolicy(
        scenario.fare_classes[0],
        scenario.fare_classes[1]
    )
    policy_40 = NestedProtectionPolicy(
        scenario.fare_classes[0],
        scenario.fare_classes[1]
    )

    policy_20.protection_level = 20
    policy_40.protection_level = 40

    result_20 = simulate_flight(scenario, policy_20, seed=42)
    result_40 = simulate_flight(scenario, policy_40, seed=42)

    assert (
        result_40["bookings"]["Low"]
        <= result_20["bookings"]["Low"]
    )

def test_zero_protection_equals_fcfs():
    scenario = Scenario(
        route="JFK-LAX",
        capacity=100,
        booking_horizon_days=30,
        fare_classes=[
            FareClass("Low", 150, 120),
            FareClass("High", 400, 50)
        ]
    )

    nested_policy = NestedProtectionPolicy(
        scenario.fare_classes[0],
        scenario.fare_classes[1]
    )

    nested_policy.protection_level = 0

    fcfs_result = simulate_flight(
        scenario, FCFSPolicy(), seed=42
    )

    nested_result = simulate_flight(
        scenario, nested_policy, seed=42
    )

    assert nested_result == fcfs_result