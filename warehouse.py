import streamlit as st
import pandas as pd
import os

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="المستودع", layout="wide")

# -----------------------
# الحالة
# -----------------------
if "role" not in st.session_state:
    st.session_state.role = "guest"

if "show_login" not in st.session_state:
    st.session_state.show_login = False

# إعدادات التواصل
if "settings" not in st.session_state:
    st.session_state.settings = {
        "whatsapp": "966XXXXXXXX",
        "facebook": "https://facebook.com/yourpage",
        "instagram": "https://instagram.com/yourpage"
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
# ⚙️ زر الترس
# -----------------------
if st.button("⚙️"):
    st.session_state.show_login = True

# -----------------------
# 🔐 تسجيل دخول المدير
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
# 👨‍💼 واجهة المدير
# =========================
if st.session_state.role == "admin":

    st.title("📦 لوحة التحكم")

    if st.button("تسجيل الخروج"):
        st.session_state.role = "guest"
        st.rerun()

    # إعدادات التواصل
    st.sidebar.header("📱 إعدادات التواصل")

    st.session_state.settings["whatsapp"] = st.sidebar.text_input(
        "رقم الواتساب", st.session_state.settings["whatsapp"]
    )

    st.session_state.settings["facebook"] = st.sidebar.text_input(
        "رابط فيسبوك", st.session_state.settings["facebook"]
    )

    st.session_state.settings["instagram"] = st.sidebar.text_input(
        "رابط إنستغرام", st.session_state.settings["instagram"]
    )

    # إضافة منتج
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

    # إدارة المنتجات
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

            col1, col2 = st.columns(2)

            with col1:
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

            with col2:
                if st.button("🗑 حذف", key=f"delete{i}"):
                    df = df.drop(i).reset_index(drop=True)
                    save_data(df)
                    st.warning("تم الحذف ❌")
                    st.rerun()

# =========================
# 👤 واجهة الزبون
# =========================
else:

    st.title("🛒 عرض المنتجات")

    search = st.text_input("🔍 ابحث")

    for index, row in df.iterrows():

        if search.lower() in str(row["القطعة"]).lower():

            st.markdown(f"### 📦 {row['القطعة']}")
            st.write(f"🔧 الموديل: {row['الموديل']}")
            st.write(f"💰 السعر: {row['السعر']} شيكل ₪")
            st.write(f"📊 المتوفر: {row['الكمية']}")
            st.write(f"📌 الحالة: {row['الحالة']}")

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=200)

            # زر تواصل واتساب
            whatsapp = st.session_state.settings["whatsapp"]
            message = f"مرحبا، بدي أطلب {row['القطعة']}"
            wa_link = f"https://wa.me/{whatsapp}?text={message}"

            st.markdown(f"[📞 اطلب عبر واتساب]({wa_link})")

            # باقي الروابط
            st.markdown(f"[فيسبوك]({st.session_state.settings['facebook']})")
            st.markdown(f"[إنستغرام]({st.session_state.settings['instagram']})")

            st.markdown("---")