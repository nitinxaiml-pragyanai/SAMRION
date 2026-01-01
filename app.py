import streamlit as st
import datetime
import random
import string
import time
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from groq import Groq

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
    
    * { font-family: 'Inter', sans-serif; color: white; }
    .stApp { background: linear-gradient(135deg, #000428 0%, #004e92 100%); background-attachment: fixed; }
    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px; margin-bottom: 20px;
    }
    .locked-card { opacity: 0.6; border: 1px dashed rgba(255, 100, 100, 0.3); filter: grayscale(0.8); }
    
    /* INPUTS & BUTTONS */
    .stTextInput > div > div > input { background: rgba(0, 0, 0, 0.5); border: 1px solid #444; color: white; border-radius: 10px; }
    div.stButton > button { background: linear-gradient(90deg, #00d2ff, #3a7bd5); border: none; color: white; font-weight: bold; border-radius: 30px; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FIREBASE & GROQ CONNECTION
# ==========================================
ADMIN_PASS = "ilovesamriddhisoni28oct"

# FIREBASE INIT
if not firebase_admin._apps:
    try:
        key_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(key_dict)
        db_url = key_dict.get("database_url", f"https://{key_dict['project_id']}-default-rtdb.firebaseio.com/")
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
    except Exception as e:
        st.error(f"🔥 FIREBASE ERROR: {e}")
        st.stop()

# GROQ INIT (For Site Manager)
def get_groq_client():
    try: return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: return None

# ==========================================
# 3. CORE LOGIC (DB & AI)
# ==========================================
# --- DATABASE FUNCTIONS ---
def get_user_access(user_pass):
    try:
        ref = db.reference(f'users/{user_pass}')
        return ref.get()
    except: return None

def add_user_with_access(new_pass, allowed_tools):
    db.reference(f'users/{new_pass}').set(allowed_tools)

def update_user_access(user_pass, new_tool_list):
    db.reference(f'users/{user_pass}').set(new_tool_list)

def add_upgrade_request(user_pass, tool_name, utr):
    req = {"user": user_pass, "tool": tool_name, "utr": utr, "date": str(datetime.date.today())}
    db.reference('upgrades').push(req)

def get_upgrades():
    return db.reference('upgrades').get() or {}

def delete_upgrade(key):
    db.reference(f'upgrades/{key}').delete()

def get_requests():
    return db.reference('requests').get() or {}

def add_request(email):
    db.reference('requests').push({"email": email, "date": str(datetime.date.today())})

def delete_request(key):
    db.reference(f'requests/{key}').delete()

def generate_pass():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=12))

# --- SITE MANAGER AI FUNCTIONS ---
def read_source_code():
    with open(__file__, "r", encoding="utf-8") as f: return f.read()

def write_source_code(new_code):
    # 1. Backup first
    with open("app_backup.py", "w", encoding="utf-8") as f:
        f.write(read_source_code())
    # 2. Overwrite
    with open(__file__, "w", encoding="utf-8") as f:
        f.write(new_code)

def consult_site_manager(instruction):
    client = get_groq_client()
    if not client: return "ERROR: Groq API Key Missing"
    
    current_code = read_source_code()
    
    prompt = f"""
    You are the 'Site Manager AI' for Samrion Central. 
    You have FULL CONTROL to edit the Python Streamlit code of this website.
    
    CURRENT CODE:
    ```python
    {current_code}
    ```
    
    USER INSTRUCTION: "{instruction}"
    
    TASK:
    1. Rewrite the full `app.py` code to implement the instruction.
    2. Maintain all existing functionality (Firebase, login, styles) unless asked to change.
    3. Return ONLY the python code inside code blocks.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# ==========================================
# 4. SESSION & NAVIGATION
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'user_pass' not in st.session_state: st.session_state.user_pass = None
if 'allowed_tools' not in st.session_state: st.session_state.allowed_tools = []

def nav_to(page): st.session_state.page = page
def logout(): 
    st.session_state.user_role = None
    st.session_state.user_pass = None
    st.session_state.allowed_tools = []
    st.session_state.page = "home"

# --- DYNAMIC TOOL LIST (AI CAN EDIT THIS) ---
ALL_TOOLS = ["MEDHA", "AKRITI", "VANI", "SANGRAH", "CODIQ"]
TOOL_DETAILS = {
    "MEDHA": {"desc": "The Brain (Knowledge)", "icon": "🧠", "url": "https://medha-ai.streamlit.app/"},
    "AKRITI": {"desc": "The Eye (Vision Gen)", "icon": "🎨", "url": "https://akriti.streamlit.app/"},
    "SANGRAH": {"desc": "The Collector (Mining)", "icon": "📦", "url": "https://sangrah.streamlit.app/"},
    "VANI": {"desc": "The Voice (Speech)", "icon": "🎙️", "url": "https://vaani-labs.streamlit.app/"},
    "CODIQ": {"desc": "The Architect (Code)", "icon": "💻", "url": "https://codiq-ai.streamlit.app/"}
}

# ==========================================
# 5. UI PAGES
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
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 50px;">
        <h2 style="color: #00d2ff;">PRAGYAN AI</h2>
        <p style="font-size: 1.2rem; color: #ccc;">The Awakening of Digital Consciousness.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c_a, c_b = st.columns(2)
    with c_a: 
        if st.button("📖 READ MANIFESTO", use_container_width=True): nav_to("about"); st.rerun()
    with c_b: 
        if st.button("🔐 LOGIN BRIDGE", use_container_width=True): nav_to("login"); st.rerun()

# --- PAGE: MANIFESTO ---
elif st.session_state.page == "about":
    if st.button("← BACK"): nav_to("home"); st.rerun()
    st.title("📖 SAMRION MANIFESTO")
    st.info("Vision & Mission Content Loaded Here...") # Placeholder to save tokens, AI preserves this

# --- PAGE: LOGIN ---
elif st.session_state.page == "login":
    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("<h1 style='text-align: center;'>🔐 BRIDGE</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            user_input = st.text_input("Enter Passkey", type="password")
            if st.button("AUTHENTICATE", type="primary", use_container_width=True):
                if user_input == ADMIN_PASS:
                    st.session_state.user_role = "admin"
                    nav_to("admin_panel"); st.rerun()
                else:
                    access = get_user_access(user_input)
                    if access is not None:
                        st.session_state.user_role = "user"
                        st.session_state.user_pass = user_input
                        st.session_state.allowed_tools = access
                        nav_to("hub"); st.rerun()
                    else:
                        st.error("⛔ Invalid Passkey")
                        st.session_state.show_buy = True
            
            if st.session_state.get('show_buy'):
                st.warning("Access Denied.")
                email = st.text_input("Email for Request")
                if st.button("📩 Send Request"):
                    add_request(email)
                    st.success("Request Sent.")
    if st.button("← Back"): nav_to("home"); st.rerun()

# --- PAGE: HUB (USER DASHBOARD) ---
elif st.session_state.page == "hub":
    st.markdown("## 💠 SAMRION AI SUITE")
    if st.button("🔒 LOGOUT"): logout(); st.rerun()
    st.markdown("---")
    
    my_access = st.session_state.allowed_tools if st.session_state.user_role == "user" else ALL_TOOLS
    
    cols = st.columns(3)
    for i, tool_name in enumerate(ALL_TOOLS):
        tool = TOOL_DETAILS.get(tool_name, {"desc": "New Tool", "icon": "❓", "url": "#"})
        is_unlocked = tool_name in my_access
        
        card_class = "glass-card" if is_unlocked else "glass-card locked-card"
        
        with cols[i % 3]:
            st.markdown(f"""
            <div class="{card_class}" style="text-align: center;">
                <h1>{tool['icon']}</h1>
                <h3>{tool_name}</h3>
                <p>{tool['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if is_unlocked:
                st.markdown(f"""<a href="{tool['url']}" target="_blank"><button style="width:100%; padding:10px; border-radius:20px; border:none; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color:white; font-weight:bold; cursor:pointer;">LAUNCH 🚀</button></a>""", unsafe_allow_html=True)
            else:
                # UPGRADE LOGIC
                with st.expander(f"🔒 UPGRADE (₹10)"):
                    st.caption("Access Restricted.")
                    st.write("1. Scan QR (Home Page)")
                    st.write("2. Pay ₹10")
                    utr = st.text_input("Enter UTR:", key=f"utr_{i}")
                    if st.button("🚀 REQUEST UNLOCK", key=f"req_{i}"):
                        if utr:
                            add_upgrade_request(st.session_state.user_pass, tool_name, utr)
                            st.success("Upgrade Request Sent!")
                        else:
                            st.error("Enter UTR")

# --- PAGE: ADMIN PANEL (THE BRAIN) ---
elif st.session_state.page == "admin_panel" and st.session_state.user_role == "admin":
    st.title("👑 FOUNDER'S CONSOLE")
    
    tab_keys, tab_reqs, tab_ai = st.tabs(["🔑 Keys & Users", "📩 Requests & Upgrades", "🤖 Site Manager AI"])
    
    # TAB 1: KEYS
    with tab_keys:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Generate Key")
            sel_tools = st.multiselect("Access Rights", ALL_TOOLS, default=ALL_TOOLS)
            if st.button("✨ CREATE KEY"):
                nk = generate_pass()
                add_user_with_access(nk, sel_tools)
                st.success(f"Key: `{nk}`"); st.code(nk)
        with c2:
            st.markdown("### Active Users")
            st.json(db.reference('users').get())

    # TAB 2: REQUESTS (NEW & UPGRADES)
    with tab_reqs:
        col_upg, col_new = st.columns(2)
        
        # UPGRADE REQUESTS
        with col_upg:
            st.markdown("### 🔼 Upgrade Requests (₹10)")
            upgrades = get_upgrades()
            if upgrades:
                for k, v in upgrades.items():
                    with st.expander(f"{v['tool']} - UTR: {v['utr']}"):
                        st.caption(f"User: {v['user']}")
                        if st.button("✅ Approve Upgrade", key=k):
                            # Fetch current tools
                            curr_access = get_user_access(v['user']) or []
                            if v['tool'] not in curr_access:
                                curr_access.append(v['tool'])
                                update_user_access(v['user'], curr_access)
                            delete_upgrade(k)
                            st.success("User Upgraded!")
                            time.sleep(1); st.rerun()
            else: st.info("No upgrades pending.")

        # NEW USER REQUESTS
        with col_new:
            st.markdown("### 📩 New User Requests")
            reqs = get_requests()
            if reqs:
                for k, v in reqs.items():
                    with st.expander(f"{v['email']}"):
                        grant_tools = st.multiselect("Tools", ALL_TOOLS, default=ALL_TOOLS, key=f"g_{k}")
                        if st.button("✅ Create & Send", key=k):
                            nk = generate_pass()
                            add_user_with_access(nk, grant_tools)
                            delete_request(k)
                            st.success(f"Key Created: {nk}")
            else: st.info("No new user requests.")

    # TAB 3: SITE MANAGER AI (SELF-EDITING)
    with tab_ai:
        st.markdown("### 🤖 Site Manager (Autonomous Admin)")
        st.caption("Powered by Llama 3.3 (80B Class) via Groq")
        
        with st.chat_message("assistant"):
            st.write("I am the Site Manager. I can add tools, fix bugs, or change the UI. What is your command, Founder?")
            
        cmd = st.chat_input("E.g., 'Add a tool named Nexus with url google.com'")
        
        if cmd:
            with st.chat_message("user"): st.write(cmd)
            
            with st.spinner("🧠 Analyzing Source Code & Generating Update..."):
                new_code_raw = consult_site_manager(cmd)
                
                # Extract code from markdown blocks
                if "```python" in new_code_raw:
                    clean_code = new_code_raw.split("```python")[1].split("```")[0]
                    
                    st.success("✅ Code Generated successfully!")
                    with st.expander("👀 Review Code Change"):
                        st.code(clean_code, language='python')
                    
                    if st.button("💾 APPLY UPDATE TO WEBSITE", type="primary"):
                        write_source_code(clean_code)
                        st.toast("SYSTEM UPDATED. REBOOTING...")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.error("AI failed to generate valid code structure.")
                    st.write(new_code_raw)

    st.markdown("---")
    if st.button("EXIT CONSOLE"): logout(); st.rerun()

else:
    nav_to("home"); st.rerun()
