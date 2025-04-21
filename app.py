import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ==================== SETUP & CONFIGURATION ====================
# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Failed to configure Gemini: {str(e)}")
    st.stop()

# ==================== STREAMLIT UI CONFIG ====================
st.set_page_config(
    page_title="AI Marketing Assistant Pro",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for visibility and styling
st.markdown("""
<style>
    /* Input text visibility */
    .stChatInput textarea {
        color: #000000 !important;
        background-color: #f8f9fa !important;
        font-size: 16px !important;
    }
    
    /* Chat message bubbles */
    .stChatMessage {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
    }
    
    /* User message bubble */
    [data-testid="stChatMessage"] [data-testid="user"] {
        background-color: #f0f2f6;
    }
    
    /* Assistant message bubble */
    [data-testid="stChatMessage"] [data-testid="assistant"] {
        background-color: #e3f2fd;
    }
    
    /* Sidebar styling */
    .st-emotion-cache-6qob1r {
        background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==================== CHATBOT FUNCTIONALITY ====================
MARKETING_CONTEXT = """You are a professional digital marketing expert with 10+ years of experience. 
Provide specific, actionable advice for social media marketing with these rules:
1. Always mention which platform you're referring to
2. Include metrics when possible (e.g., "Posts with videos get 48% more engagement")
3. Give step-by-step instructions when appropriate
4. Use bullet points for complex advice
5. Suggest tools when relevant (e.g., "Use Canva for carousel posts")"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Welcome to your AI Marketing Assistant! I can help with:\n\n"
                   "- 📱 Platform-specific strategies\n"
                   "- 🎯 Audience targeting\n"
                   "- 📊 Performance optimization\n"
                   "- 🚀 Campaign ideas\n\n"
                   "What would you like to focus on today?"
    }]

# ==================== SIDEBAR TOOLS ====================
with st.sidebar:
    st.title("🛠️ Marketing Toolkit")
    st.subheader("Quick Tools")
    
    tool = st.radio(
        "Select a tool:",
        ["💬 General Chat", 
         "📝 Content Strategy", 
         "🏷️ Hashtag Generator",
         "⏰ Posting Schedule"],
        index=0
    )
    
    if tool == "📝 Content Strategy":
        with st.form("content_strategy_form"):
            platform = st.selectbox("Platform", ["Instagram", "Facebook", "LinkedIn", "TikTok", "Twitter"])
            audience = st.text_input("Target audience")
            goal = st.text_input("Campaign goal")
            
            if st.form_submit_button("Generate Strategy"):
                prompt = f"""Create a detailed {platform} content strategy for {audience} targeting {goal}. 
                Include: content types, posting frequency, engagement tactics, and 3 post examples."""
                st.session_state.messages.append({"role": "user", "content": prompt})
    
    elif tool == "🏷️ Hashtag Generator":
        with st.form("hashtag_form"):
            platform = st.selectbox("Platform", ["Instagram", "TikTok", "Twitter"])
            niche = st.text_input("Your niche/industry")
            
            if st.form_submit_button("Generate Hashtags"):
                prompt = f"""Provide 20 highly effective hashtags for {niche} on {platform} 
                categorized by popularity (high/medium/low competition)"""
                st.session_state.messages.append({"role": "user", "content": prompt})
    
    elif tool == "⏰ Posting Schedule":
        with st.form("schedule_form"):
            platform = st.selectbox("Platform", ["Instagram", "Facebook", "LinkedIn", "TikTok"])
            timezone = st.selectbox("Timezone", ["EST", "PST", "CST", "GMT", "Other"])
            
            if st.form_submit_button("Get Best Times"):
                prompt = f"""Recommend optimal posting times for {platform} in {timezone} timezone 
                with engagement statistics"""
                st.session_state.messages.append({"role": "user", "content": prompt})

# ==================== CHAT INTERFACE ====================
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input with clear visibility
user_input = st.chat_input("Type your marketing question here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your request..."):
            try:
                response = model.generate_content(f"{MARKETING_CONTEXT}\n\nUser: {user_input}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                error_msg = f"⚠️ Error generating response: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})