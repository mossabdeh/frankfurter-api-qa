# Automation Strategy

## Purpose

Build a focused automated regression suite for the Frankfurter API based on product risk and regression value.

The goal is not to reproduce every Bruno exploratory test in Pytest, but to automate stable and valuable behaviors that should be protected across releases.

## Objectives

The automated suite should:

- keep critical exchange-rate functionality working;
- detect incorrect or inconsistent financial data;
- detect breaking API contract and validation changes;
- protect historical, time-range, and provider behavior;
- provide fast and reliable feedback in CI.

## Test Selection Principles

Automation candidates are evaluated based on:

- product risk;
- execution frequency;
- repeatability and stability;
- automation feasibility;
- maintenance cost;
- business value and expected return.

> A test should not be automated simply because it can be automated.

Exploratory, unstable, poorly specified, or low-value scenarios may remain manual.

## Product Risk Analysis

Risk level is evaluated as:

**Risk Score = Impact × Likelihood**

| Score | Priority |
|---|---|
| 1–2 | Low |
| 3–4 | Medium |
| 6–9 | High |

| Product Risk | Impact | Likelihood | Score | Priority |
|---|---:|---:|---:|---|
| Core rate endpoint becomes unavailable/unusable | 3 | 1 | 3 | Medium |
| Incorrect exchange-rate data | 3 | 2 | 6 | High |
| Base/quote filtering returns incorrect currencies | 2 | 1 | 2 | Low |
| Historical request returns incorrect date/rate data | 3 | 2 | 6 | High |
| Time-series data falls outside requested range | 2 | 2 | 4 | Medium |
| API contract changes unexpectedly | 3 | 2 | 6 | High |
| Provider filtering is ignored or incorrect | 2 | 2 | 4 | Medium |
| Related endpoints return inconsistent information | 2 | 2 | 4 | Medium |
| Validation/error handling changes | 2 | 2 | 4 | Medium |
| CSV/NDJSON formatting breaks | 2 | 1 | 2 | Low |
| Rate/provider data becomes stale | 3 | 3 | 9 | High |

Product-risk priority does not directly determine automation priority. Low-risk tests may still be excellent automation candidates when they are fast, stable, repeatable, and inexpensive to maintain.

## Automation Scope v1

### Smoke

Fast checks confirming that critical API functionality is operational.

- `/rates` availability and basic response validity
- single currency-pair retrieval
- basic base/quote filtering

### Core Regression

Stable functional and contract behavior.

- multiple quote filtering
- representative invalid-currency validation
- historical rates
- time-series ranges
- provider filtering and attribution
- currency metadata
- provider metadata
- response contracts

### Data Integrity

Checks designed to detect valid-looking but incorrect data.

- identity-rate rule
- cross-endpoint consistency
- provider consistency
- inverse-rate consistency
- cross-rate consistency

### Deferred

- CSV and NDJSON regression coverage
- grouping behavior
- `scope=all`
- case variations and equivalent edge cases
- explicit freshness/staleness validation until a reliable freshness rule is defined
