from flask import Blueprint
from app.modules.alumnos.alumno_controller import AlumnoController

alumno_bp = Blueprint('alumno_bp', __name__)

@alumno_bp.route('/alumnos/', methods=['GET'])
def get_all_alumnos():
    return AlumnoController.get_all()

@alumno_bp.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    return AlumnoController.get_by_id(id)

@alumno_bp.route('/alumnos/', methods=['POST'])
def create_alumno():
    return AlumnoController.create()

@alumno_bp.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    return AlumnoController.update(id)

@alumno_bp.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    return AlumnoController.delete(id)
