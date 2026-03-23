import os
from dotenv import load_dotenv
import streamlit as st

from src.utils.video_extractor import get_video_metadata
from src.core.seo_engine import SEOEngine

from src.common.logger import get_logger
from src.common.custom_exception import CustomException


load_dotenv()

logger = get_logger(__name__)

# Custom CSS for futuristic design
st.set_page_config(
    page_title="YT SEO Insights | AI Generator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic CSS styling
st.markdown("""
<style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0a0f1f, #03050b);
        font-family: 'Inter', 'Space Grotesk', sans-serif;
    }
    
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    /* Card styling */
    .futuristic-card {
        background: rgba(12, 20, 35, 0.55);
        backdrop-filter: blur(12px);
        border-radius: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.25);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .futuristic-card:hover {
        border-color: rgba(0, 255, 255, 0.6);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(95deg, #00c6ff, #0072ff);
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 60px;
        color: white;
        transition: all 0.3s ease;
        width: 100%;
        font-family: 'Space Grotesk', monospace;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(0,114,255,0.4);
        background: linear-gradient(95deg, #1ad0ff, #3f8eff);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid #2a3a5a;
        border-radius: 2rem;
        padding: 0.75rem 1.2rem;
        color: white;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0ff;
        box-shadow: 0 0 15px rgba(0,255,255,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(8, 12, 25, 0.8);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(0,255,255,0.2);
    }
    
    /* Tag pills */
    .tag-pill {
        display: inline-block;
        background: rgba(0, 255, 255, 0.1);
        border-left: 3px solid #0ff;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 2rem;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .tag-pill:hover {
        background: rgba(0, 255, 255, 0.2);
        transform: translateX(3px);
    }
    
    /* Timestamp styling */
    .timestamp-item {
        background: rgba(15, 25, 45, 0.7);
        border-radius: 1rem;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ff44cc;
        transition: all 0.2s ease;
    }
    
    .timestamp-item:hover {
        transform: translateX(5px);
        background: rgba(15, 25, 45, 0.9);
    }
    
    /* Flaw cards */
    .flaw-card {
        background: rgba(30, 20, 40, 0.5);
        border-radius: 1.2rem;
        padding: 1rem;
        margin: 1rem 0;
        border-right: 3px solid #ff7744;
        transition: all 0.2s ease;
    }
    
    .flaw-card:hover {
        transform: translateX(5px);
        border-right-color: #ff44cc;
    }
    
    /* Divider styling */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, #00c6ff, #ff44cc, #00c6ff);
        margin: 2rem 0;
    }
    
    /* Info box styling */
    .stInfo {
        background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,68,204,0.1));
        border-left: 4px solid #0ff;
        border-radius: 1rem;
    }
    
    /* Success message styling */
    .stSuccess {
        background: rgba(0,255,255,0.1);
        border-left: 4px solid #0ff;
        border-radius: 1rem;
    }
    
    /* Error message styling */
    .stError {
        background: rgba(255,68,68,0.1);
        border-left: 4px solid #ff4444;
        border-radius: 1rem;
    }
    
    /* Image styling */
    .stImage img {
        border-radius: 1rem;
        box-shadow: 0 8px 25px rgba(0,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .stImage img:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 35px rgba(0,255,255,0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(0, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(0,255,255,0.2);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #0ff transparent transparent transparent;
    }
    
    /* Code block for tags */
    .stCodeBlock {
        background: rgba(0,0,0,0.6);
        border-radius: 1rem;
        border-left: 4px solid #0ff;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0f1f;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00c6ff, #0072ff);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #1ad0ff, #3f8eff);
    }
    
    /* Glow text effect */
    .glow-text {
        text-shadow: 0 0 10px rgba(0,255,255,0.5);
    }
    
    /* Animated gradient text */
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .gradient-text {
        background: linear-gradient(270deg, #00c6ff, #ff44cc, #00c6ff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: gradientFlow 3s ease infinite;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with futuristic styling
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="background: linear-gradient(135deg, #00c6ff, #ff44cc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ⚡ API NEXUS
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        logger.info("API Key added to environment variables")
        st.success("✅ API Key configured", icon="🔐")
    
    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.85rem; color: #88aaff; text-align: center;">
            <i class="fas fa-robot"></i> AI-Powered SEO Engine v2.0<br>
            <span style="font-size: 0.75rem;">Real-time video optimization</span>
        </div>
    """, unsafe_allow_html=True)

# Main content area with enhanced styling
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="gradient-text" style="font-size: 3rem; font-weight: 800;">
            🚀 Social Media SEO Insights Generator AI
        </h1>
        <p style="font-size: 1.2rem; color: #aaccff;">
            <i class="fas fa-magic"></i> AI Generated Tags · Audience Analysis · Smart Timestamps · Flaw Detection
        </p>
    </div>
""", unsafe_allow_html=True)

# Video URL input with futuristic design
st.markdown("""
    <div class="futuristic-card">
        <h3 style="color: #0ff; margin-bottom: 1rem;">
            <i class="fab fa-youtube"></i> Video URL
        </h3>
    </div>
""", unsafe_allow_html=True)

url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

if "seo_data" not in st.session_state:
    st.session_state.seo_data = None

if url:
    try:
        metadata = get_video_metadata(url)
        
        # Display video details in a stylish card
        with st.container():
            st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                    <h3 style="color: #ff44cc; margin-bottom: 1rem;">
                        <i class="fas fa-film"></i> Video Insights
                    </h3>
                    <p><strong>📹 Title:</strong> <span style="color: #bbffff;">{metadata['title']}</span></p>
                    <p><strong>👤 Creator:</strong> {metadata['author']}</p>
                    <p><strong>👁️ Views:</strong> <span class="glow-text">{metadata['views']:,}</span></p>
                """, unsafe_allow_html=True)
                
                duration = metadata['duration']
                minutes = duration // 60
                seconds = duration % 60
                st.markdown(f"<p><strong>⏱️ Duration:</strong> {minutes} minutes {seconds} seconds</p>", unsafe_allow_html=True)
            
            with col2:
                st.image(metadata['thumbnail_url'], use_column_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate button with enhanced styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Generate AI Insights ✨", use_container_width=True):
                if not os.getenv("OPENAI_API_KEY"):
                    st.error("🔑 Please add your OpenAI API Key in the sidebar first!")
                else:
                    with st.spinner("🧠 AI is analyzing your video content..."):
                        seo_engine = SEOEngine()
                        st.session_state.seo_data = seo_engine.generate(metadata)
                        logger.info("SEO Insights Generated successfully..")
                        st.success("✅ Insights generated successfully!", icon="🎉")
                        st.balloons()
    
    except Exception as e:
        logger.error(f"Unexpected Error : {str(e)}")
        st.error(f"⚠️ Unexpected error: {str(e)}")

# Display SEO results with enhanced styling
data = st.session_state.seo_data
if data:
    # Tags Section
    st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
    st.markdown("""
        <h3 style="color: #0ff; margin-bottom: 1rem;">
            <i class="fas fa-tags"></i> SEO Friendly Tags
        </h3>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, tag in enumerate(data["tags"]):
        with cols[i % 4]:
            st.markdown(f'<span class="tag-pill">#{tag}</span>', unsafe_allow_html=True)
    
    if st.button("📋 Copy Tags", use_container_width=True):
        tag_string = " ".join([f'#{t}' for t in data["tags"]])
        st.code(tag_string, language="text")
        logger.info("Tags copied by user")
        st.toast("🎉 Tags copied to clipboard!", icon="✅")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Audience Analysis Section
    st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
    st.markdown("""
        <h3 style="color: #ff44cc; margin-bottom: 1rem;">
            <i class="fas fa-users"></i> Target Audience Analysis
        </h3>
    """, unsafe_allow_html=True)
    st.markdown(f'<p style="line-height: 1.6;">{data["audience"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Timestamps Section
    st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
    st.markdown("""
        <h3 style="color: #0ff; margin-bottom: 1rem;">
            <i class="fas fa-clock"></i> AI Generated Timestamps 😊
        </h3>
    """, unsafe_allow_html=True)
    
    for ts in data["timestamps"]:
        st.markdown(f"""
            <div class="timestamp-item">
                <strong style="color: #ff44cc;">⏰ {ts['time']}</strong> – {ts['description']}
            </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 These timestamps help improve viewer engagement and SEO rankings", icon="🎯")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Flaws and Improvements Section
    st.markdown('<div class="futuristic-card">', unsafe_allow_html=True)
    st.markdown("""
        <h3 style="color: #ff7744; margin-bottom: 1rem;">
            <i class="fas fa-chart-line"></i> Flaws & Improvements
        </h3>
        <p style="color: #ffaa88;">These issues can hurt your SEO rankings</p>
    """, unsafe_allow_html=True)
    
    for flaw in data["flaws"]:
        st.markdown(f"""
            <div class="flaw-card">
                <p><strong style="color: #ff7777;">❌ Issue:</strong> {flaw['issue']}</p>
                <p><strong style="color: #ffaa66;">⚡ Why It Hurts:</strong> {flaw['why_it_hurts']}</p>
                <p><strong style="color: #88ff88;">✅ Fix:</strong> {flaw['fix']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with additional metrics
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 1rem;">
            <p style="color: #88aaff;">
                <i class="fas fa-chart-bar"></i> AI-Powered SEO Analysis | 
                <i class="fas fa-rocket"></i> Optimize for Viral Growth | 
                <i class="fas fa-shield-alt"></i> Real-time Insights
            </p>
        </div>
    """, unsafe_allow_html=True)



