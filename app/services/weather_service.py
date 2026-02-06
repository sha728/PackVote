import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta

class WeatherService:
    @staticmethod
    def get_forecast(latitude: float, longitude: float, year: int, month: int):
        """
        Fetches historical weather data (as a proxy for forecast if far in future) 
        or forecast if near. For simplicity in this 'planning' context, we might 
        look at historical data for the same month last year.
        
        Using Open-Meteo Archive API for typical weather.
        """
        try:
            # Setup the Open-Meteo API client with cache and retry on error
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)

            # Construct dates. If month is in future, look at last year.
            # Simple logic: start_date = YYYY-MM-01, end_date = YYYY-MM-15
            # If YYYY-MM is > now, use (YYYY-1)-MM
            
            now = datetime.now()
            target_date = datetime(year, month, 1)
            
            if target_date > now:
                fetch_year = year - 1
            else:
                fetch_year = year
                
            start_date = f"{fetch_year}-{month:02d}-01"
            # Get ~15 days
            end_date = f"{fetch_year}-{month:02d}-15"

            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum", "snowfall_sum"]
            }
            
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            
            # Process daily data
            daily = response.Daily()
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
            daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
            
            avg_max_temp = float(daily_temperature_2m_max.mean())
            avg_min_temp = float(daily_temperature_2m_min.mean())
            total_precip = float(daily_precipitation_sum.sum())
            
            return {
                "avg_max_temp": round(avg_max_temp, 1),
                "avg_min_temp": round(avg_min_temp, 1),
                "total_precipitation": round(total_precip, 1),
                "condition_summary": "Rainy" if total_precip > 50 else "Sunny/Cloudy" # Simple heuristic
            }

        except Exception as e:
            print(f"Weather API Error: {e}")
            return None
