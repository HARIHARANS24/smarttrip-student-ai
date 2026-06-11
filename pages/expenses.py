import streamlit as st
import pandas as pd
from database.db import get_db_session
from database.models import ExpenseLog

st.set_page_config(page_title="Expenses", page_icon="🧾")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("🧾 Travel Expense Tracker")

db = get_db_session()
try:
    user_id = st.session_state.user["id"]
    
    with st.form("expense_form"):
        st.subheader("Add New Expense")
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Accommodation", "Transportation", "Food", "Activities", "Shopping", "Miscellaneous"])
            amount = st.number_input("Amount", min_value=0.01, value=10.0)
        with col2:
            currency = st.text_input("Currency", value=st.session_state.user.get("currency", "USD"))
            description = st.text_input("Description (Optional)")
            
        submit = st.form_submit_button("Add Expense")
        
        if submit:
            new_expense = ExpenseLog(
                user_id=user_id,
                category=category,
                amount=amount,
                currency=currency,
                description=description
            )
            db.add(new_expense)
            db.commit()
            st.success("Expense added!")
            st.rerun()
            
    st.markdown("---")
    st.subheader("Your Expenses")
    
    expenses = db.query(ExpenseLog).filter(ExpenseLog.user_id == user_id).order_by(ExpenseLog.expense_date.desc()).all()
    
    if not expenses:
        st.info("No expenses tracked yet.")
    else:
        # Convert to DataFrame for easy rendering
        data = [{
            "Date": e.expense_date.strftime("%Y-%m-%d"),
            "Category": e.category,
            "Amount": e.amount,
            "Currency": e.currency,
            "Description": e.description
        } for e in expenses]
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Simple summary
        total = sum([e.amount for e in expenses])
        st.metric("Total Spent", f"{total:.2f}")

finally:
    db.close()
