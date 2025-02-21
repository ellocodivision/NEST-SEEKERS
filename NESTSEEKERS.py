import streamlit as st
import pandas as pd

# Configurar la página sin barra lateral
st.set_page_config(page_title="📊 Visualización de Excel", layout="wide", initial_sidebar_state="collapsed")

# 📌 Función para cargar datos desde Google Drive
@st.cache_data
def load_data():
    URL = "https://drive.google.com/uc?export=download&id=16TiwCLni53qDo9UnB0LyFRAq3tmfiCe8"
    df = pd.read_excel(URL, engine='openpyxl', dtype=str)

    # 📌 Seleccionar solo las columnas A-J (asumiendo que son las primeras 10 columnas)
    df = df.iloc[:, :10]

    # 📌 Reemplazar valores "nan" con vacío en LOCK OFF y PH
    columnas_a_limpiar = ["LOCK OFF", "PH"]
    for col in columnas_a_limpiar:
        if col in df.columns:
            df[col] = df[col].fillna("")  # Si hay NaN, se reemplaza por vacío

    # 📌 Formatear la columna de precios con símbolo de dólar
    if "PRECIO" in df.columns:
        df["PRECIO"] = df["PRECIO"].astype(float).apply(lambda x: f"${x:,.2f}")

    # 📌 Convertir la columna "DRIVE" en enlaces clickeables
    if "DRIVE" in df.columns:
        df["DRIVE"] = df["DRIVE"].apply(
            lambda x: f'<a href="{x}" target="_blank">🔗 Click Drive</a>' if pd.notna(x) else "No disponible"
        )

    return df

# 📌 Cargar datos
df = load_data()

# 📌 Si el DataFrame está vacío, detener la ejecución
if df.empty:
    st.error("⚠️ ERROR: No se pudieron cargar los datos.")
    st.stop()

# 📌 Filtros
st.write("📍 **Ubicación**")
selected_ubicacion = st.selectbox("", ["Todos"] + list(df["UBICACIÓN"].unique()))

st.write("🛏 **Recámaras**")
selected_recamaras = st.selectbox("", ["Todos"] + list(df["RECAMARAS"].unique()))

# 📌 Aplicar filtros
filtered_df = df.copy()
if selected_ubicacion != "Todos":
    filtered_df = filtered_df[filtered_df["UBICACIÓN"] == selected_ubicacion]
if selected_recamaras != "Todos":
    filtered_df = filtered_df[filtered_df["RECAMARAS"] == selected_recamaras]

# 📌 Mostrar tabla con datos filtrados
st.write("## Datos Filtrados del Excel")
st.markdown(
    filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True
)
