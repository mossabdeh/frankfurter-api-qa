from typing import Any

import requests


DEFAULT_BASE_URL = "https://api.frankfurter.dev/v2"
DEFAULT_TIMEOUT = 10


class FrankfurterClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/{path.lstrip('/')}",
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

    def get_rates(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self._get("/rates", params=params, headers=headers)

    def get_rate(
        self,
        base: str,
        quote: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._get(f"/rate/{base}/{quote}", params=params)

    def get_currencies(
        self,
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._get("/currencies", params=params)

    def get_currency(self, code: str) -> requests.Response:
        return self._get(f"/currency/{code}")

    def get_providers(self) -> requests.Response:
        return self._get("/providers")

    def close(self) -> None:
        self.session.close()