import streamlit as st
import pandas as pd
import sqlite3

# Función para leer cotizaciones desde la base de datos
def get_cotizaciones():
    conn = sqlite3.connect("cotizaciones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, correo, detalle, archivo FROM cotizaciones ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# Vista de cotizaciones en el panel
def ver_cotizaciones():
    st.title("📑 Cotizaciones Recibidas")

    data = get_cotizaciones()

    if len(data) == 0:
        st.info("⚠️ No hay cotizaciones registradas todavía.")
        return

    # Convertir a DataFrame para mostrar en tabla
    df = pd.DataFrame(data, columns=["ID", "Nombre", "Correo", "Detalle", "Archivo adjunto"])
    st.dataframe(df, use_container_width=True)

    # Descargar como CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar cotizaciones en CSV",
        csv,
        "cotizaciones.csv",
        "text/csv",
        key="download-csv"
    )

    # Descargar como Excel
    excel_file = df.to_excel("cotizaciones.xlsx", index=False)
    with open("cotizaciones.xlsx", "rb") as f:
        st.download_button(
            "⬇️ Descargar cotizaciones en Excel",
            f,
            "cotizaciones.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download-excel"
        )
