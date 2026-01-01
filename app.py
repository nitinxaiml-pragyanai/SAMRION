import streamlit as st
import datetime
import random
import string
import time
import firebase_admin
from firebase_admin import credentials, db
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SAMRION CENTRAL",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# PHASE ♾️ ULTRA CINEMATIC CSS
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
h1,h2,h3 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 2px;
}

/* HERO */
.hero {
    padding: 90px 30px;
    border-radius: 36px;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.01));
    backdrop-filter: blur(22px);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 40px 120px rgba(0,0,0,0.7);
    animation: float 8s ease-in-out infinite;
    text-align: center;
}

/* GLASS CARD */
.glass {
    background: linear-gradient(160deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
    backdrop-filter: blur(20px);
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.14);
    padding: 38px;
    margin-bottom: 28px;
    transition: all 0.5s ease;
    position: relative;
}

.glass:hover {
    transform: translateY(-10px) scale(1.025);
    box-shadow: 0 30px 70px rgba(0,0,0,0.8);
}

/* LOCKED */
.locked {
    opacity: 0.45;
    filter: grayscale(1);
    border-style: dashed;
    pointer-events: none;
}

/* GRADIENT TEXT */
.gradient {
    background: linear-gradient(90deg, #00d2ff, #ff007f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* BUTTONS */
div.stButton > button {
    background: linear-gradient(90deg, #00d2ff, #0055ff);
    border: none;
    border-radius: 70px;
    padding: 16px 36px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    transition: all 0.35s ease;
}

div.stButton > button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 35px rgba(0,210,255,0.8);
}

/* INPUTS */
.stTextInput input {
    background: rgba(3,10,30,0.9) !important;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.18);
    padding: 14px;
}

@keyframes float {
    0% { transform: translateY(0); }
    50% { transform: translateY(-18px); }
    100% { transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MANIFESTOS
# =========================================================
MANIFESTO_PRAGYAN = """
### 🇮🇳 PRAGYAN — DIGITAL SOVEREIGNTY PROTOCOL

Pragyan is not a product.  
It is **India reclaiming intelligence**.

Built to end dependency.  
Built to keep Indian data on Indian soil.  
Built openly, transparently, fearlessly.

Founded by **Nitin Raj** under **Samrion Technologies**.

No VC control.  
No foreign masters.  
Only code, compute, and conviction.
"""

MANIFESTO_TOOLS = """
### 🛠️ THE SAMRION ARMORY

🧠 **MEDHA** — Reasoning Engine  
🎨 **AKRITI** — Visual Intelligence  
🎙️ **VANI** — Voice Soul System  
📦 **SANGRAH** — Data Mining Core  
💻 **CODIQ** — Autonomous Architect

Each tool is a weapon.
Together, they form intelligence.
"""

# =========================================================
# BACKEND INIT
# =========================================================
ADMIN_PASS = "ilovesamriddhisoni28oct"

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(
        cred,
        {"databaseURL": f"https://{cred.project_id}-default-rtdb.firebaseio.com/"}
    )

def groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================================================
# DATABASE OPS
# =========================================================
def get_user(key): return db.reference(f"users/{key}").get()
def set_user(key, tools): db.reference(f"users/{key}").set(tools)
def gen_key(): return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

# =========================================================
# STATE
# =========================================================
if "page" not in st.session_state: st.session_state.page = "home"
if "role" not in st.session_state: st.session_state.role = None
if "tools" not in st.session_state: st.session_state.tools = []

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

# =========================================================
# HOME
# =========================================================
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <h1 class="gradient">PRAGYAN AI</h1>
        <h3>The Awakening of Indian Digital Consciousness</h3>
        <p style="opacity:0.7;letter-spacing:3px;">
        BUILT IN INDIA · OWNED BY COMMUNITY · OPEN BY DESIGN
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📖 MANIFESTO", use_container_width=True):
            go("about"); st.rerun()
    with c2:
        if st.button("🔐 ENTER THE BRIDGE", use_container_width=True):
            go("login"); st.rerun()

# =========================================================
# MANIFESTO
# =========================================================
elif st.session_state.page == "about":
    if st.button("← RETURN"): go("home"); st.rerun()
    st.markdown(f"<div class='glass'>{MANIFESTO_PRAGYAN}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass'>{MANIFESTO_TOOLS}</div>", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================
elif st.session_state.page == "login":
    st.markdown("<h2 style='text-align:center'>VERIFY DIGITAL IDENTITY</h2>", unsafe_allow_html=True)
    key = st.text_input("CLEARANCE CODE", type="password")
    if st.button("AUTHORIZE"):
        if key == ADMIN_PASS:
            st.session_state.role = "admin"
            go("admin")
            st.rerun()
        user = get_user(key)
        if user:
            st.session_state.role = "user"
            st.session_state.tools = user
            go("hub")
            st.rerun()
        st.error("ACCESS DENIED")

    if st.button("← BACK"): go("home"); st.rerun()

# =========================================================
# HUB
# =========================================================
elif st.session_state.page == "hub":
    st.markdown("## 💠 SAMRION ARMORY")
    if st.button("LOGOUT"): logout(); st.rerun()
    cols = st.columns(3)

    for i,(name,(icon,url)) in enumerate(TOOLS.items()):
        unlocked = name in st.session_state.tools
        with cols[i%3]:
            st.markdown(
                f"<div class='glass {'locked' if not unlocked else ''}'>"
                f"<h2>{icon} {name}</h2>"
                f"</div>", unsafe_allow_html=True)
            if unlocked:
                st.markdown(f"<a href='{url}' target='_blank'><button>LAUNCH</button></a>", unsafe_allow_html=True)

# =========================================================
# ADMIN
# =========================================================
elif st.session_state.page == "admin":
    st.markdown("## 👑 FOUNDER MODE ENABLED")
    if st.button("EXIT"): logout(); st.rerun()

    sel = st.multiselect("Grant Access", list(TOOLS.keys()), default=list(TOOLS.keys()))
    if st.button("MINT KEY"):
        k = gen_key()
        set_user(k, sel)
        st.success(f"KEY: {k}")
