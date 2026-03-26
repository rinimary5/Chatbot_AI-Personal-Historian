import streamlit as st
from google import genai
import os

# Initialize Gemini client
from google.genai import types # Add this import at the top
st.sidebar.subheader("Current API 'Menu'")
for m in client.models.list():
    # This filters for models that work with your current code
    if 'generateContent' in m.supported_methods:
        st.sidebar.write(f"✅ {m.name}")
# Initialize Gemini client with explicit API version
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(api_version='v1')
)

st.title("AI Personal Historian")
st.write("Ask me anything about History!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask a history question...")

if prompt:

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # System prompt
    system_prompt = f"""
You are an AI Personal Historian.
Your job is to explain historical events, people, and civilizations clearly and concisely.

Rules:
- Give short answers (3–5 sentences).
- Focus on important facts: date, location, key people, and impact.
- Use simple language.
- Avoid unnecessary storytelling.

Always format the answer EXACTLY like this:

Event:
<event name>

Time Period:
<time period>

Key Figures:
<important people>

What Happened:
<short explanation>

Historical Impact:
<impact of the event>

Question: {prompt}
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=system_prompt
        )
        answer = response.text

        if not answer:
            answer = "⚠️ No response generated. Try again."

    except Exception as e:
        answer = f"❌ Error: {e}"

    # Show bot response
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
