from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash
from utils_auditoria import registrar_accion


usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/', methods=['GET', 'POST'])
def usuarios():
    if 'usuario' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('dashboard.dashboard'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        rol = request.form['rol']

        c.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        existe = c.fetchone()

        if existe:
            flash(f" El usuario '{usuario}' ya existe.", "warning")
        else:
            hashed_pass = generate_password_hash(password)
            c.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                      (usuario, hashed_pass, rol))
            conn.commit()
            flash(f" Usuario '{usuario}' creado exitosamente.", "success")

    c.execute("SELECT id, usuario, rol FROM usuarios")
    usuarios = c.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)


@usuarios_bp.route('/eliminar_usuario/<int:id>', methods=['POST'])

def eliminar_usuario(id):
    if 'usuario' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('dashboard.dashboard'))
    
    conn = sqlite3.connect('bitacoras.db')
    c.execute("SELECT usuario FROM usuarios WHERE id = ?", (id,))
    usuario_eliminado = c.fetchone()[0]
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    registrar_accion(
    accion="Eliminar usuario",
    detalle=f"Usuario eliminado: {usuario_eliminado}",
    usuario_admin=session['usuario']
)
    conn.commit()
    conn.close()

    flash("Usuario eliminado correctamente ", "success")
    return redirect(url_for('usuarios.usuarios'))


@usuarios_bp.route('/usuarios.cambiar_contrasena/<int:user_id>', methods=['GET', 'POST'])
def cambiar_contrasena(user_id):
    if 'usuario' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('dashboard.dashboard'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute("SELECT id, usuario FROM usuarios WHERE id = ?", (user_id,))
    user = c.fetchone()

    if not user:
        conn.close()
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('usuarios.usuarios'))

    if request.method == 'POST':
        nueva_pass = request.form.get('nueva_pass')
        confirmar_pass = request.form.get('confirmar_pass')

        if not nueva_pass or not confirmar_pass:
            flash("Debes completar ambos campos.", "warning")
        elif nueva_pass != confirmar_pass:
            flash("Las contraseñas no coinciden.", "danger")
        else:
            hashed_pass = generate_password_hash(nueva_pass)
            c.execute("UPDATE usuarios SET password = ? WHERE id = ?", (hashed_pass, user_id))
            conn.commit()
            flash(f"Contraseña actualizada para {user[1]}.", "success")
            conn.close()
            return redirect(url_for('usuarios.usuarios'))

    conn.close()
    return render_template('cambiar_contrasena.html', user=user)
