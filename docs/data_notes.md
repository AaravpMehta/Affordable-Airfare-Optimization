 # Data Notes - Affordable Airfare Optimization

## 1. Project Scope

This project investigates how airline demand patterns and fare distributions can inform pricing and revenue management strategies that help with balancing affordability with airline profitability, thus providing advantages to both the passengers as well as the airlines and making the safest form of travel more and more used.

The initial analysis focuses on the **JFK–LAX route in the United States**, usingdata from Bureau of Transportation Statistics (BTS) for the time period of **January–June 2025**.

The two datasets we will be using for this are:
- **T-100:** To show monthly passenger traffic for the route and it is broken down by carrier.
- **DB1B:** This is the sampled airline ticket-market data used to explore fare distributions.

## 2. T-100 Dataset

The T-100 dataset from the US Bureau of Transportation Statistics (BTS) provides us monthly airline traffic data. For this project, the data focuses solely on the **JFK–LAX route for January–June 2025**.

### Key Findings

- **Total passengers:** 682,672
- **Airlines identified:** Delta, JetBlue, American Airlines, and Frontier
- **Records analysed:** 20 scheduled passenger-service records

### Monthly Passenger Traffic

| Month | Passengers |
|---|---:|
| January | 96,834 |
| February | 93,599 |
| March | 112,671 |
| April | 120,400 |
| May | 132,224 |
| June | 126,944 |
| **Total** | **682,672** |

### Passenger Traffic by Airline

| Airline | Passengers |
|---|---:|
| Delta Air Lines | 325,637 |
| JetBlue Airways | 204,677 |
| American Airlines | 138,694 |
| Frontier Airlines | 13,664 |
| **Total** | **682,672** |

### Data Interpretation

Passenger traffic generally increased from January through May, before declining slightly in June. Delta carried the largest number of passengers among the four airlines in the filtered dataset.

The `CLASS` column identifies the **type of service**, not the ticket's fare class. For this analysis, `F` represents scheduled passenger service.

### Limitation

The processed T-100 file currently contains passenger counts but does not include seats or departures. Therefore, load factor cannot yet be calculated from this file. Additional capacity data may be required.

## 3. DB1B Dataset

The DB1B dataset, published by the US Bureau of Transportation Statistics (BTS), provides a 10% sample of airline ticket market data. It is used in this project to analyse fare distributions for the JFK–LAX route.

### Data Filtering

The Q1 and Q2 2025 datasets were filtered using `MARKET_COUPONS == 1` to identify nonstop journeys between JFK and LAX.

| Metric | Q1 2025 | Q2 2025 |
|---|---:|---:|
| Nonstop records | 6,255 | 8,605 |
| Sampled passengers | 25,740 | 33,599 |
| Records with non-positive fares | 16 | 18 |
| Records with fares above $2,000 | 270 | 704 |

### Fare Distribution

After excluding records with non-positive fares, the fare quartiles were:

| Fare statistic | Q1 2025 | Q2 2025 |
|---|---:|---:|
| 25th percentile (Q1) | $245.50 | $264.50 |
| Median | $398.00 | $441.50 |
| 75th percentile (Q3) | $950.25 | $1,054.50 |

The median and quartile fares were higher in Q2 than in Q1. This is an initial observation, not proof that fares increased for every passenger or airline.

### Data Interpretation

`MARKET_FARE` represents the fare recorded for a ticket market. It does not directly identify an airline's booking class or the price of a particular seat. The data can help us understand fare patterns and inform the design of fare categories for the simulator.

### Limitations

- DB1B is a 10% sample, so multiplying passenger counts by ten provides only an approximate expansion.
- Non-positive fares require investigation before analysis.
- Fares above $2,000 should be reviewed, but should not automatically be treated as errors or removed.
- The dataset covers Q1 and Q2 2025; conclusions should be limited to this period and route unless more data is added.

## 4. Assumptions and Remaining Limitations

### Project Assumptions

- The initial analysis focuses on the JFK–LAX route during January–June 2025.
- DB1B provides a sample of ticket-market data that can be used to study fare distributions.
- Fare categories may be developed from the observed fare distribution, but these categories will be analytical groupings rather than actual airline booking classes.
- T-100 passenger traffic can help inform demand patterns, while DB1B fares can help inform the pricing component of the simulator.

### Data Limitations

- **Sampling:** DB1B represents a 10% sample. Expanding sampled passenger counts by a factor of ten gives an approximation, not an exact total.
- **Fare interpretation:** `MARKET_FARE` does not directly represent a specific seat's price or an airline's booking class.
- **Capacity:** The processed T-100 dataset contains passenger counts but does not currently include seats or departures. Load factors cannot be calculated from the current file.
- **Time period:** The initial DB1B analysis covers only Q1 and Q2 2025, so seasonal and year-to-year patterns cannot yet be established.
- **Unusual fares:** Non-positive fares and fares above $2,000 require further investigation. They should not automatically be removed without understanding their context.
- **Demand estimation:** Observed passenger traffic alone does not reveal the full demand distribution, including passengers who wanted to travel but did not purchase a ticket.

### Next Steps

- Investigate whether additional BTS data can provide seats and departures for the selected route.
- Finalise fare categories using the cleaned DB1B data.
- Document the assumptions used to convert the historical data into simulator inputs.
- Build and validate the simulator before drawing conclusions about affordability and airline profitability.