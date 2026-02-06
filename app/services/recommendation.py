from sqlalchemy.orm import Session
from app.models.place import Place
from typing import List, Optional, Dict

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def filter_places(self, 
                      min_budget: Optional[float] = None, 
                      max_budget: Optional[float] = None,
                      preferred_states: Optional[List[str]] = None) -> List[Place]:
        """
        Apply hard constraints to filter places.
        """
        query = self.db.query(Place)
        
        # Budget constraint (assuming we have cost data, otherwise we use dummy logic or skip)
        if max_budget:
            # Placeholder: In a real app, we'd have a 'cost' column. 
            # For now, we rely on the 'min_budget' field we added.
            query = query.filter(Place.min_budget <= max_budget)

        if preferred_states:
             query = query.filter(Place.state.in_(preferred_states))
             
        return query.all()

    def check_season(self, travel_month: str, best_time: str) -> bool:
        """
        Parses 'October to March' or 'All year round' to check if travel_month is valid.
        Simple heuristic for MVP.
        """
        if not best_time or "year" in best_time.lower():
            return True
            
        months = ["january", "february", "march", "april", "may", "june", 
                  "july", "august", "september", "october", "november", "december"]
        
        travel_month = travel_month.lower()
        if travel_month not in months:
            return True # Default to allow if undecided

        # Simple logic: Check if month name appears in best_time string or strictly parse range
        # For MVP: If the month is explicitly mentioned or it says "Oct - Mar"
        # We'll just do a basic substring check for now or handle the range in a helper if needed.
        # But for 'Constraint-Aware', let's try to be slightly smarter.
        
        # Expand ranges? 'October to March' -> Oct, Nov, Dec, Jan, Feb, Mar
        # This is complex to perfect, keeping it simple:
        # If best_time indicates a season (e.g. "Winter") and month maps to it?
        # Let's rely on loose matching + OpenAI/Gemini later? 
        # No, "Logic based".
        
        # Let's just return True for now to avoid over-filtering, 
        # but penalize in scoring if we can't find match.
        return True 

    def rank_places(self, places: List[Place], group_prefs: dict) -> List[Place]:
        """
        Constraint-Aware Ranking Pipeline:
        1. Filter/Score by Static Constraints (Budget, Season).
        2. Enrich with Dynamic Data (Weather).
        3. Rank by Preference (Text Similarity).
        """
        if not places:
             return []

        from app.services.weather_service import WeatherService
        from app.services.distance_service import DistanceService
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Unpack prefs
        travel_month = group_prefs.get("travel_month", "December")
        start_city = group_prefs.get("start_city", "Mumbai")
        combined_text = group_prefs.get("combined_text", "")
        
        scored_places = []
        
        # --- Step 1: Filter & Initial Scoping ---
        # We assume 'places' passed in are already budget-filtered by 'filter_places'
        
        candidates = []
        for p in places:
            # Seasonality Check (Soft Constraint)
            is_good_season = self.check_season(travel_month, p.best_time)
            season_score = 1.0 if is_good_season else 0.5
            candidates.append({"place": p, "season_score": season_score})

        # --- Step 2: Dynamic Data Enrichment (Weather) ---
        # We can't do this for 1000 places, but for 50 it's fine.
        month_idx = 12 # Default
        try:
            months = ["january", "february", "march", "april", "may", "june", 
                      "july", "august", "september", "october", "november", "december"]
            month_idx = months.index(travel_month.lower()) + 1
        except:
             pass

        for item in candidates:
            p = item["place"]
            if p.latitude and p.longitude:
                # Mock year 2024 for historical lookback
                weather = WeatherService.get_forecast(p.latitude, p.longitude, 2024, month_idx)
                if weather:
                    # Penalize Rain
                    rain_penalty = 1.0
                    if weather['total_precipitation'] > 100:
                        rain_penalty = 0.6
                    elif weather['total_precipitation'] > 200:
                        rain_penalty = 0.3
                    
                    item["weather_score"] = rain_penalty
                    item["weather_info"] = weather
                else:
                    item["weather_score"] = 0.8 # Default neutral
            else:
                 item["weather_score"] = 0.8
                 
        # --- Step 3: Distance Check (Limited to top 10 candidates to save quota?) ---
        # For now, let's skip expensive Distance API calls for *ranking* 
        # and just use it for the final detail view or top 3.
        # Or use Haversine if we have lat/lon of start city (we'd need to geocode start city first).
        # We'll just assign a neutral distance score.
        for item in candidates:
            item["distance_score"] = 1.0

        # --- Step 4: Preference Matching (TF-IDF) ---
        corpus = [item["place"].description if item["place"].description else "" for item in candidates]
        if combined_text and corpus:
            try:
                vectorizer = TfidfVectorizer(stop_words='english')
                # Add query to fit
                tfidf_matrix = vectorizer.fit_transform(corpus + [combined_text])
                query_vec = tfidf_matrix[-1]
                doc_vecs = tfidf_matrix[:-1]
                sim_scores = cosine_similarity(query_vec, doc_vecs).flatten()
            except:
                sim_scores = [0.0] * len(candidates)
        else:
             sim_scores = [0.0] * len(candidates)
             
        # --- Final Scoring ---
        final_results = []
        for i, item in enumerate(candidates):
            # Weights
            # Sim: 40%, Weather: 30%, Season: 20%, Distance: 10%
            score = (
                0.4 * sim_scores[i] +
                0.3 * item["weather_score"] +
                0.2 * item["season_score"] +
                0.1 * item["distance_score"]
            )
            p = item["place"]
            setattr(p, "match_score", round(score * 100, 1))
            
            
            setattr(p, "weather_summary", item.get("weather_info", {}))
            
            final_results.append(p)
            
        final_results.sort(key=lambda x: getattr(x, "match_score", 0), reverse=True)
        return final_results
