import pandas as pd
import streamlit as st

# --- Cargar las dos tablas usando punto y coma ---
votantes = pd.read_csv("votantes.csv", sep=";")
centros = pd.read_csv("centros.csv", sep=";")

# --- Limpiar espacios en los nombres de columnas (opcional, pero recomendado) ---
votantes.columns = votantes.columns.str.strip()
centros.columns = centros.columns.str.strip()

# --- Unirlas por el campo 'codigo_electoral' ---
padron_completo = pd.merge(votantes, centros, on="codigo_electoral", how="left")

# --- Interfaz ---
st.title("🗳️ Buscador de Padrón Electoral")

cedula = st.text_input("Digite el número de cédula:")

if cedula:
    resultado = padron_completo[padron_completo["cedula"].astype(str) == cedula]
    if not resultado.empty:
        st.success("✅ Registro encontrado:")
        for _, row in resultado.iterrows():
            st.write(f"**Cédula:** {row['cedula']}")
            st.write(f"**Nombre completo:** {row['nombre']} {row['primer_apellido']} {row['segundo_apellido']}")
            st.write(f"**Distrito:** {row['distrito']}")
            st.write(f"**Cantón:** {row['canton']}")
            st.write(f"**Provincia:** {row['provincia']}")
    else:
        st.error("❌ No se encontró un votante con esa cédula.")
