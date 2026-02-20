"""
VIVA - AI-Powered Survey Interview Platform
Frontend Streamlit Application
This module provides the user interface for conducting AI-powered survey interviews
with integrated voice and text input capabilities.
"""

import streamlit as st
import backend as backend  # Custom backend module for AI and database operations
import requests
import re
import time as time_module

# =============================================================================
# DEPENDENCIES AND SAFE IMPORTS
# =============================================================================

# Safely import Lottie animations for enhanced UI (optional dependency)
try:
    from streamlit_lottie import st_lottie
    HAS_LOTTIE = True
except ImportError:
    HAS_LOTTIE = False
    st.warning("Lottie animations disabled - install streamlit-lottie for enhanced visuals")

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI-Powered Survey", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# ASSET LOADING FUNCTIONS
# =============================================================================

def load_lottieurl(url):
    """
    Load Lottie animation from URL with error handling.
    
    Args:
        url (str): URL to Lottie animation JSON
        
    Returns:
        dict: Lottie animation data or None if loading fails
    """
    if not HAS_LOTTIE:
        return None
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception:
        return None

# Load dark-themed animations for enhanced UI
lottie_ai = None
lottie_chat = None
if HAS_LOTTIE:
    lottie_ai = load_lottieurl(
        "https://assets3.lottiefiles.com/packages/lf20_3rwasyjy.json"
    )
    lottie_chat = load_lottieurl(
        "https://assets1.lottiefiles.com/packages/lf20_uxikzyqy.json"
    )

# =============================================================================
# CUSTOM CSS STYLING - DARK THEME
# =============================================================================

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main app background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }

    /* Container styling for main content areas */
    .main-container {
        background: rgba(15, 15, 15, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Survey card styling for dashboard items */
    .survey-card {
        background: rgba(30, 30, 46, 0.7);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    /* Hover effects for interactive cards */
    .survey-card:hover {
        background: rgba(40, 40, 60, 0.8);
        border-color: rgba(168, 85, 247, 0.3);
        transform: translateY(-2px);
    }

    /* Gradient text styling for headings */
    h1, h2, h3 {
        background: linear-gradient(90deg, #ffffff 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 1rem;
    }

    h1 {
        font-size: 3rem !important;
    }

    /* Additional gradient text class */
    .gradient-text {
        background: linear-gradient(90deg, #a855f7 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }

    /* Primary button styling */
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%);
        border: none;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
    }

    /* Secondary button variant */
    .secondary-button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* User message bubble styling */
    .user-bubble {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem auto;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        position: relative;
    }

    /* AI message bubble styling */
    .ai-bubble {
        background: rgba(30, 30, 46, 0.9);
        color: #e0e0e0;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem auto 1rem 0;
        max-width: 70%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        position: relative;
    }

    /* Form input styling */
    .stTextInput > div > div > input {
        background: rgba(20, 20, 30, 0.8);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
    }

    /* Dropdown and number input styling */
    .stSelectbox > div > div > select {
        background: rgba(20, 20, 30, 0.8);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }

    .stNumberInput > div > div > input {
        background: rgba(20, 20, 30, 0.8);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 30, 46, 0.7);
        border-radius: 12px 12px 0 0;
        padding: 1rem 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%) !important;
    }

    /* Status badge styling */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 1rem;
    }

    .status-active {
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .status-completed {
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    /* Chat container for message history */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 16px;
        background: rgba(20, 20, 30, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Custom scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }

    .chat-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 3px;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: #a855f7;
        border-radius: 3px;
    }

    /* Input area container */
    .input-container {
        background: rgba(30, 30, 46, 0.7);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Timestamp styling for messages */
    .message-time {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        text-align: right;
    }

    /* Voice recording indicator */
    .voice-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #a855f7;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Integrated input layout */
    .integrated-input {
        display: flex;
        gap: 1rem;
        align-items: flex-end;
    }

    .text-input-section {
        flex: 1;
    }

    .voice-input-section {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    /* Instruction text styling */
    .instruction-text {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-align: center;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# SESSION STATE MANAGEMENT
# =============================================================================

# Initialize session state variables for app navigation and data persistence
if "page" not in st.session_state:
    st.session_state.page = "home"  # Current page: "home", "create", or "chat"

if "current_survey" not in st.session_state:
    st.session_state.current_survey = None  # Currently active survey ID

if "messages" not in st.session_state:
    st.session_state.messages = {}  # Cache for conversation messages

if "audio_data" not in st.session_state:
    st.session_state.audio_data = None  # Store recorded audio data

if "survey_created" not in st.session_state:
    st.session_state.survey_created = False  # Track survey creation success

if "create_form_submitted" not in st.session_state:
    st.session_state.create_form_submitted = False  # Form submission state

def navigate(page):
    """
    Navigate between different pages of the application.
    
    Args:
        page (str): Target page identifier ("home", "create", "chat")
    """
    st.session_state.page = page
    st.rerun()

# =============================================================================
# PAGE VIEW FUNCTIONS
# =============================================================================

def view_home():
    """
    Render the home/dashboard page with survey overview and creation options.
    """
    # Split layout into two columns for content and visuals
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown('<h1>AI-Powered Survey Platform</h1>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style='color: #94a3b8; font-size: 1.2rem; line-height: 1.6; margin-bottom: 2rem;'>
            Deploy intelligent AI agents to conduct comprehensive interviews at scale. 
            <span class="gradient-text">Unbiased, adaptive, and deeply analytical.</span>
            </div>
            """, unsafe_allow_html=True
        )
        
        # Feature highlights in two columns
        features_col1, features_col2 = st.columns(2)
        with features_col1:
            st.markdown("""
            <div style='margin: 1.5rem 0;'>
            <div style='color: #a855f7; font-size: 1.5rem;'>🎯</div>
            <div style='color: white; font-weight: 600;'>Smart Probing</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Adaptive follow-up questions</div>
            </div>
            <div style='margin: 1.5rem 0;'>
            <div style='color: #a855f7; font-size: 1.5rem;'>⚡</div>
            <div style='color: white; font-weight: 600;'>Real-time Analysis</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Instant insights and feedback</div>
            </div>
            """, unsafe_allow_html=True)
        
        with features_col2:
            st.markdown("""
            <div style='margin: 1.5rem 0;'>
            <div style='color: #a855f7; font-size: 1.5rem;'>🌐</div>
            <div style='color: white; font-weight: 600;'>Multi-language</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Support for multiple languages</div>
            </div>
            <div style='margin: 1.5rem 0;'>
            <div style='color: #a855f7; font-size: 1.5rem;'>📊</div>
            <div style='color: white; font-weight: 600;'>Rich Analytics</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Comprehensive data insights</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Primary call-to-action button
        if st.button("🚀 Create New Survey", type="primary", use_container_width=True):
            st.session_state.create_form_submitted = False
            st.session_state.survey_created = False
            navigate("create")

    with col2:
        # Display animation or fallback emoji
        if HAS_LOTTIE and lottie_ai:
            st_lottie(lottie_ai, height=400, key="home_animation")
        else:
            st.markdown("""
            <div style='text-align: center; color: #a855f7; font-size: 8rem;'>🤖</div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # SURVEY DASHBOARD SECTION
    st.markdown('<h2>Survey Dashboard</h2>', unsafe_allow_html=True)
    
    # Tabbed interface for active and completed surveys
    tab_active, tab_done = st.tabs(["🟢 Active Surveys", "🏁 Completed Surveys"])

    with tab_active:
        surveys = backend.get_all_surveys("Incomplete")
        if not surveys:
            # Empty state for no active surveys
            st.markdown("""
            <div style='text-align: center; padding: 3rem; color: #64748b;'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>📝</div>
                <h3 style='color: #94a3b8;'>No Active Surveys</h3>
                <p>Create your first survey to get started!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display each active survey as an interactive card
            for survey in surveys:
                with st.container():
                    st.markdown('<div class="survey-card">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{survey['question']}**")
                        st.caption(f"📍 Created: {survey['created_at']} • 🔍 Probes: {survey.get('probes', 3)} • ⏱️ Length: {survey.get('length', 60)}s")
                        st.markdown(f'<span class="status-badge status-active">Active</span>', unsafe_allow_html=True)
                    with col2:
                        # Resume survey button
                        if st.button("▶️ Resume", key=f"res_{survey['id']}", use_container_width=True):
                            st.session_state.current_survey = survey["id"]
                            navigate("chat")
                    with col3:
                        # Delete survey button
                        if st.button("🗑️ Delete", key=f"del_{survey['id']}", use_container_width=True):
                            backend.delete_survey_record(survey["id"])
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    with tab_done:
        surveys = backend.get_all_surveys("Completed")
        if not surveys:
            # Empty state for no completed surveys
            st.markdown("""
            <div style='text-align: center; padding: 3rem; color: #64748b;'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>📊</div>
                <h3 style='color: #94a3b8;'>No Completed Surveys</h3>
                <p>Complete a survey to see analytics here!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display completed surveys
            for survey in surveys:
                with st.container():
                    st.markdown('<div class="survey-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{survey['question']}**")
                        st.caption(f"✅ Completed: {survey['created_at']}")
                        st.markdown(f'<span class="status-badge status-completed">Completed</span>', unsafe_allow_html=True)
                    with col2:
                        # View report button (functionality to be implemented)
                        if st.button("📋 View Report", key=f"view_{survey['id']}", use_container_width=True):
                            st.session_state.current_survey = survey["id"]
                    st.markdown('</div>', unsafe_allow_html=True)

def view_create():
    """
    Render the survey creation page with configuration form.
    """
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<h2>🎯 Create New Survey</h2>', unsafe_allow_html=True)
        st.caption("Configure your AI interviewer with precision")

        # Show success message if survey was created
        if st.session_state.survey_created:
            st.markdown("""
            <div class="success-container">
                <div style='font-size: 4rem; margin-bottom: 1rem;'>✅</div>
                <h3 style='color: #4ade80; margin-bottom: 1rem;'>Survey Created Successfully!</h3>
                <p style='color: #94a3b8; margin-bottom: 2rem;'>Your survey has been created and is ready to use.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons after successful creation
            col_start, col_back = st.columns(2)
            with col_start:
                if st.button("🎤 Start Interview Now", type="primary", use_container_width=True):
                    navigate("chat")
            with col_back:
                if st.button("🏠 Back to Dashboard", use_container_width=True):
                    st.session_state.survey_created = False
                    st.session_state.create_form_submitted = False
                    navigate("home")
        
        else:
            # Survey creation form
            with st.form("create_survey_form", clear_on_submit=True):
                question = st.text_input(
                    "**Research Topic / Core Question**",
                    placeholder="e.g., How does remote work impact team collaboration and productivity?",
                    help="Define the main focus area for your research"
                )

                st.markdown("### Survey Parameters")
                
                col1a, col2a, col3a = st.columns(3)

                with col1a:
                    probes = st.number_input(
                        "**Follow-up Depth**",
                        min_value=1, 
                        max_value=10, 
                        value=3,
                        help="Number of adaptive follow-up questions"
                    )

                with col2a:
                    length = st.number_input(
                        "**Time Limit (seconds)**",
                        min_value=30, 
                        max_value=600, 
                        value=120,
                        help="Maximum duration for each response"
                    )

                with col3a:
                    language = st.selectbox(
                        "**Interview Language**",
                        ["English", "Spanish", "French", "German", "Hindi", "Chinese"],
                        help="Language for the conversation"
                    )

                submitted = st.form_submit_button(
                    "🚀 Create Survey", 
                    type="primary", 
                    use_container_width=True
                )

                if submitted:
                    if question.strip():
                        try:
                            # Create survey in backend and store ID
                            new_id = backend.create_survey_record(
                                question=question,
                                probes=probes,
                                length=length,
                                language=language
                            )
                            st.session_state.current_survey = new_id
                            st.session_state.survey_created = True
                            st.session_state.create_form_submitted = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Failed to create survey: {str(e)}")
                    else:
                        st.error("📝 Please enter a research topic to continue.")
        
    with col2:
        # Visual element and tips sidebar
        if HAS_LOTTIE and lottie_chat:
            st_lottie(lottie_chat, height=400)
        st.markdown("""
        <div style='margin-top: 2rem; padding: 1.5rem; background: rgba(30, 30, 46, 0.7); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);'>
            <h4 style='color: white; margin-bottom: 1rem;'>💡 Pro Tips</h4>
            <ul style='color: #94a3b8; padding-left: 1.2rem;'>
                <li>Be specific with your research question</li>
                <li>Start with 3-5 follow-up probes</li>
                <li>Use 60-120 seconds for thoughtful responses</li>
                <li>Choose appropriate language for your audience</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def view_chat():
    """
    Render the chat interface for conducting AI-powered interviews.
    """
    # Validate current survey session
    if not st.session_state.current_survey:
        navigate("home")
        return

    # Fetch survey data from backend
    survey = backend.get_survey_by_id(st.session_state.current_survey)
    if not survey:
        st.error("Session expired or not found.")
        navigate("home")
        return

    # HEADER SECTION
    col_back, col_title, col_stats = st.columns([1, 3, 1])
    
    with col_back:
        if st.button("← Back to Dashboard", use_container_width=True):
            navigate("home")
    
    with col_title:
        st.markdown(f'<h2>🗣️ {survey["question"]}</h2>', unsafe_allow_html=True)
        st.caption("Live AI Interview Session")
    
    with col_stats:
        # Calculate and display probe usage statistics
        messages = backend.get_messages(survey["id"])
        ai_messages = [m for m in messages if m["role"] == "ai"]
        probes_used = max(0, len(ai_messages) - 1)  # Exclude initial question
        
        st.markdown(f"""
        <div style='text-align: center; padding: 0.5rem; background: rgba(30, 30, 46, 0.7); border-radius: 12px;'>
            <div style='color: #a855f7; font-weight: 600;'>Probes Used</div>
            <div style='color: white; font-size: 1.5rem; font-weight: 700;'>{probes_used}/{survey["probes"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # CHAT MESSAGES DISPLAY
    messages = backend.get_messages(survey["id"])
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not messages:
        # Empty state for new conversation
        st.markdown("""
        <div style='text-align: center; padding: 3rem; color: #64748b;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>💬</div>
            <h3 style='color: #94a3b8;'>Interview Ready</h3>
            <p>The AI interviewer is prepared. Start the conversation!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display conversation history
        for message in messages:
            if message["role"] == "user":
                # User message bubble (right-aligned)
                current_time = time_module.strftime("%m/%d/%y, %I:%M %p")
                
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-end; margin: 1rem 0;'>
                        <div class="user-bubble">
                            <div style='font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.5rem;'>You</div>
                            {message['content']}
                            <div class="message-time">{current_time}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                # AI message bubble (left-aligned)
                clean_content = re.sub(r'</?div[^>]*>', '', message['content'])
                clean_content = re.sub(r'<.*?>', '', clean_content)
                clean_content = clean_content.strip()
                
                st.markdown(
                    f"""
                    <div style='display: flex; align-items: flex-start; margin: 1rem 0;'>
                        <div style='font-size: 2rem; margin-right: 0.5rem;'>🤖</div>
                        <div class="ai-bubble">
                            <div style='font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.5rem;'>AI Interviewer</div>
                            {clean_content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # CHECK INTERVIEW COMPLETION STATUS
    messages = backend.get_messages(survey["id"])
    ai_messages = [m for m in messages if m["role"] == "ai"]
    probes_used = max(0, len(ai_messages) - 1)
    
    interview_complete = False
    if messages and len(ai_messages) > 0:
        last_ai_message = ai_messages[-1]["content"].lower()
        # Check for completion keywords in last AI message
        if any(word in last_ai_message for word in ["thank you", "complete", "finished", "participation"]):
            interview_complete = True
            backend.mark_survey_complete(survey["id"])

    # Show completion screen if interview is finished
    if interview_complete or probes_used >= survey["probes"]:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: rgba(34, 197, 94, 0.1); border-radius: 16px; border: 1px solid rgba(34, 197, 94, 0.3);'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🎉</div>
            <h3 style='color: #4ade80;'>Interview Completed!</h3>
            <p style='color: #94a3b8;'>Thank you for participating in this research survey.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Return to Dashboard", type="primary", use_container_width=True):
            navigate("home")
            
    else:
        # ACTIVE INTERVIEW INPUT AREA
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        # Voice recording indicator
        if st.session_state.audio_data:
            st.markdown(
                '<div class="voice-indicator">🎤 Voice recorded - Ready to send</div>',
                unsafe_allow_html=True
            )
        
        # Split input area into text and voice sections
        col_text, col_voice = st.columns([3, 1])
        
        user_input = None  # Will store final user input
        
        with col_text:
            # Text input form
            with st.form(key='text_input_form', clear_on_submit=True):
                answer = st.text_area(
                    "Type your response here...",
                    height=80,
                    placeholder="Type your response here...",
                    label_visibility="collapsed",
                    key="text_input"
                )
                
                submit_col1, submit_col2 = st.columns([2, 1])
                with submit_col2:
                    text_submitted = st.form_submit_button(
                        "Send Text", 
                        type="primary", 
                        use_container_width=True
                    )

                if text_submitted and answer.strip():
                    user_input = answer.strip()

        with col_voice:
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            
            # Voice recording input
            audio = st.audio_input(
                "Record your voice response", 
                label_visibility="collapsed",
                key="voice_input"
            )
            
            if audio:
                st.session_state.audio_data = audio
                st.success("✅ Voice recorded!")
            
            # Voice action buttons
            if st.session_state.audio_data:
                voice_col1, voice_col2 = st.columns(2)
                with voice_col1:
                    if st.button("Send Voice", type="primary", use_container_width=True, key="send_voice"):
                        with st.spinner("🔄 Transcribing..."):
                            try:
                                # Transcribe audio to text
                                transcription = backend.transcribe_audio(st.session_state.audio_data.getvalue())
                                if transcription and not transcription.startswith("Error:"):
                                    user_input = transcription
                                    st.session_state.audio_data = None
                                    st.success("Voice sent successfully!")
                                else:
                                    st.error("Could not transcribe audio. Please try again.")
                            except Exception as e:
                                st.error(f"Transcription error: {str(e)}")
                
                with voice_col2:
                    if st.button("Clear", use_container_width=True, key="clear_voice"):
                        st.session_state.audio_data = None
                        st.rerun()
            else:
                st.info("Click to record voice")
        
        st.markdown(
            '<div class="instruction-text">Press Enter to send text or use voice input</div>',
            unsafe_allow_html=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

        # SESSION INFORMATION PANEL
        with st.expander("📊 Session Information"):
            # Display survey metadata and statistics
            st.markdown("**Research Question**")
            st.info(survey['question'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Probes Used", f"{probes_used}/{survey['probes']}")
                st.metric("Time Limit", f"{survey['length']}s")
            with col2:
                st.metric("Language", survey['language'])
                st.metric("Status", "Active", delta="Active" if not interview_complete else "Completed")

        # PROCESS USER INPUT AND GENERATE AI RESPONSE
        if user_input:
            # Store user message in database
            backend.add_message(survey["id"], "user", user_input)
            
            thinking_placeholder = st.empty()
            with thinking_placeholder.container():
                with st.spinner("🤔 AI interviewer is thinking..."):
                    time_module.sleep(0.5)  # Brief pause for better UX
                    
                    try:
                        # Get updated message history
                        current_messages = backend.get_messages(survey["id"])
                        ai_messages_count = len([m for m in current_messages if m["role"] == "ai"])
                        
                        # Generate AI response
                        ai_response = backend.generate_ai_response(
                            messages=current_messages,
                            user_input=user_input,
                            survey_question=survey["question"],
                            probes_asked=ai_messages_count,
                            limit=survey["probes"]
                        )
                        # Store AI response in database
                        backend.add_message(survey["id"], "ai", ai_response)
                            
                    except Exception as e:
                        # Fallback response on error
                        fallback_response = "Thank you for sharing. What would you like to add?"
                        backend.add_message(survey["id"], "ai", fallback_response)
            
            thinking_placeholder.empty()
            st.rerun()  # Refresh to show new messages

# =============================================================================
# APPLICATION ROUTER
# =============================================================================

# Route to appropriate view based on current page state
if st.session_state.page == "home":
    view_home()
elif st.session_state.page == "create":
    view_create()
elif st.session_state.page == "chat":
    view_chat()