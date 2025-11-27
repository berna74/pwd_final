from flask import Blueprint
from .socio_controller import SocioController

socios_bp = Blueprint('socios', __name__, url_prefix='/socios')

socios_bp.route('/', methods=['GET'])(SocioController.get_all)
socios_bp.route('/<int:id>', methods=['GET'])(SocioController.get_by_id)
socios_bp.route('/', methods=['POST'])(SocioController.create)
socios_bp.route('/<int:id>', methods=['PUT'])(SocioController.update)
socios_bp.route('/<int:id>', methods=['DELETE'])(SocioController.delete)
