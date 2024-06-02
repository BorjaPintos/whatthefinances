import locale
import traceback
from datetime import datetime, date
from typing import List

from loguru import logger

try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except Exception:
    traceback.print_exc()
    logger.warning("No ha sido posible establecer el lenguaje local")

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

def apply_locale_list(list_value) -> List[int]:
    elements = []
    if isinstance(list_value, list):
        for element in list_value:
            elements.append(element)
        return elements
    if isinstance(list_value, str):
        if list_value == "":
            return []
        else:
            return apply_locale_list(list_value.split(","))

def apply_locale_list_int(list_value) -> List[int]:
    elements = []
    if isinstance(list_value, list):
        for element in list_value:
            elements.append(apply_locale_int(element))
        return elements
    if isinstance(list_value, str):
        if list_value == "":
            return []
        else:
            return apply_locale_list_int(list_value.split(","))




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
