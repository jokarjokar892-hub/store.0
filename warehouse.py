import streamlit as st
import urllib.parse

# =========================
# إعدادات
# =========================
ADMIN_USER = "محمد"
ADMIN_PASS = "7B4E9976D"
WHATSAPP = "972515906039"

st.set_page_config(page_title="TechZone", layout="wide")

# =========================
# حالة التطبيق
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "products" not in st.session_state:
    st.session_state.products = [
        {
            "name": "معالج Intel i5",
            "price": 500,
            "qty": 5,
            "category": "معالج",
            "image": "https://i.imgur.com/8zQZ6XG.png"
        },
        {
            "name": "كرت شاشة RTX 3050",
            "price": 1200,
            "qty": 3,
            "category": "كرت شاشة",
            "image": "https://i.imgur.com/2z9sP3K.png"
        }
    ]

# =========================
# اللوجو
# =========================
st.image("https://i.imgur.com/YOUR_LOGO.png", width=250)
st.title("🛒 TechZone Store")

# =========================
# الفلترة
# =========================
categories = list(set([p["category"] for p in st.session_state.products]))
selected = st.selectbox("اختر القسم", ["الكل"] + categories)

# =========================
# عرض المنتجات
# =========================
for i, item in enumerate(st.session_state.products):

    if selected != "الكل" and item["category"] != selected:
        continue

    col1, col2 = st.columns([1,2])

    with col1:
        st.image(item["image"], use_container_width=True)

    with col2:
        st.subheader(item["name"])
        st.write(f"💰 السعر: {item['price']} ₪")
        st.write(f"📦 المتوفر: {item['qty']}")

        if item["qty"] > 0:
            if st.button(f"أضف للسلة {i}"):
                st.session_state.cart.append(item)
                st.success("تمت الإضافة ✅")
        else:
            st.error("❌ غير متوفر")

    st.divider()

# =========================
# السلة
# =========================
st.header("🛍️ السلة")

total = 0
msg = ""

for item in st.session_state.cart:
    st.write(f"{item['name']} - {item['price']} ₪")
    total += item["price"]
    msg += f"{item['name']} - {item['price']} ₪\n"

st.write(f"💵 المجموع: {total} ₪")

if st.button("📲 إرسال الطلب واتساب"):
    encoded = urllib.parse.quote(msg)
    url = f"https://wa.me/{WHATSAPP}?text={encoded}"
    st.markdown(f"[اضغط هنا للإرسال]({url})")

# =========================
# دخول المدير (مخفي)
# =========================
params = st.query_params

if "admin" in params:
    st.sidebar.title("🔐 دخول المدير")

    u = st.sidebar.text_input("اسم المستخدم")
    p = st.sidebar.text_input("كلمة المرور", type="password")

    if st.sidebar.button("دخول"):
        if u == ADMIN_USER and p == ADMIN_PASS:
            st.session_state.admin = True
            st.success("تم الدخول")
        else:
            st.error("خطأ")

# =========================
# لوحة الإدارة
# =========================
if st.session_state.get("admin"):

    st.sidebar.success("أنت مدير")

    st.sidebar.header("➕ إضافة منتج")

    name = st.sidebar.text_input("اسم المنتج")
    price = st.sidebar.number_input("السعر", 0)
    qty = st.sidebar.number_input("الكمية", 0)
    category = st.sidebar.text_input("القسم")
    image = st.sidebar.text_input("رابط الصورة")

    if st.sidebar.button("إضافة"):
        st.session_state.products.append({
            "name": name,
            "price": price,
            "qty": qty,
            "category": category,
            "image": image
        })
        st.success("تمت الإضافة ✅")

    st.sidebar.header("❌ حذف منتج")

    names = [p["name"] for p in st.session_state.products]
    selected_name = st.sidebar.selectbox("اختر", names)

    if st.sidebar.button("حذف"):
        st.session_state.products = [p for p in st.session_state.products if p["name"] != selected_name]
        st.success("تم الحذف")
