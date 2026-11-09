from seatlab.policies.base import Policy


class FCFSPolicy(Policy):

    def accept_booking(self, fare_class, remaining_capacity, days_to_departure, bookings):
        """
        Accept bookings in the order they are received until capacity is full.
        """
        return remaining_capacity > 0