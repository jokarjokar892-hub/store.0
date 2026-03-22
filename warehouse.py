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

# ================== CSS ==================
st.markdown("""
<style>

.product {
    border:1px solid #ddd;
    padding:15px;
    border-radius:12px;
    text-align:center;
    margin-bottom:20px;
}

.decor {
    position:absolute;
    top:-10px;
    left:-10px;
    font-size:20px;
}

.decor2 {
    position:absolute;
    top:-10px;
    right:-10px;
    font-size:20px;
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
        {"name": "Intel i5", "price": 500, "image": "", "category": "معالج", "sale": False},
        {"name": "RTX 3050", "price": 1100, "image": "", "category": "كرت شاشة", "sale": True}
    ]

# ================== تحويل رقم ==================
def phone_format(p):
    if p.startswith("0"):
        return "970" + p[1:]
    return p

# ================== لوحة تحكم مخفية ==================
if "admin" in st.query_params:

    st.title("🔒 لوحة التحكم")

    name = st.text_input("اسم المنتج")
    price = st.number_input("السعر", 0)
    image = st.text_input("رابط الصورة")

    categories = ["كمبيوتر", "كرت شاشة", "معالج", "رام", "تخزين"]
    category = st.selectbox("القسم", categories)

    sale = st.checkbox("تخفيض")

    if st.button("➕ إضافة منتج"):
        st.session_state.products.append({
            "name": name,
            "price": price,
            "image": image,
            "category": category,
            "sale": sale
        })
        st.success("تمت الإضافة")

    st.stop()

# ================== واجهة ==================
st.title("🛒 المتجر")

search = st.text_input("🔎 ابحث")

all_categories = ["الكل", "كمبيوتر", "كرت شاشة", "معالج", "رام", "تخزين"]
selected_cat = st.selectbox("📂 اختر قسم", all_categories)

cols = st.columns(3)

for i, p in enumerate(st.session_state.products):

    if search and search.lower() not in p["name"].lower():
        continue

    if selected_cat != "الكل" and p["category"] != selected_cat:
        continue

    with cols[i % 3]:

        st.markdown("<div class='product'>", unsafe_allow_html=True)

        # صورة + نجوم
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

        # زر سلة (مهم: key مختلف)
        if st.button("🛒 أضف للسلة", key=f"cart_{i}"):
            st.session_state.cart.append(p)
            st.success("تمت الإضافة للسلة")

        # واتساب
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
    name = item.get("name", "منتج")
    price = item.get("price", 0)

    st.write(name, "-", price, "₪")
    total += price

st.write("### الإجمالي:", total, "₪")

# إرسال الطلب
if st.session_state.cart:
    phone = phone_format(st.session_state.settings["whatsapp"])

    text = "طلب:\n"
    for item in st.session_state.cart:
        text += f"- {item.get('name')} ({item.get('price')}₪)\n"

    text += f"\nالإجمالي: {total}₪"

    link = f"https://wa.me/{phone}?text={urllib.parse.quote(text)}"

    st.markdown(f"<a href='{link}'>📦 إرسال الطلب كامل واتساب</a>", unsafe_allow_html=True)
