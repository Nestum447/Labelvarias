import streamlit as st
import easyocr
import pandas as pd
from io import BytesIO
from PIL import Image
import numpy as np

st.set_page_config(page_title="Extractor de texto rápido", layout="wide")
st.title("📋 Extracción rápida de texto de varias imágenes")

# Crear lector EasyOCR
reader = easyocr.Reader(['en','es'], gpu=False)

# Subir varias imágenes
uploaded_files = st.file_uploader(
    "Sube una o varias fotos de etiquetas",
    type=["jpg","jpeg","png"],
    accept_multiple_files=True
)

if uploaded_files:
    all_texts = []

    for uploaded_file in uploaded_files:
        # Abrir imagen
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # Extraer texto
        result = reader.readtext(img_array)
        text = "\n".join([r[1] for r in result]) if result else ""
        all_texts.append({"Archivo": uploaded_file.name, "Texto": text})

    # Crear DataFrame
    df = pd.DataFrame(all_texts)

    # Mostrar DataFrame en la app
    st.subheader("Texto extraído de las imágenes")
    st.dataframe(df)

    # Preparar Excel para descargar
    output = BytesIO()
    df.to_excel(output, index=False)
    st.download_button(
        label="📥 Descargar Excel con texto",
        data=output.getvalue(),
        file_name="textos_etiquetas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("Extracción completada. Puedes descargar el Excel.")

