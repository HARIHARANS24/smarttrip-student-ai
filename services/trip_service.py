import json
from services.gemini_service import GeminiService
from utils.prompts import DESTINATION_RECOMMENDER_PROMPT, TRIP_PLANNER_PROMPT
from utils.validators import DestinationRecommendationModel, TripPlanModel
from database.db import get_db_session
from database.models import DestinationRecommendation, TripPlan

class TripService:
    def __init__(self):
        self.gemini = GeminiService()

    def recommend_destinations(self, user_id: int, user_data: dict) -> list:
        """Generates destination recommendations based on user profile and assessment."""
        prompt = DESTINATION_RECOMMENDER_PROMPT.format(**user_data)
        
        try:
            json_response = self.gemini.generate_json_structured(prompt)
            
            # Validate with Pydantic
            validated_data = [DestinationRecommendationModel(**item).model_dump() for item in json_response]
            
            # Save to DB
            db = get_db_session()
            try:
                new_rec = DestinationRecommendation(
                    user_id=user_id,
                    recommendations_json=json.dumps(validated_data)
                )
                db.add(new_rec)
                db.commit()
            except Exception as e:
                print(f"Error saving recommendations to DB: {e}")
                db.rollback()
            finally:
                db.close()
                
            return validated_data
        except Exception as e:
            print(f"Error in recommend_destinations: {e}")
            raise e

    def generate_trip_plan(self, user_id: int, trip_data: dict) -> dict:
        """Generates a detailed day-by-day trip plan."""
        prompt = TRIP_PLANNER_PROMPT.format(**trip_data)
        
        try:
            json_response = self.gemini.generate_json_structured(prompt)
            
            # Validate with Pydantic
            validated_data = TripPlanModel(**json_response).model_dump()
            
            # Save to DB
            db = get_db_session()
            try:
                new_plan = TripPlan(
                    user_id=user_id,
                    destination=trip_data.get("destination", "Unknown"),
                    itinerary_json=json.dumps(validated_data)
                )
                db.add(new_plan)
                db.commit()
            except Exception as e:
                print(f"Error saving trip plan to DB: {e}")
                db.rollback()
            finally:
                db.close()
                
            return validated_data
        except Exception as e:
            print(f"Error in generate_trip_plan: {e}")
            raise e
