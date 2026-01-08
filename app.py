"""
SAMRION TECHNOLOGIES - Production Platform
Enterprise-grade security and architecture
"""

import streamlit as st
import datetime
import secrets
import string
import time
import hashlib
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import firebase_admin
from firebase_admin import credentials, db
from groq import Groq

# =========================================================
# CONFIGURATION & CONSTANTS
# =========================================================

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@dataclass
class Tool:
    name: str
    icon: str
    url: str
    description: str

# Tool Registry
TOOLS_REGISTRY = {
    "MEDHA": Tool("MEDHA", "🧠", "https://medha-ai.streamlit.app/", "AI Intelligence Core"),
    "AKRITI": Tool("AKRITI", "🎨", "https://akriti.streamlit.app/", "Creative Studio"),
    "VANI": Tool("VANI", "🎙️", "https://vaani-labs.streamlit.app/", "Voice Technology"),
    "SANGRAH": Tool("SANGRAH", "📦", "https://sangrah.streamlit.app/", "Data Collection"),
    "CODIQ": Tool("CODIQ", "💻", "https://codiq-ai.streamlit.app/", "Code Architecture")
}

# Security Configuration
MAX_LOGIN_ATTEMPTS = 5
SESSION_TIMEOUT = 3600  # 1 hour
KEY_LENGTH = 16
MIN_PASSWORD_LENGTH = 8

# =========================================================
# STREAMLIT PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SAMRION Technologies",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ENHANCED STYLING WITH LOGO SUPPORT
# =========================================================

def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

    /* Global Theme */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 10%, #0f172a 0%, #000000 100%);
        color: #ffffff;
    }

    * {
        font-family: 'Inter', sans-serif !important;
    }

    /* Typography */
    h1, h2, h3 { 
        font-family: 'Outfit', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #ffffff !important;
    }

    /* Logo Container */
    .logo-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
    }

    .logo-container img {
        max-width: 200px;
        filter: drop-shadow(0 0 20px rgba(0, 210, 255, 0.5));
        animation: pulse 3s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Input Fields - Enhanced Visibility */
    .stTextInput input, 
    .stNumberInput input, 
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #333333 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        outline: none;
    }

    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label,
    .stTextArea label {
        color: #00d2ff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }

    /* Custom Button Styles */
    .custom-btn {
        display: inline-block;
        width: 100%;
        padding: 18px 32px;
        background: linear-gradient(135deg, #00d2ff, #0055ff);
        color: white !important;
        text-align: center;
        text-decoration: none;
        font-weight: 800;
        font-size: 16px;
        border-radius: 50px;
        margin: 10px 0;
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4);
        border: 2px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .custom-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 210, 255, 0.6);
        color: white !important;
    }

    .danger-btn {
        background: linear-gradient(135deg, #ff007f, #990033);
        box-shadow: 0 6px 20px rgba(255, 0, 127, 0.4);
    }

    .success-btn {
        background: linear-gradient(135deg, #00ff88, #00aa55);
        box-shadow: 0 6px 20px rgba(0, 255, 136, 0.4);
    }

    /* Glass Morphism Cards */
    .glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Manifesto Box */
    .manifesto-box {
        background: rgba(0, 0, 0, 0.7);
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #1a1a1a;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0, 210, 255, 0.1);
    }

    .manifesto-title {
        font-size: 32px;
        font-weight: 800;
        color: #00d2ff;
        margin-bottom: 25px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }

    .manifesto-text {
        font-size: 18px;
        line-height: 1.8;
        color: #e0e0e0;
        margin-bottom: 20px;
    }

    /* Admin Panel */
    .admin-item {
        background: linear-gradient(135deg, #0a0a0a, #1a1a1a);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #00d2ff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }

    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 10px;
    }

    .status-active {
        background: rgba(0, 255, 136, 0.2);
        color: #00ff88;
        border: 1px solid #00ff88;
    }

    .status-locked {
        background: rgba(255, 0, 127, 0.2);
        color: #ff007f;
        border: 1px solid #ff007f;
    }

    /* Streamlit Button Override */
    div.stButton > button {
        background: #46494A;
        color: white;
        border: 2px solid #00d2ff;
        border-radius: 30px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: #00d2ff;
        color: #000000;
        transform: scale(1.02);
    }

    /* Hide Streamlit Branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# SECURITY UTILITIES
# =========================================================

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_utr(utr: str) -> bool:
        """Validate UTR format (alphanumeric, min 10 chars)"""
        return len(utr) >= 10 and utr.isalnum()
    
    @staticmethod
    def generate_secure_key(length: int = KEY_LENGTH) -> str:
        """Generate cryptographically secure key"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        return text.strip()[:500]  # Limit length and trim

# =========================================================
# FIREBASE DATABASE MANAGER
# =========================================================

class DatabaseManager:
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize Firebase connection with error handling"""
        if cls._initialized:
            return True
            
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(dict(st.secrets["firebase"]))
                firebase_admin.initialize_app(cred, {
                    "databaseURL": st.secrets["firebase"].get("database_url")
                })
            cls._initialized = True
            return True
        except Exception as e:
            st.error(f"Database initialization failed: {str(e)}")
            return False
    
    # User Operations
    @staticmethod
    def get_user(key: str) -> Optional[Dict]:
        """Retrieve user data"""
        try:
            data = db.reference(f"users/{key}").get()
            if data:
                # Normalize old format
                if isinstance(data, list):
                    return {'name': 'Legacy User', 'tools': data, 'created': None}
                return data
            return None
        except Exception as e:
            st.error(f"Error fetching user: {str(e)}")
            return None
    
    @staticmethod
    def create_user(key: str, name: str, tools: List[str]) -> bool:
        """Create new user"""
        try:
            user_data = {
                'name': SecurityManager.sanitize_input(name),
                'tools': tools,
                'created': datetime.datetime.now().isoformat(),
                'last_login': None
            }
            db.reference(f"users/{key}").set(user_data)
            return True
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return False
    
    @staticmethod
    def update_user_tools(key: str, tools: List[str]) -> bool:
        """Update user's tool access"""
        try:
            db.reference(f"users/{key}/tools").set(tools)
            return True
        except Exception as e:
            st.error(f"Error updating tools: {str(e)}")
            return False
    
    @staticmethod
    def update_last_login(key: str) -> bool:
        """Update user's last login timestamp"""
        try:
            db.reference(f"users/{key}/last_login").set(
                datetime.datetime.now().isoformat()
            )
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def delete_user(key: str) -> bool:
        """Delete user"""
        try:
            db.reference(f"users/{key}").delete()
            return True
        except Exception as e:
            st.error(f"Error deleting user: {str(e)}")
            return False
    
    @staticmethod
    def get_all_users() -> Dict:
        """Get all users"""
        try:
            return db.reference("users").get() or {}
        except Exception as e:
            st.error(f"Error fetching users: {str(e)}")
            return {}
    
    # Request Operations
    @staticmethod
    def add_request(email: str) -> bool:
        """Add access request"""
        if not SecurityManager.validate_email(email):
            st.error("Invalid email format")
            return False
        
        try:
            db.reference('requests').push({
                "email": email,
                "date": datetime.datetime.now().isoformat(),
                "status": "pending"
            })
            return True
        except Exception as e:
            st.error(f"Error adding request: {str(e)}")
            return False
    
    @staticmethod
    def get_requests() -> Dict:
        """Get all requests"""
        try:
            return db.reference('requests').get() or {}
        except Exception:
            return {}
    
    @staticmethod
    def delete_request(key: str) -> bool:
        """Delete request"""
        try:
            db.reference(f'requests/{key}').delete()
            return True
        except Exception:
            return False
    
    # Upgrade Operations
    @staticmethod
    def add_upgrade_request(user_key: str, tool: str, utr: str) -> bool:
        """Add upgrade request"""
        if not SecurityManager.validate_utr(utr):
            st.error("Invalid UTR format")
            return False
        
        try:
            db.reference('upgrades').push({
                "user": user_key,
                "tool": tool,
                "utr": SecurityManager.sanitize_input(utr),
                "date": datetime.datetime.now().isoformat(),
                "status": "pending"
            })
            return True
        except Exception as e:
            st.error(f"Error adding upgrade: {str(e)}")
            return False
    
    @staticmethod
    def get_upgrade_requests() -> Dict:
        """Get all upgrade requests"""
        try:
            return db.reference('upgrades').get() or {}
        except Exception:
            return {}
    
    @staticmethod
    def delete_upgrade_request(key: str) -> bool:
        """Delete upgrade request"""
        try:
            db.reference(f'upgrades/{key}').delete()
            return True
        except Exception:
            return False
    
    # Donation Operations
    @staticmethod
    def add_donation(email: str, utr: str, amount: int) -> bool:
        """Log donation"""
        if not SecurityManager.validate_email(email) or not SecurityManager.validate_utr(utr):
            st.error("Invalid email or UTR format")
            return False
        
        try:
            db.reference('donations').push({
                "email": email,
                "utr": SecurityManager.sanitize_input(utr),
                "amount": amount,
                "date": datetime.datetime.now().isoformat()
            })
            return True
        except Exception as e:
            st.error(f"Error logging donation: {str(e)}")
            return False
    
    @staticmethod
    def get_donations() -> Dict:
        """Get all donations"""
        try:
            return db.reference('donations').get() or {}
        except Exception:
            return {}

# =========================================================
# SESSION MANAGER
# =========================================================

class SessionManager:
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        defaults = {
            "page": "home",
            "role": UserRole.GUEST,
            "user_data": {},
            "user_key": None,
            "login_attempts": 0,
            "last_activity": time.time(),
            "show_request_form": False
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def navigate_to(page: str):
        """Navigate to page"""
        st.session_state.page = page
    
    @staticmethod
    def logout():
        """Logout user"""
        st.session_state.role = UserRole.GUEST
        st.session_state.user_data = {}
        st.session_state.user_key = None
        st.session_state.page = "home"
    
    @staticmethod
    def check_session_timeout() -> bool:
        """Check if session has timed out"""
        if st.session_state.role != UserRole.GUEST:
            elapsed = time.time() - st.session_state.last_activity
            if elapsed > SESSION_TIMEOUT:
                SessionManager.logout()
                return True
        st.session_state.last_activity = time.time()
        return False
    
    @staticmethod
    def increment_login_attempts():
        """Increment failed login attempts"""
        st.session_state.login_attempts += 1
        
        if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
            st.error("Too many failed attempts. Please try again later.")
            time.sleep(3)
            return True
        return False

# =========================================================
# UI COMPONENTS
# =========================================================

def render_logo():
    """Render company logo"""
    try:
        st.markdown("""
        <div class="logo-container">
            <img src="logo.png" alt="SAMRION Logo" />
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        # Fallback if logo not found
        st.markdown("""
        <div class="logo-container">
            <h1 style="font-size: 3rem; margin: 0; text-shadow: 0 0 20px #00d2ff;">
                ♾️ SAMRION
            </h1>
        </div>
        """, unsafe_allow_html=True)

def render_manifesto_pragyan():
    """Render Pragyan manifesto"""
    st.markdown("""
    <div class="manifesto-box">
        <div class="manifesto-title">🇮🇳 PRAGYAN: THE AWAKENING</div>
        <div class="manifesto-text">
            <b>The Mission</b><br>
            Pragyan (meaning "Wisdom" or "Supreme Intelligence" in Sanskrit) is not just another AI model; 
            it is a movement towards digital sovereignty. In a world dominated by foreign AI giants, 
            India—the world's largest data consumer—risks becoming a digital colony.
        </div>
        <div class="manifesto-text">
            Pragyan exists to change that. It is India's first community-driven, open-source AI project 
            designed to build indigenous intelligence from the ground up.
        </div>
        <div class="manifesto-text">
            <b>The Origin Story</b><br>
            Founded by <b>Nitin Raj</b> under the banner of <b>Samrion Technologies</b>, Pragyan was born 
            from a simple yet powerful realization: <i>We cannot build our future on rented land.</i>
        </div>
        <div class="manifesto-text">
            <b>Why Pragyan Matters</b><br>
            • <b>Data Sovereignty:</b> Your data should not leave Indian shores<br>
            • <b>Linguistic Inclusion:</b> Trained to understand India's diverse languages<br>
            • <b>True Open Source:</b> Total transparency in code, datasets, and model weights
        </div>
        <div class="manifesto-text">
            <b>The Roadmap</b><br>
            1. ✅ <b>Nano Model (1–10M Parameters):</b> Foundation operational<br>
            2. 🔄 <b>Mini Model:</b> Currently gathering GPU compute resources<br>
            3. 🚀 <b>Base Model & Beyond:</b> GPT-Class intelligence on Indian infrastructure
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
            Your personal polymath—designed to understand context, reason through complex problems, 
            and provide insightful solutions.
        </div>
        <div class="manifesto-text">
            <b>2. 🎨 AKRITI (The Imagination)</b><br>
            Breaks the barrier between thought and visual. If you can dream it, Akriti can render it.
        </div>
        <div class="manifesto-text">
            <b>3. 🎙️ VANI (The Voice)</b><br>
            Beyond simple text-to-speech. Introducing the concept of "Digital Soul" for voice technology.
        </div>
        <div class="manifesto-text">
            <b>4. 📦 SANGRAH (The Collector)</b><br>
            The backbone of machine learning. Automates dataset collection for AI training.
        </div>
        <div class="manifesto-text">
            <b>5. 💻 CODIQ (The Architect)</b><br>
            Context-aware software engineer capable of creating production-grade applications.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE RENDERERS
# =========================================================

def render_home_page():
    """Render home page"""
    render_logo()
    
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px;">
        <h1 style="font-size: 4rem; text-shadow: 0 0 20px #00d2ff; margin-bottom: 10px;">
            SAMRION TECHNOLOGIES
        </h1>
        <h3 style="letter-spacing: 5px; color: #aaa; margin-bottom: 20px;">
            THE FUTURE OF INTELLIGENCE
        </h3>
        <p style="opacity:0.9; margin-top: 30px; font-size: 1.2rem;">
            BUILT IN INDIA · OPEN SOURCE · INDIGENOUS
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📖 READ MANIFESTO", use_container_width=True):
            SessionManager.navigate_to("manifesto")
            st.rerun()
    
    with col2:
        if st.button("🔐 ENTER BRIDGE", use_container_width=True):
            SessionManager.navigate_to("login")
            st.rerun()
    
    with col3:
        if st.button("🤝 CONTRIBUTE", use_container_width=True):
            SessionManager.navigate_to("donate")
            st.rerun()

def render_manifesto_page():
    """Render manifesto page"""
    if st.button("← RETURN TO BASE"):
        SessionManager.navigate_to("home")
        st.rerun()
    
    tab1, tab2 = st.tabs(["PRAGYAN VISION", "TOOL ECOSYSTEM"])
    
    with tab1:
        render_manifesto_pragyan()
    
    with tab2:
        render_manifesto_tools()

def render_donate_page():
    """Render donation page"""
    if st.button("← RETURN"):
        SessionManager.navigate_to("home")
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass'>
            <h3>🚀 Support The Mission</h3>
            <p style='font-size:18px'>
                Funds go directly to GPU compute for Pragyan development.<br>
                <b>Fund India's AI Future</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            st.image("qr.png", width=350, caption="Scan to Donate")
        except Exception:
            st.warning("QR code not found. Please upload qr.png to enable payments.")
    
    with col2:
        st.markdown("<div class='glass'><h3>LOG CONTRIBUTION</h3>", unsafe_allow_html=True)
        
        with st.form("donation_form"):
            email = st.text_input("Your Email Address", placeholder="name@example.com")
            utr = st.text_input("UTR / Transaction ID", placeholder="Enter 12-digit UTR")
            amount = st.number_input("Amount (₹)", min_value=10, value=100, step=10)
            
            submitted = st.form_submit_button("✅ SUBMIT CONTRIBUTION")
            
            if submitted:
                if email and utr and amount > 0:
                    if DatabaseManager.add_donation(email, utr, amount):
                        st.success("✅ Contribution recorded! Thank you for supporting Pragyan.")
                        st.balloons()
                else:
                    st.error("Please fill all fields correctly.")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_login_page():
    """Render login page"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col = st.columns([1, 2, 1])[1]
    
    with col:
        st.markdown("""
        <div class='glass'>
            <h2 style='text-align:center'>IDENTITY VERIFICATION</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            access_key = st.text_input("ENTER ACCESS CODE", type="password", 
                                      placeholder="Enter your unique key")
            login_btn = st.form_submit_button("AUTHORIZE ACCESS", use_container_width=True)
            
            if login_btn:
                if SessionManager.increment_login_attempts():
                    st.rerun()
                
                # Check admin password
                admin_hash = SecurityManager.hash_password(st.secrets.get("ADMIN_PASSWORD", "default_secure_password"))
                input_hash = SecurityManager.hash_password(access_key)
                
                if input_hash == admin_hash:
                    st.session_state.role = UserRole.ADMIN
                    st.session_state.login_attempts = 0
                    SessionManager.navigate_to("admin")
                    st.rerun()
                else:
                    # Check user key
                    user_data = DatabaseManager.get_user(access_key)
                    if user_data:
                        st.session_state.role = UserRole.USER
                        st.session_state.user_key = access_key
                        st.session_state.user_data = user_data
                        st.session_state.login_attempts = 0
                        DatabaseManager.update_last_login(access_key)
                        SessionManager.navigate_to("hub")
                        st.rerun()
                    else:
                        st.error("❌ INVALID ACCESS CODE")
                        st.session_state.show_request_form = True
        
        if st.session_state.get('show_request_form'):
            st.markdown("---")
            st.markdown("### Request Access")
            
            with st.form("request_form"):
                request_email = st.text_input("Enter Email to Request Key", 
                                             placeholder="your@email.com")
                request_btn = st.form_submit_button("SEND REQUEST")
                
                if request_btn:
                    if DatabaseManager.add_request(request_email):
                        st.success("✅ Request sent! You'll receive your key via email.")
                        st.session_state.show_request_form = False
    
    if st.button("← BACK"):
        SessionManager.navigate_to("home")
        st.rerun()

def render_hub_page():
    """Render user hub"""
    user_name = st.session_state.user_data.get('name', 'USER').upper()
    
    st.markdown(f"## 💠 TOOLS")
    st.caption(f"WELCOME, {user_name}")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("LOGOUT"):
            SessionManager.logout()
            st.rerun()
    
    st.markdown("---")
    
    user_tools = st.session_state.user_data.get('tools', [])
    
    cols = st.columns(3)
    
    for i, (tool_name, tool) in enumerate(TOOLS_REGISTRY.items()):
        is_unlocked = tool_name in user_tools
        
        with cols[i % 3]:
            status_class = "status-active" if is_unlocked else "status-locked"
            status_text = "ACTIVE" if is_unlocked else "LOCKED"
            
            st.markdown(f"""
            <div class="glass" style="text-align:center">
                <div style="font-size:4rem; margin-bottom:10px;">{tool.icon}</div>
                <h3 style="color:white;">{tool_name}</h3>
                <span class="status-badge {status_class}">{status_text}</span>
                <p style="font-size:14px; color:#aaa; margin-top:10px;">{tool.description}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if is_unlocked:
                st.markdown(f"""
                <a href="{tool.url}" target="_blank" class="custom-btn">
                    🚀 LAUNCH {tool_name}
                </a>
                """, unsafe_allow_html=True)
            else:
                with st.expander("🔒 UNLOCK THIS TOOL (₹10)"):
                    with st.form(f"unlock_form_{i}"):
                        utr_input = st.text_input("UTR / Transaction ID", 
                                                 key=f"utr_{i}",
                                                 placeholder="Enter payment UTR")
                        unlock_btn = st.form_submit_button("REQUEST UNLOCK")
                        
                        if unlock_btn and utr_input:
                            if DatabaseManager.add_upgrade_request(
                                st.session_state.user_key, 
                                tool_name, 
                                utr_input
                            ):
                                st.success("✅ Unlock request sent!")
                            else:
                                st.error("Failed to send request")

def render_admin_page():
    """Render admin console"""
    st.title("👑 FOUNDER CONSOLE")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("EXIT"):
            SessionManager.logout()
            st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 USERS & KEYS", 
        "📨 REQUESTS", 
        "💰 FINANCE",
        "📊 ANALYTICS"
    ])
    
    with tab1:
        render_admin_users_tab()
    
    with tab2:
        render_admin_requests_tab()
    
    with tab3:
        render_admin_finance_tab()
    
    with tab4:
        render_admin_analytics_tab()

def render_admin_users_tab():
    """Render admin users management"""
    st.markdown("### ✨ Mint New Access Key")
    
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("User Name / Alias", 
                                    placeholder="e.g., Nitin Raj")
        
        with col2:
            new_tools = st.multiselect("Grant Tool Access", 
                                      list(TOOLS_REGISTRY.keys()), 
                                      default=list(TOOLS_REGISTRY.keys()))
        
        create_btn = st.form_submit_button("GENERATE KEY", use_container_width=True)
        
        if create_btn:
            if new_name:
                new_key = SecurityManager.generate_secure_key()
                if DatabaseManager.create_user(new_key, new_name, new_tools):
                    st.success(f"✅ KEY CREATED FOR: {new_name}")
                    st.code(new_key, language=None)
                    st.info("⚠️ Save this key! It won't be shown again.")
                else:
                    st.error("Failed to create user")
            else:
                st.error("Please enter a user name")
    
    st.markdown("---")
    st.markdown("### 👥 Active User Database")
    
    users = DatabaseManager.get_all_users()
    
    if users:
        for user_key, user_data in users.items():
            # Handle legacy format
            if isinstance(user_data, list):
                user_name = "Legacy User"
                user_tools = user_data
                created_date = "Unknown"
            else:
                user_name = user_data.get('name', 'Unknown')
                user_tools = user_data.get('tools', [])
                created_date = user_data.get('created', 'Unknown')
                if created_date != 'Unknown':
                    try:
                        created_date = datetime.datetime.fromisoformat(created_date).strftime('%Y-%m-%d')
                    except:
                        pass
            
            st.markdown(f"""
            <div class="admin-item">
                <div>
                    <span style="color:#00d2ff; font-size:20px; font-weight:bold;">{user_name}</span>
                    <span class="status-badge status-active">ACTIVE</span><br>
                    <small style="color:#666;">KEY: {user_key}</small><br>
                    <small style="color:#888;">CREATED: {created_date}</small><br>
                    <small style="color:#ccc;">ACCESS: {', '.join(user_tools) if user_tools else 'None'}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_edit, col_delete = st.columns([4, 1])
            
            with col_edit:
                with st.expander(f"✏️ EDIT ACCESS - {user_name}"):
                    with st.form(f"edit_form_{user_key}"):
                        updated_tools = st.multiselect(
                            "Modify Tool Access",
                            list(TOOLS_REGISTRY.keys()),
                            default=user_tools,
                            key=f"tools_{user_key}"
                        )
                        
                        update_btn = st.form_submit_button("💾 UPDATE ACCESS")
                        
                        if update_btn:
                            if DatabaseManager.update_user_tools(user_key, updated_tools):
                                st.success("✅ Access updated successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to update")
            
            with col_delete:
                with st.popover("🗑️"):
                    st.warning(f"Delete {user_name}?")
                    if st.button("CONFIRM DELETE", key=f"del_{user_key}"):
                        if DatabaseManager.delete_user(user_key):
                            st.success("Deleted")
                            time.sleep(1)
                            st.rerun()
    else:
        st.info("No users in database yet")

def render_admin_requests_tab():
    """Render admin requests management"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📨 New Access Requests")
        
        requests = DatabaseManager.get_requests()
        
        if requests:
            for req_key, req_data in requests.items():
                email = req_data.get('email', 'Unknown')
                date = req_data.get('date', 'Unknown')
                
                with st.expander(f"📧 {email}"):
                    st.caption(f"Requested: {date}")
                    
                    with st.form(f"grant_form_{req_key}"):
                        grant_name = st.text_input("User Name", 
                                                  value="New User",
                                                  key=f"name_{req_key}")
                        
                        grant_tools = st.multiselect(
                            "Grant Tools",
                            list(TOOLS_REGISTRY.keys()),
                            default=list(TOOLS_REGISTRY.keys()),
                            key=f"grant_{req_key}"
                        )
                        
                        col_approve, col_reject = st.columns(2)
                        
                        with col_approve:
                            approve_btn = st.form_submit_button("✅ APPROVE", 
                                                               use_container_width=True)
                        
                        with col_reject:
                            reject_btn = st.form_submit_button("❌ REJECT",
                                                              use_container_width=True)
                        
                        if approve_btn:
                            new_key = SecurityManager.generate_secure_key()
                            if DatabaseManager.create_user(new_key, grant_name, grant_tools):
                                DatabaseManager.delete_request(req_key)
                                st.success(f"✅ KEY GENERATED: {new_key}")
                                st.info("Send this key to the user via email")
                                time.sleep(2)
                                st.rerun()
                        
                        if reject_btn:
                            DatabaseManager.delete_request(req_key)
                            st.warning("Request rejected")
                            time.sleep(1)
                            st.rerun()
        else:
            st.info("No pending requests")
    
    with col2:
        st.markdown("#### 🔓 Upgrade Requests")
        
        upgrades = DatabaseManager.get_upgrade_requests()
        
        if upgrades:
            for upg_key, upg_data in upgrades.items():
                user_key = upg_data.get('user', 'Unknown')
                tool = upg_data.get('tool', 'Unknown')
                utr = upg_data.get('utr', 'Unknown')
                date = upg_data.get('date', 'Unknown')
                
                user_info = DatabaseManager.get_user(user_key)
                user_name = user_info.get('name', 'Unknown') if user_info else 'Unknown'
                
                with st.expander(f"🔧 {tool} - {user_name}"):
                    st.caption(f"User Key: {user_key}")
                    st.caption(f"UTR: {utr}")
                    st.caption(f"Date: {date}")
                    
                    col_approve, col_reject = st.columns(2)
                    
                    with col_approve:
                        if st.button("✅ APPROVE", key=f"appr_{upg_key}"):
                            user_data = DatabaseManager.get_user(user_key)
                            if user_data:
                                current_tools = user_data.get('tools', [])
                                if tool not in current_tools:
                                    current_tools.append(tool)
                                
                                if DatabaseManager.update_user_tools(user_key, current_tools):
                                    DatabaseManager.delete_upgrade_request(upg_key)
                                    st.success("✅ Upgrade approved!")
                                    time.sleep(1)
                                    st.rerun()
                    
                    with col_reject:
                        if st.button("❌ REJECT", key=f"rej_{upg_key}"):
                            DatabaseManager.delete_upgrade_request(upg_key)
                            st.warning("Request rejected")
                            time.sleep(1)
                            st.rerun()
        else:
            st.info("No pending upgrades")

def render_admin_finance_tab():
    """Render finance overview"""
    st.markdown("### 💰 Donation Logs")
    
    donations = DatabaseManager.get_donations()
    
    if donations:
        total_amount = sum(d.get('amount', 0) for d in donations.values())
        
        st.metric("Total Contributions", f"₹{total_amount:,.2f}")
        
        st.markdown("---")
        
        for don_key, don_data in donations.items():
            email = don_data.get('email', 'Unknown')
            utr = don_data.get('utr', 'Unknown')
            amount = don_data.get('amount', 0)
            date = don_data.get('date', 'Unknown')
            
            st.markdown(f"""
            <div class="glass" style="padding: 15px; margin-bottom: 10px;">
                <b style="color:#00ff88;">₹{amount}</b> from <b>{email}</b><br>
                <small style="color:#888;">UTR: {utr} | Date: {date}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No donations recorded yet")

def render_admin_analytics_tab():
    """Render analytics dashboard"""
    st.markdown("### 📊 Platform Analytics")
    
    users = DatabaseManager.get_all_users()
    requests = DatabaseManager.get_requests()
    upgrades = DatabaseManager.get_upgrade_requests()
    donations = DatabaseManager.get_donations()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(users))
    
    with col2:
        st.metric("Pending Requests", len(requests))
    
    with col3:
        st.metric("Pending Upgrades", len(upgrades))
    
    with col4:
        total_donations = sum(d.get('amount', 0) for d in donations.values())
        st.metric("Total Raised", f"₹{total_donations}")
    
    st.markdown("---")
    
    # Tool usage statistics
    st.markdown("#### 🛠️ Tool Distribution")
    
    tool_count = {tool: 0 for tool in TOOLS_REGISTRY.keys()}
    
    for user_data in users.values():
        user_tools = user_data.get('tools', []) if isinstance(user_data, dict) else user_data
        for tool in user_tools:
            if tool in tool_count:
                tool_count[tool] += 1
    
    for tool, count in tool_count.items():
        percentage = (count / len(users) * 100) if users else 0
        st.progress(percentage / 100, text=f"{tool}: {count} users ({percentage:.1f}%)")

# =========================================================
# MAIN APPLICATION
# =========================================================

def main():
    """Main application entry point"""
    
    # Initialize
    load_custom_css()
    
    if not DatabaseManager.initialize():
        st.error("Failed to initialize database. Please check configuration.")
        return
    
    SessionManager.initialize_session()
    
    # Check session timeout
    if SessionManager.check_session_timeout():
        st.warning("Session timed out. Please login again.")
        st.rerun()
    
    # Route to appropriate page
    page = st.session_state.page
    
    if page == "home":
        render_home_page()
    
    elif page == "manifesto":
        render_manifesto_page()
    
    elif page == "donate":
        render_donate_page()
    
    elif page == "login":
        render_login_page()
    
    elif page == "hub":
        if st.session_state.role == UserRole.USER:
            render_hub_page()
        else:
            st.error("Unauthorized access")
            SessionManager.navigate_to("login")
            st.rerun()
    
    elif page == "admin":
        if st.session_state.role == UserRole.ADMIN:
            render_admin_page()
        else:
            st.error("Unauthorized access")
            SessionManager.navigate_to("login")
            st.rerun()
    
    else:
        SessionManager.navigate_to("home")
        st.rerun()

if __name__ == "__main__":
    main()
