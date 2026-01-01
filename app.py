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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* GLOBAL RESET */
    * { font-family: 'Inter', sans-serif; color: white; }
    
    /* BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        background-attachment: fixed;
    }

    /* HEADERS */
    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; }

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

    /* LOCKED CARD STYLE */
    .locked-card {
        opacity: 0.6;
        border: 1px dashed rgba(255, 100, 100, 0.3);
        filter: grayscale(0.8);
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
# 2. FIREBASE CONNECTION
# ==========================================
ADMIN_PASS = "ilovesamriddhisoni28oct"

# Initialize Firebase safely
if not firebase_admin._apps:
    try:
        key_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(key_dict)
        
        if "database_url" in key_dict:
            db_url = key_dict["database_url"]
        else:
            db_url = f"https://{key_dict['project_id']}-default-rtdb.firebaseio.com/"
            
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
    except Exception as e:
        st.error(f"🔥 FIREBASE ERROR: {e}")
        st.stop()

# --- NEW DATABASE FUNCTIONS ---

def get_user_access(user_pass):
    """Checks if user exists and returns their allowed tools"""
    try:
        # DB Structure: users -> { "USERPASS123": ["MEDHA", "AKRITI"], ... }
        ref = db.reference(f'users/{user_pass}')
        data = ref.get()
        return data # Returns list of tools or None
    except: return None

def add_user_with_access(new_pass, allowed_tools):
    """Save new pass with specific tool access"""
    ref = db.reference(f'users/{new_pass}')
    ref.set(allowed_tools)

def get_all_users():
    """Get all users for Admin Panel"""
    ref = db.reference('users')
    return ref.get() or {}

def get_requests():
    ref = db.reference('requests')
    return ref.get() or {}

def add_request(email):
    db.reference('requests').push({"email": email, "date": str(datetime.date.today())})

def delete_request(key):
    db.reference(f'requests/{key}').delete()

def generate_pass():
    chars = string.ascii_uppercase + string.digits + "@#&"
    return ''.join(random.choices(chars, k=12))

# ==========================================
# 3. SESSION & NAV
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'allowed_tools' not in st.session_state: st.session_state.allowed_tools = []

def nav_to(page): st.session_state.page = page
def logout(): 
    st.session_state.user_role = None
    st.session_state.allowed_tools = []
    st.session_state.page = "home"

# TOOL MASTER LIST
ALL_TOOLS = ["MEDHA", "AKRITI", "VANI", "SANGRAH", "CODIQ"]

# ==========================================
# 4. PAGES
# ==========================================

# --- PAGE: HOME ---
if st.session_state.page == "home":
    c1, c2 = st.columns([1, 4])
    with c1:
        try: st.image("logo.png", width=120) 
        except: st.markdown("# 👑")
    with c2:
        st.markdown("<h1 style='font-size: 3rem;'>SAMRION TECHNOLOGIES</h1>", unsafe_allow_html=True)
        st.markdown("### *The Future of Intelligence*")
    
    st.markdown("---")
    
    # Hero
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 50px;">
        <h2 style="color: #00d2ff; font-size: 2.5rem;">PRAGYAN AI</h2>
        <p style="font-size: 1.2rem; color: #ccc;">The Awakening of Digital Consciousness in India.</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        if st.button("📖 READ THE MANIFESTO", use_container_width=True):
            nav_to("about"); st.rerun()
    with col_b:
        if st.button("🔐 ENTER BRIDGE (LOGIN)", use_container_width=True):
            nav_to("login"); st.rerun()
    with col_c:
        if st.button("🤝 CONTRIBUTE (UPI)", use_container_width=True):
            st.toast("Scroll down for QR Code")

    st.markdown("<br>", unsafe_allow_html=True)
    c_qr, c_txt = st.columns([1, 2])
    with c_qr:
        try: st.image("qr.png", caption="Scan via UPI", width=250)
        except: st.warning("QR Code Missing")
    with c_txt:
        st.markdown("### Support The Mission")
        st.write("Pragyan is independent. Your contribution fuels the GPU compute needed to train India's First Open Source Model.")

# --- PAGE: MANIFESTO ---
elif st.session_state.page == "about":
    if st.button("← BACK TO HOME"): nav_to("home"); st.rerun()
    st.title("📖 THE SAMRION MANIFESTO")
    st.markdown("---")
    # (Leaving text content same as previous for brevity)
    st.info("The full manifesto content is loaded here.")

# --- PAGE: LOGIN BRIDGE (UPDATED) ---
elif st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown("<h1 style='text-align: center;'>🔐 THE BRIDGE</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            user_input = st.text_input("Enter UserPass / Admin Key", type="password")
            
            if st.button("AUTHENTICATE", type="primary", use_container_width=True):
                # 1. ADMIN CHECK
                if user_input == ADMIN_PASS:
                    st.session_state.user_role = "admin"
                    nav_to("admin_panel")
                    st.toast("👑 Welcome, Founder.", icon="🔓")
                    time.sleep(1); st.rerun()
                
                # 2. USER CHECK (With Specific Access)
                else:
                    access_list = get_user_access(user_input)
                    if access_list:
                        st.session_state.user_role = "user"
                        st.session_state.allowed_tools = access_list # Store their specific tools
                        nav_to("hub")
                        st.toast("✅ Access Granted.", icon="🚀")
                        time.sleep(1); st.rerun()
                    else:
                        st.error("⛔ Invalid or Expired Passkey")
                        st.session_state.show_buy = True

            if st.session_state.get('show_buy'):
                st.markdown("---")
                st.warning("Access Denied.")
                req_email = st.text_input("Enter Email to Buy License")
                if st.button("📩 Send Request"):
                    if req_email:
                        add_request(req_email)
                        st.success("Request Sent! Admin will contact you.")
            
    if st.button("← Back"): nav_to("home"); st.rerun()

# --- PAGE: THE HUB (SMART LOCKS) ---
elif st.session_state.page == "hub" and st.session_state.user_role in ["user", "admin"]:
    st.markdown("## 💠 SAMRION AI SUITE")
    if st.button("🔒 LOGOUT"): logout(); st.rerun()
    st.markdown("---")
    
    # Tool Data
    tools = [
        {"name": "MEDHA", "desc": "The Brain (Knowledge)", "icon": "🧠", "url": "https://medha-ai.streamlit.app/"},
        {"name": "AKRITI", "desc": "The Eye (Vision Gen)", "icon": "🎨", "url": "https://akriti.streamlit.app/"},
        {"name": "SANGRAH", "desc": "The Collector (Mining)", "icon": "📦", "url": "https://sangrah.streamlit.app/"},
        {"name": "VANI", "desc": "The Voice (Speech)", "icon": "🎙️", "url": "https://vaani-labs.streamlit.app/"},
        {"name": "CODIQ", "desc": "The Architect (Code)", "icon": "💻", "url": "https://codiq-ai.streamlit.app/"},
    ]
    
    # Allow Admin to see everything
    my_access = st.session_state.allowed_tools if st.session_state.user_role == "user" else ALL_TOOLS
    
    cols = st.columns(3)
    for i, tool in enumerate(tools):
        is_unlocked = tool['name'] in my_access
        
        # Style change based on access
        card_class = "glass-card" if is_unlocked else "glass-card locked-card"
        btn_text = "LAUNCH 🚀" if is_unlocked else "🔒 LOCKED"
        btn_color = "linear-gradient(90deg, #00d2ff, #3a7bd5)" if is_unlocked else "#444"
        
        with cols[i % 3]:
            # HTML Card
            st.markdown(f"""
            <div class="{card_class}" style="text-align: center;">
                <h1>{tool['icon']}</h1>
                <h3>{tool['name']}</h3>
                <p>{tool['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Logic Button
            if is_unlocked:
                st.markdown(f"""<a href="{tool['url']}" target="_blank"><button style="background: {btn_color}; border: none; color: white; padding: 10px 20px; border-radius: 20px; cursor: pointer; width: 100%;">{btn_text}</button></a>""", unsafe_allow_html=True)
            else:
                st.button(f"{btn_text} (Upgrade)", key=f"lock_{i}", disabled=True, use_container_width=True)

# --- PAGE: ADMIN PANEL (TIERED GENERATOR) ---
elif st.session_state.page == "admin_panel" and st.session_state.user_role == "admin":
    st.markdown("## 👑 FOUNDER'S CONSOLE")
    c_l, c_r = st.columns([1, 1])
    
    with c_l:
        st.markdown("### ➕ Generate Key")
        
        # NEW: SELECT TOOLS
        selected_tools = st.multiselect("Select Access Rights", ALL_TOOLS, default=ALL_TOOLS)
        
        if st.button("✨ CREATE CUSTOM KEY"):
            if selected_tools:
                new_key = generate_pass()
                add_user_with_access(new_key, selected_tools) # Save Dictionary
                st.success(f"CREATED: `{new_key}`")
                st.write(f"Access: {selected_tools}")
                st.code(new_key)
            else:
                st.error("Select at least one tool.")
            
        st.markdown("### 📋 Active Keys")
        users = get_all_users()
        if users:
            # Display dict nicely
            st.json(users, expanded=False)
        else:
            st.info("No active keys.")

    with c_r:
        st.markdown("### 📩 Requests")
        reqs = get_requests()
        if reqs:
            for k, v in reqs.items():
                with st.expander(f"{v['email']} - {v['date']}"):
                    # Admin can choose what to give the requester
                    req_tools = st.multiselect("Grant Access:", ALL_TOOLS, default=ALL_TOOLS, key=f"sel_{k}")
                    
                    if st.button("✅ Approve & Send", key=k):
                        nk = generate_pass()
                        add_user_with_access(nk, req_tools)
                        delete_request(k)
                        st.success(f"Key: {nk}")
                        st.write(f"Tools: {req_tools}")
                        st.code(nk)
        else: st.info("No pending requests.")

    st.markdown("---")
    if st.button("EXIT ADMIN"): logout(); st.rerun()

else:
    nav_to("home"); st.rerun()
