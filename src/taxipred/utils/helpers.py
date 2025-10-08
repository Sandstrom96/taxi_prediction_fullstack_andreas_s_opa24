import requests
from urllib.parse import urljoin
from datetime import datetime


def read_api_endpoint(endpoint="/", base_url="http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.get(url)

    return response


def post_api_endpoint(payload, endpoint="/", base_url="http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.post(url=url, json=payload)

    return response


def get_time_of_day(hour: int):
    """
    Convert an hour (0-23) into a general time of day.

    Args:
        hour (int): The hour of the day in a 24-hour format (0-23)

    Returns:
        str: "Morning" for 05-11
             "Afternoon" for 12 - 16
             "Evening" for 17 - 21
             "Night" for 22-04
    """
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 22:
        return "Evening"
    else:
        return "Night"


def get_day_of_week(date: datetime.date):
    """
    Convert a datetime.date object into a general category: Weekday or Weekend.

    Args:
        date (datetime.date): The selected date.

    Returns:
        str: 'Weekday' if the date is Monday–Friday,
             'Weekend' if the date is Saturday or Sunday.
    """
    return "Weekend" if date.weekday() >= 5 else "Weekday"


def calculate_base_fare(df, time_of_day, day_of_week):
    result = (
        df.groupby(["Time_of_Day", "Day_of_Week"])["Base_Fare"].mean().reset_index()
    )

    value = result.loc[
        (result["Time_of_Day"] == time_of_day) & (result["Day_of_Week"] == day_of_week),
        "Base_Fare",
    ]

    return value.values[0] if not value.empty else None
