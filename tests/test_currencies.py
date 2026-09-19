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
          iso_code, name
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
        
        assert isinstance(currency["name"], str)
        if "iso_numeric" in currency:
            assert isinstance(currency["iso_numeric"], (str, type(None)))
        if "symbol" in currency:
            assert isinstance(currency["symbol"], (str, type(None)))
        if "start_date" in currency:
            assert isinstance(currency["start_date"], (str, type(None)))
            if currency["start_date"] is not None:
                date.fromisoformat(currency["start_date"])
        if "end_date" in currency:
            assert isinstance(currency["end_date"], (str, type(None)))
            if currency["end_date"] is not None:
                date.fromisoformat(currency["end_date"])



@pytest.mark.regression
def test_reg_008_single_currency_metadata(client):
    """
    REG-008  Single currency metadata

    Endpoint:
        GET /currency/DZD

    Objective:
        Verify that the single-currency endpoint returns
        the expected metadata for the requested currency.

    Expected:
        - HTTP 200
        - JSON object
        - Currency code is DZD
        - Required metadata fields are present
        - Metadata fields have the expected types
        - Providers is a list of strings
    """
    response = client.get_currency("DZD")

    assert response.status_code == 200

    currency = response.json()

    assert isinstance(currency, dict)

    required_fields = {
        "iso_code",
        "iso_numeric",
        "name",
        "symbol",
        "start_date",
        "end_date",
        "providers",
    }

    assert required_fields.issubset(currency)

    assert currency["iso_code"] == "DZD"

    assert isinstance(currency["iso_numeric"], str)
    assert isinstance(currency["name"], str)
    assert isinstance(currency["symbol"], str)
    assert isinstance(currency["start_date"], str)
    assert isinstance(currency["end_date"], str)

    assert isinstance(currency["providers"], list)
    assert all(
        isinstance(provider, str)
        for provider in currency["providers"]
    )