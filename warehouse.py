import streamlit as st
import pandas as pd
import os
import urllib.parse

# -----------------------
# إعداد الصفحة
# -----------------------
st.set_page_config(page_title="TechZone", page_icon="🛒", layout="wide")

# -----------------------
# 🔥 CSS + إخفاء الترس
# -----------------------
st.markdown("""
<style>
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {background-color: var(--background-color);}

h1, h2, h3, p, span {
    color: var(--text-color) !important;
}

.product-card {
    padding: 15px;
    border-radius: 12px;
    background-color: var(--secondary-background-color);
    margin-bottom: 15px;
    border: 1px solid rgba(128,128,128,0.2);
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

.social-link {
    display: inline-block;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# الهيدر
# -----------------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image("logo.png", use_container_width=True)

st.markdown("""
<h1>🛒 TechZone</h1>
<p>عالم التقنية - أفضل الأجهزة 🔥</p>
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

# 🛒 السلة (إضافة)
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
    return pd.DataFrame(columns=["رقم", "القطعة", "الموديل", "الكمية", "الحالة", "السعر", "الصورة"])

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
            st.rerun()
        else:
            st.error("كلمة السر غلط ❌")

    password = st.text_input(
        "كلمة السر",
        type="password",
        key="password",
        on_change=login
    )

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

    st.sidebar.header("📱 إعدادات التواصل")

    st.session_state.settings["whatsapp"] = st.sidebar.text_input("واتساب", st.session_state.settings["whatsapp"])
    st.session_state.settings["facebook"] = st.sidebar.text_input("فيسبوك", st.session_state.settings["facebook"])
    st.session_state.settings["instagram"] = st.sidebar.text_input("إنستغرام", st.session_state.settings["instagram"])

    st.subheader("➕ إضافة قطعة")

    with st.form("add_form"):
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

    st.subheader("📋 إدارة المنتجات")

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
                if st.button("💾 حفظ", key=f"save{i}"):
                    df.at[i, "القطعة"] = new_name
                    df.at[i, "الموديل"] = new_model
                    df.at[i, "الكمية"] = new_qty
                    df.at[i, "السعر"] = new_price
                    save_data(df)
                    st.success("تم التعديل ✅")
                    st.rerun()

            with col2:
                if st.button("🗑 حذف", key=f"del{i}"):
                    df = df.drop(i).reset_index(drop=True)
                    save_data(df)
                    st.warning("تم الحذف 🗑")
                    st.rerun()

# =========================
# 👤 الزبون
# =========================
else:

    st.title("🛒 المنتجات")

    search = st.text_input("🔍 ابحث")

    for _, row in df.iterrows():

        if not search or search.lower() in str(row["القطعة"]).lower():

            status = "✅ متوفر" if int(row["الكمية"]) > 0 else "❌ غير متوفر"

            st.markdown(f"""
            <div class="product-card">
                <h3>📦 {row['القطعة']}</h3>
                <p>💰 {row['السعر']} ₪</p>
                <p>{status}</p>
                <p>📦 الكمية: {row['الكمية']}</p>
            """, unsafe_allow_html=True)

            if row["الصورة"] and os.path.exists(row["الصورة"]):
                st.image(row["الصورة"], width=200)

            if int(row["الكمية"]) > 0:

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"🛒 أضف للسلة {row['رقم']}"):
                        st.session_state.cart.append({
                            "name": row["القطعة"],
                            "price": row["السعر"]
                        })
                        st.success("تمت الإضافة للسلة ✅")

                with col2:
                    whatsapp = st.session_state.settings["whatsapp"]
                    msg = urllib.parse.quote("مرحبا بدي أطلب " + str(row["القطعة"]))
                    link = f"https://wa.me/{whatsapp}?text={msg}"

                    st.markdown(f"""
                    <a class="whatsapp-btn" href="{link}">📞 شراء مباشر</a>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:10px;">
                    <a class="social-link" href="{st.session_state.settings['facebook']}">📘 فيسبوك</a><br>
                    <a class="social-link" href="{st.session_state.settings['instagram']}">📷 إنستغرام</a>
                </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div style="margin-top:10px;">
                    <p style="color:red;">🚫 غير متوفر حالياً</p>
                </div>
                </div>
                """, unsafe_allow_html=True)

    # =========================
    # 🛒 السلة
    # =========================
    st.markdown("---")
    st.header("🛒 السلة")

    total = 0
    order_text = ""

    if len(st.session_state.cart) == 0:
        st.info("السلة فاضية 🛒")

    for i, item in enumerate(st.session_state.cart):

        col1, col2 = st.columns([3,1])

        with col1:
            st.write(f"{item['name']} - {item['price']} ₪")

        with col2:
            if st.button(f"❌ حذف {i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        total += item["price"]
        order_text += f"{item['name']} - {item['price']} ₪\n"

    st.write(f"💰 المجموع: {total} ₪")

    if len(st.session_state.cart) > 0:
        whatsapp = st.session_state.settings["whatsapp"]
        msg = urllib.parse.quote("طلب جديد:\n" + order_text + f"\nالمجموع: {total} ₪")
        link = f"https://wa.me/{whatsapp}?text={msg}"

        st.markdown(f"""
        <a class="whatsapp-btn" href="{link}">📲 إرسال الطلب كامل</a>
        """, unsafe_allow_html=True)

        if st.button("🗑 تفريغ السلة"):
            st.session_state.cart = []
            st.rerun()
