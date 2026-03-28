import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", layout="wide")

# -----------------------
# ستايل
# -----------------------
st.markdown("""
<style>
.card {
    padding: 15px;
    border-radius: 15px;
    background-color: #1e293b;
    margin-bottom: 15px;
}
.price {
    color: orange;
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# الحالة
# -----------------------
if "role" not in st.session_state:
    st.session_state.role = "guest"

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "settings" not in st.session_state:
    st.session_state.settings = {"whatsapp": "966XXXXXXXX"}

if "cart" not in st.session_state:
    st.session_state.cart = []

# 🔥 السلايدر
if "banners" not in st.session_state:
    st.session_state.banners = []

if "banner_index" not in st.session_state:
    st.session_state.banner_index = 0

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
# السلايدر
# -----------------------
if st.session_state.banners:
    current = st.session_state.banner_index
    total = len(st.session_state.banners)

    st.image(st.session_state.banners[current], use_column_width=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅️"):
            st.session_state.banner_index = (current - 1) % total
            st.rerun()

    with col3:
        if st.button("➡️"):
            st.session_state.banner_index = (current + 1) % total
            st.rerun()

    dots = ""
    for i in range(total):
        dots += "🔵 " if i == current else "⚪ "

    st.markdown(f"<center>{dots}</center>", unsafe_allow_html=True)
else:
    st.image("banner.jpg", use_column_width=True)

# -----------------------
# اللوقو
# -----------------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown("## TechZone Store")

# -----------------------
# زر الدخول
# -----------------------
if st.button("⋮"):
    st.session_state.show_login = True

# -----------------------
# تسجيل الدخول
# -----------------------
if st.session_state.show_login:

    st.subheader("🔐 دخول المدير")
    password = st.text_input("كلمة السر", type="password")

    if st.button("دخول"):
        if password == "7D4E976D":
            st.session_state.role = "admin"
            st.session_state.show_login = False
            st.rerun()
        else:
            st.error("كلمة السر غلط ❌")

    if st.button("إلغاء"):
        st.session_state.show_login = False
        st.rerun()

    st.stop()

# =========================
# 👨‍💼 الأدمن
# =========================
if st.session_state.role == "admin":

    st.title("📦 لوحة التحكم")

    if st.button("تسجيل الخروج"):
        st.session_state.role = "guest"
        st.rerun()

    # 🔥 إدارة البانر
    st.sidebar.header("🖼️ البانر")

    banner_files = st.sidebar.file_uploader(
        "ارفع صور البانر",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if st.sidebar.button("📥 حفظ البانرات"):
        os.makedirs("banners", exist_ok=True)

        for file in banner_files:
            path = f"banners/{file.name}"
            with open(path, "wb") as f:
                f.write(file.getbuffer())

            st.session_state.banners.append(path)

        st.success("تم رفع البانرات ✅")

    # إعداد واتساب
    st.sidebar.header("📱 واتساب")
    st.session_state.settings["whatsapp"] = st.sidebar.text_input(
        "رقم الواتساب", st.session_state.settings["whatsapp"]
    )

    # إضافة منتج
    st.sidebar.header("➕ إضافة منتج")

    with st.sidebar.form("add_form"):
        name = st.text_input("اسم القطعة")
        model = st.text_input("الموديل")
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر", min_value=0)
        status = st.selectbox("الحالة", ["جديد", "مستعمل", "للفحص"])
        image = st.file_uploader("📷 صورة", type=["png", "jpg", "jpeg"])

        if st.form_submit_button("حفظ"):

            img_path = ""
            if image:
                os.makedirs("images", exist_ok=True)
                img_path = f"images/{image.name}"
                with open(img_path, "wb") as f:
                    f.write(image.getbuffer())

            new_id = 1 if df.empty else int(df["رقم"].max()) + 1

            new_row = pd.DataFrame(
                [[new_id, name, model, qty, status, price, img_path]],
                columns=df.columns
            )

            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("تمت الإضافة ✅")
            st.rerun()

    # عرض المنتجات
    for i, row in df.iterrows():
        with st.expander(f"{row['القطعة']}"):
            if row["الصورة"]:
                st.image(row["الصورة"], width=150)

            if st.button("🗑 حذف", key=i):
                df = df.drop(i).reset_index(drop=True)
                save_data(df)
                st.rerun()

# =========================
# 👤 المستخدم
# =========================
else:

    st.subheader("🛒 المنتجات")

    search = st.text_input("🔍 ابحث")

    cols = st.columns(3)

    for index, row in df.iterrows():
        if search.lower() in str(row["القطعة"]).lower():

            with cols[index % 3]:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                if row["الصورة"]:
                    st.image(row["الصورة"], use_column_width=True)

                st.markdown(f"### {row['القطعة']}")
                st.write(row["الموديل"])
                st.markdown(f"<div class='price'>{row['السعر']} ₪</div>", unsafe_allow_html=True)

                if st.button(f"🛒 {index}"):
                    st.session_state.cart.append(row.to_dict())

                st.markdown('</div>', unsafe_allow_html=True)

    # السلة
    st.subheader("🛒 السلة")

    total = 0
    for item in st.session_state.cart:
        st.write(f"{item['القطعة']} - {item['السعر']} ₪")
        total += item["السعر"]

    st.write(f"💰 المجموع: {total} ₪")
