import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# -----------------------
# CSS + زينة
# -----------------------
st.markdown("""
<style>
[data-testid="stToolbar"] {display:none;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
    background: linear-gradient(to bottom, #0f172a, #020617);
    color: white;
}

/* زينة */
@keyframes float {
    0% {transform: translateY(0);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0);}
}

.moon {position:absolute; top:0; right:20%; font-size:25px; animation: float 3s infinite;}
.star1 {position:absolute; top:10px; left:25%; font-size:20px;}
.star2 {position:absolute; top:30px; right:30%; font-size:18px;}

.product-card {
    padding: 15px;
    border-radius: 12px;
    background: #1e293b;
    margin-bottom: 15px;
    border: 1px solid #334155;
}

.whatsapp-btn {
    background-color: #25D366;
    color: white;
    padding: 8px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# الهيدر مع الزينة
# -----------------------
st.markdown("""
<div style='text-align:center; position:relative;'>
<div class="moon">🌙</div>
<div class="star1">✨</div>
<div class="star2">⭐</div>
</div>
""", unsafe_allow_html=True)

st.image("logo.png", use_container_width=True)
st.markdown("<h1 style='text-align:center;'>🛒 TechZone</h1>", unsafe_allow_html=True)

# -----------------------
# الحالة
# -----------------------
if "role" not in st.session_state:
    st.session_state.role = "guest"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "settings" not in st.session_state:
    st.session_state.settings = {
        "whatsapp": "0515906039",
        "facebook": "https://www.facebook.com/",
        "instagram": "https://instagram.com/"
    }

# -----------------------
# البيانات
# -----------------------
FILE_NAME = "warehouse.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)

        if "القسم" not in df.columns:
            df["القسم"] = "عام"

        if "رقم" not in df.columns:
            df.insert(0, "رقم", range(1, len(df) + 1))

        if "السعر" not in df.columns:
            df["السعر"] = 0

        return df

    return pd.DataFrame(columns=["رقم","القسم","القطعة","الموديل","الكمية","الحالة","السعر","الصورة"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# -----------------------
# زر دخول مخفي
# -----------------------
col1, col2 = st.columns([9,1])
with col2:
    if st.button("⋮"):
        st.session_state.show_login = True

# -----------------------
# تسجيل الدخول (Enter يشتغل)
# -----------------------
if st.session_state.show_login:

    st.subheader("🔐 دخول المدير")

    def login():
        if st.session_state.password == "7G4E976D":
            st.session_state.role = "admin"
            st.session_state.show_login = False
            st.rerun()
        else:
            st.error("كلمة السر غلط ❌")

    st.text_input("كلمة السر", type="password", key="password", on_change=login)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("دخول"):
            login()

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

    st.sidebar.header("📱 إعدادات التواصل")
    st.session_state.settings["whatsapp"] = st.sidebar.text_input("واتساب", st.session_state.settings["whatsapp"])
    st.session_state.settings["facebook"] = st.sidebar.text_input("فيسبوك", st.session_state.settings["facebook"])
    st.session_state.settings["instagram"] = st.sidebar.text_input("إنستغرام", st.session_state.settings["instagram"])

    # إضافة منتج
    st.subheader("➕ إضافة قطعة")

    with st.form("add"):
        category = st.text_input("القسم")
        name = st.text_input("اسم القطعة")
        model = st.text_input("الموديل")
        qty = st.number_input("الكمية", min_value=0)
        price = st.number_input("السعر", min_value=0)
        image = st.file_uploader("صورة")

        if st.form_submit_button("حفظ"):
            path = ""
            if image:
                os.makedirs("images", exist_ok=True)
                path = f"images/{image.name}"
                with open(path, "wb") as f:
                    f.write(image.getbuffer())

            new_row = pd.DataFrame([[len(df)+1, category, name, model, qty, "جديد", price, path]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("تمت الإضافة ✅")
            st.rerun()

# =========================
# 👤 الزبون
# =========================
else:

    st.title("🛒 المنتجات")

    categories = ["الكل"] + list(df["القسم"].dropna().unique())
    selected_category = st.selectbox("📂 القسم", categories)

    search = st.text_input("🔍 بحث")

    for _, row in df.iterrows():

        if (selected_category == "الكل" or row["القسم"] == selected_category) and (not search or search.lower() in str(row["القطعة"]).lower()):

            status = "✅ متوفر" if int(row["الكمية"]) > 0 else "❌ غير متوفر"
            discount = int(row["السعر"]) * 0.9

            st.markdown(f"""
            <div class="product-card">
                <h3>{row['القطعة']}</h3>
                <p>{status}</p>
                <p>💰 {row['السعر']} ₪</p>
                <p>🔥 {discount} ₪</p>
                <p>📦 الكمية: {row['الكمية']}</p>
            """, unsafe_allow_html=True)

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=200)

            if int(row["الكمية"]) > 0:
                if st.button(f"🛒 أضف للسلة {row['رقم']}"):
                    st.session_state.cart.append(row["القطعة"])

            whatsapp = st.session_state.settings["whatsapp"]
            msg = urllib.parse.quote("مرحبا بدي أطلب " + str(row["القطعة"]))
            link = f"https://wa.me/{whatsapp}?text={msg}"

            if int(row["الكمية"]) > 0:
                st.markdown(f"<a class='whatsapp-btn' href='{link}' target='_blank'>📞 واتساب</a>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# السلة (شغالة 100%)
# -----------------------
st.sidebar.title("🛒 السلة")

if len(st.session_state.cart) == 0:
    st.sidebar.write("السلة فارغة")
else:
    for i, item in enumerate(st.session_state.cart):
        col1, col2 = st.sidebar.columns([3,1])
        col1.write(item)
        if col2.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()

    if st.sidebar.button("🗑 تفريغ السلة"):
        st.session_state.cart = []
        st.rerun()

    if st.sidebar.button("📦 إرسال الطلب"):
        text = "طلب:\n" + "\n".join(st.session_state.cart)
        link = f"https://wa.me/{st.session_state.settings['whatsapp']}?text={urllib.parse.quote(text)}"
        st.sidebar.markdown(f"<a href='{link}' target='_blank'>📲 اضغط لإرسال الطلب</a>", unsafe_allow_html=True)
