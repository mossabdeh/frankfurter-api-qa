from datetime import date

import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_smk_002_retrieve_single_currency_pair_rate(client):
    """
    SMK-002  Retrieve single currency-pair rate

    Endpoint:
        GET /rate/EUR/USD

    Objective:
        Verify that a single currency-pair rate can be retrieved
        successfully with valid rate data.

    Expected:
        - HTTP 200
        - JSON object
        - Base is EUR
        - Quote is USD
        - Rate is numeric and greater than 0
        - Date is valid
    """
    response = client.get_rate("EUR", "USD")

    assert response.status_code == 200

    rate = response.json()

    assert isinstance(rate, dict)

    assert rate["base"] == "EUR"
    assert rate["quote"] == "USD"

    assert isinstance(rate["rate"], (int, float))
    assert not isinstance(rate["rate"], bool)
    assert rate["rate"] > 0

    date.fromisoformat(rate["date"])