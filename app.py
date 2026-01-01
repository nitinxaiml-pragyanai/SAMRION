import streamlit as st
import datetime
import random
import string
import time
import os
import json
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
# 2. PHASE ♾️ ULTRA CINEMATIC CSS (FIXED CONTRAST)
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

/* ADMIN DATABASE CARD (FIXED VISIBILITY) */
.db-card {
    background-color: #0a0a0a !important; /* PURE BLACK */
    border: 1px solid #333;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: #fff !important;
    font-family: monospace;
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
    transform: translateY(-5px);
    border-color: #00d2ff;
}

/* LOCKED STATE */
.locked {
    opacity: 0.5;
    filter: grayscale(1);
    border: 1px dashed rgba(255, 255, 255, 0.2);
}

/* MANIFESTO TEXT */
.manifesto-body {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #e0e0e0;
    text-align: left;
    white-space: pre-line;
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
    color: white !important;
}

/* INPUTS (Fixing White Background) */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #050510 !important;
    color: white !important;
    border: 1px solid #444;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. MANIFESTOS (FULL LENGTH)
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

if not firebase_admin._apps:
    try:
        key_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(key_dict)
        db_url = key_dict.get("database_url", f"https://{key_dict['project_id']}-default-rtdb.firebaseio.com/")
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
    except Exception as e:
        st.error(f"🔥 DATABASE ERROR: {e}")
        st.stop()

def get_groq_client():
    try: return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: return None

# =========================================================
# 5. LOGIC FUNCTIONS (UPDATED FOR NAMES & EDITING)
# =========================================================

# --- NEW USER STRUCTURE: {"name": "Nitin", "tools": ["MEDHA", "AKRITI"]} ---

def get_user_data(key):
    try: 
        data = db.reference(f"users/{key}").get()
        # Backward Compatibility Fix (Handle old list format vs new dict format)
        if isinstance(data, list):
            return {"name": "Unknown", "tools": data}
        return data # Returns dict or None
    except: return None

def set_user_data(key, name, tools):
    db.reference(f"users/{key}").set({"name": name, "tools": tools})

def delete_user(key):
    db.reference(f"users/{key}").delete()

# Donations
def add_donation(email, utr, amount):
    db.reference('donations').push({"email": email, "utr": utr, "amount": amount, "date": str(datetime.date.today())})

def get_donations(): return db.reference('donations').get() or {}

# Requests
def add_request(email): db.reference('requests').push({"email": email, "date": str(datetime.date.today())})
def get_requests(): return db.reference('requests').get() or {}
def delete_request(k): db.reference(f'requests/{k}').delete()

def gen_key():
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=12))

# Site Manager AI
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
if "user_name" not in st.session_state: st.session_state.user_name = "User"

def go(p): st.session_state.page = p
def logout():
    st.session_state.role = None
    st.session_state.tools = []
    st.session_state.user_name = "User"
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
        if st.button("📖 MANIFESTO"): go("about"); st.rerun()
    with c2:
        if st.button("🔐 ENTER BRIDGE"): go("login"); st.rerun()
    with c3:
        if st.button("🤝 CONTRIBUTE"): go("donate"); st.rerun()

# --- MANIFESTO ---
elif st.session_state.page == "about":
    if st.button("← RETURN TO BASE"): go("home"); st.rerun()
    
    t1, t2 = st.tabs(["🇮🇳 PRAGYAN VISION", "🛠️ TOOL ECOSYSTEM"])
    with t1:
        st.markdown(f"<div class='glass'><div class='manifesto-body'>{MANIFESTO_PRAGYAN}</div></div>", unsafe_allow_html=True)
    with t2:
        st.markdown(f"<div class='glass'><div class='manifesto-body'>{MANIFESTO_TOOLS}</div></div>", unsafe_allow_html=True)

# --- CONTRIBUTION PAGE ---
elif st.session_state.page == "donate":
    if st.button("← RETURN TO BASE"): go("home"); st.rerun()
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""
        <div class="glass">
            <h2 class="gradient">SUPPORT THE REVOLUTION</h2>
            <p>Your contribution directly funds the GPU compute needed for Pragyan.</p>
            <ul>
                <li><b>₹50</b>: Lifetime Access (Early Adopter)</li>
                <li><b>₹500</b>: Founding Member Status</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        try: st.image("qr.png", caption="Scan via UPI", width=300)
        except: st.warning("Upload qr.png")
        
    with c2:
        st.markdown("<div class='glass'><h3>LOG YOUR CONTRIBUTION</h3>", unsafe_allow_html=True)
        d_email = st.text_input("Your Email Address")
        d_utr = st.text_input("UPI Reference ID (UTR)")
        d_amt = st.number_input("Amount (₹)", min_value=10, value=50)
        
        if st.button("✅ CONFIRM DONATION"):
            if d_email and d_utr:
                add_donation(d_email, d_utr, d_amt)
                st.balloons()
                st.success("THANK YOU! Details Received.")
            else:
                st.error("Please fill all details.")
        st.markdown("</div>", unsafe_allow_html=True)

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
                    u_data = get_user_data(key)
                    if u_data:
                        st.session_state.role = "user"
                        st.session_state.user_name = u_data.get('name', 'User')
                        st.session_state.tools = u_data.get('tools', [])
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
    st.markdown(f"## 💠 WELCOME, {st.session_state.user_name}")
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
                st.button(f"🔒 LOCKED", key=f"lk_{i}", disabled=True)

# --- ADMIN (UPDATED WITH NAMES & EDITING) ---
elif st.session_state.page == "admin":
    st.markdown("## 👑 FOUNDER CONSOLE")
    
    tabs = st.tabs(["🔑 KEY MANAGEMENT", "📩 REQUESTS", "💰 DONATIONS", "🤖 AI"])
    
    # 1. KEY MANAGEMENT (Fixes White Text & Adds Editing)
    with tabs[0]:
        c1, c2 = st.columns([1, 1.5])
        
        # MINT KEY
        with c1:
            st.markdown("### ✨ Mint New Key")
            new_name = st.text_input("User Name / Alias", placeholder="e.g. Nitin")
            sel_tools = st.multiselect("Access Rights", ALL_TOOL_NAMES, default=ALL_TOOL_NAMES)
            
            if st.button("GENERATE KEY"):
                if new_name:
                    k = gen_key()
                    set_user_data(k, new_name, sel_tools)
                    st.success(f"Generated for {new_name}: {k}")
                    st.code(k)
                    time.sleep(2); st.rerun()
                else:
                    st.error("Enter a Name.")

        # EDIT / DELETE USERS
        with c2:
            st.markdown("### 📋 Database (Edit/Delete)")
            all_users = db.reference('users').get()
            
            if all_users:
                # Select User to Edit
                user_keys = list(all_users.keys())
                user_labels = [f"{all_users[k].get('name', 'Unknown')} ({k})" if isinstance(all_users[k], dict) else f"Unknown ({k})" for k in user_keys]
                
                selected_idx = st.selectbox("Select User to Edit", range(len(user_keys)), format_func=lambda x: user_labels[x])
                target_key = user_keys[selected_idx]
                target_data = all_users[target_key]
                
                # Handling old vs new data format
                current_name = target_data.get('name', 'Unknown') if isinstance(target_data, dict) else "Unknown"
                current_tools = target_data.get('tools', target_data) if isinstance(target_data, dict) else target_data
                if not isinstance(current_tools, list): current_tools = []
                
                # Edit Form
                with st.container(border=True):
                    st.markdown(f"**Editing: {target_key}**")
                    edit_name = st.text_input("Name", value=current_name, key="ed_nm")
                    edit_tools = st.multiselect("Tools", ALL_TOOL_NAMES, default=[t for t in current_tools if t in ALL_TOOL_NAMES], key="ed_tls")
                    
                    c_save, c_del = st.columns(2)
                    with c_save:
                        if st.button("💾 SAVE CHANGES"):
                            set_user_data(target_key, edit_name, edit_tools)
                            st.success("Updated!")
                            time.sleep(1); st.rerun()
                    with c_del:
                        if st.button("❌ DELETE USER", type="primary"):
                            delete_user(target_key)
                            st.warning("User Deleted.")
                            time.sleep(1); st.rerun()
            else:
                st.info("No Users Found.")

    # 2. REQUESTS
    with tabs[1]:
        st.markdown("### 📩 Access Requests")
        reqs = get_requests()
        for k,v in reqs.items():
            with st.expander(f"Request: {v['email']}"):
                grant = st.multiselect("Grant", ALL_TOOL_NAMES, default=ALL_TOOL_NAMES, key=f"g_{k}")
                req_name = st.text_input("Assign Name", value=v['email'].split('@')[0], key=f"rn_{k}")
                if st.button("✅ Create Key", key=k):
                    nk = gen_key()
                    set_user_data(nk, req_name, grant)
                    delete_request(k)
                    st.success(f"Key Sent: {nk}")

    # 3. DONATIONS
    with tabs[2]:
        st.markdown("### 💰 Donation Logs")
        donations = get_donations()
        if donations:
            for k,v in donations.items():
                # Using HTML for high visibility (Black background)
                st.markdown(f"""
                <div class="db-card">
                    <span style="color:#00d2ff">EMAIL:</span> {v['email']}<br>
                    <span style="color:#ff007f">AMOUNT:</span> ₹{v['amount']}<br>
                    <span>UTR:</span> {v['utr']} | <span>DATE:</span> {v['date']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No donations yet.")

    # 4. AI
    with tabs[3]:
        st.markdown("### 🤖 Self-Editing AI")
        prompt = st.chat_input("Command the Site Manager")
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
