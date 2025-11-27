from flask import request, jsonify
from .socio_model import SocioModel

class SocioController:
    @staticmethod
    def get_all():
        socios = SocioModel.get_all()
        return jsonify(socios), 200

    @staticmethod
    def get_by_id(id):
        socio = SocioModel.get_by_id(id)
        if socio:
            return jsonify(socio), 200
        return jsonify({'mensaje': 'Socio no encontrado'}), 404

    @staticmethod
    def create():
        data = request.get_json()
        result = SocioModel.create(data)
        if 'id' in result:
            return jsonify(result), 201
        return jsonify(result), 400

    @staticmethod
    def update(id):
        data = request.get_json()
        result = SocioModel.update(id, data)
        return jsonify(result), 200

    @staticmethod
    def delete(id):
        result = SocioModel.delete(id)
        return jsonify(result), 200
