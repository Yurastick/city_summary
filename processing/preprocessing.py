def add_warm_clothes_flag(temp_c: float) -> bool:
    """Если температура < 0, нужно одеться тепло."""
    return temp_c < 0


def add_expensive_flag(rate: float) -> bool:
    """Если курс > 100, он считается дорогим."""
    return rate > 100


def process_weather(weather_data: dict) -> dict:
    """Добавляет флаг warm_clothes к данным о погоде."""
    temp_c = weather_data["temp_c"]
    return {
        **weather_data,
        "warm_clothes": add_warm_clothes_flag(temp_c)
    }


def process_rate(rate_data: dict) -> dict:
    """Добавляет флаг expensive к данным о курсе."""
    rate = rate_data["rate_to_rub"]
    return {
        **rate_data,
        "expensive": add_expensive_flag(rate)
    }