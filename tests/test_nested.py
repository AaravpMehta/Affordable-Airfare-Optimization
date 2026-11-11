from seatlab.scenario import FareClass, Scenario
from seatlab.policies.nested import (
    calculate_protection_level,
    calculate_emsrb_protection_levels,
    calculate_emsrb_normal_approximation,
    NestedProtectionPolicy
)
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

def test_emsrb_two_class_matches_littlewood():
    low = FareClass("Low", 150, 120)
    high = FareClass("High", 400, 50)

    littlewood = calculate_protection_level(low, high)

    emsrb = calculate_emsrb_protection_levels([low, high])

    assert emsrb["Low"] == littlewood
    assert emsrb["High"] == 0

def test_emsrb_hand_calculated_example():
    fares = [
        FareClass("Saver", 100, 100),
        FareClass("Standard", 180, 70),
        FareClass("Flex", 350, 40),
        FareClass("Business", 600, 20)
    ]

    protection = calculate_emsrb_protection_levels(fares)

    assert protection["Saver"] == 135
    assert protection["Business"] == 0

def test_emsrb_protection_levels_are_nested():
    fares = [
        FareClass("Saver", 100, 100),
        FareClass("Standard", 180, 70),
        FareClass("Flex", 350, 40),
        FareClass("Business", 600, 20)
    ]

    protection = calculate_emsrb_protection_levels(fares)

    assert (
        protection["Saver"]
        >= protection["Standard"]
        >= protection["Flex"]
        >= protection["Business"]
    )

def test_protection_increases_with_higher_fare_demand():
    low = FareClass("Low", 100, 100)

    high_low_demand = FareClass("High", 400, 30)
    high_high_demand = FareClass("High", 400, 60)

    protection_low = calculate_emsrb_protection_levels(
        [low, high_low_demand]
    )

    protection_high = calculate_emsrb_protection_levels(
        [low, high_high_demand]
    )

    assert protection_high["Low"] >= protection_low["Low"]

def test_normal_approximation_is_close_to_exact():
    fares = [
        FareClass("Saver", 100, 100),
        FareClass("Standard", 180, 70),
        FareClass("Flex", 350, 40),
        FareClass("Business", 600, 20)
    ]

    exact = calculate_emsrb_protection_levels(fares)
    approximate = calculate_emsrb_normal_approximation(fares)

    for fare in fares:
        assert abs(
            exact[fare.name] - approximate[fare.name]
        ) <= 2