"""
title: Time and location
author: Avesed
description: Get current time, timezone, IP address, and geographic location information
version: 1.0
requirements: requests
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

    def get_current_time_timezone_ip_location(self) -> str:
        """
        Get current time, timezone, IP address, and geographic location information based on the requester's IP address.

        :return: Current time with timezone, IP address, and location details including city, region, country, latitude and longitude
        """
        try:
            # Get IP address
            try:
                ip_response = requests.get(
                    "https://api.ipify.org?format=json", timeout=5
                )
                ip_address = ip_response.json().get("ip", "Unknown")
            except:
                ip_address = "Unknown"

            # Get location information
            location_info = ""
            if ip_address != "Unknown":
                try:
                    location_response = requests.get(
                        f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,lat,lon",
                        timeout=5,
                    )
                    location_data = location_response.json()

                    if location_data.get("status") == "success":
                        city = location_data.get("city", "Unknown")
                        region = location_data.get("regionName", "Unknown")
                        country = location_data.get("country", "Unknown")
                        lat = location_data.get("lat", "N/A")
                        lon = location_data.get("lon", "N/A")
                        location_info = (
                            f"{city}, {region}, {country} (Lat: {lat}, Lon: {lon})"
                        )
                    else:
                        location_info = "Unknown location"
                except:
                    location_info = "Unknown location"

            # Get time information
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

            result = f"It is currently {weekday}, {date_str}, {time_str} in {timezone} timezone\nLocation: {location_info}\nIP: {ip_address}"

            return result

        except Exception as e:
            return f"Failed to get time information: {str(e)}"
