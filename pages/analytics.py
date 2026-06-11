import streamlit as st
import plotly.express as px
from services.analytics_service import AnalyticsService

st.set_page_config(page_title="Analytics Dashboard", page_icon="📈", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("📈 Travel Analytics & Insights")

analytics_service = AnalyticsService()
user_id = st.session_state.user["id"]

df = analytics_service.get_user_expenses_df(user_id)

if df.empty:
    st.info("No expense data available to generate analytics. Please add expenses in the Expenses page.")
else:
    # Top Level Metrics
    total_spent = df['amount'].sum()
    top_category = df.groupby('category')['amount'].sum().idxmax()
    avg_expense = df['amount'].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"${total_spent:.2f}")
    col2.metric("Highest Category", top_category)
    col3.metric("Avg Expense", f"${avg_expense:.2f}")
    
    st.markdown("---")
    
    # Charts
    st.subheader("Expense Breakdown")
    colA, colB = st.columns(2)
    
    with colA:
        fig_pie = px.pie(df, values='amount', names='category', title="Spending by Category", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with colB:
        df_sorted = df.sort_values(by="date")
        fig_bar = px.bar(df_sorted, x='date', y='amount', color='category', title="Daily Spending Trend")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("---")
    st.subheader("🤖 AI Financial Insights")
    
    if st.button("Generate AI Insights"):
        with st.spinner("Analyzing your spending patterns..."):
            insights = analytics_service.generate_ai_insights(user_id)
            if "error" in insights:
                st.error(insights["error"])
            elif "message" in insights:
                st.info(insights["message"])
            else:
                st.success("Analysis Complete!")
                st.write(f"**Potential Savings:** {insights.get('SavingsPotential', 'N/A')}")
                st.write("**Suggestions:**")
                for s in insights.get('Suggestions', []):
                    st.write(f"- {s}")
