import pytest
from math import isclose


@pytest.mark.data_integrity
def test_data_001_identity_rate(client):
    """
    DATA-001  Identity rate

    Endpoint:
        GET /rate/EUR/EUR

    Objective:
        Verify the financial identity rule that a currency
        exchanged against itself has a rate of 1.

    Expected:
        - HTTP 200
        - JSON object
        - Base is EUR
        - Quote is EUR
        - Rate equals 1.0
    """
    response = client.get_rate("EUR", "EUR")

    assert response.status_code == 200

    rate = response.json()

    assert isinstance(rate, dict)

    assert rate["base"] == "EUR"
    assert rate["quote"] == "EUR"
    assert rate["rate"] == 1.0




@pytest.mark.data_integrity
def test_data_004_inverse_rate_consistency(client):
    """
    DATA-004  Inverse-rate consistency

    Endpoints:
        GET /rate/EUR/USD?date=2026-01-02
        GET /rate/USD/EUR?date=2026-01-02

    Objective:
        Verify that inverse currency-pair rates are financially
        consistent for the same historical date.

    Expected:
        - Both requests return HTTP 200
        - Both responses use the requested date
        - EUR/USD × USD/EUR is approximately 1
        - A small tolerance is allowed for rate rounding
    """
    eur_usd_response = client.get_rate(
        "EUR",
        "USD",
        params={"date": "2026-01-02"},
    )

    usd_eur_response = client.get_rate(
        "USD",
        "EUR",
        params={"date": "2026-01-02"},
    )

    assert eur_usd_response.status_code == 200
    assert usd_eur_response.status_code == 200

    eur_usd = eur_usd_response.json()
    usd_eur = usd_eur_response.json()

    assert eur_usd["date"] == "2026-01-02"
    assert usd_eur["date"] == "2026-01-02"

    product = eur_usd["rate"] * usd_eur["rate"]

    assert isclose(
        product,
        1.0,
        rel_tol=0.0,
        abs_tol=1e-4,
    )






CROSS_RATE_REL_TOLERANCE = 2e-4


@pytest.mark.data_integrity
def test_data_005_cross_rate_consistency(client):
    """
    DATA-005  Cross-rate consistency

    Endpoints:
        GET /rate/EUR/USD?date=2026-01-02&providers=ECB
        GET /rate/USD/GBP?date=2026-01-02&providers=ECB
        GET /rate/EUR/GBP?date=2026-01-02&providers=ECB

    Objective:
        Verify that related exchange rates from the same provider
        satisfy the expected cross-rate relationship.

    Expected:
        - All requests return HTTP 200
        - All responses use the requested date and currency pairs
        - EUR/USD × USD/GBP is approximately equal to EUR/GBP
        - A small tolerance is allowed for published-rate rounding
    """
    params = {
        "date": "2026-01-02",
        "providers": "ECB",
    }

    eur_usd_response = client.get_rate("EUR", "USD", params=params)
    usd_gbp_response = client.get_rate("USD", "GBP", params=params)
    eur_gbp_response = client.get_rate("EUR", "GBP", params=params)

    assert eur_usd_response.status_code == 200
    assert usd_gbp_response.status_code == 200
    assert eur_gbp_response.status_code == 200

    eur_usd = eur_usd_response.json()
    usd_gbp = usd_gbp_response.json()
    eur_gbp = eur_gbp_response.json()

    assert eur_usd["base"] == "EUR"
    assert eur_usd["quote"] == "USD"
    assert eur_usd["date"] == "2026-01-02"

    assert usd_gbp["base"] == "USD"
    assert usd_gbp["quote"] == "GBP"
    assert usd_gbp["date"] == "2026-01-02"

    assert eur_gbp["base"] == "EUR"
    assert eur_gbp["quote"] == "GBP"
    assert eur_gbp["date"] == "2026-01-02"

    calculated_eur_gbp = eur_usd["rate"] * usd_gbp["rate"]

    assert isclose(
        calculated_eur_gbp,
        eur_gbp["rate"],
        rel_tol=CROSS_RATE_REL_TOLERANCE,
        abs_tol=0.0,
    )