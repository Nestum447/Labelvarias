import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Lector de etiquetas múltiple", layout="wide")
st.title("📋 Lector de etiquetas - Varias imágenes y Excel")

# Crear lector EasyOCR (inglés y español)
reader = easyocr.Reader(['en', 'es'], gpu=False)

# Subir varias imágenes
uploaded_files = st.file_uploader(
    "Sube una o varias fotos de etiquetas",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    all_texts = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Imagen: {uploaded_file.name}", use_column_width=True)

        img_array = np.array(image)
        result = reader.readtext(img_array)

        # Extraer texto de la imagen
        text = "\n".join([r[1] for r in result]) if result else ""
        all_texts.append({"Archivo": uploaded_file.name, "Texto": text})

    # Crear DataFrame
    df = pd.DataFrame(all_texts)

    st.subheader("Texto detectado de todas las imágenes:")
    st.dataframe(df)

    # Descargar Excel
    output = BytesIO()
    df.to_excel(output, index=False)
    st.download_button(
        label="📥 Descargar Excel",
        data=output.getvalue(),
        file_name="textos_etiquetas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
