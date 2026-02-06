import google.generativeai as genai
from app.config import settings
from typing import Dict

class ItineraryService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    async def generate_itinerary(self, place_name: str, duration: int, preferences: str) -> str:
        if not self.model:
            return "Gemini API Key missing. Cannot generate itinerary."

        prompt = f"""
        Create a {duration}-day travel itinerary for a group visiting {place_name}.
        Group Preferences: {preferences}.
        
        Format the response in Markdown.
        Include:
        - Day-by-day plan
        - Suggested restaurants
        - Estimated budget tips
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating itinerary: {str(e)}"
