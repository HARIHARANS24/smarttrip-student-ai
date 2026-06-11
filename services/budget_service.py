import json
from services.gemini_service import GeminiService
from utils.prompts import BUDGET_PLANNER_PROMPT
from utils.validators import BudgetPlanModel
from database.db import get_db_session
from database.models import BudgetPlan

class BudgetService:
    def __init__(self):
        self.gemini = GeminiService()

    def generate_budget_plan(self, user_id: int, budget_data: dict) -> dict:
        """Generates a detailed budget breakdown for a trip."""
        prompt = BUDGET_PLANNER_PROMPT.format(**budget_data)
        
        try:
            json_response = self.gemini.generate_json_structured(prompt)
            
            # Validate
            validated_data = BudgetPlanModel(**json_response).model_dump()
            
            # Save to DB
            db = get_db_session()
            try:
                new_budget = BudgetPlan(
                    user_id=user_id,
                    destination=budget_data.get("destination", "Unknown"),
                    total_estimated_budget=validated_data["TotalEstimatedBudget"],
                    accommodation_cost=validated_data.get("AccommodationCost", 0),
                    transportation_cost=validated_data.get("TransportationCost", 0),
                    food_cost=validated_data.get("FoodCost", 0),
                    activities_cost=validated_data.get("ActivitiesCost", 0),
                    emergency_fund=validated_data.get("EmergencyFund", 0),
                    details_json=json.dumps(validated_data)
                )
                db.add(new_budget)
                db.commit()
            except Exception as e:
                print(f"Error saving budget plan to DB: {e}")
                db.rollback()
            finally:
                db.close()
                
            return validated_data
        except Exception as e:
            print(f"Error in generate_budget_plan: {e}")
            raise e
