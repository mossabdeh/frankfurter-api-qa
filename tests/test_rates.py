from datetime import date

import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_smk_001_retrieve_latest_rates(client):
    """
    SMK-001  Retrieve latest rates

    Endpoint:
        GET /rates

    Objective:
        Verify that the main rates endpoint is available
        and returns usable rate data.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Each rate contains date, base, quote, and rate
        - Rate is numeric and greater than 0
        - Date is valid
    """
    response = client.get_rates()

    assert response.status_code == 200

    rates = response.json()

    assert isinstance(rates, list)
    assert rates

    required_fields = {"date", "base", "quote", "rate"}

    for rate_entry in rates:
        assert isinstance(rate_entry, dict)
        assert required_fields.issubset(rate_entry)

        assert isinstance(rate_entry["rate"], (int, float))
        assert not isinstance(rate_entry["rate"], bool)
        assert rate_entry["rate"] > 0

        date.fromisoformat(rate_entry["date"])




@pytest.mark.smoke
@pytest.mark.regression
def test_smk_003_basic_base_quote_filtering(client):
    """
    SMK-003  Basic base/quote filtering

    Endpoint:
        GET /rates?base=USD&quotes=EUR

    Objective:
        Verify that the rates endpoint respects the requested
        base and quote currency filters.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Every returned rate has base USD
        - Every returned rate has quote EUR
        - Every rate is numeric and greater than 0
    """
    response = client.get_rates(
        params={
            "base": "USD",
            "quotes": "EUR",
        }
    )

    assert response.status_code == 200

    rates = response.json()

    assert isinstance(rates, list)
    assert rates

    for rate_entry in rates:
        assert rate_entry["base"] == "USD"
        assert rate_entry["quote"] == "EUR"

        assert isinstance(rate_entry["rate"], (int, float))
        assert not isinstance(rate_entry["rate"], bool)
        assert rate_entry["rate"] > 0




@pytest.mark.regression
def test_reg_001_multiple_quote_filtering(client):
    """
    REG-001  Multiple quote filtering

    Endpoint:
        GET /rates?base=EUR&quotes=USD,GBP

    Objective:
        Verify that the rates endpoint correctly handles
        multiple requested quote currencies.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Every returned rate has base EUR
        - Only USD and GBP quotes are returned
        - Both USD and GBP are present
        - Every rate is numeric and greater than 0
    """
    expected_quotes = {"USD", "GBP"}

    response = client.get_rates(
        params={
            "base": "EUR",
            "quotes": "USD,GBP",
        }
    )

    assert response.status_code == 200

    rates = response.json()

    assert isinstance(rates, list)
    assert rates

    returned_quotes = {rate_entry["quote"] for rate_entry in rates}

    assert returned_quotes == expected_quotes

    for rate_entry in rates:
        assert rate_entry["base"] == "EUR"

        assert isinstance(rate_entry["rate"], (int, float))
        assert not isinstance(rate_entry["rate"], bool)
        assert rate_entry["rate"] > 0