import streamlit as st
from database.db import get_db_session
from database.models import TravelAssessment

st.set_page_config(page_title="Travel Assessment", page_icon="📝")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("📝 Travel Preference Assessment")
st.markdown("Fill out this assessment to help our AI recommend the best trips for you.")

db = get_db_session()
try:
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            travel_experience = st.selectbox("Travel Experience", ["Novice", "Intermediate", "Expert Backpacker"])
            budget_amount = st.number_input("Total Budget ($)", min_value=0.0, value=500.0)
            trip_duration = st.number_input("Trip Duration (Days)", min_value=1, max_value=365, value=7)
            travel_dates = st.text_input("Preferred Travel Dates (e.g., Summer 2024, May 10-20)")
            accommodation = st.selectbox("Accommodation Preference", ["Hostel", "Budget Hotel", "Airbnb", "Student Housing", "Resort"])
            
        with col2:
            transportation = st.selectbox("Transportation Preference", ["Public Transit", "Walking", "Rental Car", "Flights", "Trains"])
            travel_companions = st.selectbox("Travel Companions", ["Solo", "Partner", "Friends", "Group", "Family"])
            food_prefs = st.text_input("Food Preferences / Allergies (e.g., Vegan, No Nuts)")
            safety_concerns = st.text_input("Safety Concerns (e.g., Solo Female Traveler)")
            
        interests = st.multiselect("Travel Interests", 
                                   ["Adventure", "Beaches", "Mountains", "Historical Sites", "Museums", 
                                    "Food Exploration", "Shopping", "Festivals", "Nature", "Nightlife"])
        
        preferred_dests = st.text_input("Preferred Destinations (if any)")
        special_reqs = st.text_area("Any other special requirements?")

        submit = st.form_submit_button("Submit Assessment")
        
        if submit:
            assessment = TravelAssessment(
                user_id=st.session_state.user["id"],
                travel_experience=travel_experience,
                budget_amount=budget_amount,
                trip_duration_days=trip_duration,
                travel_dates=travel_dates,
                accommodation_preference=accommodation,
                transportation_preference=transportation,
                travel_companions=travel_companions,
                food_preferences=food_prefs,
                safety_concerns=safety_concerns,
                travel_interests=", ".join(interests),
                preferred_destinations=preferred_dests,
                special_requirements=special_reqs
            )
            db.add(assessment)
            db.commit()
            st.success("Assessment saved! You can now get personalized AI recommendations.")

finally:
    db.close()
