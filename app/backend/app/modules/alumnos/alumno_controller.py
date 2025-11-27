from flask import jsonify, request
from app.modules.alumnos.alumno_model import AlumnoModel

class AlumnoController:
    @staticmethod
    def get_all():
        alumnos = AlumnoModel.get_all()
        return jsonify(alumnos), 200

    @staticmethod
    def get_by_id(id):
        alumno = AlumnoModel.get_by_id(id)
        if alumno and 'mensaje' not in alumno:
            return jsonify(alumno), 200
        return jsonify({'mensaje': 'Alumno no encontrado'}), 404

    @staticmethod
    def create():
        data = request.json
        resultado = AlumnoModel.create(data)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 201
        return jsonify(resultado), 400

    @staticmethod
    def update(id):
        data = request.json
        resultado = AlumnoModel.update(id, data)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 200
        return jsonify(resultado), 400

    @staticmethod
    def delete(id):
        resultado = AlumnoModel.delete(id)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 200
        return jsonify(resultado), 400
