import time

import requests
from requests.exceptions import ConnectionError, Timeout


def get_with_retry(
    url: str, params: dict | None = None, retries: int = 2, timeout: int = 10
) -> requests.Response:
    """Выполняет GET-запрос с повторами при временных ошибках."""
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            # Обработка 429 (Too Many Requests) с учетом Retry-After
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    time.sleep(int(retry_after))
                    continue

            # Обработка временных 5xx ошибок
            if response.status_code in (500, 502, 503, 504):
                if attempt < retries:
                    time.sleep(1)
                    continue
                response.raise_for_status()

            response.raise_for_status()
            return response

        except (Timeout, ConnectionError):
            if attempt < retries:
                time.sleep(1)
                continue
            raise

    raise RuntimeError("Не удалось выполнить запрос после всех попыток")
