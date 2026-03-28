import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", layout="wide")

# -----------------------
# CSS احترافي
# -----------------------
st.markdown("""
<style>

body {
    background-color: #0e1117;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1f2a40;
    padding: 15px;
    border-radius: 10px;
}

.logo {
    font-size: 26px;
    font-weight: bold;
    color: orange;
}

.search-box input {
    width: 400px;
    padding: 10px;
    border-radius: 10px;
    border: none;
}

.card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.05);
}

.btn {
    background: orange;
    padding: 10px;
    border-radius: 10px;
    color: black;
    text-decoration: none;
    display: inline-block;
    margin-top: 5px;
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
    st.session_state.settings = {
        "whatsapp": "966XXXXXXXX"
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
    else:
        return pd.DataFrame(columns=["رقم", "القطعة", "الموديل", "الكمية", "الحالة", "السعر", "الصورة"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# =========================
# 🔝 Navbar
# =========================
col_nav1, col_nav2, col_nav3 = st.columns([2,4,1])

with col_nav1:
    st.image("logo.png", width=120)
    st.markdown("### TechZone")

with col_nav2:
    search = st.text_input("🔍 ابحث عن منتج...")

with col_nav3:
    if st.button("⋮"):
        st.session_state.show_login = True

# =========================
# تسجيل الدخول
# =========================
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
# 👨‍💼 المدير (نفسه بدون تغيير)
# =========================
if st.session_state.role == "admin":

    st.title("📦 لوحة التحكم")

    if st.button("تسجيل الخروج"):
        st.session_state.role = "guest"
        st.rerun()

    st.sidebar.header("📱 إعدادات التواصل")
    st.session_state.settings["whatsapp"] = st.sidebar.text_input(
        "رقم الواتساب", st.session_state.settings["whatsapp"]
    )

    st.sidebar.header("➕ إضافة قطعة")

    with st.sidebar.form("add_form"):
        name = st.text_input("اسم القطعة")
        model = st.text_input("الموديل")
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر", min_value=0)
        status = st.selectbox("الحالة", ["جديد", "مستعمل", "للفحص"])
        image = st.file_uploader("📷 صورة المنتج")

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
            st.rerun()

    admin_search = st.text_input("🔍 ابحث داخل المنتجات")
    filtered_df = df[df["القطعة"].astype(str).str.contains(admin_search, case=False)]

    for i, row in filtered_df.iterrows():
        with st.expander(f"{row['القطعة']}"):
            st.write(row)

# =========================
# 👤 الزبون (تصميم احترافي)
# =========================
else:

    col1, col2 = st.columns([3,1])

    # المنتجات
    with col1:

        st.image("banner.jpg", use_container_width=True)

        cols = st.columns(3)

        for i, row in df.iterrows():

            if search.lower() in str(row["القطعة"]).lower():

                with cols[i % 3]:

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    if row["الصورة"] and os.path.exists(row["الصورة"]):
                        st.image(row["الصورة"], use_container_width=True)

                    st.markdown(f"### {row['القطعة']}")
                    st.write(f"💰 {row['السعر']} ₪")

                    if st.button(f"🛒 أضف {i}"):
                        st.session_state.cart.append(row.to_dict())

                    whatsapp = st.session_state.settings["whatsapp"]
                    msg = urllib.parse.quote(f"مرحبا بدي أطلب {row['القطعة']}")
                    link = f"https://wa.me/{whatsapp}?text={msg}"

                    st.markdown(f"<a class='btn' href='{link}'>اطلب الآن</a>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

    # السلة
    with col2:

        st.subheader("🛒 السلة")

        total = 0

        for item in st.session_state.cart:
            st.write(item["القطعة"])
            total += item["السعر"]

        st.write(f"💰 {total} ₪")

        if st.session_state.cart:
            if st.button("طلب الكل"):
                items = "\n".join([i["القطعة"] for i in st.session_state.cart])
                msg = urllib.parse.quote(f"مرحبا بدي أطلب:\n{items}")
                link = f"https://wa.me/{st.session_state.settings['whatsapp']}?text={msg}"
                st.markdown(f"[اضغط هنا]({link})")
