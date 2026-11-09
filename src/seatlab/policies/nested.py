import numpy as np
from scipy.stats import poisson

from seatlab.policies.base import Policy

def calculate_protection_level(low_fare, high_fare):

    critical_ratio = low_fare.price / high_fare.price

    protection_level = poisson.ppf(
        1 - critical_ratio,
        high_fare.expected_demand
    )

    return int(protection_level)

class NestedProtectionPolicy(Policy):

    def __init__(self, low_fare, high_fare):
        self.low_fare = low_fare
        self.high_fare = high_fare

        self.protection_level = calculate_protection_level(
            low_fare,
            high_fare
        )

    def accept_booking(self, fare_class, remaining_capacity, days_to_departure, bookings):

        if remaining_capacity <= 0:
            return False

        if fare_class.name == self.high_fare.name:
            return True

        if fare_class.name == self.low_fare.name:
            return remaining_capacity > self.protection_level

        raise ValueError("Unknown fare class")