import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

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

    # prompt
    system_prompt = f"""
You are an AI Personal Historian.
Your job is to explain historical events, people, and civilizations clearly and concisely.
Rules:
• Give short answers (3–5 sentences).
• Focus on important facts: date, location, key people, and impact.
• Use simple language.
• Avoid unnecessary storytelling.
Always format the answer EXACTLY like this with line breaks:

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

    response = model.generate_content(system_prompt)

    answer = response.text

    # Show bot response
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})