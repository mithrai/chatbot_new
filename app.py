import streamlit as st
import requests

st.set_page_config(page_title="Mini ChatGPT", layout="wide")
st.title("Mini Chatbot (Tiny GPT-2)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Say something...")

if user_input:

    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            "https://chatbot-new-1.onrender.com/chat",  
            json={"message": user_input}
        )
        bot_reply = response.json().get("response", "Error getting response")
    except Exception as e:
        bot_reply = "Backend unreachable or crashed."

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
