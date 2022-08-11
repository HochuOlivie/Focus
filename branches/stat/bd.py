from datetime import datetime, timedelta
from utils import get_datetime


def agregate_actions_by_date(user, data, actions, date_from, date_to):
    res = {}
    res["total_hours"] = 0
    res["total_points"] = 0
    res["actions"] = {}

    for action in actions:
        res["actions"][action] = {"hours": 0, "points": 0}
        for record in data[user]["records"]:
            if (
                record["action"] == action
                and date_from <= get_datetime(record["date"]).date() <= date_to
            ):
                hours = record["duration"] / 3600
                res["actions"][action]["hours"] += hours
                res["total_hours"] += hours
                if record["category_points"] is not None:
                    res["actions"][action]["points"] += (
                        record["category_points"] * hours
                    )
                    res["total_points"] += record["category_points"] * hours
    return res


def agregate_actions_by_group(user, data, group, date_from, date_to):
    return agregate_actions_by_date(
        user, data, data[user]["groups"][group], date_from, date_to
    )


def agregate_days_by_week(user, data, actions, date_from, date_to):
    res = {}
    res["total_hours"] = 0
    res["total_points"] = 0
    res["days"] = {}

    total_days = (date_to - date_from).days + 1

    for day in range(total_days):
        res["days"][day] = {"hours": 0, "points": 0}
        for record in data[user]["records"]:
            if (
                date_from + timedelta(days=day) == get_datetime(record["date"]).date()
                and record["action"] in actions
            ):
                hours = record["duration"] / 3600
                res["days"][day]["hours"] += hours
                res["total_hours"] += hours
                if record["category_points"] is not None:
                    res["days"][day]["points"] += record["category_points"] * hours
                    res["total_points"] += record["category_points"] * hours
    return res


def agregate_weeks_by_month(user, data, actions, date_from, date_to):
    res = {}
    res["total_hours"] = 0
    res["total_points"] = 0
    res["weeks"] = {}
    total_weeks = (date_to - date_from).days // 7 + 1

    for week in range(total_weeks):
        res["weeks"][week] = {"hours": 0, "points": 0}

        for record in data[user]["records"]:
            till = (
                date_to
                if week == total_weeks - 1
                else date_from + timedelta(days=(week + 1) * 7 - 1)
            )
            if (
                date_from + timedelta(days=week * 7)
                <= get_datetime(record["date"]).date()
                <= till
                and record["action"] in actions
            ):
                print(record)
                hours = record["duration"] / 3600
                res["weeks"][week]["hours"] += hours
                res["total_hours"] += hours
                if record["category_points"] is not None:
                    res["weeks"][week]["points"] += record["category_points"] * hours
                    res["total_points"] += record["category_points"] * hours
    return res
