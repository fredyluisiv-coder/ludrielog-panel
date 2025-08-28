import streamlit as st
import pandas as pd
import sqlite3
import io

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
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Cotizaciones")
    excel_data = output.getvalue()

    st.download_button(
        "⬇️ Descargar cotizaciones en Excel",
        excel_data,
        "cotizaciones.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download-excel"
    )
