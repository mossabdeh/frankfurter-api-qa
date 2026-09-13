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