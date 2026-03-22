import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# -----------------------
# 🔥 إخفاء الترس نهائيًا
# -----------------------
st.markdown("""
<style>

/* إخفاء الترس والقائمة */
[data-testid="stToolbar"] {
    display: none !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* خلفية حسب الثيم */
.stApp {
    background-color: var(--background-color);
}

/* النص */
h1, h2, h3, p, span {
    color: var(--text-color) !important;
}

/* كروت المنتجات */
.product-card {
    padding: 15px;
    border-radius: 12px;
    background-color: var(--secondary-background-color);
    margin-bottom: 15px;
    border: 1px solid rgba(128,128,128,0.2);
}

/* زر واتساب */
.whatsapp-btn {
    background-color: #25D366;
    color: white !important;
    padding: 8px 12px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-block;
    font-weight: bold;
}

/* روابط */
.social-link {
    display: inline-block;
    margin-top: 5px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# الهيدر
# -----------------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image("logo.png", use_container_width=True)

st.markdown("""
<h1>🛒 TechZone</h1>
<p>عالم التقنية - أفضل الأجهزة 🔥</p>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# الحالة
# -----------------------
if "role" not in st.session_state:
    st.session_state.role = "guest"

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "settings" not in st.session_state:
    st.session_state.settings = {
        "whatsapp": "0515906039",
        "facebook": "https://www.facebook.com/",
        "instagram": "https://instagram.com/"
    }

# -----------------------
# البيانات
# -----------------------
FILE_NAME = "warehouse.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)

        if "رقم" not in df.columns:
            df.insert(0, "رقم", range(1, len(df) + 1))

        if "السعر" not in df.columns:
            df["السعر"] = 0

        return df
    else:
        return pd.DataFrame(columns=["رقم", "القطعة", "الموديل", "الكمية", "الحالة", "السعر", "الصورة"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# -----------------------
# زر دخول مخفي (بدون ما يشوفه الزبون)
# -----------------------
col1, col2 = st.columns([9,1])
with col2:
    if st.button("⋮"):  # ثلاث نقاط بدل الترس
        st.session_state.show_login = True

# -----------------------
# تسجيل الدخول
# -----------------------
if st.session_state.show_login:

    st.subheader("🔐 دخول المدير")
    password = st.text_input("كلمة السر", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("دخول"):
            if password == "7G4E976D":
                st.session_state.role = "admin"
                st.session_state.show_login = False
                st.rerun()
            else:
                st.error("كلمة السر غلط ❌")

    with col2:
        if st.button("إلغاء"):
            st.session_state.show_login = False
            st.rerun()

    st.stop()

# =========================
# 👨‍💼 المدير
# =========================
if st.session_state.role == "admin":

    st.title("📦 لوحة التحكم")

    if st.button("تسجيل الخروج"):
        st.session_state.role = "guest"
        st.rerun()

    st.sidebar.header("📱 إعدادات التواصل")

    st.session_state.settings["whatsapp"] = st.sidebar.text_input("واتساب", st.session_state.settings["whatsapp"])
    st.session_state.settings["facebook"] = st.sidebar.text_input("فيسبوك", st.session_state.settings["facebook"])
    st.session_state.settings["instagram"] = st.sidebar.text_input("إنستغرام", st.session_state.settings["instagram"])

# =========================
# 👤 الزبون
# =========================
else:

    st.title("🛒 المنتجات")

    search = st.text_input("🔍 ابحث")

    for _, row in df.iterrows():

        if not search or search.lower() in str(row["القطعة"]).lower():

            st.markdown(f"""
            <div class="product-card">
                <h3>📦 {row['القطعة']}</h3>
                <p>💰 {row['السعر']} ₪</p>
            """, unsafe_allow_html=True)

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=200)

            whatsapp = st.session_state.settings["whatsapp"]

            msg = urllib.parse.quote("مرحبا بدي أطلب " + str(row["القطعة"]))
            link = f"https://wa.me/{whatsapp}?text={msg}"

            st.markdown(f"""
            <div style="margin-top:10px;">
                <a class="whatsapp-btn" href="{link}">📞 واتساب</a><br><br>
                <a class="social-link" href="{st.session_state.settings['facebook']}" target="_blank">📘 فيسبوك</a><br>
                <a class="social-link" href="{st.session_state.settings['instagram']}" target="_blank">📷 إنستغرام</a>
            </div>
            </div>
            """, unsafe_allow_html=True)
            
