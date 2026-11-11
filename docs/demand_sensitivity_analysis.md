# Demand Sensitivity Analysis: Nested Protection vs FCFS

## 1. Experiment Objective

The objective of this experiment is to evaluate how changes in passenger demand affect the revenue performance of two airline revenue-management policies:

- **First-Come, First-Served (FCFS):** Accepts bookings in the order they arrive until flight capacity is exhausted.
- **Nested Protection:** Reserves a predetermined number of seats for high-fare passengers and accepts low-fare bookings only when remaining capacity exceeds the protection level.

The experiment aims to identify the demand conditions under which Nested Protection begins to outperform FCFS.

## 2. Scenario Assumptions

The experiment uses a synthetic JFK–LAX flight scenario.

| Parameter | Value |
|---|---:|
| Flight capacity | 180 seats |
| Booking horizon | 30 days |
| Low fare | $150 |
| High fare | $400 |
| Base expected low-fare demand | 120 |
| Base expected high-fare demand | 50 |
| Base total expected demand | 170 |
| Simulations per scenario | 1,000 |

Demand is modelled using independent Poisson arrival processes for each fare class. Passenger arrival times are distributed uniformly across the booking horizon.

A demand multiplier is applied to both fare classes while keeping prices and capacity constant.

For example, at a multiplier of 1.5:

- Expected low-fare demand = 180
- Expected high-fare demand = 75
- Total expected demand = 255

## 3. Methodology

Each demand scenario is simulated 1,000 times using both FCFS and Nested Protection.

The same random seed is used for both policies within each simulation. This creates paired comparisons using common random numbers.

For every simulation:

\[
D_i = R_{\text{Nested},i} - R_{\text{FCFS},i}
\]

The average revenue difference is calculated as:

\[
\bar D = \frac{1}{n}\sum_{i=1}^{n}D_i
\]

A 95% confidence interval is calculated using the paired differences and the Student's t-distribution:

\[
\bar D \pm t_{0.975,n-1}\frac{s_D}{\sqrt n}
\]

A positive difference favours Nested Protection, while a negative difference favours FCFS.

If the confidence interval includes zero, the experiment does not establish a statistically clear revenue advantage for either policy at the 5% significance level.

## 4. Experimental Results

The following table consolidates the broad demand experiment and the finer crossover experiment.

| Multiplier | Total expected demand | FCFS revenue ($) | Nested revenue ($) | Difference ($) |
|---:|---:|---:|---:|---:|
| 0.60 | 102.0 | 22,838.80 | 22,838.80 | 0.00 |
| 0.80 | 136.0 | 30,449.95 | 30,035.95 | -414.00 |
| 1.00 | 170.0 | 37,631.90 | 33,561.65 | -4,070.25 |
| 1.20 | 204.0 | 40,178.90 | 36,581.00 | -3,597.90 |
| 1.25 | 212.5 | 40,215.20 | 37,244.80 | -2,970.40 |
| 1.30 | 221.0 | 40,221.45 | 38,044.30 | -2,177.15 |
| 1.35 | 229.5 | 40,217.65 | 38,713.20 | -1,504.45 |
| 1.40 | 238.0 | 40,210.25 | 39,408.10 | -802.15 |
| 1.42 | 241.4 | 40,212.75 | 39,696.55 | -516.20 |
| 1.43 | 243.1 | 40,213.25 | 39,902.90 | -310.35 |
| 1.44 | 244.8 | 40,185.75 | 39,970.75 | -215.00 |
| 1.45 | 246.5 | 40,197.75 | 40,175.35 | -22.40 |
| 1.46 | 248.2 | 40,198.25 | 40,264.45 | 66.20 |
| 1.47 | 249.9 | 40,206.00 | 40,491.60 | 285.60 |
| 1.48 | 251.6 | 40,192.25 | 40,552.10 | 359.85 |
| 1.49 | 253.3 | 40,186.50 | 40,757.65 | 571.15 |
| 1.50 | 255.0 | 40,176.00 | 40,850.75 | 674.75 |
| 1.80 | 306.0 | 40,187.75 | 45,264.70 | 5,076.95 |
| 2.00 | 340.0 | 40,203.00 | 48,157.50 | 7,954.50 |

### 95% Confidence Intervals

The following intervals correspond to the average paired revenue differences.

| Multiplier | 95% Confidence Interval ($) |
|---:|---:|
| 0.60 | [0.00, 0.00] |
| 0.80 | [-457.34, -370.66] |
| 1.00 | [-4,139.65, -4,000.85] |
| 1.20 | [-3,714.01, -3,481.79] |
| 1.25 | [-3,097.01, -2,843.79] |
| 1.30 | [-2,312.18, -2,042.12] |
| 1.35 | [-1,643.02, -1,365.88] |
| 1.40 | [-946.55, -657.75] |
| 1.42 | [-662.55, -369.85] |
| 1.43 | [-456.90, -163.80] |
| 1.44 | [-361.98, -68.02] |
| 1.45 | [-170.31, 125.51] |
| 1.46 | [-82.09, 214.49] |
| 1.47 | [135.91, 435.29] |
| 1.48 | [209.01, 510.69] |
| 1.49 | [420.11, 722.19] |
| 1.50 | [521.45, 828.05] |
| 1.80 | [4,891.98, 5,261.92] |
| 2.00 | [7,756.59, 8,152.41] |

## 5. Crossover Analysis

The finer experiment narrows the point at which Nested Protection begins to outperform FCFS.

At a demand multiplier of 1.44, FCFS has a statistically clear advantage. At 1.45 and 1.46, the confidence intervals include zero, so neither policy has a statistically clear advantage. At 1.47, Nested Protection has a statistically clear advantage.

Linear interpolation between the average differences at 1.45 and 1.46 gives an estimated zero-crossing:

\[
x = 1.45 + \frac{22.40}{66.20+22.40}(0.01)
\]

\[
x \approx 1.4525
\]

The corresponding total expected demand is:

\[
170 \times 1.4525 \approx 246.93
\]

Therefore, the estimated crossover occurs at approximately 247 expected passengers for a flight with 180 seats.

This is an estimated crossover based on interpolation, not a statistically established universal threshold.

## 6. Interpretation

The experiment reveals three broad demand conditions.

**Low demand:** Both policies perform similarly because available capacity is sufficient to accommodate arriving passengers.

**Moderate demand:** FCFS performs better because Nested Protection rejects low-fare bookings to preserve seats, but insufficient high-fare demand arrives to use all the protected capacity.

**High demand:** Nested Protection performs better because high-fare demand is sufficient to occupy protected seats. Reserving capacity for higher-paying passengers increases average revenue.

The results demonstrate that the effectiveness of a revenue-management policy depends on demand intensity and the trade-off between accepting current low-fare bookings and preserving capacity for future high-fare bookings.

## 7. Limitations

The results must be interpreted within the assumptions of the current simulator.

- Demand is generated synthetically using Poisson distributions.
- Passenger arrival times are uniformly distributed across the booking horizon.
- The model uses only two fare classes.
- The protection level is static rather than dynamically adjusted over time.
- The model assumes a fixed capacity of 180 seats.
- Cancellations, no-shows and overbooking are not included.
- The experiment does not yet use actual individual booking or reservation data to estimate passenger arrival patterns.

Consequently, the estimated crossover should not be treated as an actual JFK–LAX airline demand threshold.

## 8. Conclusion

The experiment demonstrates that Nested Protection is not inherently superior to FCFS under all demand conditions.

At low and moderate demand, FCFS can generate higher revenue by accepting available bookings without reserving unnecessary capacity. As demand increases, protecting seats for high-fare passengers becomes increasingly valuable.

Under the current synthetic scenario, the estimated revenue crossover occurs around a demand multiplier of 1.4525, corresponding to approximately 247 expected passengers for 180 seats.

These findings provide a baseline for future experiments involving time-dependent demand, dynamic protection levels and price-responsive passenger behaviour.