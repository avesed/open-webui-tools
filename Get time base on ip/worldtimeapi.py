"""
title: Get time based on IP
author: Avesed
description: Get current time information based on IP address using API by worldtimeapi.org
version: 0.2.0
"""

import requests
from datetime import datetime


class Tools:
    def __init__(self):
        self.base_url = "http://worldtimeapi.org/api"
        self.weekdays = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
        }

    def get_time_by_ip(self) -> str:
        """
        Get current time information based on the requester's IP address.

        :return: Current time in natural language format
        """
        try:
            response = requests.get(f"{self.base_url}/ip", timeout=10)
            response.raise_for_status()
            data = response.json()

            # Get timezone
            timezone = data.get("timezone", "N/A")

            # Parse datetime
            datetime_str = data.get("datetime", "")
            dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))

            # Get weekday
            day_of_week = data.get("day_of_week", 0)
            weekday = self.weekdays.get(day_of_week, "N/A")

            # Format time with AM/PM
            time_str = dt.strftime("%I:%M:%S %p")
            date_str = dt.strftime("%B %d, %Y")

            result = f"It is currently {weekday}, {date_str}, {time_str} in {timezone} timezone"

            return result

        except Exception as e:
            return f"Failed to get time information: {str(e)}"
