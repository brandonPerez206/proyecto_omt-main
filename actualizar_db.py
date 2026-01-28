import sqlite3

conn = sqlite3.connect('bitacoras.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS subcategoria4 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Tabla subcategorias creada correctamente")
