import pytest

from seatlab.scenario import Scenario, FareClass
from seatlab.policies.fcfs import FCFSPolicy
from seatlab.simulate import simulate_flight

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