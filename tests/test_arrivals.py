import numpy as np
from seatlab.arrivals import generate_arrivals

def test_same_seed_produces_same_arrivals():
    arrivals1 = generate_arrivals(120, 30, seed=42)
    arrivals2 = generate_arrivals(120, 30, seed=42)

    assert np.array_equal(arrivals1, arrivals2)

def test_arrivals_within_booking_horizon():
    arrivals = generate_arrivals(120, 30, seed=42)

    assert np.all(arrivals >= 0)
    assert np.all(arrivals <= 30)

def test_average_arrivals_approach_expected_demand():
    counts = [
        len(generate_arrivals(120, 30, seed=s))
        for s in range(100)
    ]

    assert abs(np.mean(counts) - 120) < 5