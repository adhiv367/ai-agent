import requests
import streamlit as st

# ✅ Get your correct API key from: https://aistudio.google.com
API_KEY = "Api key"

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="MAME AI", page_icon="🤖")
st.title("🤖 MAME")
st.caption("Your Smart AI Assistant — Powered by Gemini 2.5 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    gemini_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    data = {"contents": gemini_history}

    try:
        response = requests.post(URL, json=data)
        result = response.json()

        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            reply = f"❌ API Error: {result['error']['message']}"
        else:
            reply = f"❌ Unexpected response: {result}"

    except Exception as e:
        reply = f"❌ Something went wrong: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})