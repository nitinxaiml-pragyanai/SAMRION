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
    page_title="SAMRION",
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

    /* HEADERS (Outfit Font for Titles) */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }

    /* GLASS CARDS (For Tools & Vision) */
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

    /* MANIFESTO TEXT STYLE */
    .manifesto-text {
        color: #e0e0e0 !important;
        line-height: 1.8;
        font-size: 1.1rem;
        background: rgba(0,0,0,0.3);
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid #00d2ff;
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

if not firebase_admin._apps:
    try:
        key_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(key_dict)
        # Use database_url if present, else guess
        db_url = key_dict.get("database_url", f"https://{key_dict['project_id']}-default-rtdb.firebaseio.com/")
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
    except Exception as e:
        st.error(f"🔥 FIREBASE ERROR: {e}")
        st.stop()

# --- DB Functions ---
def get_users():
    try:
        ref = db.reference('users')
        data = ref.get()
        if data is None: return []
        if isinstance(data, list): return [x for x in data if x]
        return list(data.values())
    except: return []

def add_user(new_pass):
    db.reference('users').push(new_pass)

def get_requests():
    return db.reference('requests').get() or {}

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

def nav_to(page): st.session_state.page = page
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
    
    # Navigation Buttons
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        if st.button("📖 READ THE MANIFESTO", use_container_width=True):
            nav_to("about")
            st.rerun()
    with col_b:
        if st.button("🔐 ENTER BRIDGE (LOGIN)", use_container_width=True):
            nav_to("login")
            st.rerun()
    with col_c:
        if st.button("🤝 CONTRIBUTE (UPI)", use_container_width=True):
            # Just scroll to QR or show modal (Simulated by staying on page)
            st.toast("Scroll down for QR Code")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # QR Section
    c_qr, c_txt = st.columns([1, 2])
    with c_qr:
        try: st.image("qr.png", caption="Scan via UPI", width=250)
        except: st.warning("QR Code Missing")
    with c_txt:
        st.markdown("### Support The Mission")
        st.write("Pragyan is independent. We have no corporate overlords. Your contribution fuels the GPU compute needed to train India's First Open Source Model.")

# --- PAGE: MANIFESTO (LONG ABOUT) ---
elif st.session_state.page == "about":
    if st.button("← BACK TO HOME"): nav_to("home"); st.rerun()
    
    st.title("📖 THE SAMRION MANIFESTO")
    st.caption("Our Vision, Our Tools, Our Future.")
    st.markdown("---")

    # TABS FOR ORGANIZATION
    tab_pragyan, tab_tools = st.tabs(["🇮🇳 PRAGYAN (The Vision)", "🛠️ THE ECOSYSTEM (Tools)"])

    with tab_pragyan:
        st.markdown("""
        <div class="manifesto-text">
            <h2 style="color:#00d2ff">PRAGYAN: The Awakening of Indian Digital Consciousness</h2>
            <br>
            <h3>The Mission</h3>
            <p>Pragyan (meaning "Wisdom" or "Supreme Intelligence" in Sanskrit) is not just another AI model; it is a movement towards digital sovereignty. In a world dominated by foreign AI giants like OpenAI and Google, India—the world's largest data consumer—risks becoming a digital colony. We rely on foreign servers, foreign policies, and foreign algorithms.</p>
            <p>Pragyan exists to change that. It is India’s first community-driven, open-source AI project designed to build indigenous intelligence from the ground up.</p>
            <br>
            <h3>The Origin Story</h3>
            <p>Founded by <b>Nitin Raj</b> under the banner of <b>Samrion Technologies</b>, Pragyan was born from a simple yet powerful realization: <i>We cannot build our future on rented land.</i> Without big corporate sponsors or billion-dollar funding, Pragyan is being built line-by-line, tensor-by-tensor, by an independent developer and a community of believers.</p>
            <br>
            <h3>Why Pragyan Matters?</h3>
            <ul>
                <li><b>Data Sovereignty:</b> Your data should not leave Indian shores. Pragyan aims to keep Indian data within India.</li>
                <li><b>Linguistic Inclusion:</b> While Western models focus on English, Pragyan is being trained to understand the nuance of India's diverse languages.</li>
                <li><b>True Open Source:</b> Unlike "Open" AI companies that keep their weights closed, Pragyan believes in total transparency.</li>
            </ul>
            <br>
            <h3>The Roadmap to Ultra</h3>
            <p>We are climbing the ladder of intelligence:</p>
            <ol>
                <li><b>✅ The Nano Model (1–10M Parameters):</b> The foundation has been laid. The proof of concept is operational.</li>
                <li><b>🔄 The Mini Model (Current Goal):</b> We are currently gathering the GPU compute resources required to train a model capable of complex reasoning.</li>
                <li><b>🚀 The Base Model & Beyond:</b> The ultimate goal is to achieve GPT-Class intelligence that runs on Indian infrastructure.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with tab_tools:
        st.markdown("### The Samrion Ecosystem")
        
        # MEDHA
        st.markdown("""
        <div class="glass-card">
            <h3>🧠 MEDHA: The Ultimate Knowledge Engine</h3>
            <p><i>Sanskrit Meaning: Intellect / Wisdom</i></p>
            <p>Medha is the intellectual core. It serves as your personal polymath—a digital entity designed not just to answer questions, but to understand context, reason through complex problems, and provide insightful solutions.</p>
            <ul>
                <li><b>Deep Reasoning:</b> Powered by advanced LLMs optimized for logical deduction.</li>
                <li><b>Contextual Awareness:</b> Medha remembers your conversation and builds upon previous exchanges.</li>
                <li><b>Multilingual Fluency:</b> Capable of processing English, Hindi, and Hinglish.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # AKRITI
        st.markdown("""
        <div class="glass-card">
            <h3>🎨 AKRITI: The Visual Reality Engine</h3>
            <p><i>Sanskrit Meaning: Form / Shape</i></p>
            <p>Akriti is the manifestation of pure imagination. It breaks the barrier between "thought" and "visual."</p>
            <ul>
                <li><b>Text-to-Image:</b> Creates hyper-realistic images from simple prompts using Flux-Realism.</li>
                <li><b>The Remix Engine:</b> A specialized module for photo editing and AI alterations.</li>
                <li><b>High-Contrast UI:</b> Designed for professional designers with a sleek, visible interface.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # VANI
        st.markdown("""
        <div class="glass-card">
            <h3>🎙️ VANI: The Neural Voice Ecosystem</h3>
            <p><i>Sanskrit Meaning: Voice / Speech</i></p>
            <p>Vani is the voice of the machine. It introduces the concept of "Digital Soul," allowing users to clone and transport voices.</p>
            <ul>
                <li><b>.SMRV Format:</b> Proprietary file format (Samrion Real Voice) to encrypt voice tensors.</li>
                <li><b>God Mode (Cloning):</b> Clones a human voice with 99% accuracy using ElevenLabs.</li>
                <li><b>Phonetic Calibration:</b> Uses scientific pangrams to capture accents perfectly.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # SANGRAH
        st.markdown("""
        <div class="glass-card">
            <h3>📦 SANGRAH: The Infinite Resource Miner</h3>
            <p><i>Sanskrit Meaning: Collection / Hoard</i></p>
            <p>Sangrah is the heavy machinery of machine learning. It automates dataset collection.</p>
            <ul>
                <li><b>Industrial Mining:</b> Scrapes 50,000+ images in a single session.</li>
                <li><b>Flash-Speed:</b> Opens 30 parallel connections for instant downloads.</li>
                <li><b>Auto-Zipping:</b> Categorizes and compresses datasets for immediate training.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # CODIQ
        st.markdown("""
        <div class="glass-card">
            <h3>💻 CODIQ: The Infrastructure Architect</h3>
            <p><i>Sanskrit Meaning: Coded Intelligence</i></p>
            <p>Codiq is the builder. It creates other tools. It is a context-aware software engineer.</p>
            <ul>
                <li><b>Genesis Protocol:</b> Architects full software projects with dependencies in one go.</li>
                <li><b>Neural Memory:</b> Remembers project history for step-by-step building.</li>
                <li><b>Smart Packaging:</b> Auto-names and zips code into deployable packages.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- PAGE: LOGIN BRIDGE ---
elif st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown("<h1 style='text-align: center;'>🔐 THE BRIDGE</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            user_input = st.text_input("Enter UserPass / Admin Key", type="password")
            
            if st.button("AUTHENTICATE", type="primary", use_container_width=True):
                if user_input == ADMIN_PASS:
                    st.session_state.user_role = "admin"
                    nav_to("admin_panel")
                    st.toast("👑 Welcome, Founder.", icon="🔓")
                    time.sleep(1); st.rerun()
                
                else:
                    valid_users = get_users()
                    if user_input in valid_users:
                        st.session_state.user_role = "user"
                        nav_to("hub")
                        st.toast("✅ Access Granted.", icon="🚀")
                        time.sleep(1); st.rerun()
                    else:
                        st.error("⛔ Invalid Passkey")
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

# --- PAGE: THE HUB ---
elif st.session_state.page == "hub" and st.session_state.user_role in ["user", "admin"]:
    st.markdown("## 💠 SAMRION AI SUITE")
    if st.button("🔒 LOGOUT"): logout(); st.rerun()
    st.markdown("---")
    
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
    st.markdown("## 👑 FOUNDER'S CONSOLE")
    c_l, c_r = st.columns([1, 1])
    
    with c_l:
        st.markdown("### ➕ Generate Key")
        if st.button("✨ CREATE USERPASS"):
            new_key = generate_pass()
            add_user(new_key)
            st.success(f"CREATED: `{new_key}`")
            st.code(new_key)
        st.markdown("### 📋 Active Keys")
        st.dataframe(get_users(), use_container_width=True)

    with c_r:
        st.markdown("### 📩 Requests")
        reqs = get_requests()
        if reqs:
            for k, v in reqs.items():
                with st.expander(f"{v['email']} - {v['date']}"):
                    if st.button("✅ Approve", key=k):
                        nk = generate_pass()
                        add_user(nk)
                        delete_request(k)
                        st.success(f"Send Key: {nk}")
                        st.code(nk)
                        time.sleep(2); st.rerun()
        else: st.info("No pending requests.")

    st.markdown("---")
    if st.button("EXIT ADMIN"): logout(); st.rerun()

else:
    nav_to("home"); st.rerun()
