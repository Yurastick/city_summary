import argparse
import sys

import requests

from processing.service import build_city_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Сводка по городу: погода и курс валют")
    parser.add_argument("--city", required=True, help="Название города")
    parser.add_argument("--currency", default="USD", help="ISO-код валюты (по умолчанию USD)")

    args = parser.parse_args()

    try:
        summary = build_city_summary(args.city, args.currency)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(3)
    except requests.RequestException as e:
        print(f"Ошибка внешнего сервиса: {e}", file=sys.stderr)
        sys.exit(4)

    weather = summary["weather"]
    rates = summary["rates"]

    print(f"Город: {summary['city']}")
    print(f"Погода: {weather['temp_c']}°C, {weather['description']}")
    print(f"Тёплая одежда: {'да' if weather['warm_clothes'] else 'нет'}")
    print(f"{rates['currency']}→RUB: {rates['rate_to_rub']:.2f}")
    print(f"Дорогой курс: {'да' if rates['expensive'] else 'нет'}")


if __name__ == "__main__":
    main()