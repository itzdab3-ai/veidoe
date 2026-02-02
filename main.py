import streamlit as st
import requests
import binascii
import uuid
import time
import random
import os
import secrets
import urllib3
import threading
from urllib.parse import urlencode
from MedoSigner import Argus, Gorgon, md5, Ladon

# إعدادات الصفحة والواجهة المرعبة
st.set_page_config(page_title="Ghost Reporter Pro", page_icon="💀", layout="centered")

# CSS مخصص للواجهة المرعبة (ألوان سوداء، حمراء، وتأثيرات بصرية)
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #ff0000;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: #ff3333;
        border: 1px solid #ff0000;
    }
    h1, h2, h3 {
        color: #ff0000 !important;
        text-shadow: 2px 2px 5px #550000;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #660000;
        color: white;
        border-radius: 10px;
        border: 2px solid #ff0000;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        color: black;
    }
    .report-card {
        padding: 20px;
        border: 1px solid #ff0000;
        border-radius: 10px;
        background-color: #0d0d0d;
    }
    </style>
    """, unsafe_allow_html=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# بيانات الدول وأنواع البلاغات (نفس الكود الأصلي)
COUNTRIES = {"US": "United States", "GB": "United Kingdom", "DE": "Germany", "FR": "France", "CA": "Canada", "SA": "Saudi Arabia", "EG": "Egypt", "YE": "Yemen"}
REPORT_TYPES = {
    "المحتوى الجنسي": {"reason": "90087", "category": "porn"},
    "العنف والإجرام": {"reason": "90044", "category": "violence"},
    "الكراهية والتحرش": {"reason": "90045", "category": "hate"},
    "الانتحار": {"reason": "90046", "category": "suicide"},
    "معلومات خاطئة": {"reason": "90050", "category": "misinformation"},
    "الغش والاحتيال": {"reason": "90053", "category": "scam"},
    "التقليد": {"reason": "90055", "category": "impersonation"}
}

# --- الدوال البرمجية (تم الحفاظ عليها بالكامل) ---

def sign(params, payload=None, sec_device_id="", cookie=None, aid=1233, license_id=1611921764, sdk_version_str="2.3.1.i18n", sdk_version=2, platform=19, unix=None):  
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None  
    if not unix: unix = int(time.time())  
    return Gorgon(params, unix, payload, cookie).get_value() | { 
        "x-ladon": Ladon.encrypt(unix, license_id, aid),
        "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid, license_id=license_id, sec_device_id=sec_device_id, sdk_version=sdk_version_str, sdk_version_int=sdk_version)
    }

def get_video_info(link):
    try:
        response = requests.get(
            "https://api16-normal-c-alisg.ttapis.com/tiktok/linker/target/get/v1/",
            params={'url': link, 'aid': '1233', 'app_name': 'musical_ly', 'device_platform': 'android'},
            headers={'x-argus': 'ahmed mahoz'}, timeout=5
        )
        video_url = response.json()['landing_url']
        username = video_url.split("@")[1].split("/")[0]
        video_id = video_url.split("/video/")[1].split("?")[0]
        
        # جلب ID المستخدم
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', timeout=5).text
        user_id = tikinfo.split('id":"')[1].split('",')[0]
        return video_id, user_id, username
    except:
        return None, None, None

def report_video_fast(sessionid, idVd, UserId, report_reason, report_category, proxy=None):
    try:
        secret = secrets.token_hex(16)
        cookies = {"sessionid": sessionid, "passport_csrf_token": secret}
        country = random.choice(list(COUNTRIES.keys()))
        params = {
            'report_type': "video", 'object_id': str(idVd), 'owner_id': str(UserId),
            'reason': report_reason, 'category': report_category, 'aid': "1233",
            'device_id': str(random.randint(1, 10**19)), 'iid': str(random.randint(1, 10**19)),
            'current_region': country, 'app_language': "ar"
        }
        m = sign(params=urlencode(params), payload="", cookie=urlencode(cookies))
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 11)",
            'x-tt-passport-csrf-token': secret, 'x-argus': m["x-argus"], 'x-gorgon': m["x-gorgon"]
        }
        proxies = {"http": proxy, "https": proxy} if proxy else None
        res = requests.get(f"https://api16-normal-c-alisg.ttapis.com/aweme/v2/aweme/feedback/?{urlencode(params)}", 
                           headers=headers, cookies=cookies, proxies=proxies, verify=False, timeout=5)
        return '"status_code":0' in res.text
    except:
        return False

# --- واجهة المستخدم (Streamlit UI) ---

st.markdown("<h1 style='text-align: center;'>💀 GHOST REPORTER SYSTEM 💀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Don't look back... The shadows are watching.</p>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        target_user = st.text_input("👤 يوزر المستخدم المستهدف", placeholder="@username")
    with col2:
        report_choice = st.selectbox("🚫 نوع البلاغ المرعب", list(REPORT_TYPES.keys()))

    video_link = st.text_input("🔗 رابط الفيديو", placeholder="https://www.tiktok.com/...")
    
    sessions_input = st.text_area("🔑 لصق السيزنات (سيزن في كل سطر)", height=150)
    proxies_input = st.text_area("🌐 لصق البروكسيات (IP:Port)", height=100)
    
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("🚀 إطلاق الهجوم السريع"):
    if not video_link or not sessions_input:
        st.error("❌ يجب إدخال الرابط والسيزنات أولاً!")
    else:
        sessions = [s.strip() for s in sessions_input.split('\n') if s.strip()]
        proxies = [p.strip() for p in proxies_input.split('\n') if p.strip()]
        
        st.info("🔍 جلب معلومات الهدف من الأعماق...")
        idVd, UserId, Username = get_video_info(video_link)
        
        if idVd:
            st.success(f"💀 تم تحديد الهدف: {Username} | ID: {UserId}")
            
            # عدادات النتائج
            ok = 0
            bad = 0
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # تنفيذ البلاغات
            reason = REPORT_TYPES[report_choice]['reason']
            category = REPORT_TYPES[report_choice]['category']
            
            for i, session in enumerate(sessions):
                current_proxy = random.choice(proxies) if proxies else None
                success = report_video_fast(session, idVd, UserId, reason, category, current_proxy)
                
                if success:
                    ok += 1
                    st.write(f"✅ تم الإرسال من سيزن {i+1}")
                else:
                    bad += 1
                    st.write(f"❌ فشل السيزن {i+1}")
                
                # تحديث الواجهة
                progress = (i + 1) / len(sessions)
                progress_bar.progress(progress)
                status_text.markdown(f"**الناجح: {ok} | الفاشل: {bad}**")
                time.sleep(0.2)
                
            st.markdown("---")
            st.balloons()
            st.markdown(f"### 🏁 اكتملت العملية! الناجح: {ok}")
        else:
            st.error("💀 فشل جلب معلومات الفيديو، تأكد من الرابط.")

# تذييل الصفحة
st.markdown("<br><hr><p style='text-align: center; font-size: 10px;'>Dark AI System © 2026</p>", unsafe_allow_html=True)
