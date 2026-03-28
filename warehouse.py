import streamlit as st
import pandas as pd
import os
import urllib.parse

st.set_page_config(page_title="TechZone", layout="wide")

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

# -----------------------
# ملفات
# -----------------------
FILE_NAME = "warehouse.csv"
BANNER_FILE = "banners.csv"

# -----------------------
# دوال
# -----------------------
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        if "رقم" not in df.columns:
            df.insert(0, "رقم", range(1, len(df) + 1))
        if "السعر" not in df.columns:
            df["السعر"] = 0
        return df
    return pd.DataFrame(columns=["رقم","القطعة","الموديل","الكمية","الحالة","السعر","الصورة"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

def load_banners():
    if os.path.exists(BANNER_FILE):
        return pd.read_csv(BANNER_FILE)
    return pd.DataFrame(columns=["path"])

def save_banners(df):
    df.to_csv(BANNER_FILE, index=False)

df = load_data()
banners_df = load_banners()

# -----------------------
# 🎯 سلايدر بالسحب (Drag)
# -----------------------
if not banners_df.empty:

    images = banners_df["path"].tolist()

    slider_html = f"""
    <style>
    .slider {{
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
    }}

    .slider img {{
        width: 100%;
        height: 300px;
        object-fit: cover;
        scroll-snap-align: start;
        border-radius: 10px;
        margin-right: 10px;
    }}

    .slider::-webkit-scrollbar {{
        display: none;
    }}
    </style>

    <div class="slider">
        {''.join([f'<img src="{img}">' for img in images])}
    </div>
    """

    st.components.v1.html(slider_html, height=320)

else:
    st.image("banner.jpg", use_column_width=True)

# -----------------------
# اللوقو
# -----------------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.title("TechZone")

# -----------------------
# تسجيل الدخول
# -----------------------
if st.button("⋮"):
    st.session_state.show_login = True

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

    # -----------------------
    # 🖼️ البانرات
    # -----------------------
    st.sidebar.header("🖼️ إدارة البانرات")

    banner_file = st.sidebar.file_uploader("اختر صورة بانر")

    if st.sidebar.button("➕ إضافة بانر"):
        if banner_file:
            os.makedirs("banners", exist_ok=True)
            path = f"banners/{banner_file.name}"

            with open(path, "wb") as f:
                f.write(banner_file.getbuffer())

            new = pd.DataFrame([[path]], columns=["path"])
            banners_df = pd.concat([banners_df, new], ignore_index=True)
            save_banners(banners_df)

            st.success("تمت إضافة البانر ✅")
            st.rerun()
        else:
            st.warning("ارفع صورة أولاً")

    st.sidebar.subheader("📂 الصور الحالية")

    for i, row in banners_df.iterrows():
        col1, col2 = st.sidebar.columns([3,1])

        with col1:
            st.image(row["path"], width=100)

        with col2:
            if st.button("❌", key=f"del{i}"):
                banners_df = banners_df.drop(i).reset_index(drop=True)
                save_banners(banners_df)
                st.rerun()

    # -----------------------
    # واتساب
    # -----------------------
    st.sidebar.header("📱 واتساب")
    st.session_state.settings["whatsapp"] = st.sidebar.text_input(
        "رقم الواتساب", st.session_state.settings["whatsapp"]
    )

    # -----------------------
    # إضافة منتج (بدون أي منتجات جاهزة)
    # -----------------------
    st.sidebar.header("➕ إضافة قطعة")

    with st.sidebar.form("add_form"):
        name = st.text_input("اسم القطعة")
        model = st.text_input("الموديل")
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر", min_value=0)
        status = st.selectbox("الحالة", ["جديد","مستعمل","للفحص"])
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

            st.success("تمت الإضافة ✅")
            st.rerun()

# =========================
# 👤 المستخدم
# =========================
else:

    st.subheader("🛒 المنتجات")

    search = st.text_input("🔍 ابحث")

    for index, row in df.iterrows():
        if search.lower() in str(row["القطعة"]).lower():

            st.markdown(f"### {row['القطعة']}")
            st.write(row["الموديل"])
            st.write(f"💰 {row['السعر']} ₪")

            if row["الصورة"]:
                st.image(row["الصورة"], width=200)

            # زر إضافة للسلة
            if st.button(f"🛒 أضف {index}"):
                st.session_state.cart.append(row.to_dict())
                st.success("تمت الإضافة للسلة")

            st.markdown("---")

    # -----------------------
    # 🛒 السلة + واتساب
    # -----------------------
    st.subheader("🛒 السلة")

    if st.session_state.cart:

        total = 0
        items_text = ""

        for item in st.session_state.cart:
            st.write(f"{item['القطعة']} - {item['السعر']} ₪")
            total += item["السعر"]
            items_text += f"- {item['القطعة']}\n"

        st.write(f"💰 المجموع: {total} ₪")

        if st.button("📞 طلب الكل عبر واتساب"):
            whatsapp = st.session_state.settings["whatsapp"]

            message = urllib.parse.quote(
                f"مرحبا، بدي أطلب:\n{items_text}\nالمجموع: {total} ₪"
            )

            wa_link = f"https://wa.me/{whatsapp}?text={message}"

            st.markdown(f"[اضغط هون لإرسال الطلب]({wa_link})")

    else:
        st.info("السلة فارغة")
