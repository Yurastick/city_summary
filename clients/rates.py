from clients.http import get_with_retry


def get_rate(currency: str) -> float:
    """Получает курс валюты к RUB."""
    url = f"https://api.frankfurter.dev/v2/rate/{currency}/RUB"

    response = get_with_retry(url)
    data = response.json()

    if "rate" not in data:
        raise ValueError(f"Курс для валюты '{currency}' не найден")

    return float(data["rate"])