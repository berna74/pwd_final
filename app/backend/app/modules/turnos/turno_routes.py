from flask import Blueprint
from app.modules.turnos.turno_controller import TurnoController

turno_bp = Blueprint('turno_bp', __name__)

@turno_bp.route('/turnos/', methods=['GET'])
def get_all_turnos():
    return TurnoController.get_all()

@turno_bp.route('/turnos/<int:id>', methods=['GET'])
def get_turno(id):
    return TurnoController.get_by_id(id)

@turno_bp.route('/turnos/', methods=['POST'])
def create_turno():
    return TurnoController.create()

@turno_bp.route('/turnos/<int:id>', methods=['PUT'])
def update_turno(id):
    return TurnoController.update(id)

@turno_bp.route('/turnos/<int:id>', methods=['DELETE'])
def delete_turno(id):
    return TurnoController.delete(id)
