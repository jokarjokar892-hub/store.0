import streamlit as st
import urllib.parse

# ================== إعداد الصفحة ==================
st.set_page_config(page_title="متجري", layout="wide")

# ================== إخفاء الترس ==================
st.markdown("""
<style>
[data-testid="stToolbar"] {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== CSS تصميم ==================
st.markdown("""
<style>

.product {
    border:1px solid #ddd;
    padding:15px;
    border-radius:12px;
    text-align:center;
    background:#fff;
}

[data-theme="dark"] .product {
    background:#1e1e1e;
}

.decor {
    position:absolute;
    top:-10px;
    left:-10px;
    font-size:20px;
    z-index:999;
}

.decor2 {
    position:absolute;
    top:-10px;
    right:-10px;
    font-size:20px;
    z-index:999;
}

img {
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ================== إعدادات ==================
if "settings" not in st.session_state:
    st.session_state.settings = {
        "whatsapp": "0515906039",
        "facebook": "https://facebook.com/",
        "instagram": "https://instagram.com/"
    }

if "cart" not in st.session_state:
    st.session_state.cart = []

if "products" not in st.session_state:
    st.session_state.products = [
        {"name": "Intel i5", "price": 500, "image": "", "category": "كمبيوتر", "sale": False},
        {"name": "RTX 3050", "price": 1100, "image": "", "category": "كرت شاشة", "sale": True}
    ]

# ================== تحويل رقم ==================
def phone_format(p):
    if p.startswith("0"):
        return "970" + p[1:]
    return p

# ================== لوحة التحكم المخفية ==================
if "admin" in st.query_params:

    st.title("🔒 لوحة التحكم")

    name = st.text_input("اسم المنتج")
    price = st.number_input("السعر", 0)
    image = st.text_input("رابط الصورة")
    category = st.text_input("القسم")
    sale = st.checkbox("تخفيض")

    if st.button("➕ إضافة"):
        st.session_state.products.append({
            "name": name,
            "price": price,
            "image": image,
            "category": category,
            "sale": sale
        })
        st.success("تمت الإضافة")

    st.write("### المنتجات الحالية")
    st.write(st.session_state.products)

    st.stop()

# ================== الواجهة ==================
st.title("🛒 المتجر")

search = st.text_input("🔎 ابحث")

categories = list(set([p["category"] for p in st.session_state.products]))
selected_cat = st.selectbox("📂 اختر قسم", ["الكل"] + categories)

cols = st.columns(3)

for i, p in enumerate(st.session_state.products):

    if search and search.lower() not in p["name"].lower():
        continue

    if selected_cat != "الكل" and p["category"] != selected_cat:
        continue

    with cols[i % 3]:

        st.markdown(f"<div class='product'>", unsafe_allow_html=True)

        # صورة + ديكور
        if p["image"]:
            st.markdown(f"""
            <div style="position:relative;">
                <img src="{p['image']}" width="100%">
                <div class="decor">🌙✨</div>
                <div class="decor2">⭐✨</div>
            </div>
            """, unsafe_allow_html=True)

        st.write(f"### {p['name']}")
        st.write(f"💰 {p['price']} ₪")

        if p["sale"]:
            st.success("🔥 عرض خاص")

        # زر سلة
        if st.button("🛒 أضف للسلة", key=f"cart{i}"):
            st.session_state.cart.append(p)
            st.success("تمت الإضافة")

        # روابط
        phone = phone_format(st.session_state.settings["whatsapp"])
        msg = urllib.parse.quote("مرحبا بدي طلب " + p["name"])
        link = f"https://wa.me/{phone}?text={msg}"

        st.markdown(f"""
        <a href="{link}">📞 واتساب</a><br>
        <a href="{st.session_state.settings['facebook']}">📘 فيسبوك</a><br>
        <a href="{st.session_state.settings['instagram']}">📷 انستغرام</a>
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
    phone = phone_format(st.session_state.settings["whatsapp"])

    text = "طلب:\n"
    for item in st.session_state.cart:
        text += f"- {item['name']} ({item['price']}₪)\n"

    text += f"\nالإجمالي: {total}₪"

    link = f"https://wa.me/{phone}?text={urllib.parse.quote(text)}"

    st.markdown(f"<a href='{link}'>📦 إرسال الطلب كامل</a>", unsafe_allow_html=True)
