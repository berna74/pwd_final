from flask import jsonify, request
from app.modules.pagos.pago_model import PagoModel

class PagoController:
    @staticmethod
    def get_all():
        pagos = PagoModel.get_all()
        return jsonify(pagos), 200

    @staticmethod
    def get_by_id(id):
        pago = PagoModel.get_by_id(id)
        if pago and 'mensaje' not in pago:
            return jsonify(pago), 200
        return jsonify({'mensaje': 'Pago no encontrado'}), 404

    @staticmethod
    def create():
        data = request.json
        resultado = PagoModel.create(data)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 201
        return jsonify(resultado), 400

    @staticmethod
    def update(id):
        data = request.json
        resultado = PagoModel.update(id, data)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 200
        return jsonify(resultado), 400

    @staticmethod
    def delete(id):
        resultado = PagoModel.delete(id)
        if 'mensaje' in resultado and 'Error' not in resultado['mensaje']:
            return jsonify(resultado), 200
        return jsonify(resultado), 400
