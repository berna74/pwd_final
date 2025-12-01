from flask import Flask
from flask_cors import CORS
from .modules.socios.socio_routes import socios_bp
from .modules.categoria.categoria_routes import categoria_bp
from .modules.turnos.turno_routes import turno_bp
from .modules.profesor.profesor_routes import profesor_bp
from .modules.alumnos.alumno_routes import alumno_bp
from .modules.pagos.pago_routes import pago_bp
from .modules.pelotitas.pelotita_routes import pelotita_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(socios_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(turno_bp)
    app.register_blueprint(profesor_bp)
    app.register_blueprint(alumno_bp)
    app.register_blueprint(pago_bp)
    app.register_blueprint(pelotita_bp)
    return app