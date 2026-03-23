import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# -----------------------
# 🔥 CSS + إخفاء الترس + تزيين اللوجو
# -----------------------
st.markdown("""
<style>
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {background-color: var(--background-color);}

h1, h2, h3, p, span {
    color: var(--text-color) !important;
}

.product-card {
    padding: 15px;
    border-radius: 12px;
    background-color: var(--secondary-background-color);
    margin-bottom: 15px;
    border: 1px solid rgba(128,128,128,0.2);
}

.whatsapp-btn {
    background-color: #25D366;
    color: white !important;
    padding: 8px 12px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-block;
    font-weight: bold;
}

.social-link {
    display: inline-block;
    margin-top: 5px;
}

/* 🌙✨ تزيين اللوجو */
.header-decor {
    position: relative;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
}

.logo-img {
    width: 100%;
    max-height: 230px;
    object-fit: contain;
    margin-top: 25px;
}

.moon {
    position: absolute;
    top: -5px;
    right: 25px;
    font-size: 34px;
    opacity: 0.85;
}

.top-stars {
    position: absolute;
    top: -10px;
    left: 20px;
    font-size: 20px;
    opacity: 0.7;
}

.bottom-stars {
    position: absolute;
    bottom: -5px;
    right: 30px;
    font-size: 18px;
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# الهيدر (مع الزينة)
# -----------------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

st.markdown("""
<div class="header-decor">
    <div class="moon">🌙</div>
    <div class="top-stars">✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧</div>

    <img src="logo.png" class="logo-img">

    <div class="bottom-stars">✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦</div>
</div>
""", unsafe_allow_html=True)

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

if "cart" not in st.session_state:
    st.session_state.cart = []

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
    return pd.DataFrame(columns=["رقم", "القطعة", "الموديل", "الكمية", "الحالة", "السعر", "الصورة"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# -----------------------
# زر دخول
# -----------------------
col1, col2 = st.columns([9,1])
with col2:
    if st.button("⋮"):
        st.session_state.show_login = True

# -----------------------
# تسجيل الدخول
# -----------------------
if st.session_state.show_login:

    st.subheader("🔐 دخول المدير")

    def login():
        if st.session_state.password == "7B4E976D":
            st.session_state.role = "admin"
            st.session_state.show_login = False
        else:
            st.error("كلمة السر غلط ❌")

    password = st.text_input("كلمة السر", type="password", key="password", on_change=login)

    if st.button("دخول"):
        login()
        st.rerun()   # ✅ هون مسموح

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

    st.subheader("➕ إضافة قطعة")

    with st.form("add_form"):
        name = st.text_input("اسم القطعة")
        model = st.text_input("الموديل")
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر", min_value=0)
        image = st.file_uploader("📷 صورة", type=["png", "jpg", "jpeg"])

        if st.form_submit_button("حفظ"):

            img_path = ""
            if image:
                os.makedirs("images", exist_ok=True)
                img_path = f"images/{image.name}"
                with open(img_path, "wb") as f:
                    f.write(image.getbuffer())

            new_id = 1 if df.empty else int(df["رقم"].max()) + 1

            new_row = pd.DataFrame([[new_id, name, model, qty, "جديد", price, img_path]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("تمت الإضافة ✅")
            st.rerun()

# =========================
# 👤 الزبون
# =========================
else:

    st.title("🛒 المنتجات")

    for _, row in df.iterrows():

        st.markdown(f"""
        <div class="product-card">
            <h3>{row['القطعة']}</h3>
            <p>💰 {row['السعر']} ₪</p>
        """, unsafe_allow_html=True)

        if row["الصورة"] and os.path.exists(row["الصورة"]):
            st.image(row["الصورة"], width=200)

        if st.button(f"🛒 أضف للسلة {row['رقم']}"):
            st.session_state.cart.append(row["القطعة"])
            st.success("تمت الإضافة ✅")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛒 السلة")

    for item in st.session_state.cart:
        st.write(item)
