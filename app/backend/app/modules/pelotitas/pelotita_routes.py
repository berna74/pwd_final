from flask import Blueprint
from app.modules.pelotitas.pelotita_controller import PelotitaController

pelotita_bp = Blueprint('pelotitas', __name__, url_prefix='/pelotitas')

pelotita_bp.route('/', methods=['GET'])(PelotitaController.index)
pelotita_bp.route('/<int:pelotita_id>', methods=['GET'])(PelotitaController.show)
pelotita_bp.route('/', methods=['POST'])(PelotitaController.store)
pelotita_bp.route('/<int:pelotita_id>', methods=['PUT'])(PelotitaController.update)
pelotita_bp.route('/<int:pelotita_id>', methods=['DELETE'])(PelotitaController.destroy)
pelotita_bp.route('/resumen', methods=['GET'])(PelotitaController.resumen)
