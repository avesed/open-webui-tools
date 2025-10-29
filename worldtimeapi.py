import requests
from typing import Optional


class Tools:
    def __init__(self):
        self.base_url = "http://worldtimeapi.org/api"

    def get_time_by_ip(self) -> str:
        """
        Get current time information based on the requester's IP address.
        
        :return: Current time and timezone information
        """
        try:
            response = requests.get(f"{self.base_url}/ip", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = f"""
            Timezone Information:
            - Timezone: {data.get('timezone', 'N/A')}
            - Current Time: {data.get('datetime', 'N/A')}
            - UTC Offset: {data.get('utc_offset', 'N/A')}
            - Day of Week: {data.get('day_of_week', 'N/A')}
            - Daylight Saving Time: {'Yes' if data.get('dst') else 'No'}
            """
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Failed to get time information: {str(e)}"
