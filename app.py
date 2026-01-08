import streamlit as st
import datetime
import random
import string
import time
import firebase_admin
from firebase_admin import credentials, db
from groq import Groq
import os
from typing import Dict, List, Optional, Union

# =========================================================
# CONFIGURATION & CONSTANTS
# =========================================================
st.set_page_config(
    page_title="SAMRION Technologies",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Security Constants
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ilovesamriddhisoni28oct")
SESSION_TIMEOUT_MINUTES = 30

# Tool Configuration
TOOLS = {
    "MEDHA": {
        "icon": "🧠",
        "url": "https://medha-ai.streamlit.app/",
        "description": "AI Brain - Advanced Reasoning"
    },
    "AKRITI": {
        "icon": "🎨",
        "url": "https://akriti.streamlit.app/",
        "description": "Creative Image Generation"
    },
    "VANI": {
        "icon": "🎙️",
        "url": "https://vaani-labs.streamlit.app/",
        "description": "Voice Synthesis & Cloning"
    },
    "SANGRAH": {
        "icon": "📦",
        "url": "https://sangrah.streamlit.app/",
        "description": "Dataset Collection Engine"
    },
    "CODIQ": {
        "icon": "💻",
        "url": "https://codiq-ai.streamlit.app/",
        "description": "Code Generation Assistant"
    }
}

# =========================================================
# ENHANCED CSS WITH LOGO SUPPORT
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

/* Force Dark Theme */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 50% 10%, #0f172a 0%, #000000 100%);
    color: white;
}

* { 
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

/* Headers */
h1, h2, h3 { 
    font-family: 'Outfit', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: 2px;
    color: white !important;
}

/* Logo Styling */
.logo-container {
    text-align: center;
    margin-bottom: 30px;
}

.logo-container img {
    max-width: 200px;
    height: auto;
    filter: drop-shadow(0 0 20px rgba(0, 210, 255, 0.5));
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { filter: drop-shadow(0 0 10px rgba(0, 210, 255, 0.3)); }
    to { filter: drop-shadow(0 0 30px rgba(0, 210, 255, 0.8)); }
}

/* Input Fields - Fixed Visibility */
.stTextInput input, 
.stNumberInput input, 
.stSelectbox div[data-baseweb="select"] > div,
.stTextArea textarea {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 2px solid #333 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    font-size: 16px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: #00d2ff !important;
    box-shadow: 0 0 15px rgba(0, 210, 255, 0.5) !important;
    outline: none !important;
}

/* Labels */
.stTextInput label, 
.stNumberInput label, 
.stSelectbox label,
.stTextArea label {
    color: #00d2ff !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
}

/* Multiselect Fix */
.stMultiSelect div[data-baseweb="select"] {
    background-color: #000000 !important;
    border: 2px solid #333 !important;
}

.stMultiSelect span[data-baseweb="tag"] {
    background-color: #00d2ff !important;
    color: #000 !important;
}

/* Custom Buttons */
.custom-btn {
    display: inline-block;
    width: 100%;
    padding: 18px;
    background: linear-gradient(90deg, #00d2ff, #0055ff);
    color: white !important;
    text-align: center;
    text-decoration: none;
    font-weight: 800;
    font-size: 18px;
    border-radius: 50px;
    margin: 10px 0;
    box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
    border: 2px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}

.custom-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 30px rgba(0, 210, 255, 0.8);
    color: white !important;
    text-decoration: none;
}

.custom-btn:active {
    transform: translateY(0);
}

/* Danger Button */
.danger-btn {
    background: linear-gradient(90deg, #ff007f, #990033) !important;
    box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4) !important;
}

/* Success Button */
.success-btn {
    background: linear-gradient(90deg, #00ff88, #00cc66) !important;
}

/* Glass Card */
.glass {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Manifesto Box */
.manifesto-box {
    background: rgba(0,0,0,0.6);
    padding: 40px;
    border-radius: 20px;
    border: 1px solid #333;
    margin-bottom: 30px;
}

.manifesto-title {
    font-size: 32px;
    font-weight: 800;
    color: #00d2ff;
    margin-bottom: 25px;
    text-transform: uppercase;
}

.manifesto-text {
    font-size: 18px;
    line-height: 1.8;
    color: #e0e0e0;
    margin-bottom: 20px;
}

/* Admin Item */
.admin-item {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border-left: 5px solid #00d2ff;
    border-top: 1px solid #222;
    transition: all 0.3s ease;
}

.admin-item:hover {
    border-left-color: #00ff88;
    box-shadow: 0 5px 20px rgba(0, 210, 255, 0.2);
}

/* Streamlit Button Override */
div.stButton > button {
    background: linear-gradient(135deg, #1a1a1a, #0a0a0a);
    color: white;
    border: 2px solid #00d2ff;
    border-radius: 30px;
    padding: 12px 30px;
    font-weight: 600;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background: #00d2ff;
    color: black;
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0, 210, 255, 0.5);
}

/* Expander Styling */
.streamlit-expanderHeader {
    background-color: rgba(0, 0, 0, 0.3) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Alert Messages */
.stAlert {
    border-radius: 15px;
    border-left: 5px solid;
}

/* Error Messages */
.stError {
    background-color: rgba(255, 0, 127, 0.1) !important;
    border-color: #ff007f !important;
}

/* Success Messages */
.stSuccess {
    background-color: rgba(0, 255, 136, 0.1) !important;
    border-color: #00ff88 !important;
}

/* Tool Card */
.tool-card {
    background: linear-gradient(135deg, rgba(0, 210, 255, 0.1) 0%, rgba(0, 85, 255, 0.05) 100%);
    border: 2px solid rgba(0, 210, 255, 0.3);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}

.tool-card:hover {
    transform: translateY(-5px);
    border-color: #00d2ff;
    box-shadow: 0 10px 40px rgba(0, 210, 255, 0.3);
}

.tool-card.locked {
    opacity: 0.5;
    border-color: #666;
}

/* Hide Streamlit Branding */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Responsive Design */
@media (max-width: 768px) {
    .manifesto-title { font-size: 24px; }
    .manifesto-text { font-size: 16px; }
    .custom-btn { font-size: 16px; padding: 15px; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE FUNCTIONS WITH ERROR HANDLING
# =========================================================

def initialize_firebase() -> bool:
    """Initialize Firebase with proper error handling"""
    if firebase_admin._apps:
        return True
    
    try:
        if "firebase" in st.secrets:
            cred = credentials.Certificate(dict(st.secrets["firebase"]))
            database_url = st.secrets["firebase"].get("database_url")
            
            if not database_url:
                st.error("❌ Database URL not configured in secrets")
                return False
            
            firebase_admin.initialize_app(cred, {"databaseURL": database_url})
            return True
        else:
            st.error("❌ Firebase credentials not found in secrets")
            return False
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {str(e)}")
        return False

def safe_db_operation(operation, *args, **kwargs):
    """Wrapper for safe database operations"""
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

# User Operations
def get_user_data(key: str) -> Optional[Dict]:
    """Retrieve user data by key"""
    try:
        data = db.reference(f"users/{key}").get()
        if data:
            # Normalize old format to new format
            if isinstance(data, list):
                return {'name': 'Legacy User', 'tools': data}
            return data
        return None
    except Exception as e:
        st.error(f"Error fetching user: {str(e)}")
        return None

def create_user(key: str, name: str, tools: List[str]) -> bool:
    """Create a new user"""
    try:
        user_data = {
            'name': name,
            'tools': tools,
            'created_at': datetime.datetime.now().isoformat(),
            'last_login': None
        }
        db.reference(f"users/{key}").set(user_data)
        return True
    except Exception as e:
        st.error(f"Error creating user: {str(e)}")
        return False

def update_user_tools(key: str, tools: List[str]) -> bool:
    """Update user's tool access"""
    try:
        db.reference(f"users/{key}/tools").set(tools)
        db.reference(f"users/{key}/updated_at").set(datetime.datetime.now().isoformat())
        return True
    except Exception as e:
        st.error(f"Error updating tools: {str(e)}")
        return False

def update_user_name(key: str, name: str) -> bool:
    """Update user's name"""
    try:
        db.reference(f"users/{key}/name").set(name)
        return True
    except Exception as e:
        st.error(f"Error updating name: {str(e)}")
        return False

def update_last_login(key: str) -> None:
    """Update user's last login timestamp"""
    try:
        db.reference(f"users/{key}/last_login").set(datetime.datetime.now().isoformat())
    except:
        pass

def delete_user(key: str) -> bool:
    """Delete a user"""
    try:
        db.reference(f"users/{key}").delete()
        return True
    except Exception as e:
        st.error(f"Error deleting user: {str(e)}")
        return False

def get_all_users() -> Dict:
    """Get all users"""
    try:
        users = db.reference("users").get()
        return users if users else {}
    except Exception as e:
        st.error(f"Error fetching users: {str(e)}")
        return {}

# Request Operations
def add_request(email: str) -> bool:
    """Add access request"""
    try:
        request_data = {
            "email": email,
            "date": datetime.datetime.now().isoformat(),
            "status": "pending"
        }
        db.reference('requests').push(request_data)
        return True
    except Exception as e:
        st.error(f"Error adding request: {str(e)}")
        return False

def get_requests() -> Dict:
    """Get all access requests"""
    try:
        reqs = db.reference('requests').get()
        return reqs if reqs else {}
    except:
        return {}

def delete_request(key: str) -> bool:
    """Delete a request"""
    try:
        db.reference(f'requests/{key}').delete()
        return True
    except:
        return False

# Upgrade Operations
def add_upgrade(user_key: str, tool: str, utr: str) -> bool:
    """Add upgrade request"""
    try:
        upgrade_data = {
            "user": user_key,
            "tool": tool,
            "utr": utr,
            "date": datetime.datetime.now().isoformat(),
            "status": "pending"
        }
        db.reference('upgrades').push(upgrade_data)
        return True
    except Exception as e:
        st.error(f"Error adding upgrade: {str(e)}")
        return False

def get_upgrades() -> Dict:
    """Get all upgrade requests"""
    try:
        upgs = db.reference('upgrades').get()
        return upgs if upgs else {}
    except:
        return {}

def delete_upgrade(key: str) -> bool:
    """Delete an upgrade request"""
    try:
        db.reference(f'upgrades/{key}').delete()
        return True
    except:
        return False

# Donation Operations
def add_donation(email: str, utr: str, amount: int) -> bool:
    """Log a donation"""
    try:
        donation_data = {
            "email": email,
            "utr": utr,
            "amount": amount,
            "date": datetime.datetime.now().isoformat()
        }
        db.reference('donations').push(donation_data)
        return True
    except Exception as e:
        st.error(f"Error logging donation: {str(e)}")
        return False

def get_donations() -> Dict:
    """Get all donations"""
    try:
        dons = db.reference('donations').get()
        return dons if dons else {}
    except:
        return {}

# Utility Functions
def generate_key() -> str:
    """Generate a unique access key"""
    return "SAM-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "page": "home",
        "role": None,
        "user_data": {},
        "user_key": None,
        "show_req": False,
        "last_activity": datetime.datetime.now()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def check_session_timeout():
    """Check if session has timed out"""
    if st.session_state.role and st.session_state.last_activity:
        elapsed = datetime.datetime.now() - st.session_state.last_activity
        if elapsed.total_seconds() > SESSION_TIMEOUT_MINUTES * 60:
            logout()
            st.warning("Session expired. Please login again.")
            return True
    st.session_state.last_activity = datetime.datetime.now()
    return False

# =========================================================
# NAVIGATION FUNCTIONS
# =========================================================

def navigate_to(page: str):
    """Navigate to a different page"""
    st.session_state.page = page
    st.rerun()

def logout():
    """Logout and clear session"""
    st.session_state.role = None
    st.session_state.user_data = {}
    st.session_state.user_key = None
    st.session_state.page = "home"

# =========================================================
# MANIFESTO CONTENT
# =========================================================

def render_manifesto_pragyan():
    """Render Pragyan manifesto"""
    st.markdown("""
    <div class="manifesto-box">
        <div class="manifesto-title">🇮🇳 PRAGYAN: THE AWAKENING</div>
        <div class="manifesto-text">
            <b>The Mission</b><br>
            Pragyan (meaning "Wisdom" in Sanskrit) is India's first community-driven, 
            open-source AI project designed to build indigenous intelligence. In a world 
            dominated by foreign AI giants, India—the world's largest data consumer—risks 
            becoming a digital colony.
        </div>
        <div class="manifesto-text">
            <b>The Origin Story</b><br>
            Founded by <b>Nitin Raj</b> under <b>Samrion Technologies</b>, Pragyan was 
            born from a simple realization: <i>We cannot build our future on rented land.</i> 
            Built line-by-line by an independent developer and a community of believers.
        </div>
        <div class="manifesto-text">
            <b>Why Pragyan Matters</b><br>
            • <b>Data Sovereignty:</b> Your data stays within Indian borders<br>
            • <b>Linguistic Inclusion:</b> Training for India's diverse languages<br>
            • <b>True Open Source:</b> Complete transparency in code and models
        </div>
        <div class="manifesto-text">
            <b>The Roadmap</b><br>
            1. ✅ <b>Nano Model (1-10M):</b> Foundation laid<br>
            2. 🔄 <b>Mini Model (Current):</b> Gathering GPU resources<br>
            3. 🚀 <b>Base Model & Beyond:</b> GPT-class intelligence on Indian infrastructure
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_manifesto_tools():
    """Render tools manifesto"""
    st.markdown("""
    <div class="manifesto-box" style="border-left-color: #ff007f;">
        <div class="manifesto-title">🛠️ THE SAMRION ARMORY</div>
        <div class="manifesto-text">
            <b>1. 🧠 MEDHA (The Brain)</b><br>
            Your personal polymath designed to understand context, reason through 
            complex problems, and provide insightful solutions.
        </div>
        <div class="manifesto-text">
            <b>2. 🎨 AKRITI (The Imagination)</b><br>
            Breaking the barrier between thought and visual. A complete creative 
            studio for image generation.
        </div>
        <div class="manifesto-text">
            <b>3. 🎙️ VANI (The Voice)</b><br>
            Voice synthesis with "Digital Soul" - clone, preserve, and transport 
            voices across the digital realm.
        </div>
        <div class="manifesto-text">
            <b>4. 📦 SANGRAH (The Collector)</b><br>
            The backbone of ML - automated dataset collection for AI training.
        </div>
        <div class="manifesto-text">
            <b>5. 💻 CODIQ (The Architect)</b><br>
            Context-aware software engineer capable of building complete applications.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE RENDERERS
# =========================================================

def render_logo():
    """Render logo if it exists"""
    try:
        if os.path.exists("logo.png"):
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            st.image("logo.png", use_container_width=False, width=200)
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        pass

def render_home():
    """Render home page"""
    render_logo()
    
    st.markdown("""
    <div style="text-align:center; padding: 80px 20px;">
        <h1 style="font-size: 4.5rem; text-shadow: 0 0 20px #00d2ff; margin-bottom: 10px;">
            SAMRION TECHNOLOGIES
        </h1>
        <h3 style="letter-spacing: 5px; color: #aaa;">THE FUTURE OF INTELLIGENCE</h3>
        <p style="opacity:0.9; margin-top: 30px; font-size: 1.2rem;">
            BUILT IN INDIA · OPEN SOURCE · INDIGENOUS
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        if st.button("📖 READ MANIFESTO", use_container_width=True):
            navigate_to("about")
    
    with col2:
        if st.button("🔐 ENTER BRIDGE", use_container_width=True):
            navigate_to("login")
    
    with col3:
        if st.button("🤝 CONTRIBUTE", use_container_width=True):
            navigate_to("donate")

def render_about():
    """Render about/manifesto page"""
    if st.button("← RETURN TO BASE"):
        navigate_to("home")
    
    tab1, tab2 = st.tabs(["🇮🇳 PRAGYAN VISION", "🛠️ TOOL ECOSYSTEM"])
    
    with tab1:
        render_manifesto_pragyan()
    
    with tab2:
        render_manifesto_tools()

def render_donate():
    """Render donation page"""
    if st.button("← RETURN"):
        navigate_to("home")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass'>
            <h3>🚀 Support The Mission</h3>
            <p style='font-size:18px; line-height:1.6;'>
                Funds go directly to GPU compute resources.<br>
                <b style='color:#00d2ff;'>Fund India's AI Future</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists("qr.png"):
            st.image("qr.png", width=350, caption="Scan to Donate")
        else:
            st.warning("⚠️ QR code not found. Please add 'qr.png' to the app directory.")
    
    with col2:
        st.markdown("<div class='glass'><h3>LOG YOUR CONTRIBUTION</h3>", unsafe_allow_html=True)
        
        with st.form("donation_form"):
            email = st.text_input("Your Email Address", placeholder="your.email@example.com")
            utr = st.text_input("UTR / Transaction ID", placeholder="Enter transaction reference")
            amount = st.number_input("Amount (₹)", min_value=10, value=100, step=10)
            
            submitted = st.form_submit_button("✅ SUBMIT DETAILS", use_container_width=True)
            
            if submitted:
                if not email or not validate_email(email):
                    st.error("❌ Please enter a valid email address")
                elif not utr or len(utr) < 5:
                    st.error("❌ Please enter a valid UTR/Transaction ID")
                else:
                    if add_donation(email, utr, amount):
                        st.success("✅ Contribution logged! Thank you for supporting the mission.")
                        time.sleep(2)
                        st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_login():
    """Render login page"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col = st.columns([1,2,1])[1]
    
    with col:
        st.markdown("<div class='glass'><h2 style='text-align:center'>🔐 IDENTITY VERIFICATION</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            access_key = st.text_input("ENTER ACCESS CODE", type="password", placeholder="Enter your key")
            login_btn = st.form_submit_button("AUTHORIZE ACCESS", use_container_width=True)
            
            if login_btn:
                if not access_key:
                    st.error("❌ Please enter an access code")
                elif access_key == ADMIN_PASSWORD:
                    st.session_state.role = "admin"
                    navigate_to("admin")
                else:
                    user_data = get_user_data(access_key)
                    if user_data:
                        st.session_state.role = "user"
                        st.session_state.user_key = access_key
                        st.session_state.user_data = user_data
                        update_last_login(access_key)
                        navigate_to("hub")
                    else:
                        st.error("❌ INVALID ACCESS CODE")
                        st.session_state.show_req = True
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Request Access Section
        if st.session_state.get('show_req', False):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='glass'><h3>Request Access</h3>", unsafe_allow_html=True)
            
            with st.form("request_form"):
                req_email = st.text_input("Enter Your Email", placeholder="your.email@example.com")
                req_btn = st.form_submit_button("📨 SEND REQUEST", use_container_width=True)
                
                if req_btn:
                    if req_email and validate_email(req_email):
                        if add_request(req_email):
                            st.success("✅ Request sent! You'll receive a key via email.")
                            st.session_state.show_req = False
                            time.sleep(2)
                            st.rerun()
                    else:
                        st.error("❌ Please enter a valid email")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("← BACK TO HOME"):
        st.session_state.show_req = False
        navigate_to("home")

def render_hub():
    """Render user hub/dashboard"""
    st.markdown("## 💠 SAMRION ARMORY")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_name = st.session_state.user_data.get('name', 'USER')
        st.caption(f"WELCOME, **{user_name.upper()}**")
    with col2:
        if st.button("🚪 LOGOUT", use_container_width=True):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    my_tools = st.session_state.user_data.get('tools', [])
    
    # Display tools in grid
    cols = st.columns(3)
    
    for idx, (tool_name, tool_data) in enumerate(TOOLS.items()):
        unlocked = tool_name in my_tools
        
        with cols[idx % 3]:
            card_class = "tool-card" if unlocked else "tool-card locked"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size:4rem; margin-bottom:10px;">{tool_data['icon']}</div>
                <h3 style="color:white; margin-bottom:5px;">{tool_name}</h3>
                <p style="color:#999; font-size:14px;">{tool_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if unlocked:
                # Launch
