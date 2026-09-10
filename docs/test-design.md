# Automated Test Design

Automated scenarios selected from the completed Bruno exploratory-testing phase.

The v1 suite contains:

- 3 smoke tests
- 9 core regression tests
- 5 data-integrity tests

## Smoke Tests

| ID | Scenario | Request | Key Assertions |
|---|---|---|---|
| SMK-001 | Retrieve latest rates | `GET /rates` | `200`, non-empty array, required rate fields, valid date, positive numeric rate |
| SMK-002 | Retrieve single currency-pair rate | `GET /rate/EUR/USD` | `200`, correct pair, valid date, positive numeric rate |
| SMK-003 | Basic base/quote filtering | `GET /rates?base=USD&quotes=EUR` | `200`, only requested base and quote returned, positive numeric rate |

The smoke suite should remain small, fast, and suitable for frequent CI execution.

## Core Regression Tests

| ID | Scenario | Request | Key Assertions |
|---|---|---|---|
| REG-001 | Multiple quote filtering | `/rates?base=EUR&quotes=USD,GBP` | Only USD and GBP returned; both present; EUR base respected |
| REG-002 | Invalid currency validation | Representative `/rates` and `/rate` requests using `XYZ` | `422`, expected error structure and invalid-currency message |
| REG-003 | Historical rate retrieval | `/rate/EUR/USD?date=2026-01-02` | Requested date/pair respected; valid positive rate |
| REG-004 | Time-series range | `/rates?from=2026-01-02&to=2026-01-05&quotes=USD` | All dates inside range; USD filter respected |
| REG-005 | Provider filtering | `/rates?providers=ECB&quotes=USD` | Successful non-empty provider-filtered result |
| REG-006 | Provider attribution | `/rates?providers=ECB&expand=providers&quotes=USD` | Attribution exists and identifies ECB |
| REG-007 | Currency collection contract | `/currencies` | Non-empty collection; required metadata fields and types |
| REG-008 | Single currency metadata | `/currency/DZD` | Correct currency; metadata fields; provider list |
| REG-009 | Provider collection contract | `/providers` | Non-empty collection; required provider fields and types |

Representative invalid cases should use parametrization where appropriate instead of duplicated test implementations.

## Data Integrity Tests

| ID | Scenario | Validation |
|---|---|---|
| DATA-001 | Identity rate | `X/X == 1.0` |
| DATA-002 | Cross-endpoint consistency | `/rates` and `/rate` return the same rate for the same pair, date, and context |
| DATA-003 | Provider consistency | Provider filter, attribution, and returned rate remain coherent |
| DATA-004 | Inverse-rate consistency | `A/B × B/A ≈ 1` |
| DATA-005 | Cross-rate consistency | Related currency pairs satisfy the expected cross-rate relationship within tolerance |

Financial comparisons will use an explicit tolerance to account for rounding. The tolerance will be defined and justified during implementation.

## Test Data Strategy

Use a small and stable data set:

| Purpose | Test Data |
|---|---|
| Main currencies | `EUR`, `USD`, `GBP` |
| Currency metadata | `DZD` |
| Provider | `ECB` |
| Invalid currency | `XYZ` |
| Historical reference date | `2026-01-02` |

Latest rates are suitable for smoke testing, but exact latest values must not be hard-coded.

Fixed historical dates should be preferred for regression and financial consistency tests where repeatability matters.
