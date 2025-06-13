import streamlit as st
import qrcode
from PIL import Image
import io
import os

# Налаштування конфігурації
if os.path.exists('streamlit_config.toml'):
    st.set_page_config(
        page_title="QR Generator",
        page_icon="📱",
        layout="centered"
    )

# Ініціалізація станів
if 'url' not in st.session_state:
    st.session_state.url = ""
if 'show_qr' not in st.session_state:
    st.session_state.show_qr = False

st.title("📱 Генератор QR-кодів")
st.write("Введіть URL для створення QR-коду")

# Поле вводу
url = st.text_input("URL:", value=st.session_state.url, placeholder="https://example.com")

# Кнопка генерації
if st.button("🔄 Згенерувати QR-код"):
    if url:
        st.session_state.url = url
        st.session_state.show_qr = True
    else:
        st.warning("Будь ласка, введіть URL")

# Відображення QR-коду
if st.session_state.show_qr:
    # Створення QR-коду
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(st.session_state.url)
    qr.make(fit=True)
    
    # Створення зображення
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Зменшення розміру зображення
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    
    # Конвертація в байти для відображення
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Відображення QR-коду в колонці
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(img_byte_arr, caption="Ваш QR-код", width=200)
        
        # Кнопка для завантаження
        if st.download_button(
            label="📥 Завантажити QR-код",
            data=img_byte_arr,
            file_name="qr_code.png",
            mime="image/png"
        ):
            # Очищаємо все
            st.session_state.url = ""
            st.session_state.show_qr = False
            st.rerun()

# Інформація про програму
st.markdown("---")
st.markdown("""
### Як користуватися:
1. Введіть URL у поле вище
2. Натисніть кнопку "Згенерувати QR-код"
3. Натисніть кнопку "Завантажити" щоб зберегти QR-код
""") 