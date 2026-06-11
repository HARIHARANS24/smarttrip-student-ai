import streamlit as st
from services.auth_service import AuthService
from database.db import get_db_session
from database.models import User

st.set_page_config(page_title="Profile - Travel Planner", page_icon="👤")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("👤 My Profile")

db = get_db_session()
try:
    user = db.query(User).filter(User.id == st.session_state.user["id"]).first()
    
    with st.form("profile_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", value=user.full_name)
            age = st.number_input("Age", min_value=16, max_value=100, value=user.age if user.age else 20)
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], 
                                  index=["Male", "Female", "Other", "Prefer not to say"].index(user.gender) if user.gender else 0)
        with col2:
            country = st.text_input("Country", value=user.country if user.country else "")
            currency = st.selectbox("Preferred Currency", ["USD", "EUR", "GBP", "INR", "AUD"], 
                                    index=["USD", "EUR", "GBP", "INR", "AUD"].index(user.preferred_currency) if user.preferred_currency else 0)
            
        st.subheader("Academic Information")
        col3, col4 = st.columns(2)
        with col3:
            university = st.text_input("University", value=user.university if user.university else "")
            course = st.text_input("Course/Degree", value=user.course if user.course else "")
        with col4:
            year_of_study = st.selectbox("Year of Study", ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"],
                                         index=["Freshman", "Sophomore", "Junior", "Senior", "Graduate"].index(user.year_of_study) if user.year_of_study else 0)

        st.subheader("Travel Logistics")
        col5, col6 = st.columns(2)
        with col5:
            passport = st.checkbox("I have a valid passport", value=user.passport_status)
        with col6:
            visa = st.text_input("Visa Requirements / Status", value=user.visa_requirements if user.visa_requirements else "")

        submit = st.form_submit_button("Save Profile")
        
        if submit:
            updates = {
                "full_name": full_name,
                "age": age,
                "gender": gender,
                "country": country,
                "preferred_currency": currency,
                "university": university,
                "course": course,
                "year_of_study": year_of_study,
                "passport_status": passport,
                "visa_requirements": visa
            }
            
            res = AuthService.update_profile(user.id, updates)
            if res["success"]:
                st.session_state.user["full_name"] = full_name
                st.session_state.user["currency"] = currency
                st.success("Profile updated successfully!")
            else:
                st.error(res["message"])

finally:
    db.close()
