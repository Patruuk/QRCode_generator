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

st.title("📱 Генератор QR-кодів")
st.write("Введіть URL для створення QR-коду і натисніть 'Enter'")

# Поле вводу
url = st.text_input("URL:", placeholder="https://example.com")

if url:
    # Створення QR-коду
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Створення зображення
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Конвертація в байти для відображення
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Відображення QR-коду
    st.image(img_byte_arr, caption="Ваш QR-код", use_container_width=True)
    
    # Кнопка для завантаження
    st.download_button(
        label="📥 Завантажити QR-код",
        data=img_byte_arr,
        file_name="qr_code.png",
        mime="image/png"
    )

# Інформація про програму
st.markdown("---")
st.markdown("""
### Як користуватися:
1. Введіть URL у поле вище
2. QR-код згенерується автоматично
3. Натисніть кнопку "Завантажити" щоб зберегти QR-код
""") 