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


week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
