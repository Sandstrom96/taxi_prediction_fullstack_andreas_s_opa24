import requests
from urllib.parse import urljoin


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
             "Evning" for 17 - 21
             "Night" for 22-04
    """
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 22:
        return "Evning"
    else:
        return "Night"


def get_day_of_week(day: str):
    """
    Convert a specific day (e.g. "Monday") into a general category.

    Args:
        day (str): Name of the day (e.g. 'Monday', 'Saturday').

    Returns:
        str: 'Weekday' if the day is Monday–Friday,
             'Weekend' if Saturday or Sunday,
             otherwise 'Unknown'.
    """
    if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        return "Weekday"
    elif day in ["Saturday", "Sunday"]:
        return "Weekend"
    else:
        return "Unknown"
