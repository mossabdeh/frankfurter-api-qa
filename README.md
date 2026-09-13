# Frankfurter API QA

[![API Test Suite](https://github.com/mossabdeh/frankfurter-api-qa/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/mossabdeh/frankfurter-api-qa/actions/workflows/tests.yml)

API testing and data-validation project for the [Frankfurter](https://frankfurter.dev/) foreign-exchange API using **Python, Pytest, Bruno, and GitHub Actions**.

## Overview

This project demonstrates an end-to-end API QA workflow, from exploratory testing to automated regression and data-integrity validation.

Testing started in Bruno to understand API behavior, validation rules, edge cases, providers, historical data, and response formats. Stable and valuable scenarios were then selected for automation using a risk-based approach.

The automated suite currently contains **17 designed scenarios / 18 Pytest executions**.

## Setup

Requires Python 3.10+.

```bash
git clone https://github.com/mossabdeh/frankfurter-api-qa.git
cd frankfurter-api-qa

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -e .
```

Run the complete suite:

```bash
pytest -v
```

## Environment Configuration

Tests run against the public Frankfurter API by default:

```text
https://api.frankfurter.dev/v2
```

A different environment can be selected with:

```bash
export FRANKFURTER_BASE_URL="http://localhost:8080/v2"
pytest
```

Remove the override with:

```bash
unset FRANKFURTER_BASE_URL
```

## QA Approach

```text
Exploratory testing with Bruno
        ↓
Observed API behavior
        ↓
Risk-based automation selection
        ↓
Test design
        ↓
Pytest automation
        ↓
Continuous integration
```

Automation candidates were selected based on risk, repeatability, stability, execution frequency, maintenance cost, and automation value.

Not every exploratory case was automated. Redundant, low-value, unstable, or insufficiently specified scenarios were intentionally kept outside the initial automated scope.

## Manual / Exploratory Testing

The Bruno collection used during exploratory testing is available under:

```text
bruno/frankfurter_v2/
```

It includes coverage for rates, historical queries, time ranges, grouping, providers, metadata, CSV/NDJSON responses, and representative invalid scenarios.

Bruno is used for exploratory/manual testing, while Pytest contains the selected automated suite.

## Automated Test Coverage

### Smoke

Fast checks for critical API functionality:

- Latest rates retrieval
- Single currency-pair retrieval
- Base and quote filtering

```bash
pytest -m smoke
```

### Regression

Core API behavior and contracts:

- Multiple quote filtering
- Invalid currency validation
- Historical rates
- Time-series ranges
- Provider filtering and attribution
- Currency collection contract
- Single-currency metadata
- Provider collection contract

```bash
pytest -m regression
```

### Data Integrity

Validation of relationships between exchange-rate data:

- Identity rate: `X/X == 1`
- `/rates` and `/rate` consistency
- Provider attribution consistency
- Inverse-rate consistency: `A/B × B/A ≈ 1`
- Cross-rate consistency

```bash
pytest -m data_integrity
```

## Documentation

- [Automation Strategy](docs/automation-strategy.md)
- [Automated Test Design](docs/test-design.md)

## Continuous Integration

GitHub Actions runs the complete test suite on pushes and pull requests to `master`.

JUnit XML results are generated and stored as workflow artifacts for test-execution evidence.