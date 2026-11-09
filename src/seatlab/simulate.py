from seatlab.arrivals import generate_arrivals


def simulate_flight(scenario, policy, seed=42):

    arrivals = []

    # Generate arrivals for each fare class
    for i, fare in enumerate(scenario.fare_classes):

        times = generate_arrivals(
            fare.expected_demand,
            scenario.booking_horizon_days,
            seed + i
        )

        for time in times:
            arrivals.append((time, fare))

    # Process arrivals chronologically
    arrivals.sort(key=lambda x: x[0])

    # Initialise flight inventory
    remaining_capacity = scenario.capacity

    bookings = {
        fare.name: 0
        for fare in scenario.fare_classes
    }

    revenue = 0
    rejected_bookings = 0

    # Process bookings
    for arrival_time, fare in arrivals:

        days_to_departure = (
            scenario.booking_horizon_days - arrival_time
        )

        accepted = policy.accept_booking(
            fare,
            remaining_capacity,
            days_to_departure,
            bookings
        )

        if accepted:
            remaining_capacity -= 1
            bookings[fare.name] += 1
            revenue += fare.price

        else:
            rejected_bookings += 1

    return {
        "revenue": revenue,
        "bookings": bookings,
        "rejected_bookings": rejected_bookings,
        "remaining_capacity": remaining_capacity
    }