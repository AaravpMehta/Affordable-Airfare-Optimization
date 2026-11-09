from seatlab.scenario import FareClass, Scenario
from seatlab.policies.nested import calculate_protection_level
from seatlab.simulate import simulate_flight



def test_protection_level_is_positive():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    protection = calculate_protection_level(low, high)

    assert protection > 0
    assert isinstance(protection, int)


def test_protection_level_respects_aircraft_demand():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    protection = calculate_protection_level(low, high)

    assert protection <= high.expected_demand + 5

from seatlab.policies.nested import NestedProtectionPolicy

def test_high_fare_booking_is_accepted():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    policy = NestedProtectionPolicy(low, high)

    assert policy.accept_booking(high, 10, 5, {}) is True

def test_low_fare_booking_rejected_at_protection_level():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    policy = NestedProtectionPolicy(low, high)

    assert policy.accept_booking(
        low, policy.protection_level, 5, {}
    ) is False

def test_full_flight_rejects_all_bookings():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    policy = NestedProtectionPolicy(low, high)

    assert policy.accept_booking(high, 0, 5, {}) is False
    assert policy.accept_booking(low, 0, 5, {}) is False

def test_nested_policy_works_with_simulator():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    scenario = Scenario(
        route="JFK-LAX",
        capacity=180,
        booking_horizon_days=30,
        fare_classes=[low, high]
    )

    policy = NestedProtectionPolicy(low, high)

    result = simulate_flight(scenario, policy, seed=42)

    assert result["remaining_capacity"] >= 0
    assert sum(result["bookings"].values()) <= 180

    assert result["bookings"]["Low"] <= (
        scenario.capacity - policy.protection_level
    )