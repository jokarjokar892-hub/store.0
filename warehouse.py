import streamlit as st
import pandas as pd
import os

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# خلفية
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# 🔥 الهيدر (مع لوجو)
# -----------------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image("logo.png", width=150)
st.markdown("""
<h1 style='color:#1B4F72; font-size:50px;'>🛒 TechZone</h1>
<p style='color:#555; font-size:20px;'>عالم التقنية - أفضل الأجهزة 🔥</p>
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
# ملف البيانات
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
# زر الإعدادات
# -----------------------
if st.button("⚙️"):
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

    # إعدادات
    st.sidebar.header("📱 إعدادات التواصل")

    st.session_state.settings["whatsapp"] = st.sidebar.text_input("واتساب", st.session_state.settings["whatsapp"])
    st.session_state.settings["facebook"] = st.sidebar.text_input("فيسبوك", st.session_state.settings["facebook"])
    st.session_state.settings["instagram"] = st.sidebar.text_input("إنستغرام", st.session_state.settings["instagram"])

    # إضافة منتج
    st.sidebar.header("➕ إضافة قطعة")

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

    # إدارة
    st.subheader("📋 المنتجات")

    for i, row in df.iterrows():

        with st.expander(f"{row['القطعة']}"):

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=150)

            new_name = st.text_input("الاسم", row["القطعة"], key=f"name{i}")
            new_model = st.text_input("الموديل", row["الموديل"], key=f"model{i}")
            new_qty = st.number_input("الكمية", value=int(row["الكمية"]), key=f"qty{i}")
            new_price = st.number_input("السعر", value=int(row["السعر"]), key=f"price{i}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾", key=f"save{i}"):
                    df.at[i, "القطعة"] = new_name
                    df.at[i, "الموديل"] = new_model
                    df.at[i, "الكمية"] = new_qty
                    df.at[i, "السعر"] = new_price
                    save_data(df)
                    st.rerun()

            with col2:
                if st.button("🗑", key=f"del{i}"):
                    df = df.drop(i).reset_index(drop=True)
                    save_data(df)
                    st.rerun()

# =========================
# 👤 الزبون
# =========================
else:

    st.title("🛒 المنتجات")

    search = st.text_input("🔍 ابحث")

    for _, row in df.iterrows():

        if search.lower() in str(row["القطعة"]).lower():

            st.markdown(f"### 📦 {row['القطعة']}")
            st.write(f"💰 {row['السعر']} ₪")

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=200)

            whatsapp = st.session_state.settings["whatsapp"]
            msg = f"مرحبا بدي أطلب {row['القطعة']}"
            link = f"https://wa.me/{whatsapp}?text={msg}"

            st.markdown(f"[📞 اطلب عبر واتساب]({link})")
            st.markdown("---")
