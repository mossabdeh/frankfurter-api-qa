from datetime import date

import pytest


@pytest.mark.regression
def test_reg_007_currency_collection_contract(client):
    """
    REG-007  Currency collection contract

    Endpoint:
        GET /currencies

    Objective:
        Verify that the currencies endpoint returns a non-empty
        collection with the expected currency metadata contract.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Every currency contains:
          iso_code, iso_numeric, name, symbol, start_date, end_date
        - Metadata fields have the expected types
        - Date fields contain valid dates
    """
    response = client.get_currencies()

    assert response.status_code == 200

    currencies = response.json()

    assert isinstance(currencies, list)
    assert currencies

    required_fields = {
        "iso_code",
        "iso_numeric",
        "name",
        "symbol",
        "start_date",
        "end_date",
    }

    for currency in currencies:
        assert isinstance(currency, dict)
        assert required_fields.issubset(currency)

        assert isinstance(currency["iso_code"], str)
        assert isinstance(currency["iso_numeric"], str)
        assert isinstance(currency["name"], str)
        assert isinstance(currency["symbol"], str)
        assert isinstance(currency["start_date"], str)
        assert isinstance(currency["end_date"], str)

        date.fromisoformat(currency["start_date"])
        date.fromisoformat(currency["end_date"])