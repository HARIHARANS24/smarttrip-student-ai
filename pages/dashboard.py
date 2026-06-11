import streamlit as st
from database.db import get_db_session
from database.models import User, TripPlan, ExpenseLog

st.set_page_config(page_title="Dashboard - Travel Planner", page_icon="📊", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("📊 Travel Dashboard")
st.markdown("Welcome to your travel command center!")

# Fetch quick stats
db = get_db_session()
try:
    user_id = st.session_state.user["id"]
    trips_count = db.query(TripPlan).filter(TripPlan.user_id == user_id).count()
    expenses = db.query(ExpenseLog).filter(ExpenseLog.user_id == user_id).all()
    total_spent = sum([e.amount for e in expenses])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Trips Planned", trips_count)
    with col2:
        st.metric("Total Spent", f"${total_spent:.2f}")
    with col3:
        st.metric("Expenses Tracked", len(expenses))
    with col4:
        st.metric("Saved Destinations", 0) # Placeholder
        
    st.markdown("---")
    
    st.subheader("Quick Actions")
    colA, colB, colC = st.columns(3)
    
    with colA:
        if st.button("🗺️ Plan a New Trip", use_container_width=True):
            st.switch_page("pages/trip_planner.py")
    with colB:
        if st.button("💰 Add Expense", use_container_width=True):
            st.switch_page("pages/expenses.py")
    with colC:
        if st.button("🤖 Ask AI Assistant", use_container_width=True):
            st.switch_page("pages/chatbot.py")

finally:
    db.close()
