import sqlite3

DB_NAME = "cotizaciones.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cotizaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        cotizacion TEXT,
        archivo BLOB
    )
    """)
    conn.commit()
    conn.close()

def save_cotizacion(nombre, email, cotizacion, archivo_bytes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cotizaciones (nombre, email, cotizacion, archivo) VALUES (?, ?, ?, ?)",
                   (nombre, email, cotizacion, archivo_bytes))
    conn.commit()
    conn.close()

def get_cotizaciones():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, cotizacion FROM cotizaciones")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_cotizacion_file(cotizacion_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT archivo FROM cotizaciones WHERE id=?", (cotizacion_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
