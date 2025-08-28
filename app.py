import streamlit as st
import pandas as pd
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from db import init_db, get_cotizaciones, get_cotizacion_file
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # SSL por defecto

# Inicializar base de datos
init_db()

st.title("📧 Panel Comercial - Ludriel Logistic SAC")

menu = st.sidebar.selectbox("Menú", ["Enviar correos", "Ver cotizaciones"])

# ================== FUNCIÓN DE ENVÍO ==================
def send_mail(to_email, subject, body, pdf_path):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    # Cuerpo del correo
    msg.attach(MIMEText(body, "html"))

    # Adjuntar PDF
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
        pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", "attachment", filename="CartaPresentacion.pdf")
        msg.attach(pdf_attachment)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# ================== ENVIAR CORREOS ==================
if menu == "Enviar correos":
    st.subheader("📤 Envío de correos de presentación")

    uploaded_file = st.file_uploader("Sube tu lista de correos (CSV con columna 'email')", type=["csv"])
    subject = st.text_input("Asunto del correo", "Presentación de Ludriel Logistic SAC")
    mensaje = st.text_area("Mensaje de presentación (HTML o texto plano)")

    if uploaded_file and st.button("Enviar correos"):
        df = pd.read_csv(uploaded_file)
        for email in df["email"]:
            try:
                send_mail(email, subject, mensaje, "CARTA DE PRESETNACION.pdf")
                st.success(f"✅ Enviado a {email}")
            except Exception as e:
                st.error(f"❌ Error enviando a {email}: {e}")

# ================== VER COTIZACIONES ==================
if menu == "Ver cotizaciones":
    st.subheader("📑 Cotizaciones recibidas")

    rows = get_cotizaciones()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Nombre", "Email", "Cotización"])
        st.dataframe(df)

        selected_id = st.number_input("Ingrese el ID de la cotización para descargar el archivo:", min_value=1, step=1)
        if st.button("Descargar archivo"):
            file_bytes = get_cotizacion_file(selected_id)
            if file_bytes:
                st.download_button("Descargar Cotización", file_bytes, file_name=f"cotizacion_{selected_id}.pdf")
            else:
                st.warning("⚠️ Esta cotización no tiene archivo adjunto.")
    else:
        st.info("Aún no hay cotizaciones registradas.")
