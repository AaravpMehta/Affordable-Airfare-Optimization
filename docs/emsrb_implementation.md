
# EMSR-b Implementation

## 1. Overview

The project implements the Expected Marginal Seat Revenue (EMSR-b) heuristic for multiple fare classes sharing a common aircraft capacity.

EMSR-b calculates protection levels for lower-fare classes by aggregating all higher-fare classes into a synthetic fare class.

The objective is to reserve sufficient inventory for higher-paying demand while allowing lower-fare bookings when capacity is available.

## 2. Mathematical Methodology

Fare classes are sorted in ascending order of price.

For each lower-fare class i, all higher-fare classes are aggregated.

### Aggregate expected demand

\[
\mu_i^+ = \sum_{j=i+1}^{n}\mu_j
\]

### Weighted average fare

\[
\bar p_i =
\frac{\sum_{j=i+1}^{n}p_j\mu_j}
{\sum_{j=i+1}^{n}\mu_j}
\]

### Critical ratio

\[
CR_i = \frac{p_i}{\bar p_i}
\]

### Protection level

\[
y_i =
F^{-1}_{Poisson(\mu_i^+)}
(1-CR_i)
\]

The Poisson inverse cumulative distribution function provides the exact integer protection level.

The highest-fare class has a protection level of zero because there are no higher-fare classes to protect inventory for.

## 3. Implementation Details

The implementation is located in:

`src/seatlab/policies/nested.py`

The function `calculate_emsrb_protection_levels()`:

- Sorts fare classes by ascending price.
- Aggregates the expected demand of higher-fare classes.
- Calculates their demand-weighted average fare.
- Calculates the critical ratio.
- Uses the Poisson inverse CDF to determine protection levels.
- Returns a dictionary mapping fare-class names to protection levels.

The existing `calculate_protection_level()` and `NestedProtectionPolicy` are retained for compatibility with the original two-class implementation.

## 4. Assumptions and Limitations

- All fare classes share a single inventory pool.
- Demand for each fare class follows a Poisson distribution.
- Fare-class demands are independent.
- Expected demand is treated as known.
- EMSR-b uses aggregated higher-fare demand and a weighted average fare.
- Protection levels are calculated independently for each lower-fare class.
- The implementation uses static protection levels rather than dynamically updating them as bookings arrive.

## 5. Testing and Validation

The implementation was tested using `tests/test_nested.py`.

The test suite contains 10 passing tests, covering:

- Existing two-class protection-level calculations.
- High-fare booking acceptance.
- Low-fare booking rejection at the protection threshold.
- Full-flight booking rejection.
- Simulator integration.
- Two-class EMSR-b equivalence to Littlewood's rule.
- A four-class hand-calculated example.
- Nested protection-level ordering.
- Increased protection under increased higher-fare demand.

The hand-calculated example uses four fare classes: Saver, Standard, Flex and Business.

For the Saver class, the aggregate higher-fare demand is 130 passengers, the weighted average fare is approximately 296.92, and the calculated protection level is 135 seats.

## 6. Normal Approximation Cross-Check

A normal approximation with continuity correction was implemented
to compare against the exact Poisson quantile method.

The approximation uses:

y ≈ μ + z√μ - 0.5

The four-class example produced results within two seats of the
exact Poisson protection levels for every fare class.

The exact Poisson method remains the primary implementation,
while the normal approximation serves as a validation and
comparison method.

The expanded test suite contains 11 passing tests.

## 7. Conclusion

The project now supports multi-class EMSR-b protection-level calculations using exact Poisson quantiles.

The implementation preserves the original two-class policy and has passed the current 10-test validation suite.
