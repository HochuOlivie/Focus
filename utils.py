from datetime import datetime
import math


def get_user(message):
    return str(message.from_user.id)


def get_datetime(datetime_str):
    format = "%Y-%m-%d %H:%M:%S.%f"
    try:
        return datetime.strptime(datetime_str, format)
    except ValueError:
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


def get_hour_string(hours, decimal_places, little_decimal_places):
    if hours == 0:
        return "0h"
    if little_decimal_places == 0:
        if hours < 1:
            return "<1h"
    if little_decimal_places == 1:
        if hours < 0.1:
            return "<0.1h"
    if decimal_places == 0:
        return f"{math.floor(hours)}h"
    if decimal_places == 1:
        return f"{truncate(hours, 1)}h"


week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
