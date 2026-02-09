import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for

auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/auditoria')

@auditoria_bp.route('/')
def ver_auditoria():
    if 'usuario' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('dashboard.dashboard'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute("""
        SELECT accion, detalle, usuario_admin, fecha, hora
        FROM auditoria
        ORDER BY id DESC
    """)
    acciones = c.fetchall()
    conn.close()

    return render_template('auditoria.html', acciones=acciones)

def registrar_accion(accion, detalle, usuario_admin):
    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    c.execute("""
        INSERT INTO auditoria (accion, detalle, usuario_admin, fecha, hora)
        VALUES (?, ?, ?, ?, ?)
    """, (accion, detalle, usuario_admin, fecha, hora))

    conn.commit()
    conn.close()
    

