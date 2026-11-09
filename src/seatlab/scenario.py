from dataclasses import dataclass


@dataclass
class FareClass:
    name: str
    price: float
    expected_demand: float

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("Fare class name must be a string")

        if not isinstance(self.price, (int, float)):
            raise TypeError("Fare price must be numeric")

        if not isinstance(self.expected_demand, (int, float)):
            raise TypeError("Expected demand must be numeric")
        
        if not self.name.strip():
            raise ValueError("Fare class name cannot be empty")

        if self.price <= 0:
            raise ValueError("Fare price must be positive")

        if self.expected_demand < 0:
            raise ValueError("Expected demand cannot be negative")


@dataclass
class Scenario:
    route: str
    capacity: int
    booking_horizon_days: int
    fare_classes: list[FareClass]

    def __post_init__(self):

        if not isinstance(self.route, str):
            raise TypeError("Route must be a string")

        if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
            raise TypeError("Capacity must be an integer")

        if not isinstance(self.booking_horizon_days, int) or isinstance(self.booking_horizon_days, bool):
            raise TypeError("Booking horizon must be an integer")

        if not isinstance(self.fare_classes, list):
            raise TypeError("Fare classes must be provided as a list")

        if not all(isinstance(fare, FareClass) for fare in self.fare_classes):
            raise TypeError("Every fare class must be a FareClass object")
        
        if not self.route.strip():
            raise ValueError("Route cannot be empty")

        if self.capacity <= 0:
            raise ValueError("Capacity must be positive")

        if self.booking_horizon_days <= 0:
            raise ValueError("Booking horizon must be positive")

        if not self.fare_classes:
            raise ValueError("At least one fare class is required")

        names = [fare.name for fare in self.fare_classes]

        if len(names) != len(set(names)):
            raise ValueError("Fare class names must be unique")