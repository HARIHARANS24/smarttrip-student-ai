import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Set up SQLite database by default if no DATABASE_URL is provided
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///student_travel_planner.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

Base = declarative_base()

class User(Base):
    """User profile model storing authentication and basic student information."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Academic Info
    university = Column(String(150))
    course = Column(String(150))
    year_of_study = Column(String(50))
    
    # Profile Info
    age = Column(Integer)
    gender = Column(String(20))
    country = Column(String(100))
    preferred_currency = Column(String(10), default="USD")
    
    # Travel Preferences (stored as JSON strings or comma-separated for simplicity in SQLite)
    travel_preferences = Column(Text)  # e.g. "Solo Travel, Group Travel"
    budget_category = Column(String(50)) # e.g. "Budget Traveler", "Moderate", "Premium"
    interests = Column(Text) # e.g. "Adventure, Beaches"
    travel_style = Column(Text) # e.g. "Weekend Trips, Backpacking"
    accommodation_preferences = Column(Text)
    
    # Status
    passport_status = Column(Boolean, default=False)
    visa_requirements = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    assessments = relationship("TravelAssessment", back_populates="user", cascade="all, delete-orphan")
    destinations = relationship("DestinationRecommendation", back_populates="user", cascade="all, delete-orphan")
    trip_plans = relationship("TripPlan", back_populates="user", cascade="all, delete-orphan")
    budget_plans = relationship("BudgetPlan", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("ExpenseLog", back_populates="user", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    saved_destinations = relationship("SavedDestination", back_populates="user", cascade="all, delete-orphan")

class TravelAssessment(Base):
    """Stores detailed travel assessment form responses."""
    __tablename__ = "travel_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    age = Column(Integer)
    country = Column(String(100))
    travel_experience = Column(String(50))
    budget_amount = Column(Float)
    preferred_destinations = Column(Text)
    trip_duration_days = Column(Integer)
    travel_dates = Column(String(100))
    accommodation_preference = Column(String(100))
    transportation_preference = Column(String(100))
    travel_interests = Column(Text)
    passport_availability = Column(Boolean)
    visa_status = Column(String(100))
    travel_companions = Column(String(100))
    food_preferences = Column(Text)
    special_requirements = Column(Text)
    safety_concerns = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="assessments")

class DestinationRecommendation(Base):
    """Stores AI-generated destination recommendations."""
    __tablename__ = "destination_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Storing the JSON response from Gemini as text
    recommendations_json = Column(Text, nullable=False) 
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="destinations")

class SavedDestination(Base):
    """Destinations the user has saved/bookmarked."""
    __tablename__ = "saved_destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_name = Column(String(150), nullable=False)
    details_json = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="saved_destinations")

class TripPlan(Base):
    """Stores AI-generated trip itineraries."""
    __tablename__ = "trip_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination = Column(String(150), nullable=False)
    start_date = Column(String(50))
    end_date = Column(String(50))
    itinerary_json = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="trip_plans")

class BudgetPlan(Base):
    """Stores AI-generated or user-created budget plans."""
    __tablename__ = "budget_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination = Column(String(150), nullable=False)
    
    total_estimated_budget = Column(Float, nullable=False)
    accommodation_cost = Column(Float)
    transportation_cost = Column(Float)
    food_cost = Column(Float)
    activities_cost = Column(Float)
    emergency_fund = Column(Float)
    
    details_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="budget_plans")

class ExpenseLog(Base):
    """Tracks actual travel expenses."""
    __tablename__ = "expense_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=True) # Optional link to a specific trip
    
    category = Column(String(50), nullable=False) # e.g. Accommodation, Food, Transport
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    description = Column(String(255))
    expense_date = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="expenses")
    # if we want a relationship to trip: trip = relationship("TripPlan")

class ChatHistory(Base):
    """Stores conversations with the AI Travel Chatbot."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    role = Column(String(20), nullable=False) # 'user' or 'model'
    content = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="chat_history")

class AIInsight(Base):
    """Stores generated insights/reports for the user."""
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    report_type = Column(String(50)) # 'weekly', 'monthly'
    insights_json = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class TravelReport(Base):
    """Stores metadata about generated PDF reports."""
    __tablename__ = "travel_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_name = Column(String(150))
    file_path = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Creates all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Returns a new database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
