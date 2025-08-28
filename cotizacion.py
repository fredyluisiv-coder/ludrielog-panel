import streamlit as st
from db import init_db, save_cotizacion

# Inicializar base de datos
init_db()

st.title("📑 Deja tu Cotización")
st.write("Por favor complete sus datos y adjunte su propuesta:")

# Campos de entrada
nombre = st.text_input("Nombre")
email = st.text_input("Correo electrónico")
cotizacion = st.text_area("Escriba aquí su cotización o propuesta")
archivo = st.file_uploader("Adjunte su archivo de cotización", type=["pdf", "docx"])

# Guardar cotización
if st.button("Enviar"):
    if nombre and email and cotizacion:
        archivo_bytes = archivo.read() if archivo else None
        save_cotizacion(nombre, email, cotizacion, archivo_bytes)
        st.success("✅ ¡Su cotización fue enviada correctamente!")
    else:
        st.error("⚠️ Complete todos los campos obligatorios (Nombre, Correo y Cotización).")
