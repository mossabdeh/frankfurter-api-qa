import pytest


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