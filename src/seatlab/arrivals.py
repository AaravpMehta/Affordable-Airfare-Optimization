import numpy as np

def generate_arrivals(expected_demand, booking_horizon_days, seed):
    rng = np.random.default_rng(seed)

    number_of_arrivals = rng.poisson(expected_demand)

    arrival_times = rng.uniform(
        0,
        booking_horizon_days,
        size=number_of_arrivals
    )

    return np.sort(arrival_times)