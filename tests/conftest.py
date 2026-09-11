import os

import pytest

from frankfurter_qa.client import FrankfurterClient


@pytest.fixture(scope="session")
def client():
    base_url = os.getenv("FRANKFURTER_BASE_URL")

    api_client = (
        FrankfurterClient(base_url=base_url)
        if base_url
        else FrankfurterClient()
    )

    yield api_client

    api_client.close()