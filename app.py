
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

st.set_page_config(
    page_title="AI Marketing Assistant Pro",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stChatInput textarea {
    color: #000000 !important;
    background-color: #f8f9fa !important;
    font-size: 16px !important;
}
.stChatMessage {
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
}
[data-testid="stChatMessage"] [data-testid="user"] {
    background-color: #f0f2f6;
}
[data-testid="stChatMessage"] [data-testid="assistant"] {
    background-color: #e3f2fd;
}
</style>
""", unsafe_allow_html=True)

MARKETING_CONTEXT = """You are a professional digital marketing expert with 10+ years of experience. 
Provide specific, actionable advice for social media marketing with these rules:
1. Always mention which platform you're referring to
2. Include metrics when possible
3. Give step-by-step instructions
4. Use bullet points for complex advice
5. Suggest tools when relevant"""

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Welcome to your AI Marketing Assistant! What do you want help with?"
    }]

with st.sidebar:
    st.title("🛠️ Marketing Toolkit")
    tool = st.radio(
        "Select a tool:",
        ["💬 General Chat", "📝 Content Strategy", "🏷️ Hashtag Generator", "⏰ Posting Schedule"],
        index=0
    )

    if tool == "📝 Content Strategy":
        with st.form("f1"):
            p = st.selectbox("Platform", ["Instagram", "Facebook", "LinkedIn", "TikTok", "Twitter"])
            a = st.text_input("Audience")
            g = st.text_input("Goal")
            if st.form_submit_button("Generate"):
                pr = f"Create {p} content strategy for {a} targeting {g}"
                st.session_state.messages.append({"role": "user", "content": pr})

    elif tool == "🏷️ Hashtag Generator":
        with st.form("f2"):
            p = st.selectbox("Platform", ["Instagram", "TikTok", "Twitter"])
            n = st.text_input("Niche")
            if st.form_submit_button("Generate"):
                pr = f"Give 20 hashtags for {n} on {p}"
                st.session_state.messages.append({"role": "user", "content": pr})

    elif tool == "⏰ Posting Schedule":
        with st.form("f3"):
            p = st.selectbox("Platform", ["Instagram", "Facebook", "LinkedIn", "TikTok"])
            t = st.selectbox("Timezone", ["IST", "EST", "PST", "GMT"])
            if st.form_submit_button("Generate"):
                pr = f"Best posting times for {p} in {t}"
                st.session_state.messages.append({"role": "user", "content": pr})

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

u = st.chat_input("Ask your marketing question...")

if u:
    st.session_state.messages.append({"role": "user", "content": u})
    with st.chat_message("user"):
        st.markdown(u)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = model.generate_content(f"{MARKETING_CONTEXT}\nUser: {u}")
                st.markdown(r.text)
                st.session_state.messages.append({"role": "assistant", "content": r.text})
            except Exception as e:
                st.error(str(e))

