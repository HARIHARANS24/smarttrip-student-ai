import streamlit as st
import json
from services.budget_service import BudgetService
from database.db import get_db_session
from database.models import BudgetPlan
from reports.generator import PDFReportGenerator

st.set_page_config(page_title="Budget Planner", page_icon="💰")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("💰 AI Budget Planner")

with st.form("budget_form"):
    destination = st.text_input("Destination")
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Duration (Days)", min_value=1, value=5)
        accommodation = st.selectbox("Accommodation", ["Hostel", "Budget Hotel", "Airbnb", "Luxury"])
    with col2:
        transportation = st.selectbox("Transportation", ["Public Transit", "Flights", "Rental Car"])
        food = st.selectbox("Food Preference", ["Street Food", "Restaurants", "Fine Dining", "Mix"])
        
    submit = st.form_submit_button("Generate Budget")

if submit:
    if not destination:
        st.error("Please enter a destination.")
    else:
        with st.spinner(f"Calculating budget for {destination}..."):
            budget_service = BudgetService()
            budget_data = {
                "destination": destination,
                "duration": duration,
                "accommodation": accommodation,
                "transportation": transportation,
                "food": food
            }
            
            try:
                plan = budget_service.generate_budget_plan(st.session_state.user["id"], budget_data)
                st.success("Budget generated successfully!")
                
                # Save into session state for PDF export
                st.session_state.latest_budget = plan
                st.session_state.latest_budget_dest = destination
                
                colA, colB = st.columns(2)
                with colA:
                    st.metric("Total Estimated Budget", f"${plan['TotalEstimatedBudget']:.2f}")
                    st.write(f"**Accommodation:** ${plan['AccommodationCost']:.2f}")
                    st.write(f"**Transportation:** ${plan['TransportationCost']:.2f}")
                with colB:
                    st.metric("Emergency Fund", f"${plan['EmergencyFund']:.2f}")
                    st.write(f"**Food:** ${plan['FoodCost']:.2f}")
                    st.write(f"**Activities:** ${plan['ActivitiesCost']:.2f}")
                
                st.subheader("💡 Budget Tips")
                for tip in plan['Tips']:
                    st.info(tip)
                
            except Exception as e:
                st.error(f"Failed to generate budget: {e}")

if "latest_budget" in st.session_state:
    if st.button("📄 Export Budget to PDF"):
        try:
            pdf_gen = PDFReportGenerator(st.session_state.user["full_name"], st.session_state.latest_budget_dest)
            pdf_gen.add_budget_section(st.session_state.latest_budget)
            file_path = pdf_gen.generate_pdf()
            
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=file_path.split("/")[-1],
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Could not generate PDF: {e}")
