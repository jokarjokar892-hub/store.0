import streamlit as st
import urllib.parse

st.set_page_config(page_title="متجري", layout="wide")

# إخفاء الترس
st.markdown("""
<style>
[data-testid="stToolbar"] {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== بيانات ==================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "products" not in st.session_state:
    st.session_state.products = [
        {"name": "Intel i5", "price": 500, "image": "cpu.jpg", "category": "معالج", "stock": 5},
        {"name": "RTX 3050", "price": 1100, "image": "gpu.jpg", "category": "كرت شاشة", "stock": 3}
    ]

# ================== واتساب ==================
def phone_format(p):
    if p.startswith("0"):
        return "970" + p[1:]
    return p

phone_number = phone_format("0515906039")

# ================== تسجيل دخول ==================
query = st.query_params

if query.get("admin") == "login":

    st.title("🔒 تسجيل دخول المدير")

    user = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if user == "محمد" and password == "7B4E9976D":
        st.session_state.admin = True
        st.success("تم الدخول")

    if st.session_state.get("admin"):

        st.title("🛠️ لوحة التحكم")

        # إضافة
        st.subheader("➕ إضافة منتج")
        name = st.text_input("اسم المنتج")
        price = st.number_input("السعر", 0)
        image = st.text_input("الصورة (رابط أو اسم ملف)")

        categories = ["كمبيوتر", "كرت شاشة", "معالج", "رام", "تخزين"]
        category = st.selectbox("القسم", categories)

        stock = st.number_input("الكمية", 0)

        if st.button("إضافة"):
            st.session_state.products.append({
                "name": name,
                "price": price,
                "image": image,
                "category": category,
                "stock": stock
            })
            st.success("تمت الإضافة")

        # حذف
        st.subheader("🗑️ حذف منتج")
        names = [p["name"] for p in st.session_state.products]
        selected = st.selectbox("اختر منتج", names)

        if st.button("حذف"):
            st.session_state.products = [p for p in st.session_state.products if p["name"] != selected]
            st.success("تم الحذف")

        # تعديل
        st.subheader("✏️ تعديل منتج")
        edit = st.selectbox("اختر للتعديل", names)

        for p in st.session_state.products:
            if p["name"] == edit:
                new_price = st.number_input("سعر جديد", p["price"])
                new_stock = st.number_input("كمية جديدة", p["stock"])

                if st.button("حفظ التعديل"):
                    p["price"] = new_price
                    p["stock"] = new_stock
                    st.success("تم التعديل")

        st.stop()

# ================== واجهة المستخدم ==================
st.title("🛒 المتجر")

search = st.text_input("🔎 بحث")

categories = ["الكل", "كمبيوتر", "كرت شاشة", "معالج", "رام", "تخزين"]
selected_cat = st.selectbox("📂 اختر قسم", categories)

cols = st.columns(3)

for i, p in enumerate(st.session_state.products):

    if search and search.lower() not in p["name"].lower():
        continue

    if selected_cat != "الكل" and p["category"] != selected_cat:
        continue

    with cols[i % 3]:

        st.markdown("<div style='border:1px solid #ddd;padding:10px;border-radius:10px;'>", unsafe_allow_html=True)

        # صورة
        if p["image"]:
            if p["image"].startswith("http"):
                st.markdown(f"""
                <div style="position:relative;">
                    <img src="{p['image']}" width="100%">
                    <div style="position:absolute;top:-10px;left:-10px;">🌙✨</div>
                    <div style="position:absolute;top:-10px;right:-10px;">⭐✨</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.image(p["image"], use_container_width=True)

        st.write(f"### {p['name']}")
        st.write(f"💰 {p['price']} ₪")
        st.write(f"📦 المتوفر: {p['stock']}")

        # السلة
        if st.button("🛒 أضف للسلة", key=f"cart{i}"):
            if p["stock"] > 0:
                st.session_state.cart.append(p)
                p["stock"] -= 1
                st.success("تمت الإضافة")
            else:
                st.error("غير متوفر")

        # روابط
        msg = urllib.parse.quote("مرحبا بدي طلب " + p["name"])
        link = f"https://wa.me/{phone_number}?text={msg}"

        st.markdown(f"""
        <a href="{link}">📞 واتساب</a>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ================== السلة ==================
st.subheader("🛒 السلة")

total = 0

for item in st.session_state.cart:
    st.write(item["name"], "-", item["price"], "₪")
    total += item["price"]

st.write("### الإجمالي:", total, "₪")

if st.session_state.cart:
    text = "طلب:\n"
    for item in st.session_state.cart:
        text += f"- {item['name']} ({item['price']}₪)\n"

    text += f"\nالإجمالي: {total}₪"

    link = f"https://wa.me/{phone_number}?text={urllib.parse.quote(text)}"

    st.markdown(f"<a href='{link}'>📦 إرسال الطلب واتساب</a>", unsafe_allow_html=True)
