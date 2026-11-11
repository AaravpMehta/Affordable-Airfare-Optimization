
from scipy.stats import poisson
from scipy.stats import norm
from seatlab.policies.base import Policy


def calculate_protection_level(low_fare, high_fare):
    critical_ratio = low_fare.price / high_fare.price

    protection_level = poisson.ppf(
        1 - critical_ratio,
        high_fare.expected_demand
    )

    return int(protection_level)


def calculate_emsrb_protection_levels(fare_classes):
    """
    Calculate EMSR-b protection levels for multiple fare classes.
    """
    fare_classes = sorted(fare_classes, key=lambda fare: fare.price)

    if len(fare_classes) < 2:
        raise ValueError("At least two fare classes are required")

    protection_levels = {fare.name: 0 for fare in fare_classes}

    for i in range(len(fare_classes) - 1):
        low_fare = fare_classes[i]
        higher_fares = fare_classes[i + 1:]

        total_higher_demand = sum(
            fare.expected_demand for fare in higher_fares
        )

        if total_higher_demand == 0:
            protection_levels[low_fare.name] = 0
            continue

        weighted_average_fare = sum(
            fare.price * fare.expected_demand
            for fare in higher_fares
        ) / total_higher_demand

        critical_ratio = low_fare.price / weighted_average_fare

        if critical_ratio >= 1:
            protection_levels[low_fare.name] = 0
            continue

        protection_level = poisson.ppf(
            1 - critical_ratio,
            total_higher_demand
        )

        protection_levels[low_fare.name] = int(protection_level)

    return protection_levels


def calculate_emsrb_normal_approximation(fare_classes):
    fare_classes = sorted(fare_classes, key=lambda fare: fare.price)

    if len(fare_classes) < 2:
        raise ValueError("At least two fare classes are required")

    protection_levels = {fare.name: 0 for fare in fare_classes}

    for i in range(len(fare_classes) - 1):
        low_fare = fare_classes[i]
        higher_fares = fare_classes[i + 1:]

        total_demand = sum(
            fare.expected_demand for fare in higher_fares
        )

        if total_demand == 0:
            continue

        average_fare = sum(
            fare.price * fare.expected_demand
            for fare in higher_fares
        ) / total_demand

        critical_ratio = 1 - low_fare.price / average_fare

        if critical_ratio <= 0:
            continue

        z = norm.ppf(critical_ratio)

        protection = (
            total_demand
            + z * (total_demand ** 0.5)
            - 0.5
        )

        protection_levels[low_fare.name] = max(
            0, round(protection)
        )

    return protection_levels


class NestedProtectionPolicy(Policy):

    def __init__(self, low_fare, high_fare):
        self.low_fare = low_fare
        self.high_fare = high_fare

        self.protection_level = calculate_protection_level(
            low_fare,
            high_fare
        )

    def accept_booking(
        self, fare_class, remaining_capacity,
        days_to_departure, bookings
    ):
        if remaining_capacity <= 0:
            return False

        if fare_class.name == self.high_fare.name:
            return True

        if fare_class.name == self.low_fare.name:
            return remaining_capacity > self.protection_level

        raise ValueError("Unknown fare class")
