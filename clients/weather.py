from clients.http import get_with_retry


def get_weather(city: str) -> dict:
    """Получает погоду по названию города."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {"name": city, "count": 1, "language": "ru", "format": "json"}

    geo_response = get_with_retry(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise ValueError(f"Город '{city}' не найден")

    location = geo_data["results"][0]
    lat, lon = location["latitude"], location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code",
        "timezone": "auto"
    }

    weather_response = get_with_retry(weather_url, params=weather_params)
    weather_data = weather_response.json()

    current = weather_data.get("current")
    if not current:
        raise ValueError("Не удалось получить данные о погоде")

    weather_codes = {
        0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
        45: "fog", 48: "depositing rime fog", 51: "light drizzle", 53: "moderate drizzle",
        55: "dense drizzle", 61: "slight rain", 63: "moderate rain", 65: "heavy rain",
        71: "slight snow", 73: "moderate snow", 75: "heavy snow", 95: "thunderstorm"
    }

    return {
        "temp_c": current["temperature_2m"],
        "description": weather_codes.get(current["weather_code"], "unknown")
    }