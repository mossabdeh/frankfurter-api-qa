import pytest


@pytest.mark.regression
def test_reg_009_provider_collection_contract(client):
    """
    REG-009  Provider collection contract

    Endpoint:
        GET /providers

    Objective:
        Verify that the providers endpoint returns a non-empty
        collection with the expected provider metadata contract.

    Expected:
        - HTTP 200
        - JSON array
        - Response is not empty
        - Every provider contains the required metadata fields
        - Metadata fields have the expected types
        - country_code and rate_type may be null
    """
    response = client.get_providers()

    assert response.status_code == 200

    providers = response.json()

    assert isinstance(providers, list)
    assert providers

    required_fields = {
        "key",
        "name",
        "country_code",
        "rate_type",
        "pivot_currency",
        "start_date",
        "end_date",
        "currencies",
    }

    for provider in providers:
        assert isinstance(provider, dict)
        assert required_fields.issubset(provider)

        assert isinstance(provider["key"], str)
        assert isinstance(provider["name"], str)

        assert isinstance(provider["country_code"], (str, type(None)))
        assert isinstance(provider["rate_type"], (str, type(None)))

        assert isinstance(provider["pivot_currency"], str)
        assert isinstance(provider["start_date"], str)
        assert isinstance(provider["end_date"], str)

        assert isinstance(provider["currencies"], list)
        assert all(
            isinstance(currency, str)
            for currency in provider["currencies"]
        )