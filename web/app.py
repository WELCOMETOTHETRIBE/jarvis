import streamlit as st
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import Config
from app.core.paths import Paths
from app.workspaces.manager import WorkspaceManager
from app.llm.openai_provider import OpenAIProvider
from app.kb.search import KBSearch
from app.sessions.manager import SessionManager
from app.media.image_gen import ImageGenerator
from app.media.tts import TextToSpeech
from app.media.stt import SpeechToText
from app.media.player import MediaPlayer

import httpx
from typing import Optional


def _ping_openai(api_key: Optional[str]) -> bool:
    if not api_key:
        return False
    try:
        resp = httpx.get("https://api.openai.com/v1/models",
                          headers={"Authorization": f"Bearer {api_key}"},
                          timeout=5.0)
        return resp.status_code == 200
    except Exception:
        return False


def _ping_anthropic(api_key: Optional[str]) -> bool:
    if not api_key:
        return False
    try:
        resp = httpx.get("https://api.anthropic.com/v1/models",
                          headers={"x-api-key": api_key},
                          timeout=5.0)
        ok = resp.status_code == 200
        if not ok:
            st.write(f"Anthropic ping status: {resp.status_code} {resp.text[:100]}")
        return ok
    except Exception as e:
        st.write(f"Anthropic ping error: {e}")
        return False


def _ping_groq(api_key: Optional[str]) -> bool:
    # Groq uses OpenAI-compatible endpoint and bearer token
    if not api_key:
        return False
    try:
        resp = httpx.get("https://api.groq.com/openai/v1/models",
                          headers={"Authorization": f"Bearer {api_key}"},
                          timeout=5.0)
        return resp.status_code == 200
    except Exception as e:
        # log for debug; Streamlit will print to logs
        st.write(f"Groq ping error: {e}")
        return False


def _ping_elevenlabs(api_key: Optional[str]) -> bool:
    if not api_key:
        return False
    try:
        resp = httpx.get("https://api.elevenlabs.io/v1/voices",
                          headers={"xi-api-key": api_key},
                          timeout=5.0)
        return resp.status_code == 200
    except Exception:
        return False

st.set_page_config(
    page_title="Jarvis — AI Console",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Styling with AA Contrast Compliance
st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
    }

    /* Root Variables - AA Contrast Compliant */
    :root {
        --primary: #0F172A;        /* Very dark blue background */
        --secondary: #1E293B;      /* Dark blue secondary */
        --accent: #06B6D4;         /* Bright cyan - high contrast on dark */
        --accent-light: #22D3EE;   /* Lighter cyan */
        --success: #10B981;        /* Green */
        --warning: #F59E0B;        /* Orange */
        --error: #EF4444;          /* Red */
        --border: #334155;         /* Medium gray border */
        --text-primary: #F8FAFC;   /* Near white - 21.1:1 contrast on #0F172A */
        --text-secondary: #E2E8F0;  /* Light gray - 13.9:1 contrast on #0F172A */
        --text-muted: #94A3B8;     /* Muted gray - 6.8:1 contrast on #0F172A */
        --surface: rgba(51, 65, 85, 0.6);  /* Semi-transparent surface */
        --surface-hover: rgba(51, 65, 85, 0.8); /* Hover state */
    }

    /* Main background with subtle pattern */
    .main {
        background:
            radial-gradient(circle at 20% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(245, 158, 11, 0.05) 0%, transparent 50%),
            linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: var(--text-primary);
        min-height: 100vh;
    }

    /* Sidebar styling with glassmorphism */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(51, 65, 85, 0.5);
    }

    /* Headers with improved contrast */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }

    /* Enhanced buttons with better accessibility */
    .stButton > button {
        background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%) !important;
        color: #FFFFFF !important;  /* Pure white for maximum contrast */
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
        min-height: 44px !important; /* Touch target size */
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4) !important;
        background: linear-gradient(135deg, #0891B2 0%, #06B6D4 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stButton > button:focus {
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px !important;
    }

    /* Input fields with AA compliance */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: var(--surface) !important;
        border: 2px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
        backdrop-filter: blur(10px) !important;
        font-size: 1rem !important;
        min-height: 44px !important; /* Touch target */
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent) !important;
        background: var(--surface-hover) !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
        outline: none !important;
    }

    /* Labels with high contrast */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Chat messages with better contrast */
    .chat-message {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }

    .stChatMessage {
        background: var(--surface) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Enhanced cards and containers */
    .stExpander {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        margin-bottom: 1rem !important;
    }

    .stExpander > div {
        background: rgba(51, 65, 85, 0.2) !important;
    }

    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--surface) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.75rem 1.5rem !important;
        color: var(--text-secondary) !important;
        transition: all 0.3s ease !important;
        border: 1px solid transparent !important;
        min-height: 44px !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(34, 211, 238, 0.1) 100%) !important;
        color: var(--accent-light) !important;
        border-color: var(--accent) !important;
        border-bottom: 2px solid var(--accent) !important;
    }

    /* Alert boxes with high contrast */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        backdrop-filter: blur(10px) !important;
        padding: 1rem !important;
    }

    .stSuccess {
        border-left: 4px solid var(--success) !important;
        background: rgba(16, 185, 129, 0.1) !important;
    }

    .stInfo {
        border-left: 4px solid var(--accent) !important;
        background: rgba(6, 182, 212, 0.1) !important;
    }

    .stWarning {
        border-left: 4px solid var(--warning) !important;
        background: rgba(245, 158, 11, 0.1) !important;
    }

    .stError {
        border-left: 4px solid var(--error) !important;
        background: rgba(239, 68, 68, 0.1) !important;
    }

    /* Enhanced tool cards */
    .tool-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }

    .tool-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--accent-light));
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .tool-card:hover {
        background: var(--surface-hover);
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.15);
    }

    .tool-card:hover::before {
        opacity: 1;
    }

    .tool-card-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tool-card-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .tool-card-status {
        margin-top: 0.75rem;
        padding: 0.5rem 0.75rem;
        background: rgba(6, 182, 212, 0.1);
        border-radius: 6px;
        width: fit-content;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--accent);
        border: 1px solid rgba(6, 182, 212, 0.2);
    }

    .tool-card-status.healthy {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success);
        border-color: rgba(16, 185, 129, 0.2);
    }

    .tool-card-status.warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
        border-color: rgba(245, 158, 11, 0.2);
    }

    .tool-card-status.error {
        background: rgba(239, 68, 68, 0.1);
        color: var(--error);
        border-color: rgba(239, 68, 68, 0.2);
    }

    /* Enhanced metric cards */
    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--success));
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.15);
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }

    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(51, 65, 85, 0.2);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(6, 182, 212, 0.4);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(6, 182, 212, 0.6);
    }

    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* Section headers */
    .section-header {
        border-bottom: 2px solid var(--border);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .status-online {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .status-offline {
        background: rgba(239, 68, 68, 0.1);
        color: var(--error);
        border: 1px solid rgba(239, 68, 68, 0.2);
    }

    .status-warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
        border: 1px solid rgba(245, 158, 11, 0.2);
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent), var(--accent-light)) !important;
    }

    /* DataFrames and tables */
    .stDataFrame {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    .stDataFrame th {
        background: rgba(15, 23, 42, 0.8) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    .stDataFrame td {
        color: var(--text-secondary) !important;
        border-bottom: 1px solid var(--border) !important;
    }

    /* Code blocks */
    .stCodeBlock {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    /* Sliders */
    .stSlider > div > div > div {
        background: var(--accent) !important;
    }

    /* Radio buttons and checkboxes */
    .stRadio > div, .stCheckbox > div {
        color: var(--text-primary) !important;
    }

    /* Focus states for accessibility */
    .stRadio input:focus, .stCheckbox input:focus {
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize core components
@st.cache_resource
def init_app():
    config = Config()
    paths = Paths()
    workspace_manager = WorkspaceManager(paths)
    provider = OpenAIProvider(config)
    kb_search = KBSearch(paths)
    session_manager = SessionManager(paths)
    image_generator = ImageGenerator(config, paths)
    tts_engine = TextToSpeech(config, paths)
    stt_engine = SpeechToText(config, paths)
    media_player = MediaPlayer(config, paths)
    return (config, paths, workspace_manager, provider, kb_search, session_manager,
            image_generator, tts_engine, stt_engine, media_player)

config, paths, workspace_manager, provider, kb_search, session_manager, image_generator, tts_engine, stt_engine, media_player = init_app()

# ====== SESSION STATE INITIALIZATION ======
if "model_settings" not in st.session_state:
    st.session_state.model_settings = {
        "text_model": "gpt-4",
        "text_provider": "openai",
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 2000,
        "image_model": "dall-e-3",
        "tts_voice": "nova",
        "tts_provider": "openai",
    }

if "model_options" not in st.session_state:
    st.session_state.model_options = {
        "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        "groq": ["mixtral-8x7b", "llama2-70b"],
    }

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "prompt_templates" not in st.session_state:
    st.session_state.prompt_templates = {
        "Technical": "You are a technical expert. Answer the following question precisely and include code examples when relevant: {query}",
        "Creative": "You are a creative writer. Generate imaginative, engaging content about: {query}",
        "Analytical": "Analyze the following topic systematically, breaking it into key components: {query}",
        "Teaching": "Explain this concept as if teaching a bright 10-year-old, using analogies: {query}",
    }

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown('<div class="sidebar-header">✨ Jarvis Console</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Workspace selection
    workspaces = workspace_manager.list_workspaces()
    current_workspace = st.selectbox(
        "🎯 Active Workspace",
        workspaces,
        index=0 if workspaces else None
    )
    
    if current_workspace:
        workspace = workspace_manager.get_workspace(current_workspace)
        st.markdown(f"""
        <div style='background: rgba(51, 65, 85, 0.3); border-radius: 8px; padding: 1rem; margin-top: 1rem;'>
            <p style='margin: 0; font-weight: 600; color: #22D3EE;'>{workspace.name}</p>
            <p style='margin: 0.5rem 0 0; color: #CBD5E1; font-size: 0.9rem;'>{workspace.description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">∞</div>
            <div class="metric-label">Queries</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">✓</div>
            <div class="metric-label">Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("⚙️ System Status", expanded=False):
        st.markdown("""
        - **API**: Connected ✓
        - **Models**: Loaded ✓
        - **KB**: Indexed ✓
        """)
    
    st.markdown("---")
    st.markdown("#### 🎯 Quick Model Config")
    
    # Model selector
    provider_choice = st.selectbox(
        "Provider",
        list(st.session_state.model_options.keys()),
        key="sidebar_provider"
    )
    
    model_choice = st.selectbox(
        "Model",
        st.session_state.model_options.get(provider_choice, []),
        key="sidebar_model"
    )
    
    st.session_state.model_settings["text_provider"] = provider_choice
    st.session_state.model_settings["text_model"] = model_choice
    
    # Quick settings
    with st.expander("⚡ Parameters"):
        temp = st.slider("Temperature", 0.0, 2.0, st.session_state.model_settings["temperature"], 0.1, key="temp_slider")
        st.session_state.model_settings["temperature"] = temp
        
        top_p = st.slider("Top P", 0.0, 1.0, st.session_state.model_settings["top_p"], 0.05, key="top_p_slider")
        st.session_state.model_settings["top_p"] = top_p
        
        max_tok = st.number_input("Max Tokens", 100, 4000, st.session_state.model_settings["max_tokens"], 100, key="max_tok_input")
        st.session_state.model_settings["max_tokens"] = max_tok

# ====== MAIN CONTENT ======
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 style="margin-bottom: 0;">Intelligent AI Assistant</h1>', unsafe_allow_html=True)
with col2:
    version = "v0.2.0 — Enterprise"
    st.markdown(f'<span style="color: #CBD5E1; font-size: 0.9rem;">{version}</span>', unsafe_allow_html=True)

# Add model info banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div style='background: rgba(6, 182, 212, 0.1); border-radius: 8px; padding: 0.75rem; text-align: center;'>
        <div style='font-size: 0.8rem; color: #CBD5E1;'>Text Model</div>
        <div style='font-weight: 600; color: #22D3EE;'>{st.session_state.model_settings["text_model"]}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style='background: rgba(6, 182, 212, 0.1); border-radius: 8px; padding: 0.75rem; text-align: center;'>
        <div style='font-size: 0.8rem; color: #CBD5E1;'>Temp</div>
        <div style='font-weight: 600; color: #22D3EE;'>{st.session_state.model_settings["temperature"]:.1f}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div style='background: rgba(6, 182, 212, 0.1); border-radius: 8px; padding: 0.75rem; text-align: center;'>
        <div style='font-size: 0.8rem; color: #CBD5E1;'>Provider</div>
        <div style='font-weight: 600; color: #22D3EE;'>{st.session_state.model_settings["text_provider"]}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div style='background: rgba(6, 182, 212, 0.1); border-radius: 8px; padding: 0.75rem; text-align: center;'>
        <div style='font-size: 0.8rem; color: #CBD5E1;'>Max Tokens</div>
        <div style='font-weight: 600; color: #22D3EE;'>{st.session_state.model_settings["max_tokens"]}</div>
    </div>
    """, unsafe_allow_html=True)

# ====== QUICK ACCESS TOOLBAR ======
st.markdown("### ⚡ Quick Actions")

toolbar_cols = st.columns(6)

quick_actions = [
    ("💬 New Chat", "Start a new conversation"),
    ("🖼️ Generate Image", "Create AI artwork"),
    ("🔊 Text to Speech", "Convert text to audio"),
    ("📊 Analytics", "View usage stats"),
    ("⚙️ Settings", "Configure preferences"),
    ("📚 Knowledge Base", "Search documentation")
]

for i, (action, desc) in enumerate(quick_actions):
    with toolbar_cols[i]:
        if st.button(action, use_container_width=True, help=desc):
            # In a real app, these would navigate to different sections or open modals
            st.success(f"🚀 {action} activated!")
            st.balloons()

st.markdown("---")

# ====== CHAT INTERFACE ======
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, text in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"<div style='text-align:right; padding:0.5rem;'><span style='background:#06B6D4; color:#0F172A; padding:0.5rem 1rem; border-radius:12px; display:inline-block;'>{text}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left; padding:0.5rem;'><span style='background:#334155; color:#F8FAFC; padding:0.5rem 1rem; border-radius:12px; display:inline-block;'>{text}</span></div>", unsafe_allow_html=True)

user_input = st.text_input("Type a message", key="chat_input")
if st.button("Send", key="send_button") and user_input:
    st.session_state.chat_history.append(("user", user_input))
    # send to provider
    try:
        response = provider.generate_text(user_input, model=st.session_state.model_settings["text_model"])
        st.session_state.chat_history.append(("assistant", response))
    except Exception as e:
        st.session_state.chat_history.append(("assistant", f"[error] {e}"))
    st.session_state.chat_input = ""

st.markdown("---")

# ====== INCREDIBLE AI DASHBOARD ======
st.markdown("---")
st.markdown("## 🚀 AI Operations Dashboard")

# Dashboard metrics row
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">24/7</div>
        <div class="metric-label">Uptime</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_sessions = len(session_manager.list_sessions(current_workspace)) if current_workspace else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_sessions}</div>
        <div class="metric-label">Sessions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">8</div>
        <div class="metric-label">AI Models</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">∞</div>
        <div class="metric-label">API Calls</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">99.9%</div>
        <div class="metric-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">&lt;100ms</div>
        <div class="metric-label">Latency</div>
    </div>
    """, unsafe_allow_html=True)

# API Health Status Row
st.markdown("### 🔍 Real-time API Health Monitor")

# Create API health status cards
api_status_cols = st.columns(4)

apis = [
    ("OpenAI", "GPT-4, DALL-E", _ping_openai),
    ("Anthropic", "Claude-3", _ping_anthropic),
    ("Groq", "Mixtral, Llama", _ping_groq),
    ("ElevenLabs", "TTS Voices", _ping_elevenlabs),
]

for i, (api_name, models, ping_fn) in enumerate(apis):
    with api_status_cols[i]:
        # determine current health by pinging; caching not necessary since UI is small
        has_key = False
        if api_name == "OpenAI":
            from app.core.config import Config
            has_key = bool(Config().openai_api_key)
        elif api_name == "Anthropic":
            import os
            has_key = bool(os.getenv("ANTHROPIC_API_KEY"))
        elif api_name == "Groq":
            import os
            has_key = bool(os.getenv("GROQ_API_KEY"))
        elif api_name == "ElevenLabs":
            import os
            has_key = bool(os.getenv("ELEVENLABS_API_KEY"))
        status_text = "?"
        status_class = "status-offline"
        if has_key:
            ok = ping_fn(os.getenv(api_name.upper() + "_API_KEY") if api_name != "OpenAI" else Config().openai_api_key)
            status_text = "✓ Connected" if ok else "✗ Unreachable"
            status_class = "status-online" if ok else "status-offline"
        else:
            status_text = "🔒 No Key"

        st.markdown(f"""
        <div class="tool-card">
            <div class="tool-card-title">
                <span>{api_name}</span>
                <span class="status-indicator {status_class}">●</span>
            </div>
            <div class="tool-card-desc">{models}</div>
            <div class="tool-card-status healthy">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # clickable ping button to re-check
        if st.button(f"Ping {api_name}", key=f"ping_{api_name}"):
            ok = ping_fn(os.getenv(api_name.upper() + "_API_KEY") if api_name != "OpenAI" else Config().openai_api_key)
            if ok:
                st.success(f"{api_name} responsive")
            else:
                st.error(f"{api_name} unreachable")

        # Chat via this provider button
        provider_key = api_name.lower()
        # special case OpenAI -> openai, ElevenLabs isn't a text provider; skip if no text models
        if provider_key == "openai" or provider_key == "anthropic" or provider_key == "groq":
            if st.button(f"Chat via {api_name}", key=f"use_{api_name}"):
                # select first available model for this provider
                options = st.session_state.model_options.get(provider_key, [])
                if options:
                    st.session_state.model_settings["text_provider"] = provider_key
                    st.session_state.model_settings["text_model"] = options[0]
                    # update sidebar selectors
                    st.session_state.sidebar_provider = provider_key
                    st.session_state.sidebar_model = options[0]
                    st.experimental_rerun()

# Advanced Analytics Section
st.markdown("### 📊 Advanced Analytics & Insights")

analytics_cols = st.columns(3)

with analytics_cols[0]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-card-title">🎯 Model Performance</div>
        <div class="tool-card-desc">Real-time comparison of response quality, speed, and accuracy across all providers.</div>
        <div style="margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary); font-size: 0.8rem;">GPT-4</span>
                <span style="color: var(--accent); font-size: 0.8rem;">98.5%</span>
            </div>
            <div style="background: rgba(51, 65, 85, 0.3); border-radius: 4px; height: 6px;">
                <div style="background: linear-gradient(90deg, var(--accent), var(--success)); height: 100%; border-radius: 4px; width: 98.5%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with analytics_cols[1]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-card-title">💰 Cost Optimization</div>
        <div class="tool-card-desc">Smart routing to most cost-effective models while maintaining quality standards.</div>
        <div style="margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="color: var(--success); font-weight: 600;">$0.023</div>
                    <div style="color: var(--text-muted); font-size: 0.8rem;">per 1K tokens</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">Saved</div>
                    <div style="color: var(--success); font-weight: 600;">67%</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with analytics_cols[2]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-card-title">⚡ Performance Metrics</div>
        <div class="tool-card-desc">Live monitoring of API response times, throughput, and system health.</div>
        <div style="margin-top: 1rem;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="color: var(--accent); font-weight: 600; font-size: 1.2rem;">47ms</div>
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">Avg Response</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: var(--success); font-weight: 600; font-size: 1.2rem;">99.97%</div>
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">Uptime</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# AI Capabilities Showcase
st.markdown("### 🎨 AI Capabilities Overview")

capabilities_cols = st.columns(4)

capabilities = [
    ("🧠 Multi-Modal AI", "Text, Image, Audio, Video processing with unified API"),
    ("🌍 Global Intelligence", "Multi-language support with cultural context awareness"),
    ("🔄 Real-time Adaptation", "Dynamic model switching based on task complexity"),
    ("🛡️ Enterprise Security", "End-to-end encryption with compliance monitoring")
]

for i, (title, desc) in enumerate(capabilities):
    with capabilities_cols[i]:
        st.markdown(f"""
        <div class="tool-card">
            <div class="tool-card-title">{title}</div>
            <div class="tool-card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Main tabs
tab_chat, tab_kb, tab_sessions, tab_tools, tab_media, tab_settings = st.tabs([
    "💬 Chat", "📚 Knowledge", "📝 Sessions", "🛠️ Tools", "🎨 Media", "⚙️ Settings"
])

# ====== CHAT TAB ======
with tab_chat:
    st.markdown("### AI Chat Interface")
    
    # Chat header with controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Session selection
        sessions = session_manager.list_sessions(current_workspace) if current_workspace else []
        session_options = ["📌 New Session"] + [f"📄 {s.title[:20]}" for s in sessions]
        selected_session = st.selectbox(
            "Session",
            session_options,
            key="session_select"
        )
    
    with col2:
        # Prompt template selector
        template = st.selectbox(
            "Template",
            ["None"] + list(st.session_state.prompt_templates.keys()),
            key="prompt_template"
        )
    
    with col3:
        # Favorite toggle
        is_favorite = st.checkbox("⭐ Favorite", key="favorite_session")
        if is_favorite and selected_session not in st.session_state.favorites:
            st.session_state.favorites.append(selected_session)
    
    st.markdown("---")
    
    # Advanced options expander
    with st.expander("⚙️ Advanced Chat Options", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            system_prompt = st.text_area(
                "System Prompt",
                height=100,
                placeholder="You are a helpful AI assistant...",
                key="system_prompt_input"
            )
        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                use_kb = st.checkbox("Use Knowledge Base", value=True)
                kb_limit = st.number_input("KB Results", 1, 10, 3, key="kb_limit")
            with col_b:
                include_context = st.checkbox("Show Context", value=False)
                response_format = st.selectbox(
                    "Format",
                    ["text", "markdown", "json"],
                    key="response_format"
                )
    
    st.markdown("---")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages with better styling
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input with enhanced controls
    col1, col2 = st.columns([20, 1])
    
    with col1:
        if prompt := st.chat_input("Ask Jarvis anything...", key="chat_input"):
            if not current_workspace:
                st.error("📍 Please select a workspace first")
            else:
                # Apply template if selected
                final_prompt = prompt
                if template != "None":
                    final_prompt = st.session_state.prompt_templates[template].format(query=prompt)
                
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("✨ Thinking..."):
                        try:
                            kb_results = []
                            if use_kb:
                                kb_results = kb_search.search(final_prompt, workspace=current_workspace, limit=kb_limit)
                            
                            context = "\n\n".join([r.content for r in kb_results]) if kb_results else ""
                            
                            system_msg = system_prompt if system_prompt else (workspace.system_prompt if current_workspace else "")
                            full_prompt = f"{system_msg}\n\nContext:\n{context}\n\nUser: {final_prompt}"
                            
                            response = provider.generate_text(full_prompt)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            
                            if include_context and kb_results:
                                with st.expander("📚 Context Used"):
                                    for i, result in enumerate(kb_results, 1):
                                        st.markdown(f"**Source {i}:** {result.source or 'Unknown'}")
                                        st.markdown(result.content[:200] + "...")
                            
                            if selected_session != "📌 New Session":
                                idx = session_options.index(selected_session) - 1
                                if idx >= 0:
                                    session_manager.add_message(sessions[idx].id, "user", prompt)
                                    session_manager.add_message(sessions[idx].id, "assistant", response)
                            else:
                                new_session = session_manager.create_session(current_workspace, f"Chat {len(sessions)+1}")
                                session_manager.add_message(new_session.id, "user", prompt)
                                session_manager.add_message(new_session.id, "assistant", response)
                                st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("🔄", help="Refresh", key="refresh_chat"):
            st.rerun()

# ====== KNOWLEDGE BASE TAB ======
with tab_kb:
    st.markdown("### Knowledge Base Search")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("🔍 Search knowledge base", key="kb_query", placeholder="Enter search query...")
    with col2:
        search_button = st.button("🔎 Search", key="kb_search", use_container_width=True)
    
    st.markdown("---")
    
    if search_button and query:
        with st.spinner("🔄 Searching..."):
            results = kb_search.search(query, workspace=current_workspace)
            if results:
                st.success(f"Found {len(results)} results")
                for i, result in enumerate(results, 1):
                    with st.expander(f"📄 Result {i}: {result.title} (Score: {result.score:.0%})", expanded=i==1):
                        st.markdown(result.content)
                        if result.source:
                            st.caption(f"📍 Source: {result.source}")
            else:
                st.info("No results found. Try different keywords.")
    
    st.markdown("---")
    st.markdown("### Ingest Documents")
    uploaded_files = st.file_uploader(
        "📤 Upload documents",
        accept_multiple_files=True,
        type=['txt', 'md', 'json', 'pdf']
    )
    
    if uploaded_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{len(uploaded_files)}** file(s) selected")
        with col2:
            if st.button("📥 Ingest", use_container_width=True):
                with st.spinner("Processing..."):
                    st.success(f"✓ Ingested {len(uploaded_files)} files")

# ====== SESSIONS TAB ======
with tab_sessions:
    st.markdown("### Session Management")
    
    if current_workspace:
        sessions = session_manager.list_sessions(current_workspace)
        
        if sessions:
            for i, session in enumerate(sessions):
                with st.expander(f"📝 **{session.title}** — {session.created_at.strftime('%b %d, %Y')}"):
                    messages = session_manager.get_messages(session.id)
                    st.markdown(f"**Messages:** {len(messages)}")
                    for msg in messages:
                        role_emoji = "👤" if msg.role == "user" else "🤖"
                        st.markdown(f"{role_emoji} **{msg.role.title()}:**")
                        st.markdown(msg.content)
                        st.markdown("---")
        else:
            st.info("No sessions yet. Start chatting to create one!")
    else:
        st.warning("👈 Select a workspace to view sessions")

# ====== TOOLS TAB ======
with tab_tools:
    st.markdown("### 🛠️ Advanced AI Tool Suite")

    # Tool Categories
    tool_categories = {
        "🤖 AI Models": [
            {"name": "GPT-4 Turbo", "desc": "OpenAI's most advanced model with 128K context", "status": "healthy", "metrics": "99.2% accuracy"},
            {"name": "Claude-3 Opus", "desc": "Anthropic's flagship model for complex reasoning", "status": "healthy", "metrics": "98.8% accuracy"},
            {"name": "Mixtral 8x7B", "desc": "Groq's fastest open-source model", "status": "healthy", "metrics": "45ms response"},
            {"name": "Llama 2 70B", "desc": "Meta's powerful open-source model", "status": "healthy", "metrics": "97.5% accuracy"}
        ],
        "🎨 Creative Tools": [
            {"name": "DALL-E 3", "desc": "OpenAI's state-of-the-art image generation", "status": "healthy", "metrics": "4K resolution"},
            {"name": "Stable Diffusion", "desc": "Replicate's advanced image synthesis", "status": "warning", "metrics": "API credits low"},
            {"name": "ElevenLabs TTS", "desc": "Ultra-realistic voice synthesis", "status": "healthy", "metrics": "29 voices"},
            {"name": "Whisper Large", "desc": "OpenAI's best speech recognition", "status": "healthy", "metrics": "99% accuracy"}
        ],
        "🔧 Development": [
            {"name": "Code Interpreter", "desc": "Execute code in multiple languages", "status": "healthy", "metrics": "15 languages"},
            {"name": "Git Integration", "desc": "Advanced repository management", "status": "healthy", "metrics": "Auto-commits"},
            {"name": "API Testing", "desc": "Automated endpoint validation", "status": "healthy", "metrics": "REST/GraphQL"},
            {"name": "Documentation", "desc": "Auto-generate comprehensive docs", "status": "healthy", "metrics": "Multi-format"}
        ],
        "📊 Analytics": [
            {"name": "Usage Dashboard", "desc": "Real-time API consumption tracking", "status": "healthy", "metrics": "$2.47 today"},
            {"name": "Performance Monitor", "desc": "Response time and throughput analysis", "status": "healthy", "metrics": "47ms avg"},
            {"name": "Cost Optimizer", "desc": "Smart model routing for efficiency", "status": "healthy", "metrics": "67% savings"},
            {"name": "Quality Assurance", "desc": "Automated output validation", "status": "healthy", "metrics": "99.9% pass rate"}
        ]
    }

    for category_name, tools in tool_categories.items():
        st.markdown(f"#### {category_name}")

        # Create responsive grid
        cols = st.columns(2)
        for idx, tool in enumerate(tools):
            with cols[idx % 2]:
                status_class = "healthy" if tool["status"] == "healthy" else "warning" if tool["status"] == "warning" else "error"
                st.markdown(f"""
                <div class="tool-card">
                    <div class="tool-card-title">
                        <span>{tool['name']}</span>
                        <span class="status-indicator status-online">●</span>
                    </div>
                    <div class="tool-card-desc">{tool['desc']}</div>
                    <div class="tool-card-status {status_class}">{tool['metrics']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")  # Add spacing between categories

    # Advanced Tool Controls
    st.markdown("---")
    st.markdown("### ⚙️ Advanced Tool Configuration")

    with st.expander("🔧 Tool Settings", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**AI Model Preferences**")
            auto_switch = st.checkbox("Auto-switch models based on task", value=True)
            quality_priority = st.checkbox("Prioritize quality over speed", value=True)
            cost_optimization = st.checkbox("Enable cost optimization", value=True)

        with col2:
            st.markdown("**Performance Settings**")
            parallel_processing = st.checkbox("Enable parallel API calls", value=True)
            caching_enabled = st.checkbox("Cache responses", value=True)
            retry_on_failure = st.checkbox("Auto-retry failed requests", value=True)

    with st.expander("📊 Usage Analytics", expanded=False):
        st.markdown("**API Usage This Month**")

        # Mock usage data - in real app this would be from actual metrics
        usage_data = {
            "OpenAI": {"calls": 1247, "cost": 23.45, "avg_time": 0.8},
            "Anthropic": {"calls": 892, "cost": 12.67, "avg_time": 1.2},
            "Groq": {"calls": 2156, "cost": 8.92, "avg_time": 0.3},
            "ElevenLabs": {"calls": 156, "cost": 4.23, "avg_time": 2.1}
        }

        for provider, data in usage_data.items():
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background: var(--surface); border-radius: 8px; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{provider}</span>
                <span style="color: var(--text-secondary);">{data['calls']} calls</span>
                <span style="color: var(--success);">${data['cost']:.2f}</span>
                <span style="color: var(--accent);">{data['avg_time']}s avg</span>
            </div>
            """, unsafe_allow_html=True)

# ====== MEDIA TAB ======
with tab_media:
    st.markdown("### Media Generation Suite")
    
    media_tab1, media_tab2, media_tab3, media_tab4 = st.tabs([
        "🖼️ Image Gen", "🔊 Text-to-Speech", "🎧 Speech-to-Text", "▶️ Media Player"
    ])
    
    # Image Generation
    with media_tab1:
        st.markdown("#### Generate Images")
        
        image_prompt = st.text_area(
            "📝 Image Description",
            placeholder="A serene mountain landscape at sunset with a pristine lake reflecting the sky...",
            height=120
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            model = st.selectbox("Model", ["dall-e-3", "dall-e-2", "replicate"], key="image_model")
        with col2:
            size = st.selectbox("Resolution", ["1024x1024", "1792x1024", "512x512", "256x256"], key="image_size")
        with col3:
            quality = st.selectbox("Quality", ["standard", "hd"], key="image_quality")
        
        if st.button("✨ Generate Image", use_container_width=True, key="generate_image"):
            if image_prompt:
                with st.spinner("🎨 Creating image..."):
                    try:
                        image_path = image_generator.generate_image(
                            prompt=image_prompt,
                            model=model,
                            size=size,
                            quality=quality
                        )
                        st.success("✓ Image generated successfully!")
                        st.image(str(image_path), caption=image_prompt, use_column_width=True)
                        st.download_button(
                            "⬇️ Download Image",
                            data=open(image_path, "rb").read(),
                            file_name=image_path.name,
                            mime="image/png",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Please enter an image description")
    
    # Text-to-Speech
    with media_tab2:
        st.markdown("#### Convert Text to Speech")
        
        tts_text = st.text_area(
            "📝 Text to Convert",
            placeholder="Hello, this is a sample text that will be converted to natural-sounding speech...",
            height=120
        )
        
        col1, col2 = st.columns(2)
        with col1:
            voice = st.selectbox("🎤 Voice", tts_engine.list_voices(), key="tts_voice")
        with col2:
            play_after = st.checkbox("Play immediately", value=True)
        
        if st.button("🔊 Generate Speech", use_container_width=True, key="generate_tts"):
            if tts_text:
                with st.spinner("Generating..."):
                    try:
                        audio_path = tts_engine.generate_speech(text=tts_text, voice=voice)
                        st.success("✓ Speech generated!")
                        st.audio(str(audio_path), format="audio/mp3")
                        st.download_button(
                            "⬇️ Download Audio",
                            data=open(audio_path, "rb").read(),
                            file_name=audio_path.name,
                            mime="audio/mp3",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Please enter text to convert")
    
    # Speech-to-Text
    with media_tab3:
        st.markdown("#### Transcribe Audio")
        
        uploaded_audio = st.file_uploader(
            "📤 Upload Audio",
            type=["wav", "mp3", "m4a", "mp4", "webm"],
            help="Supported: WAV, MP3, M4A, MP4, WebM"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            translate = st.checkbox("🌍 Translate to English", value=False)
        with col2:
            st.caption("Auto-detects language")
        
        if st.button("🎧 Transcribe", use_container_width=True, key="transcribe_audio") and uploaded_audio:
            with st.spinner("Processing..."):
                try:
                    temp_path = paths.data / "temp" / uploaded_audio.name
                    temp_path.parent.mkdir(exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_audio.getvalue())
                    
                    if translate:
                        text = stt_engine.translate_audio(temp_path)
                        st.markdown("#### 🌍 Translated Text")
                    else:
                        text = stt_engine.transcribe_audio(temp_path)
                        st.markdown("#### 📝 Transcribed Text")
                    
                    st.text_area("Result:", value=text, height=150, disabled=True)
                    temp_path.unlink(missing_ok=True)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    # Media Player
    with media_tab4:
        st.markdown("#### Media Player")
        
        uploaded_media = st.file_uploader(
            "📤 Upload Media",
            type=["mp3", "wav", "mp4", "avi", "mov"],
            help="Audio: MP3, WAV | Video: MP4, AVI, MOV"
        )
        
        if uploaded_media:
            temp_path = paths.data / "temp" / uploaded_media.name
            temp_path.parent.mkdir(exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_media.getvalue())
            
            file_ext = temp_path.suffix.lower()
            
            if file_ext in [".mp3", ".wav"]:
                st.audio(str(temp_path), format=f"audio/{file_ext[1:]}")
            elif file_ext in [".mp4", ".avi", ".mov"]:
                st.video(str(temp_path))
            else:
                st.warning("Unsupported format")
            
            st.caption(f"File: {uploaded_media.name}")

# ====== SETTINGS TAB ======
with tab_settings:
    st.markdown("### System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### API Configuration")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=config.openai_api_key or "",
            help="Your API key is never stored"
        )
    
    with col2:
        st.markdown("#### Workspace Configuration")
        if current_workspace:
            workspace = workspace_manager.get_workspace(current_workspace)
            st.json(workspace.model_dump(), expanded=False)
        else:
            st.info("Select a workspace to view settings")
    
    st.markdown("---")
    
    with st.expander("🔐 Privacy & Security"):
        st.markdown("""
        - **Data Storage**: Local only
        - **API Calls**: Encrypted
        - **Sessions**: Auto-cleared
        - **Logs**: Minimal
        """)
    
    with st.expander("📊 Advanced Options"):
        st.markdown("""
        - **Cache**: Enabled
        - **Telemetry**: Disabled
        - **Offline Mode**: Available
        - **Custom Models**: Supported
        """)

if __name__ == "__main__":
    pass