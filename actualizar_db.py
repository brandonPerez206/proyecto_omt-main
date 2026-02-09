import sqlite3

conn = sqlite3.connect('bitacoras.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accion TEXT NOT NULL,
    detalle TEXT,
    usuario_admin TEXT NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Tabla auditoria creada o ya existente")
