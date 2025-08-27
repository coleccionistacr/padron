import pandas as pd
import streamlit as st
from io import StringIO

# --- VALIDACIÓN DE ACCESO ---
st.set_page_config(page_title="Buscador de Padrón Electoral", page_icon="🗳️")
st.title("🔒 Acceso al Buscador de Padrón Electoral")

# Usuario y contraseña (personalizable)
USERNAME = "admin"
PASSWORD = "1234"

username = st.text_input("Usuario:")
password = st.text_input("Contraseña:", type="password")

if username != USERNAME or password != PASSWORD:
    st.warning("⚠️ Usuario o contraseña incorrectos.")
    st.stop()  # Detiene la app si no hay acceso

st.success("✅ Acceso concedido")

# --- CARGAR CSV ---
votantes = pd.read_csv("votantes.csv", sep=";")
centros = pd.read_csv("centros.csv", sep=";")

# Limpiar espacios en nombres de columnas
votantes.columns = votantes.columns.str.strip()
centros.columns = centros.columns.str.strip()

# --- UNIR TABLAS ---
padron_completo = pd.merge(votantes, centros, on="codigo_electoral", how="left")

# --- BÚSQUEDA ---
st.title("🗳️ Buscador de Padrón Electoral")
busqueda = st.text_input("Ingrese cédula o parte del nombre/apellido:")

if busqueda:
    busqueda = busqueda.lower()
    mask = (
        padron_completo["cedula"].astype(str).str.contains(busqueda) |
        padron_completo["nombre"].str.lower().str.contains(busqueda) |
        padron_completo["primer_apellido"].str.lower().str.contains(busqueda) |
        padron_completo["segundo_apellido"].str.lower().str.contains(busqueda)
    )
    resultado = padron_completo[mask]

    if not resultado.empty:
        st.success(f"✅ {len(resultado)} registro(s) encontrado(s):")
        for _, row in resultado.iterrows():
            st.markdown(
                f"""
                <div style='border:1px solid #4CAF50; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9fff9'>
                <strong>Cédula:</strong> {row['cedula']}<br>
                <strong>Nombre completo:</strong> {row['nombre']} {row['primer_apellido']} {row['segundo_apellido']}<br>
                <strong>Distrito:</strong> {row['distrito']}<br>
                <strong>Cantón:</strong> {row['canton']}<br>
                <strong>Provincia:</strong> {row['provincia']}
                </div>
                """, unsafe_allow_html=True
            )

        # --- BOTÓN PARA DESCARGAR RESULTADOS ---
        csv_buffer = StringIO()
        resultado.to_csv(csv_buffer, index=False, sep=';')
        st.download_button(
            label="📥 Descargar resultados en CSV",
            data=csv_buffer.getvalue(),
            file_name="resultados_padron.csv",
            mime="text/csv"
        )

    else:
        st.error("❌ No se encontró ningún registro.")
