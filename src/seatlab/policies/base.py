from abc import ABC, abstractmethod


class Policy(ABC):

    @abstractmethod
    def accept_booking(self, fare_class, remaining_capacity, days_to_departure, bookings):
        pass