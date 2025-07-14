import streamlit as st
import requests

st.set_page_config(page_title="Chatbot", layout="wide")

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Type your message here..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            "https://chatbot-new-1.onrender.com/chat",  
            json={"message": user_input}
        )
        response.raise_for_status()
        bot_reply = response.json().get("response", "No reply received from server.")
    except requests.exceptions.RequestException as e:
        bot_reply = f"Error: {e}"

    # Show bot reply
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
