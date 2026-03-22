import streamlit as st

# ---------- إعدادات ----------
ADMIN_USER = "محمد"
ADMIN_PASS = "7B4E9976D"
WHATSAPP = "972515906039"

# ---------- حالة الجلسة ----------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "products" not in st.session_state:
    st.session_state.products = [
        {
            "name": "معالج Intel i5",
            "price": 500,
            "qty": 5,
            "category": "معالج",
            "image": "cpu.png"
        },
        {
            "name": "كرت شاشة RTX 3050",
            "price": 1200,
            "qty": 3,
            "category": "كرت شاشة",
            "image": "gpu.png"
        }
    ]

# ---------- اللوجو ----------
st.image("logo.png", width=200)
st.title("🛒 TechZone Store")

# ---------- فلتر ----------
categories = list(set([p["category"] for p in st.session_state.products]))
selected_category = st.selectbox("اختر القسم", ["الكل"] + categories)

# ---------- عرض المنتجات ----------
for i, item in enumerate(st.session_state.products):

    if selected_category != "الكل" and item["category"] != selected_category:
        continue

    st.image(item["image"], width=200)
    st.subheader(item["name"])
    st.write(f"السعر: {item['price']} ₪")
    st.write(f"المتوفر: {item['qty']}")

    if item["qty"] > 0:
        if st.button(f"أضف للسلة {i}"):
            st.session_state.cart.append(item)
            st.success("تمت الإضافة")
    else:
        st.error("غير متوفر")

    st.markdown("---")

# ---------- السلة ----------
st.header("🛍️ السلة")

total = 0
msg = ""

for item in st.session_state.cart:
    st.write(item["name"], "-", item["price"], "₪")
    total += item["price"]
    msg += f"{item['name']} - {item['price']} ₪\n"

st.write("المجموع:", total, "₪")

if st.button("إرسال الطلب واتساب"):
    link = f"https://wa.me/{WHATSAPP}?text={msg}"
    st.markdown(f"[اضغط للإرسال]({link})")

# ---------- دخول المدير ----------
query = st.query_params

if "admin" in query:
    st.sidebar.title("🔐 تسجيل دخول المدير")

    user = st.sidebar.text_input("اسم المستخدم")
    password = st.sidebar.text_input("كلمة المرور", type="password")

    if st.sidebar.button("دخول"):
        if user == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.admin = True
        else:
            st.error("خطأ")

# ---------- لوحة التحكم ----------
if st.session_state.get("admin"):

    st.sidebar.success("أنت مدير")

    st.sidebar.header("➕ إضافة منتج")

    name = st.sidebar.text_input("اسم المنتج")
    price = st.sidebar.number_input("السعر", 0)
    qty = st.sidebar.number_input("الكمية", 0)
    category = st.sidebar.text_input("القسم")
    image = st.sidebar.text_input("اسم الصورة (مثلاً cpu.png)")

    if st.sidebar.button("إضافة"):
        st.session_state.products.append({
            "name": name,
            "price": price,
            "qty": qty,
            "category": category,
            "image": image
        })
        st.success("تمت الإضافة")

    st.sidebar.header("❌ حذف منتج")

    delete_name = st.sidebar.selectbox("اختر منتج", [p["name"] for p in st.session_state.products])

    if st.sidebar.button("حذف"):
        st.session_state.products = [p for p in st.session_state.products if p["name"] != delete_name]
        st.success("تم الحذف")
