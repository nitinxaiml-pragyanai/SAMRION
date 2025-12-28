import streamlit as st
import datetime
import random
import string
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# ==========================================
# 1. CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="SAMRION CENTRAL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === THE ROYAL CSS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* GLOBAL RESET */
    * { font-family: 'Inter', sans-serif; color: white; }
    
    /* BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        background-attachment: fixed;
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border-color: #00d2ff;
    }

    /* INPUTS */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.5); border: 1px solid #444; color: white; border-radius: 10px;
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        border: none; color: white; font-weight: bold; padding: 10px 25px; border-radius: 30px;
    }
    
    /* HIDE JUNK */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FIREBASE CONNECTION (THE CLOUD BRAIN)
# ==========================================
ADMIN_PASS = "ilovesamriddhisoni28oct"

# Initialize Firebase safely (prevent double-init error on reload)
if not firebase_admin._apps:
    try:
        # Load credentials from Streamlit Secrets
        key_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(key_dict)
        
        # Connect to Realtime Database
        # Note: Replace the URL below with YOUR database URL from Firebase Console
        # It usually looks like: https://project-id-default-rtdb.firebaseio.com/
        firebase_admin.initialize_app(cred, {
            'databaseURL': f"https://{key_dict['project_id']}-default-rtdb.firebaseio.com/"
        })
    except Exception as e:
        st.error(f"🔥 FIREBASE ERROR: {e}")
        st.stop()

def get_users():
    """Fetch valid user passes from Cloud"""
    ref = db.reference('users')
    data = ref.get()
    if data is None: return []
    # Return list of values (the passes)
    return list(data.values())

def add_user(new_pass):
    """Save new pass to Cloud"""
    ref = db.reference('users')
    ref.push(new_pass)

def get_requests():
    """Fetch pending buy requests"""
    ref = db.reference('requests')
    return ref.get() or {}

def add_request(email):
    """Save a buy request"""
    ref = db.reference('requests')
    ref.push({"email": email, "date": str(datetime.date.today())})

def delete_request(key):
    """Remove request after approval"""
    ref = db.reference(f'requests/{key}')
    ref.delete()

def generate_pass():
    chars = string.ascii_uppercase + string.digits + "@#&"
    return ''.join(random.choices(chars, k=12))

# ==========================================
# 3. SESSION STATE
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_role' not in st.session_state: st.session_state.user_role = None

def go_home(): st.session_state.page = "home"
def go_login(): st.session_state.page = "login"
def logout(): 
    st.session_state.user_role = None
    st.session_state.page = "home"

# ==========================================
# 4. PAGES
# ==========================================

# --- PAGE: HOME ---
if st.session_state.page == "home":
    c1, c2 = st.columns([1, 4])
    with c1:
        try: st.image("logo.png", width=100) 
        except: st.markdown("# 👑")
    with c2:
        st.markdown("# SAMRION TECHNOLOGIES")
        st.markdown("### *The Future of Intelligence*")
    st.markdown("---")
    
    st.markdown("""
    <div class="glass-card">
        <h2>🚀 Vision: PRAGYAN</h2>
        <p>Pragyan is not just AI. It is the awakening of digital consciousness in Bihar. 
        Founded by <b>Nitin Raj</b>, Samrion Technologies bridges human creativity and machine intelligence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🤝 Contribute")
        try: st.image("qr.png", caption="Scan via UPI", width=200)
        except: st.warning("QR Missing")
    with col_b:
        st.markdown("### 🔐 Access Hub")
        if st.button("ENTER BRIDGE ➔", use_container_width=True):
            go_login()
            st.rerun()

# --- PAGE: LOGIN ---
elif st.session_state.page == "login":
    st.markdown("<h1 style='text-align: center;'>🔐 THE BRIDGE</h1>", unsafe_allow_html=True)
    
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        with st.container(border=True):
            user_input = st.text_input("Enter UserPass / Admin Key", type="password")
            
            if st.button("AUTHENTICATE", type="primary", use_container_width=True):
                # 1. Check Admin
                if user_input == ADMIN_PASS:
                    st.session_state.user_role = "admin"
                    st.session_state.page = "admin_panel"
                    st.toast("👑 Welcome, Founder.", icon="🔓")
                    time.sleep(1)
                    st.rerun()
                
                # 2. Check Cloud Database for User
                else:
                    valid_users = get_users()
                    if user_input in valid_users:
                        st.session_state.user_role = "user"
                        st.session_state.page = "hub"
                        st.toast("✅ Access Granted.", icon="🚀")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("⛔ Invalid Passkey")
                        st.session_state.show_buy = True

            if st.session_state.get('show_buy'):
                st.markdown("---")
                st.warning("Access Denied.")
                st.write("Buy a license to access the Samrion Suite.")
                req_email = st.text_input("Email Address")
                if st.button("📩 Send Request"):
                    if req_email:
                        add_request(req_email)
                        st.success("Request sent to Admin.")
            
    if st.button("← Back"): go_home(); st.rerun()

# --- PAGE: THE HUB (YOUR LIVE APPS) ---
elif st.session_state.page == "hub" and st.session_state.user_role in ["user", "admin"]:
    st.markdown("## 💠 SAMRION AI SUITE")
    if st.button("🔒 LOGOUT"): logout(); st.rerun()
    st.markdown("---")
    
    # YOUR REAL URLS
    tools = [
        {"name": "MEDHA", "desc": "The Brain (Knowledge)", "icon": "🧠", "url": "https://medha-ai.streamlit.app/"},
        {"name": "AKRITI", "desc": "The Eye (Vision Gen)", "icon": "🎨", "url": "https://akriti.streamlit.app/"},
        {"name": "SANGRAH", "desc": "The Collector (Mining)", "icon": "📦", "url": "https://sangrah.streamlit.app/"},
        {"name": "VANI", "desc": "The Voice (Speech)", "icon": "🎙️", "url": "https://vaani-labs.streamlit.app/"},
        {"name": "CODIQ", "desc": "The Architect (Code)", "icon": "💻", "url": "https://codiq-ai.streamlit.app/"},
    ]
    
    cols = st.columns(3)
    for i, tool in enumerate(tools):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h1>{tool['icon']}</h1>
                <h3>{tool['name']}</h3>
                <p>{tool['desc']}</p>
                <a href="{tool['url']}" target="_blank">
                    <button style="background: linear-gradient(90deg, #00d2ff, #3a7bd5); border: none; color: white; padding: 10px 20px; border-radius: 20px; cursor: pointer; width: 100%;">
                        LAUNCH 🚀
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

# --- PAGE: ADMIN PANEL ---
elif st.session_state.page == "admin_panel" and st.session_state.user_role == "admin":
    st.markdown("## 👑 FOUNDER'S CONSOLE (FIREBASE CONNECTED)")
    
    c_l, c_r = st.columns([1, 1])
    
    with c_l:
        st.markdown("### ➕ Generate Key")
        if st.button("✨ CREATE USERPASS"):
            new_key = generate_pass()
            add_user(new_key) # Save to Cloud
            st.success(f"CREATED: `{new_key}`")
            st.code(new_key)
            
        st.markdown("### 📋 Active Keys (Cloud)")
        users = get_users()
        st.dataframe(users, use_container_width=True)

    with c_r:
        st.markdown("### 📩 Requests (Cloud)")
        requests = get_requests() # Returns dict {key: {email, date}}
        
        if requests:
            for key, val in requests.items():
                with st.expander(f"{val['email']} - {val['date']}"):
                    if st.button("✅ Approve", key=key):
                        new_key = generate_pass()
                        add_user(new_key) # Add user
                        delete_request(key) # Remove request
                        st.success(f"Approved! Send Key: {new_key}")
                        st.code(new_key)
                        time.sleep(2)
                        st.rerun()
        else:
            st.info("No requests.")

    st.markdown("---")
    if st.button("EXIT ADMIN"): logout(); st.rerun()

else:
    go_home(); st.rerun()
