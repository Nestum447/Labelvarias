import streamlit as st
from PIL import Image
import easyocr

st.title("📋 Lector de etiquetas - Sin Tesseract")

# Crear lector (puedes poner ['en','es'] para inglés y español)
reader = easyocr.Reader(['en', 'es'], gpu=False)

uploaded_file = st.file_uploader("Sube una foto de la etiqueta", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

    # Convertir a RGB y pasar a numpy array
    import numpy as np
    img_array = np.array(image)

    # Leer texto
    result = reader.readtext(img_array)

    # Mostrar resultado
    if result:
        text = "\n".join([r[1] for r in result])
        st.subheader("Texto detectado:")
        st.text_area("Texto extraído", text, height=300)
    else:
        st.info("No se detectó texto en la imagen.")
