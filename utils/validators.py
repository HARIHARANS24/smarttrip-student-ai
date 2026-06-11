from pydantic import BaseModel, Field
from typing import List

# Validators for Gemini JSON responses

class DestinationRecommendationModel(BaseModel):
    Destination: str
    EstimatedCost: str
    BestTime: str
    Attractions: List[str]
    Why: str

class DayItineraryModel(BaseModel):
    Day: int
    Activities: List[str]
    Meals: List[str]
    Transportation: str
    EstimatedCost: str
    Tips: str

class TripPlanModel(BaseModel):
    Destination: str
    TotalEstimatedCost: str
    Itinerary: List[DayItineraryModel]

class BudgetPlanModel(BaseModel):
    TotalEstimatedBudget: float
    AccommodationCost: float
    TransportationCost: float
    FoodCost: float
    ActivitiesCost: float
    EmergencyFund: float
    Tips: List[str]

class InsightModel(BaseModel):
    TotalSpent: float
    TopCategory: str
    Suggestions: List[str]
    SavingsPotential: str
