import sqlite3

def init_db():
    conn = sqlite3.connect("cotizaciones.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            detalle TEXT,
            archivo TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_cotizacion(nombre, correo, detalle, archivo):
    conn = sqlite3.connect("cotizaciones.db")
    cursor = conn.cursor()
    archivo_nombre = archivo.name if archivo else None
    cursor.execute("INSERT INTO cotizaciones (nombre, correo, detalle, archivo) VALUES (?, ?, ?, ?)",
                   (nombre, correo, detalle, archivo_nombre))
    conn.commit()
    conn.close()
