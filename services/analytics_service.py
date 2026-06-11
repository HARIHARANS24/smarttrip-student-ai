import pandas as pd
from database.db import get_db_session
from database.models import ExpenseLog, BudgetPlan
from services.gemini_service import GeminiService
from utils.prompts import INSIGHTS_PROMPT
from utils.validators import InsightModel
import json

class AnalyticsService:
    def __init__(self):
        self.gemini = GeminiService()

    def get_user_expenses_df(self, user_id: int) -> pd.DataFrame:
        """Returns a Pandas DataFrame of the user's expenses."""
        db = get_db_session()
        try:
            expenses = db.query(ExpenseLog).filter(ExpenseLog.user_id == user_id).all()
            if not expenses:
                return pd.DataFrame()
                
            data = [{
                "id": e.id,
                "category": e.category,
                "amount": e.amount,
                "date": e.expense_date,
                "description": e.description
            } for e in expenses]
            
            return pd.DataFrame(data)
        finally:
            db.close()

    def generate_ai_insights(self, user_id: int) -> dict:
        """Generates AI insights based on the user's expenses and budgets."""
        db = get_db_session()
        try:
            # Gather data
            expenses = db.query(ExpenseLog).filter(ExpenseLog.user_id == user_id).all()
            budgets = db.query(BudgetPlan).filter(BudgetPlan.user_id == user_id).all()
            
            exp_data = [{"category": e.category, "amount": e.amount} for e in expenses]
            bud_data = [{"destination": b.destination, "total": b.total_estimated_budget} for b in budgets]
            
            if not exp_data:
                return {"message": "Not enough data to generate insights."}
            
            # Format Prompt
            prompt = INSIGHTS_PROMPT.format(
                expenses=json.dumps(exp_data),
                budgets=json.dumps(bud_data)
            )
            
            # Generate insights
            json_response = self.gemini.generate_json_structured(prompt)
            validated_data = InsightModel(**json_response).model_dump()
            
            return validated_data
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return {"error": str(e)}
        finally:
            db.close()
