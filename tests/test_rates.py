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