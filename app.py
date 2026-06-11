import streamlit as st
from database.db import init_db
from services.auth_service import AuthService

# Must be the first Streamlit command
st.set_page_config(
    page_title="Student Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def init_app():
    """Initialize application state and database."""
    init_db()
    
    if "user" not in st.session_state:
        st.session_state.user = None

def login_page():
    st.title("✈️ AI-Powered Student Travel Planner")
    st.markdown("Plan affordable, personalized trips with the power of Google Gemini AI.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                res = AuthService.login(email, password)
                if res["success"]:
                    st.session_state.user = res["user"]
                    st.success(res["message"])
                    st.rerun()
                else:
                    st.error(res["message"])
                    
    with tab2:
        st.header("Sign Up")
        with st.form("signup_form"):
            full_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password", help="Minimum 8 characters")
            submit_signup = st.form_submit_button("Sign Up")
            
            if submit_signup:
                if not full_name or not new_email or not new_password:
                    st.error("Please fill in all fields.")
                else:
                    res = AuthService.signup(full_name, new_email, new_password)
                    if res["success"]:
                        st.session_state.user = res["user"]
                        st.success(res["message"])
                        st.rerun()
                    else:
                        st.error(res["message"])

def sidebar_nav():
    st.sidebar.title(f"Welcome, {st.session_state.user['full_name']}!")
    st.sidebar.markdown("---")
    
    # We use Streamlit's native multi-page app feature
    # Streamlit automatically creates navigation from the `pages/` directory
    # We can just add a logout button here
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()

def main():
    init_app()
    
    if st.session_state.user is None:
        login_page()
    else:
        sidebar_nav()
        
        st.title("Main Menu")
        st.info("Please use the sidebar to navigate through the application features.")
        st.markdown("""
        ### Features Available:
        - 📊 **Dashboard**: Overview of your travel profile and plans.
        - 👤 **Profile**: Manage your personal and academic info.
        - 📝 **Assessment**: Take the travel preference assessment.
        - 🌍 **Destinations**: Get AI-powered destination recommendations.
        - 🗺️ **Trip Planner**: Generate detailed day-by-day itineraries.
        - 💰 **Budget**: Plan and optimize your travel budget.
        - 🧾 **Expenses**: Track your actual spending.
        - 📈 **Analytics**: View insights and charts.
        - 🤖 **Chatbot**: Talk to your AI Travel Assistant.
        """)

if __name__ == "__main__":
    main()
