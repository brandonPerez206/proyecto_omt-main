import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_mail import Mail
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.registros_routes import registros_bp
from routes.usuarios_routes import usuarios_bp
from routes.historial_routes import historial_bp
from routes.setup_templates import ensure_templates_and_static

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

# Registrar blueprints
def register_routes(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registros_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(historial_bp)

register_routes(app)  

@app.route('/test')
def test():
    return "HTTPS funciona"

from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('dashboard.dashboard'))


app = Flask(__name__)

