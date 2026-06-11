import streamlit as st
import json
from services.trip_service import TripService
from database.db import get_db_session
from database.models import TravelAssessment
from reports.generator import PDFReportGenerator

st.set_page_config(page_title="Trip Planner", page_icon="🗺️")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("🗺️ AI Trip Planner")

# Pre-fill destination if passed from recommendations
default_dest = st.session_state.get("selected_destination", "")

with st.form("trip_form"):
    destination = st.text_input("Where do you want to go?", value=default_dest)
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Budget ($)", min_value=0.0, value=500.0)
        duration = st.number_input("Duration (Days)", min_value=1, max_value=30, value=5)
    with col2:
        travel_style = st.selectbox("Travel Style", ["Backpacking", "Comfort", "Luxury", "Study Tour"])
        interests = st.text_input("Specific Interests (e.g., Museums, Hiking)")
    
    submit = st.form_submit_button("Generate Itinerary")

if submit:
    if not destination:
        st.error("Please enter a destination.")
    else:
        with st.spinner(f"Crafting the perfect itinerary for {destination}..."):
            trip_service = TripService()
            trip_data = {
                "destination": destination,
                "budget": budget,
                "duration": duration,
                "travel_style": travel_style,
                "interests": interests
            }
            
            try:
                plan = trip_service.generate_trip_plan(st.session_state.user["id"], trip_data)
                
                st.success("Itinerary generated successfully!")
                
                # Save into session state for PDF export
                st.session_state.latest_itinerary = plan
                
                st.subheader(f"Trip to {plan['Destination']}")
                st.write(f"**Total Estimated Cost:** {plan['TotalEstimatedCost']}")
                
                for day in plan['Itinerary']:
                    with st.expander(f"Day {day['Day']}", expanded=True):
                        st.write("**Activities:**")
                        for act in day['Activities']:
                            st.write(f"- {act}")
                        st.write(f"**Meals:** {', '.join(day['Meals'])}")
                        st.write(f"**Transport:** {day['Transportation']}")
                        st.write(f"**Estimated Cost:** {day['EstimatedCost']}")
                        st.info(f"💡 {day['Tips']}")
                
            except Exception as e:
                st.error(f"Failed to generate trip plan: {e}")

if "latest_itinerary" in st.session_state:
    if st.button("📄 Export to PDF"):
        try:
            pdf_gen = PDFReportGenerator(st.session_state.user["full_name"], st.session_state.latest_itinerary["Destination"])
            pdf_gen.create_header("Travel Itinerary")
            pdf_gen.add_itinerary_section(st.session_state.latest_itinerary['Itinerary'])
            file_path = pdf_gen.generate_pdf()
            
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=file_path.split("/")[-1],
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Could not generate PDF. Have you installed fpdf2? Error: {e}")
