from flask import jsonify, request
from app.modules.pelotitas.pelotita_model import Pelotita

class PelotitaController:
    @staticmethod
    def index():
        try:
            pelotitas = Pelotita.get_all()
            return jsonify([p.to_dict() for p in pelotitas]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def show(pelotita_id):
        try:
            pelotita = Pelotita.get_by_id(pelotita_id)
            if pelotita:
                return jsonify(pelotita.to_dict()), 200
            return jsonify({'error': 'Pelotita no encontrada'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def store():
        try:
            data = request.get_json()
            
            # Validaciones
            required_fields = ['fecha', 'tipo', 'cantidad', 'precio_unitario']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'El campo {field} es requerido'}), 400
            
            if data['tipo'] not in ['compra', 'venta']:
                return jsonify({'error': 'El tipo debe ser compra o venta'}), 400
            
            # Calcular total
            data['total'] = float(data['cantidad']) * float(data['precio_unitario'])
            
            pelotita = Pelotita.create(data)
            return jsonify(pelotita.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(pelotita_id):
        try:
            data = request.get_json()
            
            # Validaciones
            required_fields = ['fecha', 'tipo', 'cantidad', 'precio_unitario']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'El campo {field} es requerido'}), 400
            
            if data['tipo'] not in ['compra', 'venta']:
                return jsonify({'error': 'El tipo debe ser compra o venta'}), 400
            
            # Calcular total
            data['total'] = float(data['cantidad']) * float(data['precio_unitario'])
            
            pelotita = Pelotita.update(pelotita_id, data)
            if pelotita:
                return jsonify(pelotita.to_dict()), 200
            return jsonify({'error': 'Pelotita no encontrada'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def destroy(pelotita_id):
        try:
            pelotita = Pelotita.get_by_id(pelotita_id)
            if not pelotita:
                return jsonify({'error': 'Pelotita no encontrada'}), 404
            
            Pelotita.delete(pelotita_id)
            return jsonify({'message': 'Pelotita eliminada exitosamente'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def resumen():
        try:
            resumen = Pelotita.get_resumen()
            return jsonify(resumen), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
