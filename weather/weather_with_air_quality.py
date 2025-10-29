"""
title: Open-Meteo Weather & Air Quality Tool
author: Avesed
version: 1.1
description: Get weather forecasts and air quality data
"""

import requests
from typing import Optional
from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        pass

    def get_current_weather(self, latitude: float, longitude: float) -> str:
        """
        Get current weather and air quality for a specified location

        Parameters:
        - latitude: Latitude coordinate (-90 to 90)
        - longitude: Longitude coordinate (-180 to 180)

        Returns: Current weather and air quality information
        """

        # Weather data parameters
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "current": [
                "temperature_2m",
                "apparent_temperature",
                "wind_speed_10m",
                "precipitation",
                "weather_code",
                "is_day",
            ],
        }

        # Air quality parameters
        air_params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "current": ["us_aqi", "pm10", "pm2_5", "carbon_monoxide"],
            "domains": "cams_global",
        }

        try:
            # Request weather data
            weather_response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params=weather_params,
                timeout=10,
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            # Request air quality data
            air_response = requests.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params=air_params,
                timeout=10,
            )
            air_response.raise_for_status()
            air_data = air_response.json()

            # Assemble results
            result = f"Location: Latitude {latitude}, Longitude {longitude}\n"
            result += f"Timezone: {weather_data.get('timezone', 'N/A')}\n\n"

            # Weather information
            if "current" in weather_data:
                current = weather_data["current"]
                weather_desc = self._get_weather_description(
                    current.get("weather_code", 0)
                )
                result += "Current Weather\n"
                result += f"  - Time: {current.get('time', 'N/A')}\n"
                result += f"  - Condition: {weather_desc}\n"
                result += f"  - Temperature: {current.get('temperature_2m', 'N/A')}°C\n"
                result += (
                    f"  - Feels Like: {current.get('apparent_temperature', 'N/A')}°C\n"
                )
                result += (
                    f"  - Wind Speed: {current.get('wind_speed_10m', 'N/A')} km/h\n"
                )
                result += (
                    f"  - Precipitation: {current.get('precipitation', 'N/A')} mm\n"
                )
                result += f"  - Day/Night: {'Day' if current.get('is_day') == 1 else 'Night'}\n\n"

            # Air quality information
            if "current" in air_data:
                current = air_data["current"]
                aqi = current.get("us_aqi", "N/A")
                aqi_level = self._get_aqi_level(aqi)

                result += "Current Air Quality\n"
                result += f"  - US AQI: {aqi} ({aqi_level})\n"
                result += f"  - PM10: {current.get('pm10', 'N/A')} μg/m³\n"
                result += f"  - PM2.5: {current.get('pm2_5', 'N/A')} μg/m³\n"
                result += f"  - Carbon Monoxide: {current.get('carbon_monoxide', 'N/A')} μg/m³\n"

            return result

        except requests.exceptions.RequestException as e:
            return f"Failed to retrieve data: {str(e)}"

    def get_daily_forecast(
        self, latitude: float, longitude: float, days: int = 7
    ) -> str:
        """
        Get daily weather forecast for a specified location

        Parameters:
        - latitude: Latitude coordinate (-90 to 90)
        - longitude: Longitude coordinate (-180 to 180)
        - days: Number of forecast days (1-16 days), default 7

        Returns: Daily weather forecast information
        """

        days = max(1, min(16, days))

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "forecast_days": days,
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "sunrise",
                "sunset",
                "wind_speed_10m_max",
                "precipitation_sum",
                "precipitation_probability_max",
            ],
        }

        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast", params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            result = f"Location: Latitude {latitude}, Longitude {longitude}\n"
            result += f"Timezone: {data.get('timezone', 'N/A')}\n\n"

            if "daily" in data:
                daily = data["daily"]
                result += f"{days}-Day Forecast\n\n"

                times = daily.get("time", [])
                for i in range(len(times)):
                    date = times[i]
                    weather_code = (
                        daily.get("weather_code", [])[i]
                        if i < len(daily.get("weather_code", []))
                        else 0
                    )
                    temp_max = (
                        daily.get("temperature_2m_max", [])[i]
                        if i < len(daily.get("temperature_2m_max", []))
                        else "N/A"
                    )
                    temp_min = (
                        daily.get("temperature_2m_min", [])[i]
                        if i < len(daily.get("temperature_2m_min", []))
                        else "N/A"
                    )
                    apparent_max = (
                        daily.get("apparent_temperature_max", [])[i]
                        if i < len(daily.get("apparent_temperature_max", []))
                        else "N/A"
                    )
                    apparent_min = (
                        daily.get("apparent_temperature_min", [])[i]
                        if i < len(daily.get("apparent_temperature_min", []))
                        else "N/A"
                    )
                    sunrise = (
                        daily.get("sunrise", [])[i]
                        if i < len(daily.get("sunrise", []))
                        else "N/A"
                    )
                    sunset = (
                        daily.get("sunset", [])[i]
                        if i < len(daily.get("sunset", []))
                        else "N/A"
                    )
                    wind_max = (
                        daily.get("wind_speed_10m_max", [])[i]
                        if i < len(daily.get("wind_speed_10m_max", []))
                        else "N/A"
                    )
                    precip_sum = (
                        daily.get("precipitation_sum", [])[i]
                        if i < len(daily.get("precipitation_sum", []))
                        else "N/A"
                    )
                    precip_prob = (
                        daily.get("precipitation_probability_max", [])[i]
                        if i < len(daily.get("precipitation_probability_max", []))
                        else "N/A"
                    )

                    weather_desc = self._get_weather_description(weather_code)

                    result += f"[{date}]\n"
                    result += f"  Condition: {weather_desc}\n"
                    result += f"  Temperature: {temp_min}°C ~ {temp_max}°C\n"
                    result += f"  Feels Like: {apparent_min}°C ~ {apparent_max}°C\n"
                    result += f"  Max Wind Speed: {wind_max} km/h\n"
                    result += f"  Precipitation: {precip_sum} mm (Probability: {precip_prob}%)\n"
                    result += f"  Sunrise: {sunrise} | Sunset: {sunset}\n\n"

            return result

        except requests.exceptions.RequestException as e:
            return f"Failed to retrieve daily forecast: {str(e)}"

    def get_hourly_forecast(
        self, latitude: float, longitude: float, hours: int = 24
    ) -> str:
        """
        Get hourly weather forecast and air quality for a specified location

        Parameters:
        - latitude: Latitude coordinate (-90 to 90)
        - longitude: Longitude coordinate (-180 to 180)
        - hours: Number of forecast hours (1-168 hours), default 24

        Returns: Hourly weather forecast and air quality information
        """

        hours = max(1, min(168, hours))

        # Weather forecast parameters
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "forecast_days": (hours // 24) + 1,
            "hourly": [
                "temperature_2m",
                "apparent_temperature",
                "precipitation",
                "precipitation_probability",
                "wind_speed_10m",
                "uv_index",
            ],
        }

        # Air quality parameters
        air_params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "forecast_days": (hours // 24) + 1,
            "hourly": ["us_aqi", "pm2_5"],
            "domains": "cams_global",
        }

        try:
            # Get weather data
            weather_response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params=weather_params,
                timeout=10,
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            # Get air quality data
            air_response = requests.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params=air_params,
                timeout=10,
            )
            air_response.raise_for_status()
            air_data = air_response.json()

            result = f"Location: Latitude {latitude}, Longitude {longitude}\n"
            result += f"Timezone: {weather_data.get('timezone', 'N/A')}\n\n"
            result += f"{hours}-Hour Forecast\n\n"

            if "hourly" in weather_data:
                weather_hourly = weather_data["hourly"]
                air_hourly = air_data.get("hourly", {})

                times = weather_hourly.get("time", [])
                for i in range(min(hours, len(times))):
                    time = times[i]
                    temp = (
                        weather_hourly.get("temperature_2m", [])[i]
                        if i < len(weather_hourly.get("temperature_2m", []))
                        else "N/A"
                    )
                    apparent = (
                        weather_hourly.get("apparent_temperature", [])[i]
                        if i < len(weather_hourly.get("apparent_temperature", []))
                        else "N/A"
                    )
                    precip = (
                        weather_hourly.get("precipitation", [])[i]
                        if i < len(weather_hourly.get("precipitation", []))
                        else "N/A"
                    )
                    wind = (
                        weather_hourly.get("wind_speed_10m", [])[i]
                        if i < len(weather_hourly.get("wind_speed_10m", []))
                        else "N/A"
                    )
                    uv = (
                        weather_hourly.get("uv_index", [])[i]
                        if i < len(weather_hourly.get("uv_index", []))
                        else "N/A"
                    )

                    # Air quality data
                    aqi = (
                        air_hourly.get("us_aqi", [])[i]
                        if i < len(air_hourly.get("us_aqi", []))
                        else "N/A"
                    )
                    pm25 = (
                        air_hourly.get("pm2_5", [])[i]
                        if i < len(air_hourly.get("pm2_5", []))
                        else "N/A"
                    )
                    aqi_level = self._get_aqi_level(aqi)

                    result += f"{time}: {temp}°C (Feels {apparent}°C), Wind {wind} km/h, Precip {precip} mm, UV {uv}, AQI {aqi} ({aqi_level}), PM2.5 {pm25} μg/m³\n"

            return result

        except requests.exceptions.RequestException as e:
            return f"Failed to retrieve hourly forecast: {str(e)}"

    def _get_weather_description(self, code: int) -> str:
        """Convert weather code to description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail",
        }
        return weather_codes.get(code, f"Unknown weather (code: {code})")

    def _get_aqi_level(self, aqi) -> str:
        """Get air quality level based on AQI value"""
        try:
            aqi_value = float(aqi)
            if aqi_value <= 50:
                return "Good"
            elif aqi_value <= 100:
                return "Moderate"
            elif aqi_value <= 150:
                return "Unhealthy for Sensitive Groups"
            elif aqi_value <= 200:
                return "Unhealthy"
            elif aqi_value <= 300:
                return "Very Unhealthy"
            else:
                return "Hazardous"
        except (ValueError, TypeError):
            return "Unknown"
