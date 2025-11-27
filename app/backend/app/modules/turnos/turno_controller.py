from flask import jsonify, request
from app.modules.turnos.turno_model import TurnoModel

class TurnoController:
    @staticmethod
    def get_all():
        turnos = TurnoModel.get_all()
        return jsonify(turnos), 200

    @staticmethod
    def get_by_id(id):
        turno = TurnoModel.get_by_id(id)
        if turno:
            return jsonify(turno.serializar()), 200
        return jsonify({'mensaje': 'Turno no encontrado'}), 404

    @staticmethod
    def create():
        data = request.json
        resultado = TurnoModel.create(data)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 201
        return jsonify(resultado), 400

    @staticmethod
    def update(id):
        data = request.json
        resultado = TurnoModel.update(id, data)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 200
        return jsonify(resultado), 400

    @staticmethod
    def delete(id):
        resultado = TurnoModel.delete(id)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 200
        return jsonify(resultado), 400
