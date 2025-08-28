import streamlit as st
import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from db import init_db, save_cotizacion
import cotizacion  # Importa funciones de cotizacion.py

# Inicializar base de datos
init_db()

# ----------- PANEL COMERCIAL (enviar correos) -----------
def panel_comercial():
    st.title("📧 Panel Comercial - Ludriel Logistic SAC")
    st.subheader("📮 Envío de correos de presentación")

    file = st.file_uploader("Sube tu lista de correos (CSV con columna 'email')", type=["csv"])
    subject = st.text_input("Asunto del correo", "Presentación de Ludriel Logistic SAC")
    message = st.text_area("Mensaje de presentación (HTML o texto plano)")

    if st.button("Enviar correos"):
        if file is not None and message.strip():
            df = pd.read_csv(file)
            emails = df['email'].dropna().tolist()

            smtp_server = os.getenv("SMTP_SERVER")
            smtp_port = int(os.getenv("SMTP_PORT"))
            email_user = os.getenv("EMAIL_USER")
            email_pass = os.getenv("EMAIL_PASS")

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(email_user, email_pass)

                for e in emails:
                    msg = MIMEMultipart()
                    msg["From"] = email_user
                    msg["To"] = e
                    msg["Subject"] = subject

                    msg.attach(MIMEText(message, "html"))

                    # Adjuntar PDF
                    with open("CARTA DE PRESETNACION.pdf", "rb") as f:
                        attach = MIMEApplication(f.read(), _subtype="pdf")
                        attach.add_header("Content-Disposition", "attachment", filename="CARTA_DE_PRESENTACION.pdf")
                        msg.attach(attach)

                    server.sendmail(email_user, e, msg.as_string())
                    st.success(f"Correo enviado a {e}")
        else:
            st.error("Por favor sube un CSV y escribe un mensaje.")

# ----------- FORMULARIO DE COTIZACIÓN -----------
def formulario_cotizacion():
    st.title("📑 Formulario de Cotización - Ludriel Logistic SAC")

    nombre = st.text_input("Nombre completo")
    correo = st.text_input("Correo electrónico")
    detalle = st.text_area("Detalles de la carga")
    archivo = st.file_uploader("Adjuntar archivo de cotización (opcional)", type=["pdf", "xlsx", "docx"])

    if st.button("Enviar cotización"):
        if nombre and correo and detalle:
            save_cotizacion(nombre, correo, detalle, archivo)
            st.success("✅ Gracias, su cotización fue enviada correctamente.")
        else:
            st.error("Por favor complete todos los campos obligatorios.")

# ----------- LÓGICA PRINCIPAL -----------

# Detectar parámetros de la URL (?page=cotizacion)
query_params = st.query_params
path = query_params.get("page", [""])[0]

menu = st.sidebar.selectbox("Menú", ["Enviar correos", "Cotizaciones"])

if path == "cotizacion":
    # Forzar formulario de cotización si viene en la URL
    formulario_cotizacion()
elif menu == "Enviar correos":
    panel_comercial()
elif menu == "Cotizaciones":
    cotizacion.ver_cotizaciones()


