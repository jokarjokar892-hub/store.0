import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", layout="wide")

# -----------------------
# ستايل احترافي
# -----------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.card {
    padding: 15px;
    border-radius: 15px;
    background-color: #1e293b;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
.price {
    color: #f59e0b;
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
    st.session_state.settings = {
        "whatsapp": "966XXXXXXXX"
    }

if "cart" not in st.session_state:
    st.session_state.cart = []

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
# البانر + اللوقو
# -----------------------
st.image("banner.jpg", use_column_width=True)

col1, col2 = st.columns([1,5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown("## TechZone Store")

# -----------------------
# زر القائمة
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
# 👨‍💼 المدير
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
        image = st.file_uploader("📷 صورة المنتج", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("حفظ")

        if submitted:
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

            st.success(f"تمت الإضافة ✅ رقم المنتج: #{new_id}")
            st.rerun()

    st.subheader("📋 إدارة المنتجات")

    for i, row in df.iterrows():

        with st.expander(f"#{row['رقم']} - {row['القطعة']}"):

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=150)

            new_name = st.text_input("اسم القطعة", row["القطعة"], key=f"name{i}")
            new_model = st.text_input("الموديل", row["الموديل"], key=f"model{i}")
            new_qty = st.number_input("الكمية", value=int(row["الكمية"]), key=f"qty{i}")
            new_price = st.number_input("السعر", value=int(row["السعر"]), key=f"price{i}")

            new_status = st.selectbox(
                "الحالة",
                ["جديد", "مستعمل", "للفحص"],
                index=["جديد", "مستعمل", "للفحص"].index(row["الحالة"]),
                key=f"status{i}"
            )

            new_image = st.file_uploader("تغيير الصورة", key=f"img{i}")

            if st.button("💾 حفظ", key=f"save{i}"):

                df.at[i, "القطعة"] = new_name
                df.at[i, "الموديل"] = new_model
                df.at[i, "الكمية"] = new_qty
                df.at[i, "الحالة"] = new_status
                df.at[i, "السعر"] = new_price

                if new_image:
                    img_path = f"images/{new_image.name}"
                    with open(img_path, "wb") as f:
                        f.write(new_image.getbuffer())
                    df.at[i, "الصورة"] = img_path

                save_data(df)
                st.success("تم التعديل ✅")
                st.rerun()

            if st.button("🗑 حذف", key=f"delete{i}"):
                df = df.drop(i).reset_index(drop=True)
                save_data(df)
                st.warning("تم الحذف ❌")
                st.rerun()

# =========================
# 👤 الزبون
# =========================
else:

    st.subheader("🛒 منتجاتنا")

    search = st.text_input("🔍 ابحث")

    cols = st.columns(3)

    for index, row in df.iterrows():

        if search.lower() in str(row["القطعة"]).lower():

            with cols[index % 3]:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                if row["الصورة"] and os.path.exists(row["الصورة"]):
                    st.image(row["الصورة"], use_column_width=True)

                st.markdown(f"### {row['القطعة']}")
                st.write(f"🔧 {row['الموديل']}")
                st.markdown(f"<div class='price'>{row['السعر']} ₪</div>", unsafe_allow_html=True)

                whatsapp = st.session_state.settings["whatsapp"]
                message = urllib.parse.quote(f"مرحبا، بدي أطلب {row['القطعة']}")
                wa_link = f"https://wa.me/{whatsapp}?text={message}"

                st.markdown(f"[📞 واتساب]({wa_link})")

                if st.button(f"🛒 أضف للسلة {index}"):
                    st.session_state.cart.append(row.to_dict())
                    st.success("تمت الإضافة ✅")

                st.markdown('</div>', unsafe_allow_html=True)

    # 🛒 السلة
    st.subheader("🛒 سلة المشتريات")

    if st.session_state.cart:
        total = 0
        for item in st.session_state.cart:
            st.write(f"{item['القطعة']} - {item['السعر']} ₪")
            total += item["السعر"]

        st.write(f"💰 المجموع: {total} ₪")

    else:
        st.info("السلة فارغة")
