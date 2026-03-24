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

# ✅ حل المشكلة (تنظيف السلة القديمة)
clean_cart = []
for item in st.session_state.cart:
    if isinstance(item, dict):
        clean_cart.append(item)
st.session_state.cart = clean_cart

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

   # -----------------------
# 🛒 السلة (شكل احترافي)
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
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">
            <div>
                <div style="font-size:18px;font-weight:bold;">
                    {item['name']}
                </div>
                <div style="color:gray;">
                    الكمية: {item['qty']}
                </div>
            </div>

            <div style="text-align:right;">
                <div style="font-size:16px;">
                    💰 {item['price']} ₪
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # زر حذف
        if st.button(f"❌ حذف {item['name']}", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"] * item["qty"]

    st.markdown("---")

    # 💰 المجموع بشكل جميل
    st.markdown(f"""
    <div style="
        background:#111;
        padding:15px;
        border-radius:12px;
        text-align:center;
        font-size:20px;
        font-weight:bold;
    ">
        💰 المجموع الكلي: {total} ₪
    </div>
    """, unsafe_allow_html=True)

    # 📱 زر واتساب
    cart_text = "\n".join([
        f"{item['name']} × {item['qty']}"
        for item in st.session_state.cart
    ])

    message = urllib.parse.quote(
        f"مرحبا، بدي أطلب:\n{cart_text}\n\nالمجموع: {total} ₪"
    )

    whatsapp_url = f"https://wa.me/{phone}?text={message}"

    st.markdown(f"""
    <br>
    <a href="{whatsapp_url}" target="_blank"
    style="
        background:#25D366;
        color:white;
        padding:12px 20px;
        border-radius:10px;
        text-decoration:none;
        font-size:18px;
        font-weight:bold;
        display:block;
        text-align:center;
    ">
    📱 إتمام الطلب عبر واتساب
    </a>
    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------
    # 🛒 السلة
    # -----------------------
    st.markdown("---")
    st.header("🛒 السلة")

    if len(st.session_state.cart) == 0:
        st.write("السلة فارغة")
    else:
        total = 0

        for i, item in enumerate(st.session_state.cart):

            col1, col2, col3, col4 = st.columns([4,2,2,1])

            with col1:
                st.write(item["name"])

            with col2:
                st.write(f"{item['price']} ₪")

            with col3:
                qty = st.number_input(
                    "الكمية",
                    min_value=1,
                    value=item["qty"],
                    key=f"qty_{i}"
                )
                item["qty"] = qty

            with col4:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

            total += item["price"] * item["qty"]

        st.markdown("---")
        st.write(f"💰 المجموع: {total} ₪")

        # إرسال الطلب واتساب
        cart_text = "\n".join([
            f"{item['name']} × {item['qty']}"
            for item in st.session_state.cart
        ])

        message = urllib.parse.quote(
            f"مرحبا، بدي أطلب:\n{cart_text}\n\nالمجموع: {total} ₪"
        )

        whatsapp_url = f"https://wa.me/{phone}?text={message}"

        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
        📱 إتمام الطلب عبر واتساب
        </a>
        """, unsafe_allow_html=True)
    
