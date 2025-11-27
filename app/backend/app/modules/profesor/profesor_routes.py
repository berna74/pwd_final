from flask import Blueprint
from .profesor_controller import ProfesorController

profesor_bp = Blueprint('profesores', __name__, url_prefix='/profesores')

profesor_bp.route('/', methods=['GET'])(ProfesorController.get_all)
profesor_bp.route('/<int:id>', methods=['GET'])(ProfesorController.get_by_id)
profesor_bp.route('/', methods=['POST'])(ProfesorController.create)
profesor_bp.route('/<int:id>', methods=['PUT'])(ProfesorController.update)
profesor_bp.route('/<int:id>', methods=['DELETE'])(ProfesorController.delete)
