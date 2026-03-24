import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.product-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #1e1e1e;
    margin-bottom: 15px;
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
</style>
""", unsafe_allow_html=True)

# -----------------------
# الهيدر
# -----------------------
st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)

if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)

st.markdown("<h1>🛒 TechZone</h1>", unsafe_allow_html=True)
st.markdown("<p>عالم التقنية 🔥</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# الحالة
# -----------------------
if "role" not in st.session_state:
    st.session_state.role = "guest"

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "cart" not in st.session_state:
    st.session_state.cart = []

if "settings" not in st.session_state:
    st.session_state.settings = {
        "whatsapp": "0515906039"
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
        return df
    return pd.DataFrame(columns=["رقم","القطعة","الموديل","الكمية","الحالة","السعر","الصورة"])

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

    st.text_input("كلمة السر", type="password", key="password")

    if st.button("دخول"):
        login()
        st.rerun()

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
        image = st.file_uploader("📷 صورة", type=["png","jpg","jpeg"])

        if st.form_submit_button("حفظ"):

            img_path = ""
            if image:
                os.makedirs("images", exist_ok=True)
                img_path = f"images/{image.name}"
                with open(img_path, "wb") as f:
                    f.write(image.getbuffer())

            new_id = 1 if df.empty else int(df["رقم"].max()) + 1

            new_row = pd.DataFrame(
                [[new_id, name, model, qty, "جديد", price, img_path]],
                columns=df.columns
            )

            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("تمت الإضافة ✅")
            st.rerun()

# =========================
# 👤 الزبون
# =========================
else:

    st.title("🛒 المنتجات")

    phone = st.session_state.settings["whatsapp"]
    if phone.startswith("0"):
        phone = "972" + phone[1:]

    for _, row in df.iterrows():

        st.markdown(f"""
        <div class="product-card">
            <h3>{row['القطعة']}</h3>
            <p>💰 {row['السعر']} ₪</p>
        """, unsafe_allow_html=True)

        if row["الصورة"] and os.path.exists(row["الصورة"]):
            st.image(row["الصورة"], width=200)

        # ✅ الزر بدون رقم + key مخفي
        if st.button("🛒 أضف للسلة", key=f"add_{row['رقم']}"):

            found = False
            for item in st.session_state.cart:
                if item["name"] == row["القطعة"]:
                    item["qty"] += 1
                    found = True
                    break

            if not found:
                st.session_state.cart.append({
                    "name": row["القطعة"],
                    "price": row["السعر"],
                    "qty": 1
                })

            st.success("تمت الإضافة ✅")

        message = urllib.parse.quote(
            f"مرحبا، بدي أطلب: {row['القطعة']} - السعر {row['السعر']} ₪"
        )
        whatsapp_url = f"https://wa.me/{phone}?text={message}"

        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
        📱 شراء مباشر
        </a>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------
    # 🛒 السلة
    # -----------------------
    st.markdown("---")
    st.header("🛒 السلة")

    if len(st.session_state.cart) == 0:
        st.info("السلة فارغة 🛒")

    else:
        total = 0

        for i, item in enumerate(st.session_state.cart):

            st.markdown(f"""
            <div style="
                background:#1e1e1e;
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
            ">
                <b>{item['name']}</b><br>
                الكمية: {item['qty']}<br>
                💰 {item['price']} ₪
            </div>
            """, unsafe_allow_html=True)

            if st.button("❌ حذف", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

            total += item["price"] * item["qty"]

        st.markdown(f"### 💰 المجموع: {total} ₪")
