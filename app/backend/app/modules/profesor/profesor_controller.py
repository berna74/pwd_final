from flask import request, jsonify
from .profesor_model import ProfesorModel

class ProfesorController:
    @staticmethod
    def get_all():
        profesores = ProfesorModel.get_all()
        return jsonify(profesores), 200

    @staticmethod
    def get_by_id(id):
        profesor = ProfesorModel.get_by_id(id)
        if profesor:
            return jsonify(profesor.serializar()), 200
        return jsonify({'mensaje': 'Profesor no encontrado'}), 404

    @staticmethod
    def create():
        data = request.get_json()
        result = ProfesorModel.create(data)
        if 'id' in result:
            return jsonify(result), 201
        return jsonify(result), 400

    @staticmethod
    def update(id):
        data = request.get_json()
        result = ProfesorModel.update(id, data)
        return jsonify(result), 200

    @staticmethod
    def delete(id):
        result = ProfesorModel.delete(id)
        return jsonify(result), 200
