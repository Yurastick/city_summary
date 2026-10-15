from clients.weather import get_weather
from clients.rates import get_rate
from processing.preprocessing import process_weather, process_rate


def build_city_summary(city: str, currency: str = "USD") -> dict:
    """Собирает сводку по городу: погода + курс валюты."""
    weather_raw = get_weather(city)
    rate_raw = get_rate(currency)

    weather_processed = process_weather(weather_raw)
    rate_processed = process_rate({
        "currency": currency,
        "rate_to_rub": rate_raw
    })

    return {
        "city": city,
        "weather": weather_processed,
        "rates": rate_processed
    }