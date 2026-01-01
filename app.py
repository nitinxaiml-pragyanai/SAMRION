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
    page_title="SAMRION ",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. THE NUCLEAR CSS PATCH (FORCED VISIBILITY)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

/* FORCE DARK THEME & RESET */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 50% 10%, #0f172a 0%, #000000 100%);
    color: white;
}

* { font-family: 'Inter', sans-serif !important; }

/* HEADERS */
h1, h2, h3 { 
    font-family: 'Outfit', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: 2px;
    color: white !important;
}

/* INPUT FIELDS - FORCE PITCH BLACK BACKGROUND WITH WHITE TEXT */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    font-size: 16px !important;
}
.stTextInput input:focus {
    border-color: #00d2ff !important;
    box-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
}
/* Label Color */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #00d2ff !important;
    font-size: 14px !important;
    font-weight: bold !important;
}

/* CUSTOM NEON BUTTONS (REPLACING STREAMLIT BUTTONS) */
.custom-btn {
    display: block;
    width: 100%;
    padding: 18px;
    background: linear-gradient(90deg, #00d2ff, #0055ff);
    color: white !important;
    text-align: center;
    text-decoration: none;
    font-weight: 800;
    font-size: 18px;
    border-radius: 50px;
    margin-top: 10px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
    border: 2px solid rgba(255,255,255,0.1);
    transition: transform 0.2s;
    cursor: pointer;
}
.custom-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px rgba(0, 210, 255, 0.8);
    color: white !important;
    text-decoration: none;
}

/* RED DANGER BUTTON */
.danger-btn {
    background: linear-gradient(90deg, #ff007f, #990033);
    box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4);
}

/* MANIFESTO TYPOGRAPHY - HUGE & CLEAR */
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
    font-size: 20px; /* BIG TEXT */
    line-height: 1.8;
    color: #e0e0e0;
    margin-bottom: 20px;
}

/* GLASS CARD */
.glass {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
}

/* ADMIN LIST ITEM */
.admin-item {
    background: #050505;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border-left: 5px solid #00d2ff;
    border-top: 1px solid #222;
}

/* STREAMLIT BUTTON OVERRIDE (For Form Submit Buttons) */
div.stButton > button {
    background: #111;
    color: white;
    border: 1px solid #00d2ff;
    border-radius: 30px;
    padding: 10px 25px;
}
div.stButton > button:hover {
    background: #00d2ff;
    color: black;
}

/* HIDE JUNK */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. THE GRAND MANIFESTO (FULL TEXT)
# =========================================================
def render_manifesto_pragyan():
    st.markdown("""
    <div class="manifesto-box">
        <div class="manifesto-title">🇮🇳 PRAGYAN: THE AWAKENING</div>
        <div class="manifesto-text">
            <b>The Mission</b><br>
            Pragyan (meaning "Wisdom" or "Supreme Intelligence" in Sanskrit) is not just another AI model; it is a movement towards digital sovereignty. In a world dominated by foreign AI giants like OpenAI and Google, India—the world's largest data consumer—risks becoming a digital colony. We rely on foreign servers, foreign policies, and foreign algorithms.
        </div>
        <div class="manifesto-text">
            Pragyan exists to change that. It is India’s first community-driven, open-source AI project designed to build indigenous intelligence from the ground up.
        </div>
        <div class="manifesto-text">
            <b>The Origin Story</b><br>
            Founded by <b>Nitin Raj</b> under the banner of <b>Samrion Technologies</b>, Pragyan was born from a simple yet powerful realization: <i>We cannot build our future on rented land.</i> Without big corporate sponsors or billion-dollar funding, Pragyan is being built line-by-line, tensor-by-tensor, by an independent developer and a community of believers.
        </div>
        <div class="manifesto-text">
            <b>Why Pragyan Matters?</b><br>
            • <b>Data Sovereignty:</b> Your data should not leave Indian shores. Pragyan aims to keep Indian data within India.<br>
            • <b>Linguistic Inclusion:</b> While Western models focus on English, Pragyan is being trained to understand the nuance of India's diverse languages.<br>
            • <b>True Open Source:</b> Unlike "Open" AI companies that keep their weights closed, Pragyan believes in total transparency. Every line of code, every dataset, and every model weight is shared with the people.
        </div>
        <div class="manifesto-text">
            <b>The Roadmap to Ultra</b><br>
            1. ✅ <b>The Nano Model (1–10M Parameters):</b> The foundation has been laid. The proof of concept is operational.<br>
            2. 🔄 <b>The Mini Model (Current Goal):</b> We are currently gathering the GPU compute resources required to train a model capable of complex reasoning.<br>
            3. 🚀 <b>The Base Model & Beyond:</b> The ultimate goal is to achieve GPT-Class intelligence that runs on Indian infrastructure.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_manifesto_tools():
    st.markdown("""
    <div class="manifesto-box" style="border-left-color: #ff007f;">
        <div class="manifesto-title">🛠️ THE SAMRION ARMORY</div>
        <div class="manifesto-text">
            <b>1. 🧠 MEDHA (The Brain)</b><br>
            Medha is the intellectual core of the Samrion Ecosystem. It serves as your personal polymath—a digital entity designed not just to answer questions, but to understand context, reason through complex problems, and provide insightful solutions.
        </div>
        <div class="manifesto-text">
            <b>2. 🎨 AKRITI (The Imagination)</b><br>
            Akriti is the manifestation of pure imagination. It breaks the barrier between "thought" and "visual." If you can dream it, Akriti can render it. It is not just an image generator; it is a complete creative studio.
        </div>
        <div class="manifesto-text">
            <b>3. 🎙️ VANI (The Voice)</b><br>
            Vani is the voice of the machine. It goes beyond simple text-to-speech by introducing the concept of "Digital Soul." Vani allows users to not only generate speech but to clone, preserve, and transport voices across the digital realm.
        </div>
        <div class="manifesto-text">
            <b>4. 📦 SANGRAH (The Collector)</b><br>
            Sangrah is the backbone of machine learning. In the AI age, data is the new oil, and Sangrah is the heavy machinery designed to mine it. It automates the tedious process of dataset collection.
        </div>
        <div class="manifesto-text">
            <b>5. 💻 CODIQ (The Architect)</b><br>
            Codiq is the builder. It is the most dangerous and powerful tool in the Samrion arsenal because it has the power to create *other* tools. Codiq is not just a code generator; it is a context-aware software engineer.
        </div>
    </div>
    """, unsafe_allow_html=True)

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

# --- DATABASE OPS (UPDATED FOR EDITING/NAMING) ---
def get_user_data(k): 
    try: return db.reference(f"users/{k}").get() 
    except: return None

def create_user(key, name, tools): 
    # Store as Object: { 'name': 'Nitin', 'tools': ['MEDHA', 'VANI'] }
    db.reference(f"users/{key}").set({'name': name, 'tools': tools})

def update_user_tools(key, tools):
    db.reference(f"users/{key}/tools").set(tools)

def delete_user(k): db.reference(f"users/{k}").delete()

def get_all_users(): return db.reference("users").get()

def add_req(em): db.reference('requests').push({"email": em, "date": str(datetime.date.today())})
def get_reqs(): return db.reference('requests').get() or {}
def del_req(k): db.reference(f'requests/{k}').delete()

def add_upgrade(u, t, utr): db.reference('upgrades').push({"user": u, "tool": t, "utr": utr})
def get_upgrades(): return db.reference('upgrades').get() or {}
def del_upgrade(k): db.reference(f'upgrades/{k}').delete()

def add_donation(e, u, a): db.reference('donations').push({"email": e, "utr": u, "amt": a, "date": str(datetime.date.today())})
def get_donations(): return db.reference('donations').get() or {}

def gen_key(): return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

# =========================================================
# 5. STATE & NAV
# =========================================================
if "page" not in st.session_state: st.session_state.page = "home"
if "role" not in st.session_state: st.session_state.role = None
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "user_key" not in st.session_state: st.session_state.user_key = None

def go(p): st.session_state.page = p
def logout():
    st.session_state.role = None
    st.session_state.user_data = {}
    st.session_state.user_key = None
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
    st.markdown("""
    <div style="text-align:center; padding: 80px 20px;">
        <h1 style="font-size: 4.5rem; text-shadow: 0 0 20px #00d2ff; margin-bottom: 10px;">SAMRION TECHNOLOGIES</h1>
        <h3 style="letter-spacing: 5px; color: #aaa;">THE FUTURE OF INTELLIGENCE</h3>
        <p style="opacity:0.9; margin-top: 30px; font-size: 1.2rem;">BUILT IN INDIA · OPEN SOURCE · INDIGENOUS</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1,1])
    with c1: 
        if st.button("📖 READ MANIFESTO", use_container_width=True): go("about"); st.rerun()
    with c2: 
        if st.button("🔐 ENTER BRIDGE", use_container_width=True): go("login"); st.rerun()
    with c3: 
        if st.button("🤝 CONTRIBUTE", use_container_width=True): go("donate"); st.rerun()

# --- MANIFESTO ---
elif st.session_state.page == "about":
    if st.button("← RETURN TO BASE"): go("home"); st.rerun()
    t1, t2 = st.tabs(["PRAGYAN VISION", "TOOL ECOSYSTEM"])
    with t1: render_manifesto_pragyan()
    with t2: render_manifesto_tools()

# --- DONATE ---
elif st.session_state.page == "donate":
    if st.button("← RETURN"): go("home"); st.rerun()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass'><h3>🚀 Support The Mission</h3><p style='font-size:18px'>Funds go directly to GPU compute.<br><b>Fund India's Future</b></p></div>", unsafe_allow_html=True)
        try: st.image("qr.png", width=350)
        except: st.warning("Please upload qr.png")
    with c2:
        st.markdown("<div class='glass'><h3>LOG CONTRIBUTION</h3>", unsafe_allow_html=True)
        email = st.text_input("Your Email Address")
        utr = st.text_input("UTR / Transaction ID")
        amt = st.number_input("Amount (₹)", min_value=10, value=50)
        if st.button("✅ SUBMIT DETAILS"):
            if email and utr:
                add_donation(email, utr, amt)
                st.success("Details Recorded! Check your email soon.")
            else:
                st.error("Please fill all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIN ---
elif st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c = st.columns([1,2,1])[1]
    with c:
        st.markdown("<div class='glass'><h2 style='text-align:center'>IDENTITY VERIFICATION</h2>", unsafe_allow_html=True)
        key = st.text_input("ENTER ACCESS CODE", type="password")
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            if key == ADMIN_PASS:
                st.session_state.role = "admin"
                go("admin"); st.rerun()
            else:
                u_data = get_user_data(key)
                if u_data:
                    # Handle both old list format and new dict format
                    if isinstance(u_data, list): 
                        u_tools = u_data
                        u_name = "Unknown"
                    else:
                        u_tools = u_data.get('tools', [])
                        u_name = u_data.get('name', 'Unknown')
                        
                    st.session_state.role = "user"
                    st.session_state.user_key = key
                    st.session_state.user_data = {'name': u_name, 'tools': u_tools}
                    go("hub"); st.rerun()
                else:
                    st.error("INVALID KEY")
                    st.session_state.show_req = True
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.session_state.get('show_req'):
            em = st.text_input("Enter Email to Request Key")
            if st.button("SEND REQUEST"):
                add_req(em)
                st.success("Request Sent")
    
    if st.button("← BACK"): go("home"); st.rerun()

# --- HUB (FIXED LAUNCH BUTTONS) ---
elif st.session_state.page == "hub":
    st.markdown("## 💠 SAMRION ARMORY")
    st.caption(f"WELCOME, {st.session_state.user_data.get('name', 'USER').upper()}")
    if st.button("LOGOUT"): logout(); st.rerun()
    st.markdown("---")
    
    my_tools = st.session_state.user_data.get('tools', [])
    cols = st.columns(3)
    
    for i, (name, (icon, url)) in enumerate(TOOLS.items()):
        unlocked = name in my_tools
        cls = "glass" if unlocked else "glass locked"
        
        with cols[i % 3]:
            # Clean Card
            st.markdown(f"""
            <div class="{cls}" style="text-align:center">
                <div style="font-size:4rem; margin-bottom:10px;">{icon}</div>
                <h3 style="color:white;">{name}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # THE FIX: NATIVE HTML BUTTON (Blue/Pink Gradient)
            if unlocked:
                st.markdown(f"""
                    <a href="{url}" target="_blank" class="custom-btn">🚀 LAUNCH {name}</a>
                """, unsafe_allow_html=True)
            else:
                with st.expander("🔒 UNLOCK (₹10)"):
                    utr = st.text_input("UTR", key=f"u{i}")
                    if st.button("REQ UNLOCK", key=f"b{i}"):
                        add_upgrade(st.session_state.user_key, name, utr)
                        st.success("Sent")

# --- ADMIN (FIXED EDIT/DELETE/NAME) ---
elif st.session_state.page == "admin":
    st.title("👑 FOUNDER CONSOLE")
    if st.button("EXIT"): logout(); st.rerun()
    
    t1, t2, t3 = st.tabs(["USERS & KEYS", "REQUESTS", "FINANCE"])
    
    with t1:
        # MINT NEW KEY
        st.markdown("### ✨ Mint New Key")
        c_gen1, c_gen2 = st.columns(2)
        with c_gen1:
            new_name = st.text_input("User Name / Alias", placeholder="e.g. Nitin Raj")
        with c_gen2:
            new_tools = st.multiselect("Grant Access", ALL_TOOLS, default=ALL_TOOLS)
            
        if st.button("GENERATE KEY"):
            if new_name:
                k = gen_key()
                create_user(key=k, name=new_name, tools=new_tools)
                st.success(f"CREATED: {k} for {new_name}"); st.code(k)
            else:
                st.error("Enter a name.")
        
        st.markdown("---")
        st.markdown("### 👥 Active Database")
        
        users = get_all_users()
        if users:
            for k, v in users.items():
                # Handle old data format vs new
                if isinstance(v, list):
                    u_name = "Unknown"
                    u_tools = v
                else:
                    u_name = v.get('name', 'Unknown')
                    u_tools = v.get('tools', [])

                # ROW FOR EACH USER
                st.markdown(f"""
                <div class="admin-item">
                    <div>
                        <span style="color:#00d2ff; font-size:18px; font-weight:bold;">{u_name}</span> 
                        <span style="color:#666; margin-left:10px;">({k})</span><br>
                        <small style="color:#ccc;">ACCESS: {', '.join(u_tools)}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_edit, c_del = st.columns([4, 1])
                with c_edit:
                    # EDIT TOOLS LOGIC
                    with st.expander(f"✏️ EDIT TOOLS ({u_name})"):
                        updated_tools = st.multiselect("Modify Access", ALL_TOOLS, default=u_tools, key=f"edit_{k}")
                        if st.button("UPDATE ACCESS", key=f"save_{k}"):
                            update_user_tools(k, updated_tools)
                            st.success("Updated!")
                            time.sleep(1); st.rerun()
                with c_del:
                    # DELETE LOGIC
                    if st.button("🗑️ DELETE", key=f"del_{k}"):
                        delete_user(k)
                        st.error(f"Deleted {u_name}")
                        time.sleep(1); st.rerun()
        else:
            st.info("No users found.")

    with t2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### New Access Requests")
            reqs = get_reqs()
            for k, v in reqs.items():
                with st.expander(v['email']):
                    grant_name = st.text_input("Name", value="New User", key=f"nm{k}")
                    sel = st.multiselect("Grant", ALL_TOOLS, default=ALL_TOOLS, key=f"g{k}")
                    if st.button("CREATE", key=f"c{k}"):
                        nk = gen_key()
                        create_user(nk, grant_name, sel)
                        del_req(k)
                        st.success(f"Key: {nk}")
        with c2:
            st.markdown("#### Upgrade Requests")
            upgs = get_upgrades()
            for k, v in upgs.items():
                with st.expander(f"{v['tool']} | UTR: {v['utr']}"):
                    if st.button("APPROVE", key=f"a{k}"):
                        # Fetch current data
                        curr_data = get_user_data(v['user'])
                        if curr_data:
                            # Handle structure
                            if isinstance(curr_data, list): tools = curr_data
                            else: tools = curr_data.get('tools', [])
                            
                            if v['tool'] not in tools: tools.append(v['tool'])
                            
                            # Save back
                            update_user_tools(v['user'], tools)
                            del_upgrade(k)
                            st.success("Upgraded!")
                            time.sleep(1); st.rerun()

    with t3:
        st.markdown("#### 💰 Donation Logs")
        dons = get_donations()
        if dons:
            for k, v in dons.items():
                st.code(f"DATE: {v.get('date')} | Email: {v.get('email')} | UTR: {v.get('utr')} | ₹{v.get('amt')}")
        else: st.info("No donations yet")

else:
    go("home"); st.rerun()
