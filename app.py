import streamlit as st
import requests

st.set_page_config(page_title="Chatbot", layout="centered")
st.title("Chatbot - Hugging Face")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()
with chat_container:
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"<div style='text-align: left; color: white; background: #1c1c1c; padding: 10px; border-radius: 8px; margin-bottom: 5px'><b>👤 You:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: right; color: white; background: #3c3c3c; padding: 10px; border-radius: 8px; margin-bottom: 5px'><b>🤖 Bot:</b> {message}</div>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message and press Enter", key="user_input", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

    if submitted and user_input:

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input}
        )
        bot_reply = response.json().get("response", "Sorry, no reply.")

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))
