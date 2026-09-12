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





@pytest.mark.regression
@pytest.mark.parametrize(
    "endpoint",
    [
        pytest.param("rates", id="rates-invalid-base"),
        pytest.param("single-rate", id="single-rate-invalid-base"),
    ],
)
def test_reg_002_invalid_currency_validation(client, endpoint):
    """
    REG-002  Invalid currency validation

    Endpoints:
        GET /rates?base=XYZ
        GET /rate/XYZ/USD

    Objective:
        Verify that representative endpoints consistently reject
        an unsupported currency code.

    Expected:
        - HTTP 422
        - JSON error object
        - Error message identifies XYZ as an invalid currency
    """
    if endpoint == "rates":
        response = client.get_rates(params={"base": "XYZ"})
    else:
        response = client.get_rate("XYZ", "USD")

    assert response.status_code == 422

    error = response.json()

    assert isinstance(error, dict)
    assert "message" in error
    assert isinstance(error["message"], str)
    assert "invalid currency" in error["message"].lower()
    assert "XYZ" in error["message"]





@pytest.mark.regression
def test_reg_004_time_series_range(client):
    """
    REG-004  Time-series range

    Endpoint:
        GET /rates?from=2026-01-02&to=2026-01-05&quotes=USD

    Objective:
        Verify that the rates endpoint returns only rates inside
        the requested date range and respects the quote filter.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Every returned date is inside the requested range
        - Every returned quote is USD
        - Every rate is numeric and greater than 0
    """
    start_date = date.fromisoformat("2026-01-02")
    end_date = date.fromisoformat("2026-01-05")

    response = client.get_rates(
        params={
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
            "quotes": "USD",
        }
    )

    assert response.status_code == 200

    rates = response.json()

    assert isinstance(rates, list)
    assert rates

    for rate_entry in rates:
        returned_date = date.fromisoformat(rate_entry["date"])

        assert start_date <= returned_date <= end_date
        assert rate_entry["quote"] == "USD"

        assert isinstance(rate_entry["rate"], (int, float))
        assert not isinstance(rate_entry["rate"], bool)
        assert rate_entry["rate"] > 0




@pytest.mark.regression
def test_reg_005_provider_filtering(client):
    """
    REG-005  Provider filtering

    Endpoint:
        GET /rates?providers=ECB&quotes=USD

    Objective:
        Verify that the rates endpoint successfully accepts
        a valid provider filter.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Every returned quote is USD
        - Every rate is numeric and greater than 0
    """
    response = client.get_rates(
        params={
            "providers": "ECB",
            "quotes": "USD",
        }
    )

    assert response.status_code == 200

    rates = response.json()

    assert isinstance(rates, list)
    assert rates

    for rate_entry in rates:
        assert rate_entry["quote"] == "USD"

        assert isinstance(rate_entry["rate"], (int, float))
        assert not isinstance(rate_entry["rate"], bool)
        assert rate_entry["rate"] > 0