import streamlit as st
import datetime
import random
import string
import time
import os
import json  # Added for the fix
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
# 2. PHASE ♾️ ULTRA CINEMATIC CSS
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
    margin-bottom: 40px;
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
    overflow: hidden;
}

.glass:hover {
    transform: translateY(-10px) scale(1.025);
    box-shadow: 0 30px 70px rgba(0,0,0,0.8);
    border-color: #00d2ff;
}

/* LOCKED STATE */
.locked {
    opacity: 0.5;
    filter: grayscale(1);
    border: 1px dashed rgba(255, 255, 255, 0.2);
}

/* GRADIENT TEXT */
.gradient {
    background: linear-gradient(90deg, #00d2ff, #ff007f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* MANIFESTO TEXT */
.manifesto-body {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #e0e0e0;
    text-align: left;
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
    width: 100%;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 35px rgba(0,210,255,0.8);
}

/* INPUTS */
.stTextInput input {
    background: rgba(3,10,30,0.9) !important;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.18);
    padding: 14px;
    color: white !important;
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
# 3. CONTENT MANIFESTOS (FULL LENGTH)
# =========================================================
MANIFESTO_PRAGYAN = """
### 🇮🇳 PRAGYAN: The Awakening of Indian Digital Consciousness

**The Mission**
Pragyan (meaning "Wisdom" or "Supreme Intelligence" in Sanskrit) is not just another AI model; it is a movement towards digital sovereignty. In a world dominated by foreign AI giants like OpenAI and Google, India—the world's largest data consumer—risks becoming a digital colony. We rely on foreign servers, foreign policies, and foreign algorithms.

Pragyan exists to change that. It is India’s first community-driven, open-source AI project designed to build indigenous intelligence from the ground up.

**The Origin Story**
Founded by **Nitin Raj** under the banner of **Samrion Technologies**, Pragyan was born from a simple yet powerful realization: *We cannot build our future on rented land.* Without big corporate sponsors or billion-dollar funding, Pragyan is being built line-by-line, tensor-by-tensor, by an independent developer and a community of believers.

**Why Pragyan Matters?**
* **Data Sovereignty:** Your data should not leave Indian shores. Pragyan aims to keep Indian data within India.
* **Linguistic Inclusion:** While Western models focus on English, Pragyan is being trained to understand the nuance of India's diverse languages.
* **True Open Source:** Unlike "Open" AI companies that keep their weights closed, Pragyan believes in total transparency. Every line of code, every dataset, and every model weight is shared with the people.

**The Roadmap to Ultra**
We are climbing the ladder of intelligence:
1.  **✅ The Nano Model (1–10M Parameters):** The foundation has been laid. The proof of concept is operational.
2.  **🔄 The Mini Model (Current Goal):** We are currently gathering the GPU compute resources required to train a model capable of complex reasoning.
3.  **🚀 The Base Model & Beyond:** The ultimate goal is to achieve GPT-Class intelligence that runs on Indian infrastructure.
"""

MANIFESTO_TOOLS = """
### 🛠️ THE SAMRION ECOSYSTEM

**1. 🧠 MEDHA (The Brain)**
*Sanskrit Meaning: Intellect / Wisdom*
Medha is the intellectual core of the Samrion Ecosystem. It serves as your personal polymath—a digital entity designed not just to answer questions, but to understand context, reason through complex problems, and provide insightful solutions.
* **Capabilities:** Deep Reasoning, Contextual Memory, Multilingual Fluency.

**2. 🎨 AKRITI (The Imagination)**
*Sanskrit Meaning: Form / Shape*
Akriti is the manifestation of pure imagination. It breaks the barrier between "thought" and "visual." If you can dream it, Akriti can render it. It is not just an image generator; it is a complete creative studio.
* **Capabilities:** Flux-Realism Generation, Photo Remixing, High-Contrast Designer UI.

**3. 🎙️ VANI (The Voice)**
*Sanskrit Meaning: Voice / Speech*
Vani is the voice of the machine. It goes beyond simple text-to-speech by introducing the concept of "Digital Soul." Vani allows users to not only generate speech but to clone, preserve, and transport voices across the digital realm.
* **Capabilities:** .SMRV Voice Files, God Mode Cloning, Phonetic Calibration.

**4. 📦 SANGRAH (The Collector)**
*Sanskrit Meaning: Collection / Archive*
Sangrah is the backbone of machine learning. In the AI age, data is the new oil, and Sangrah is the heavy machinery designed to mine it. It automates the tedious process of dataset collection.
* **Capabilities:** Industrial Scale Mining (50k+ images), Flash-Speed Downloading, Auto-Zipping.

**5. 💻 CODIQ (The Architect)**
*Sanskrit Meaning: Coded Intelligence*
Codiq is the builder. It is the most dangerous and powerful tool in the Samrion arsenal because it has the power to create *other* tools. Codiq is not just a code generator; it is a context-aware software engineer.
* **Capabilities:** Genesis Protocol (Full Projects), Neural Memory, Smart Packaging (.zip).
"""

# =========================================================
# 4. BACKEND INIT (FIREBASE & GROQ)
# =========================================================
ADMIN_PASS = "ilovesamriddhisoni28oct"

# Initialize Firebase
if not firebase_admin._apps:
    try:
        key_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(key_dict)
        db_url = key_dict.get("database_url", f"https://{key_dict['project_id']}-default-rtdb.firebaseio.com/")
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
    except Exception as e:
        st.error(f"🔥 DATABASE ERROR: {e}")
        st.stop()

# Initialize Groq (Site Manager)
def get_groq_client():
    try: return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: return None

# =========================================================
# 5. LOGIC FUNCTIONS
# =========================================================
# Database Ops
def get_user_access(key):
    try: return db.reference(f"users/{key}").get()
    except: return None

def set_user_access(key, tools):
    db.reference(f"users/{key}").set(tools)

def add_upgrade_req(user_key, tool, utr):
    db.reference('upgrades').push({"user": user_key, "tool": tool, "utr": utr, "date": str(datetime.date.today())})

def get_upgrades(): return db.reference('upgrades').get() or {}
def delete_upgrade(k): db.reference(f'upgrades/{k}').delete()

def add_request(email): db.reference('requests').push({"email": email, "date": str(datetime.date.today())})
def get_requests(): return db.reference('requests').get() or {}
def delete_request(k): db.reference(f'requests/{k}').delete()

def gen_key():
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=12))

# Site Manager AI Logic
def read_code():
    with open(__file__, "r", encoding="utf-8") as f: return f.read()

def write_code(new_code):
    with open("app_backup.py", "w", encoding="utf-8") as f: f.write(read_code())
    with open(__file__, "w", encoding="utf-8") as f: f.write(new_code)

def consult_ai(prompt):
    client = get_groq_client()
    if not client: return "ERROR: API Key Missing"
    sys_prompt = f"You are Site Manager AI. Rewrite this Streamlit code based on: '{prompt}'. Return ONLY Python code."
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": read_code()}],
            temperature=0.1
        )
        return res.choices[0].message.content
    except Exception as e: return str(e)

# =========================================================
# 6. STATE & NAVIGATION
# =========================================================
if "page" not in st.session_state: st.session_state.page = "home"
if "role" not in st.session_state: st.session_state.role = None
if "tools" not in st.session_state: st.session_state.tools = []
if "user_pass" not in st.session_state: st.session_state.user_pass = None

def go(p): st.session_state.page = p
def logout():
    st.session_state.role = None
    st.session_state.tools = []
    st.session_state.user_pass = None
    go("home")

TOOLS = {
    "MEDHA": ("🧠", "https://medha-ai.streamlit.app/"),
    "AKRITI": ("🎨", "https://akriti.streamlit.app/"),
    "VANI": ("🎙️", "https://vaani-labs.streamlit.app/"),
    "SANGRAH": ("📦", "https://sangrah.streamlit.app/"),
    "CODIQ": ("💻", "https://codiq-ai.streamlit.app/")
}
ALL_TOOL_NAMES = list(TOOLS.keys())

# =========================================================
# 7. PAGES
# =========================================================

# --- HOME ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <h1 class="gradient" style="font-size: 3.5rem;">SAMRION TECHNOLOGIES</h1>
        <h3>THE FUTURE OF INTELLIGENCE</h3>
        <p style="opacity:0.7;letter-spacing:3px;">BUILT IN INDIA · OPEN SOURCE · INDIGENOUS</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("📖 READ MANIFESTO"): go("about"); st.rerun()
    with c2:
        if st.button("🔐 ENTER BRIDGE"): go("login"); st.rerun()
    with c3:
        if st.button("🤝 CONTRIBUTE"): st.toast("See QR Below")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contribution Section
    c_qr, c_txt = st.columns([1, 2])
    with c_qr:
        try: st.image("qr.png", caption="Scan via UPI", width=250)
        except: st.warning("Upload qr.png")
    with c_txt:
        st.markdown(f"<div class='glass'><h3>🚀 SUPPORT THE MISSION</h3><p class='manifesto-body'>Your contribution funds the GPU compute for Pragyan Mini Model. <br><b>₹50</b> = Lifetime Access to current tools.</p></div>", unsafe_allow_html=True)

# --- MANIFESTO ---
elif st.session_state.page == "about":
    if st.button("← RETURN TO BASE"): go("home"); st.rerun()
    
    t1, t2 = st.tabs(["🇮🇳 PRAGYAN VISION", "🛠️ TOOL ECOSYSTEM"])
    with t1:
        st.markdown(f"<div class='glass'><div class='manifesto-body'>{MANIFESTO_PRAGYAN}</div></div>", unsafe_allow_html=True)
    with t2:
        st.markdown(f"<div class='glass'><div class='manifesto-body'>{MANIFESTO_TOOLS}</div></div>", unsafe_allow_html=True)

# --- LOGIN ---
elif st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c = st.columns([1, 2, 1])[1]
    with c:
        st.markdown("<h2 style='text-align:center'>VERIFY DIGITAL IDENTITY</h2>", unsafe_allow_html=True)
        with st.container(border=True):
            key = st.text_input("ACCESS CODE", type="password")
            if st.button("AUTHORIZE"):
                if key == ADMIN_PASS:
                    st.session_state.role = "admin"
                    go("admin"); st.rerun()
                else:
                    user_tools = get_user_access(key)
                    if user_tools is not None:
                        st.session_state.role = "user"
                        st.session_state.user_pass = key
                        st.session_state.tools = user_tools
                        go("hub"); st.rerun()
                    else:
                        st.error("ACCESS DENIED")
                        st.session_state.show_req = True
            
            if st.session_state.get('show_req'):
                st.markdown("---")
                em = st.text_input("Enter Email for Access Request")
                if st.button("SEND REQUEST"):
                    add_request(em)
                    st.success("Request Sent.")

    if st.button("← BACK"): go("home"); st.rerun()

# --- HUB (USER) ---
elif st.session_state.page == "hub":
    st.markdown("## 💠 SAMRION ARMORY")
    if st.button("LOGOUT"): logout(); st.rerun()
    st.markdown("---")
    
    my_tools = st.session_state.tools
    cols = st.columns(3)
    
    for i, (name, (icon, url)) in enumerate(TOOLS.items()):
        unlocked = name in my_tools
        cls = "glass" if unlocked else "glass locked"
        
        with cols[i % 3]:
            st.markdown(f"""
            <div class="{cls}" style="text-align:center">
                <h1 style="font-size:3rem">{icon}</h1>
                <h3>{name}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if unlocked:
                st.markdown(f"<a href='{url}' target='_blank'><button>LAUNCH</button></a>", unsafe_allow_html=True)
            else:
                with st.expander("🔒 UPGRADE (₹10)"):
                    utr = st.text_input("UTR #", key=f"u_{i}")
                    if st.button("REQUEST UNLOCK", key=f"b_{i}"):
                        add_upgrade_req(st.session_state.user_pass, name, utr)
                        st.success("Sent!")

# --- ADMIN ---
elif st.session_state.page == "admin":
    st.markdown("## 👑 FOUNDER CONSOLE")
    
    tabs = st.tabs(["🔑 KEYS", "📩 REQUESTS", "🤖 SITE MANAGER"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Mint Key")
            sel = st.multiselect("Access Rights", ALL_TOOL_NAMES, default=ALL_TOOL_NAMES)
            if st.button("GENERATE"):
                k = gen_key()
                set_user_access(k, sel)
                st.success(f"KEY: {k}"); st.code(k)
        with c2:
            st.markdown("### Database")
            # --- FIX: USE ST.CODE TO FORCE CONTRAST ---
            user_data = db.reference('users').get()
            st.code(json.dumps(user_data, indent=2), language='json')

    with tabs[1]:
        c_up, c_new = st.columns(2)
        with c_up:
            st.markdown("### Upgrades")
            upgs = get_upgrades()
            for k,v in upgs.items():
                with st.expander(f"{v['tool']} | UTR: {v['utr']}"):
                    if st.button("APPROVE", key=k):
                        curr = get_user_access(v['user']) or []
                        if v['tool'] not in curr: curr.append(v['tool'])
                        set_user_access(v['user'], curr)
                        delete_upgrade(k)
                        st.success("Done!")
                        time.sleep(1); st.rerun()
        with c_new:
            st.markdown("### New Users")
            reqs = get_requests()
            for k,v in reqs.items():
                with st.expander(f"{v['email']}"):
                    grant = st.multiselect("Grant", ALL_TOOL_NAMES, default=ALL_TOOL_NAMES, key=f"g_{k}")
                    if st.button("CREATE KEY", key=k):
                        nk = gen_key()
                        set_user_access(nk, grant)
                        delete_request(k)
                        st.success(f"KEY: {nk}")

    with tabs[2]:
        st.markdown("### 🤖 Self-Editing AI")
        prompt = st.chat_input("Command the Site Manager (e.g., 'Change background color')")
        if prompt:
            with st.spinner("Rewriting Code..."):
                res = consult_ai(prompt)
                if "```python" in res:
                    code = res.split("```python")[1].split("```")[0]
                    if st.button("💾 APPLY UPDATE"):
                        write_code(code)
                        st.rerun()
                    with st.expander("Preview"): st.code(code)
                else: st.error("AI Generation Failed"); st.write(res)

    if st.button("EXIT CONSOLE"): logout(); st.rerun()

else:
    go("home"); st.rerun()
