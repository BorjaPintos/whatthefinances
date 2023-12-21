import locale
from datetime import datetime, date

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')


def apply_locale_float(value) -> float:
    if isinstance(value, int):
        return float(value)
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        if value == "":
            return 0.0
        return locale.atof(value)


def apply_locale_int(value) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        if value == "":
            return 0
        return int(locale.atof(value))


def apply_locale_date(value) -> date:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, '%d/%m/%Y').date()

def apply_locale_datetime(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, '%d/%m/%Y %H:%M')


def apply_locale_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value in ["True", "true"]:
            return True
        else:
            return False
