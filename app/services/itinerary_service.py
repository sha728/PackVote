import google.generativeai as genai
from app.config import settings
import json

class ItineraryService:
    @staticmethod
    def generate_itinerary(destination_name: str, duration: int, group_context: str, weather_summary: str):
        """
        Generates a day-wise itinerary using Gemini.
        """
        if not settings.GEMINI_API_KEY:
             return {"error": "Gemini API Key missing"}
             
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Act as a professional travel planner.
        Create a detailed {duration}-day itinerary for a group trip to {destination_name}.
        
        Context:
        - Group Preferences: {group_context}
        - Current Weather Forecast: {weather_summary}
        
        Constraints:
        - Suggest specific activities suitable for the weather.
        - Include budget tips.
        - Format the response as JSON with keys: "title", "summary", "daily_plan" (list of objects with "day", "activities"), "packing_tips".
        """
        
        try:
            response = model.generate_content(prompt)
            
            text = response.text.replace("```json", "").replace("```", "")
            return json.loads(text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            return {
                "title": f"Trip to {destination_name}", 
                "summary": "AI generation failed, but here is a basic outline.", 
                "daily_plan": [],
                "error": str(e)
            }
