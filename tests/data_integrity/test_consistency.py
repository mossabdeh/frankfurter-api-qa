import pytest


@pytest.mark.data_integrity
def test_data_002_cross_endpoint_consistency(client):
    """
    DATA-002  Cross-endpoint consistency

    Endpoints:
        GET /rates?base=EUR&quotes=USD&date=2026-01-02
        GET /rate/EUR/USD?date=2026-01-02

    Objective:
        Verify that the collection and single-rate endpoints
        return consistent data for the same currency pair and date.

    Expected:
        - Both requests return HTTP 200
        - Both responses refer to EUR/USD
        - Both responses use the requested date
        - Both endpoints return the same rate
    """
    rates_response = client.get_rates(
        params={
            "base": "EUR",
            "quotes": "USD",
            "date": "2026-01-02",
        }
    )

    single_rate_response = client.get_rate(
        "EUR",
        "USD",
        params={"date": "2026-01-02"},
    )

    assert rates_response.status_code == 200
    assert single_rate_response.status_code == 200

    rates = rates_response.json()
    single_rate = single_rate_response.json()

    assert isinstance(rates, list)
    assert rates

    assert isinstance(single_rate, dict)

    collection_rate = rates[0]

    assert collection_rate["base"] == "EUR"
    assert collection_rate["quote"] == "USD"
    assert collection_rate["date"] == "2026-01-02"

    assert single_rate["base"] == "EUR"
    assert single_rate["quote"] == "USD"
    assert single_rate["date"] == "2026-01-02"

    assert collection_rate["rate"] == single_rate["rate"]