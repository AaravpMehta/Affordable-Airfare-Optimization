# Hand-Checked Simulator Examples

These examples are used to validate the expected behaviour of First-Come, First-Served (FCFS) and Nested Protection policies in ticket sales simulations.

## Common Scenario

| Parameter | Value |
|---|---:|
| Route | JFK-LAX |
| Aircraft capacity | 3 seats |
| Low fare | $100 |
| High fare | $300 |
| Protection level | 1 seat |

---

## Example 1: High-Fare Demand Arrives

**Passenger arrival sequence:**

$100 → $300 → $100 → $300 → $100

### Nested Protection

| Arrival | Fare | Decision | Remaining seats |
|---|---:|---|---:|
| 1 | $100 | Accept | 2 |
| 2 | $300 | Accept | 1 |
| 3 | $100 | Reject | 1 |
| 4 | $300 | Accept | 0 |
| 5 | $100 | Reject | 0 |

**Expected results:**
- Low bookings: 1
- High bookings: 2
- Rejected bookings: 2
- Remaining capacity: 0
- Revenue: **$700**

### FCFS

FCFS accepts the first three passengers.

- Low bookings: 2
- High bookings: 1
- Rejected bookings: 2
- Remaining capacity: 0
- Revenue: **$500**

**Observation:** Nested protection generates higher revenue as compared to FCFS by preserving some capacity for high-fare passengers.

---

## Example 2: High-Fare Demand Does Not Fully Materialise

**Passenger arrival sequence:**

$100 → $300 → $100 → $100 → $100

### Nested Protection

| Arrival | Fare | Decision | Remaining seats |
|---|---:|---|---:|
| 1 | $100 | Accept | 2 |
| 2 | $300 | Accept | 1 |
| 3 | $100 | Reject | 1 |
| 4 | $100 | Reject | 1 |
| 5 | $100 | Reject | 1 |

**Expected results:**
- Low bookings: 1
- High bookings: 1
- Rejected bookings: 3
- Remaining capacity: 1
- Revenue: **$400**

### FCFS

FCFS accepts the first three passengers.

- Low bookings: 2
- High bookings: 1
- Rejected bookings: 2
- Remaining capacity: 0
- Revenue: **$500**

**Observation:** Static protection can sacrifice revenue and leave seats empty when anticipated high-fare demand does not materialise and in those times FCFS will generate more revenue.

---

## Example 3: High-Fare Demand Arrives After Low-Fare Bookings

**Passenger arrival sequence:**

$100 → $100 → $100 → $300 → $100

### Nested Protection

| Arrival | Fare | Decision | Remaining seats |
|---|---:|---|---:|
| 1 | $100 | Accept | 2 |
| 2 | $100 | Accept | 1 |
| 3 | $100 | Reject | 1 |
| 4 | $300 | Accept | 0 |
| 5 | $100 | Reject | 0 |

**Expected results:**
- Low bookings: 2
- High bookings: 1
- Rejected bookings: 2
- Remaining capacity: 0
- Revenue: **$500**

### FCFS

FCFS accepts the first three passengers.

- Low bookings: 3
- High bookings: 0
- Rejected bookings: 2
- Remaining capacity: 0
- Revenue: **$300**

**Observation:** Nested protection is used to prevent low-fare demand from consuming all thes available capacity before higher-paying passengers arrive.

---

## Overall Comparison

| Metric | Example 1 | Example 2 | Example 3 |
|---|---:|---:|---:|
| FCFS revenue | $500 | $500 | $300 |
| Nested protection revenue | $700 | $400 | $500 |
| Revenue difference | +$200 | -$100 | +$200 |

## Key Takeaways

Static protection creates a trade-off:

- Too little protection can result in high-fare passengers being rejected.
- Too much protection can leave seats empty.
- The effectiveness of protection depends on the timing and volume of passenger demand.

The objective of airline revenue management is to determine a protection level that maximises expected revenue while balancing these risks.