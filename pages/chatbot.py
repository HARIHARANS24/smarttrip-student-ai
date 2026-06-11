import streamlit as st
from services.gemini_service import GeminiService
from database.db import get_db_session
from database.models import ChatHistory
from utils.prompts import CHATBOT_SYSTEM_PROMPT

st.set_page_config(page_title="AI Travel Assistant", page_icon="🤖")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view this page.")
    st.stop()

st.title("🤖 AI Travel Assistant")

# Initialize chat service
if "gemini_chat" not in st.session_state:
    gemini_service = GeminiService()
    # Convert system prompt to the first message if needed, or just let the model handle it
    # Gemini 1.5 allows system_instruction, but for compatibility we'll send it as the first context
    
    # Let's load history from DB
    db = get_db_session()
    try:
        user_id = st.session_state.user["id"]
        history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.id).all()
        
        formatted_history = []
        for h in history:
            formatted_history.append({"role": h.role, "parts": [h.content]})
            
        st.session_state.gemini_chat = gemini_service.start_chat(history=formatted_history)
        st.session_state.chat_history_db = history # purely to display
    finally:
        db.close()

# Display chat messages from history on app rerun
for message in st.session_state.gemini_chat.history:
    role = message.role
    if role == "model":
        with st.chat_message("assistant"):
            st.markdown(message.parts[0].text)
    else:
        with st.chat_message("user"):
            st.markdown(message.parts[0].text)

# React to user input
prompt = st.chat_input("Ask me about travel, budgets, or packing...")

if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Save to DB
    db = get_db_session()
    user_id = st.session_state.user["id"]
    try:
        db.add(ChatHistory(user_id=user_id, role="user", content=prompt))
        db.commit()
    except Exception as e:
        print(e)
    
    # Send to Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # We enforce the rules by appending them to the prompt silently or relying on model configuration
            full_prompt = f"{CHATBOT_SYSTEM_PROMPT}\n\nUser: {prompt}"
            
            response = st.session_state.gemini_chat.send_message(full_prompt)
            message_placeholder.markdown(response.text)
            
            # Save response to DB
            db.add(ChatHistory(user_id=user_id, role="model", content=response.text))
            db.commit()
        except Exception as e:
            st.error(f"Error communicating with AI: {e}")
    
    db.close()
