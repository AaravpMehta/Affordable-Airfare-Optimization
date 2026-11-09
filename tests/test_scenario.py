import pytest
from seatlab.scenario import FareClass, Scenario

def test_valid_fare_class():
    fare = FareClass("low", 150, 120)

    assert fare.name == "low"
    assert fare.price == 150
    assert fare.expected_demand == 120

def test_invalid_fare_price():
    with pytest.raises(ValueError):
        FareClass("low", -150, 120)

def test_invalid_expected_demand():
    with pytest.raises(ValueError):
        FareClass("low", 150, -10)

def test_valid_scenario():
    low = FareClass("low", 150, 120)
    high = FareClass("high", 400, 50)

    scenario = Scenario(
        route="JFK-LAX",
        capacity=180,
        booking_horizon_days=30,
        fare_classes=[low, high]
    )

    assert scenario.route == "JFK-LAX"
    assert scenario.capacity == 180
    assert len(scenario.fare_classes) == 2

def test_invalid_capacity():
    fare = FareClass("low", 150, 120)

    with pytest.raises(ValueError):
        Scenario(
            route="JFK-LAX",
            capacity=0,
            booking_horizon_days=30,
            fare_classes=[fare]
        )

def test_invalid_booking_horizon():
    fare = FareClass("low", 150, 120)

    with pytest.raises(ValueError):
        Scenario(
            route="JFK-LAX",
            capacity=180,
            booking_horizon_days=0,
            fare_classes=[fare]
        )

def test_duplicate_fare_class_names():
    low1 = FareClass("low", 150, 120)
    low2 = FareClass("low", 200, 80)

    with pytest.raises(ValueError):
        Scenario(
            route="JFK-LAX",
            capacity=180,
            booking_horizon_days=30,
            fare_classes=[low1, low2]
        )

def test_invalid_fare_class_object():
    with pytest.raises(TypeError):
        Scenario(
            route="JFK-LAX",
            capacity=180,
            booking_horizon_days=30,
            fare_classes=["low", "high"]
        )