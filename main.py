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

# --- الواجهة الخاصة بـ Streamlit (التصميم المرعب) ---
st.set_page_config(page_title="GHOST V2 - NON STOP", page_icon="👹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050000; color: #ff0000; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #111; color: #ff3333; border: 1px solid #ff0000;
    }
    h1, h2, h3 { color: #ff0000 !important; text-shadow: 0 0 10px #ff0000; text-align: center; }
    .stButton>button {
        background: linear-gradient(45deg, #440000, #ff0000); color: white;
        border: none; width: 100%; font-weight: bold; height: 50px;
    }
    .status-box { padding: 15px; border: 2px solid #ff0000; background: #000; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👹 GHOST REPORTING SYSTEM - NO LIMIT 👹</h1>", unsafe_allow_html=True)

# دالة الإبلاغ السريع (بدون تغيير حرف واحد من منطقها الأصلي)
def report_video_fast(sessionid, idVd, UserId, report_type, proxy=None, country=None):
    try:
        secret = secrets.token_hex(16)
        cookies = {
            "sessionid": sessionid,
            "passport_csrf_token": secret,
            "passport_csrf_token_default": secret
        }
        if not country:
            country_code = random.choice(["US", "GB", "DE", "FR", "SA", "EG", "YE"])
        else:
            country_code = country
            
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        params = {
            'report_type': "video", 'object_id': str(idVd), 'owner_id': str(UserId),
            'enter_from': "homepage_hot", 'group_id': str(idVd), 'reason': report_type['reason'],
            'category': report_type['category'], 'device_platform': "android", 'aid': "1233",
            'app_name': "musical_ly", 'version_code': "370805", 'current_region': country_code,
            'ts': str(int(time.time())), 'iid': str(random.randint(1, 10**19)),
            'device_id': str(random.randint(1, 10**19)), 'openudid': str(binascii.hexlify(os.urandom(8)).decode()),
        }
        
        # استخدام دالة التوقيع الأصلية
        m = sign(params=urlencode(params), payload="", cookie=urlencode(cookies))
        
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 11)",
            'x-tt-passport-csrf-token': secret, 'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"], 'x-khronos': m["x-khronos"], 'x-ladon': m["x-ladon"],
        }
        
        response = requests.get(
            f"https://api16-normal-c-alisg.ttapis.com/aweme/v2/aweme/feedback/?{urlencode(params)}", 
            headers=headers, cookies=cookies, proxies=proxies, verify=False, timeout=5
        )
        return '"status_code":0' in response.text
    except:
        return False

# دالة التوقيع (كما هي في الكود الأصلي)
def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", sdk_version: int =2, platform: int = 19, unix: int = None):  
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None  
    if not unix: unix = int(time.time())  
    return Gorgon(params, unix, payload, cookie).get_value() | { "x-ladon"   : Ladon.encrypt(unix, license_id, aid),"x-argus"   : Argus.get_sign(params, x_ss_stub, unix,platform        = platform,aid             = aid,license_id      = license_id,sec_device_id   = sec_device_id,sdk_version     = sdk_version_str, sdk_version_int = sdk_version)}  

# دالة جلب المعلومات الأصلية
def get_video_info(link):
    try:
        response = requests.get("https://api16-normal-c-alisg.ttapis.com/tiktok/linker/target/get/v1/", params={'url': link, 'aid': '1233'}, timeout=5)
        Video = response.json()['landing_url']
        Username = Video.split("https://www.tiktok.com/@")[1].split("/video")[0]
        idVd = Video.split("/video/")[1].split("?")[0]
        tikinfo = requests.get(f'https://www.tiktok.com/@{Username}', timeout=5).text
        UserId = tikinfo.split('id":"')[1].split('",')[0]
        return idVd, UserId, Username
    except:
        return None, None, None

# --- إدخالات المستخدم عبر واجهة الويب ---
with st.sidebar:
    st.header("💀 TARGET SETTINGS")
    user_target = st.text_input("يوزر المستخدم")
    report_name = st.selectbox("نوع البلاغ", ["المحتوى الجنسي", "العنف", "الكراهية", "الانتحار", "معلومات خاطئة", "الغش", "التقليد"])
    
    # تحويل الاختيار لبيانات البلاغ الأصلية
    REPORT_TYPES = {
        "المحتوى الجنسي": {"reason": "90087", "category": "porn"},
        "العنف": {"reason": "90044", "category": "violence"},
        "الكراهية": {"reason": "90045", "category": "hate"},
        "الانتحار": {"reason": "90046", "category": "suicide"},
        "معلومات خاطئة": {"reason": "90050", "category": "misinformation"},
        "الغش": {"reason": "90053", "category": "scam"},
        "التقليد": {"reason": "90055", "category": "impersonation"}
    }

col1, col2 = st.columns(2)
with col1:
    sessions_input = st.text_area("🔑 لصق السيزنات (واحد لكل سطر)", height=200)
with col2:
    proxies_input = st.text_area("🌐 لصق البروكسيات (IP:Port)", height=200)

links_input = st.text_area("🔗 لصق روابط الفيديوهات (رابط لكل سطر)", height=150)

if st.button("🔥 START ATTACK - ابدأ الهجوم المستمر"):
    if not sessions_input or not links_input:
        st.error("⚠️ يرجى ملء السيزنات والروابط أولاً!")
    else:
        sessions = [s.strip() for s in sessions_input.split('\n') if s.strip()]
        proxies = [p.strip() for p in proxies_input.split('\n') if p.strip()]
        links = [l.strip() for l in links_input.split('\n') if l.strip()]
        
        st.warning("⚡ الهجوم يعمل الآن في الخلفية بدون توقف...")
        
        results_container = st.empty()
        ok, bad = 0, 0
        
        # حلقة لا نهائية للإرسال بدون توقف
        while True:
            for link in links:
                idVd, UserId, Username = get_video_info(link)
                if idVd:
                    for session in sessions:
                        proxy = random.choice(proxies) if proxies else None
                        success = report_video_fast(session, idVd, UserId, REPORT_TYPES[report_name], proxy)
                        if success:
                            ok += 1
                        else:
                            bad += 1
                        
                        # تحديث الإحصائيات في الواجهة
                        results_container.markdown(f"""
                        <div class='status-box'>
                            <h3 style='color:white'>📊 LIVE ATTACK STATS</h3>
                            <p style='color:#00ff00; font-size:20px'>✅ SUCCESS: {ok}</p>
                            <p style='color:#ff0000; font-size:20px'>❌ FAILED: {bad}</p>
                            <p style='color:#ffff00;'>Target: {Username}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.1) # سرعة فائقة

