import streamlit as st
import datetime
import random
import string
import time
import firebase_admin
from firebase_admin import credentials, db
from groq import Groq

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="SAMRION CENTRAL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. PHASE ♾️ ULTRA CINEMATIC CSS (FIXED)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

* { font-family: 'Inter', sans-serif; color: white; }

.stApp {
    background:
        radial-gradient(1200px circle at 15% 10%, rgba(0,210,255,0.09), transparent 40%),
        radial-gradient(900px circle at 85% 20%, rgba(255,0,127,0.07), transparent 40%),
        linear-gradient(180deg, #020617 0%, #000428 100%);
    background-attachment: fixed;
}

/* TYPOGRAPHY */
h1,h2,h3 { font-family: 'Outfit', sans-serif !important; letter-spacing: 2px; }

/* GLASS CARD */
.glass {
    background: linear-gradient(160deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.14);
    padding: 30px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}
.glass:hover { transform: translateY(-5px); border-color: #00d2ff; }

/* LOCKED STATE */
.locked { opacity: 0.5; filter: grayscale(1); border: 1px dashed rgba(255, 255, 255, 0.2); }

/* INPUTS & DROPDOWNS (FIXED VISIBILITY) */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: rgba(10, 20, 40, 0.8) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px;
}
/* Fix dropdown popup text color */
ul[data-testid="stSelectboxVirtualDropdown"] li { background-color: #000428 !important; color: white !important; }

/* BUTTONS */
div.stButton > button {
    background: linear-gradient(90deg, #00d2ff, #0055ff);
    border: none; border-radius: 50px;
    padding: 12px 30px; font-weight: 800;
    text-transform: uppercase; transition: 0.3s;
    color: white !important;
}
div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 25px rgba(0,210,255,0.6); }

/* REMOVE WHITE BACKGROUNDS */
div[data-testid="stExpander"] { background-color: transparent !important; border: 1px solid #333; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. MANIFESTOS
# =========================================================
MANIFESTO_PRAGYAN = """
### 🇮🇳 PRAGYAN: The Awakening of Indian Digital Consciousness
**The Mission:** Pragyan is not just AI; it is a movement. In a world dominated by foreign giants like GPT and Claude, India risks becoming a digital colony. Pragyan exists to change that.
**The Origin:** Founded by **Nitin Raj**, built without sponsors.
**The Roadmap:** 1. ✅ Nano Model (1–10M) 
2. 🔄 Mini Model (Current Goal) 
3. 🚀 Base Model
"""

MANIFESTO_TOOLS = """
### 🛠️ THE SAMRION ECOSYSTEM
**🧠 MEDHA:** The Ultimate Knowledge Engine.
**🎨 AKRITI:** The Visual Reality Engine.
**🎙️ VANI:** The Neural Voice Ecosystem.
**📦 SANGRAH:** The Infinite Resource Miner.
**💻 CODIQ:** The Infrastructure Architect.
"""

# =========================================================
# 4. BACKEND INIT
# =========================================================
ADMIN_PASS = "ilovesamriddhisoni28oct"

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred, {"databaseURL": st.secrets["firebase"].get("database_url")})
    except Exception as e: st.error(f"DB Error: {e}")

def get_groq():
    try: return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: return None

# DB Ops
def get_user(k): 
    try: return db.reference(f"users/{k}").get() 
    except: return None
def set_user(k, v): db.reference(f"users/{k}").set(v)
def del_user(k): db.reference(f"users/{k}").delete()
def get_all_users(): return db.reference("users").get()
def add_req(em): db.reference('requests').push({"email": em, "date": str(datetime.date.today())})
def get_reqs(): return db.reference('requests').get() or {}
def del_req(k): db.reference(f'requests/{k}').delete()
def add_upgrade(u, t, utr): db.reference('upgrades').push({"user": u, "tool": t, "utr": utr})
def get_upgrades(): return db.reference('upgrades').get() or {}
def del_upgrade(k): db.reference(f'upgrades/{k}').delete()
def add_donation(e, u, a): db.reference('donations').push({"email": e, "utr": u, "amt": a})
def get_donations(): return db.reference('donations').get() or {}

def gen_key(): return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

# =========================================================
# 5. NAV
# =========================================================
if "page" not in st.session_state: st.session_state.page = "home"
if "role" not in st.session_state: st.session_state.role = None
if "tools" not in st.session_state: st.session_state.tools = []
if "user_pass" not in st.session_state: st.session_state.user_pass = None

def go(p): st.session_state.page = p
def logout():
    st.session_state.role = None
    st.session_state.tools = []
    go("home")

TOOLS = {
    "MEDHA": ("🧠", "https://medha-ai.streamlit.app/"),
    "AKRITI": ("🎨", "https://akriti.streamlit.app/"),
    "VANI": ("🎙️", "https://vaani-labs.streamlit.app/"),
    "SANGRAH": ("📦", "https://sangrah.streamlit.app/"),
    "CODIQ": ("💻", "https://codiq-ai.streamlit.app/")
}
ALL_TOOLS = list(TOOLS.keys())

# =========================================================
# 6. PAGES
# =========================================================

# --- HOME ---
if st.session_state.page == "home":
    st.markdown("<br><br><h1 style='text-align:center; font-size:4rem; color:#00d2ff;'>SAMRION TECHNOLOGIES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:3px; opacity:0.8;'>THE FUTURE OF INTELLIGENCE</p><br><br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1,1])
    with c1: 
        if st.button("📖 MANIFESTO", use_container_width=True): go("about"); st.rerun()
    with c2: 
        if st.button("🔐 ENTER BRIDGE", use_container_width=True): go("login"); st.rerun()
    with c3: 
        if st.button("🤝 CONTRIBUTE", use_container_width=True): go("donate"); st.rerun()

# --- MANIFESTO ---
elif st.session_state.page == "about":
    if st.button("← BACK"): go("home"); st.rerun()
    t1, t2 = st.tabs(["VISION", "TOOLS"])
    with t1: st.markdown(f"<div class='glass'>{MANIFESTO_PRAGYAN}</div>", unsafe_allow_html=True)
    with t2: st.markdown(f"<div class='glass'>{MANIFESTO_TOOLS}</div>", unsafe_allow_html=True)

# --- DONATE ---
elif st.session_state.page == "donate":
    if st.button("← BACK"): go("home"); st.rerun()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass'><h3>🚀 Support Pragyan</h3><p>Funds go directly to GPU compute.</p></div>", unsafe_allow_html=True)
        try: st.image("qr.png", width=300)
        except: st.warning("Upload qr.png")
    with c2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        email = st.text_input("Your Email")
        utr = st.text_input("UTR (Transaction ID)")
        amt = st.number_input("Amount", value=50)
        if st.button("LOG DONATION"):
            add_donation(email, utr, amt)
            st.success("Recorded! Check email soon.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIN ---
elif st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c = st.columns([1,2,1])[1]
    with c:
        st.markdown("<div class='glass'><h2 style='text-align:center'>IDENTITY VERIFICATION</h2>", unsafe_allow_html=True)
        key = st.text_input("ACCESS CODE", type="password")
        if st.button("AUTHORIZE", use_container_width=True):
            if key == ADMIN_PASS:
                st.session_state.role = "admin"
                go("admin"); st.rerun()
            else:
                u = get_user(key)
                if u is not None:
                    st.session_state.role = "user"
                    st.session_state.user_pass = key
                    st.session_state.tools = u
                    go("hub"); st.rerun()
                else:
                    st.error("INVALID KEY")
                    st.session_state.show_req = True
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.session_state.get('show_req'):
            em = st.text_input("Enter Email to Request Access")
            if st.button("SEND REQUEST"):
                add_req(em)
                st.success("Request Sent")
    
    if st.button("← BACK"): go("home"); st.rerun()

# --- HUB (FIXED LAUNCH BUTTON) ---
elif st.session_state.page == "hub":
    st.markdown("## 💠 SAMRION ARMORY")
    if st.button("LOGOUT"): logout(); st.rerun()
    
    my_tools = st.session_state.tools
    cols = st.columns(3)
    
    for i, (name, (icon, url)) in enumerate(TOOLS.items()):
        unlocked = name in my_tools
        cls = "glass" if unlocked else "glass locked"
        
        with cols[i % 3]:
            # Clean Card
            st.markdown(f"""
            <div class="{cls}" style="text-align:center">
                <div style="font-size:3rem">{icon}</div>
                <h3>{name}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # FIXED BUTTON: Uses Streamlit Native Link Button (Clean & Working)
            if unlocked:
                st.link_button(f"🚀 LAUNCH {name}", url, use_container_width=True)
            else:
                with st.expander("🔒 UNLOCK (₹10)"):
                    utr = st.text_input("UTR", key=f"u{i}")
                    if st.button("REQ UNLOCK", key=f"b{i}"):
                        add_upgrade(st.session_state.user_pass, name, utr)
                        st.success("Sent")

# --- ADMIN (FIXED UI) ---
elif st.session_state.page == "admin":
    st.title("👑 FOUNDER CONSOLE")
    if st.button("EXIT"): logout(); st.rerun()
    
    t1, t2, t3 = st.tabs(["USERS", "REQUESTS", "FINANCE"])
    
    with t1:
        # CLEANER USER MANAGEMENT
        st.markdown("### 👥 User Database")
        c_gen, c_list = st.columns([1, 2])
        
        with c_gen:
            st.info("Mint New Key")
            sel = st.multiselect("Tools", ALL_TOOLS, default=ALL_TOOLS)
            if st.button("GENERATE KEY"):
                k = gen_key()
                set_user(k, sel)
                st.success(f"KEY: {k}"); st.code(k)
        
        with c_list:
            st.info("Active Users (Delete Enabled)")
            users = get_all_users()
            if users:
                for k, v in users.items():
                    # ROW LAYOUT
                    r1, r2 = st.columns([4, 1])
                    with r1: st.code(f"{k} : {v}")
                    with r2: 
                        if st.button("❌", key=f"del_{k}"):
                            del_user(k)
                            st.rerun()
            else:
                st.warning("No users found.")

    with t2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### New Access Requests")
            reqs = get_reqs()
            for k, v in reqs.items():
                with st.expander(v['email']):
                    sel = st.multiselect("Grant", ALL_TOOLS, default=ALL_TOOLS, key=f"g{k}")
                    if st.button("CREATE", key=f"c{k}"):
                        nk = gen_key()
                        set_user(nk, sel)
                        del_req(k)
                        st.success(f"Key: {nk}")
        with c2:
            st.markdown("#### Upgrade Requests")
            upgs = get_upgrades()
            for k, v in upgs.items():
                with st.expander(f"{v['tool']} | UTR: {v['utr']}"):
                    if st.button("APPROVE", key=f"a{k}"):
                        curr = get_user(v['user']) or []
                        if v['tool'] not in curr: curr.append(v['tool'])
                        set_user(v['user'], curr)
                        del_upgrade(k)
                        st.success("Done")
                        time.sleep(1); st.rerun()

    with t3:
        st.markdown("#### 💰 Donation Logs")
        dons = get_donations()
        if dons:
            for k, v in dons.items():
                st.code(f"Email: {v.get('email')} | UTR: {v.get('utr')} | ₹{v.get('amt')}")
        else: st.info("No donations yet")

else:
    go("home"); st.rerun()
