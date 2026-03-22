import streamlit as st
import pandas as pd
import os
import urllib.parse

st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# 🌙 CSS + نجوم متحركة
st.markdown("""
<style>

/* إخفاء الترس */
[data-testid="stToolbar"] {display:none;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

/* خلفية */
.stApp {
    background: linear-gradient(to bottom, #0f172a, #020617);
    color: white;
}

/* نجوم */
body::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(white 1px, transparent 1px);
    background-size: 40px 40px;
    animation: moveStars 60s linear infinite;
    z-index: -1;
}

@keyframes moveStars {
    from {transform: translateY(0);}
    to {transform: translateY(-1000px);}
}

/* كروت */
.product-card {
    padding: 15px;
    border-radius: 15px;
    background: #1e293b;
    margin: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

/* زر */
.whatsapp-btn {
    background-color: #25D366;
    padding: 8px;
    border-radius: 8px;
    color: white;
    text-decoration: none;
}

/* الهلال */
.moon {
    font-size: 30px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0% {transform: translateY(0);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# 🌙 هيدر
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
st.markdown("<div class='moon'>🌙✨</div>", unsafe_allow_html=True)
st.image("logo.png", use_container_width=True)
st.markdown("<h1>🛒 TechZone</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# الحالة
# -----------------------
if "role" not in st.session_state:
    st.session_state.role = "guest"

if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------
# البيانات
# -----------------------
FILE_NAME = "warehouse.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    return pd.DataFrame(columns=["القسم","القطعة","الكمية","السعر","الصورة"])

df = load_data()

# -----------------------
# فلترة
# -----------------------
st.sidebar.title("📂 الأقسام")

categories = ["الكل"] + list(df["القسم"].dropna().unique())
selected_category = st.sidebar.selectbox("اختر", categories)

search = st.text_input("🔍 بحث")

# -----------------------
# المنتجات
# -----------------------
cols = st.columns(3)

for i, row in df.iterrows():

    if (selected_category == "الكل" or row["القسم"] == selected_category) and (not search or search.lower() in str(row["القطعة"]).lower()):

        with cols[i % 3]:

            status = "✅ متوفر" if int(row["الكمية"]) > 0 else "❌ غير متوفر"
            discount = int(row["السعر"]) * 0.9

            st.markdown(f"""
            <div class="product-card">
                <h3>{row['القطعة']}</h3>
                <p>{status}</p>
                <p>💰 {row['السعر']} ₪</p>
                <p>🔥 {discount} ₪</p>
                <p>📦 {row['الكمية']}</p>
            """, unsafe_allow_html=True)

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"])

            if int(row["الكمية"]) > 0:
                if st.button(f"🛒 أضف {i}"):
                    st.session_state.cart.append(row["القطعة"])
                    st.success("تمت الإضافة ✅")

            whatsapp = "0515906039"
            msg = urllib.parse.quote("بدي أطلب " + str(row["القطعة"]))
            link = f"https://wa.me/{whatsapp}?text={msg}"

            if int(row["الكمية"]) > 0:
                st.markdown(f"<a class='whatsapp-btn' href='{link}'>واتساب</a>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# السلة
# -----------------------
st.sidebar.title("🛒 السلة")

for item in st.session_state.cart:
    st.sidebar.write("✔ " + item)

# -----------------------
# إرسال الطلب
# -----------------------
if st.sidebar.button("📦 إرسال الطلب"):
    text = "طلب:\n" + "\n".join(st.session_state.cart)
    link = f"https://wa.me/0515906039?text={urllib.parse.quote(text)}"
    st.sidebar.markdown(f"[إرسال عبر واتساب]({link})")
