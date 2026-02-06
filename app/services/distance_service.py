import requests
from app.config import settings
from typing import Optional

class DistanceService:
    @staticmethod
    def get_distance_matrix(origins: list, destinations: list):
        """
        Calculates distance and duration between origins and destinations using Google Maps API.
        origins: list of strings (e.g. ["Mumbai", "Delhi"])
        destinations: list of strings (e.g. ["Goa", "Manali"])
        """
        if not settings.GOOGLE_MAPS_API_KEY:
            print("WARNING: Google Maps API Key not set.")
            return None

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        
        # Prepare pipe-separated strings
        origins_str = "|".join(origins)
        destinations_str = "|".join(destinations)
        
        params = {
            "origins": origins_str,
            "destinations": destinations_str,
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] != 'OK':
                print(f"Google Maps API Error: {data.get('error_message', data['status'])}")
                return None
                
            return data
        except Exception as e:
            print(f"Distance Function Error: {e}")
            return None

    @staticmethod
    def is_reachable(origin: str, destination: str, max_hours: int) -> bool:
        """
        Simple check if a destination is reachable within max_hours.
        """
        data = DistanceService.get_distance_matrix([origin], [destination])
        if not data:
            return False # Fail safe
            
        try:
            element = data['rows'][0]['elements'][0]
            if element['status'] != 'OK':
                return False
                
            duration_text = element['duration']['text'] # e.g. "5 hours 10 mins"
            duration_value_seconds = element['duration']['value']
            
            hours = duration_value_seconds / 3600
            return hours <= max_hours
        except Exception:
            return False
