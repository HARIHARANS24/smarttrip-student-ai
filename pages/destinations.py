import streamlit as st
from services.trip_service import TripService
from database.db import get_db_session
from database.models import User, TravelAssessment

st.set_page_config(page_title="Destinations", page_icon="🌍")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("🌍 AI Destination Recommender")

db = get_db_session()
try:
    user = db.query(User).filter(User.id == st.session_state.user["id"]).first()
    assessment = db.query(TravelAssessment).filter(TravelAssessment.user_id == user.id).order_by(TravelAssessment.created_at.desc()).first()

    if not assessment:
        st.info("Please fill out the Travel Assessment first to get personalized recommendations.")
        st.button("Go to Assessment", on_click=lambda: st.switch_page("pages/assessment.py"))
    else:
        st.markdown(f"**Budget:** ${assessment.budget_amount} | **Duration:** {assessment.trip_duration_days} days | **Interests:** {assessment.travel_interests}")
        
        if st.button("Generate Recommendations", type="primary"):
            with st.spinner("Gemini AI is analyzing your profile to find the best destinations..."):
                trip_service = TripService()
                
                user_data = {
                    "age": user.age or 20,
                    "country": user.country or "Unknown",
                    "budget": assessment.budget_amount,
                    "duration": assessment.trip_duration_days,
                    "travel_style": assessment.travel_companions,
                    "interests": assessment.travel_interests
                }
                
                try:
                    recs = trip_service.recommend_destinations(user.id, user_data)
                    st.success("Recommendations generated!")
                    
                    for i, rec in enumerate(recs):
                        with st.expander(f"✨ Option {i+1}: {rec['Destination']}", expanded=True):
                            st.write(f"**Estimated Cost:** {rec['EstimatedCost']}")
                            st.write(f"**Best Time to Visit:** {rec['BestTime']}")
                            st.write(f"**Why it fits you:** {rec['Why']}")
                            st.write("**Top Attractions:**")
                            for attr in rec['Attractions']:
                                st.write(f"- {attr}")
                            
                            if st.button(f"Plan trip to {rec['Destination']}", key=f"plan_{i}"):
                                st.session_state.selected_destination = rec['Destination']
                                st.switch_page("pages/trip_planner.py")
                
                except Exception as e:
                    st.error(f"Error generating recommendations: {e}")

finally:
    db.close()
