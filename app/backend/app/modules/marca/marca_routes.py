from flask import Blueprint, request, jsonify
from .marca_controller import MarcaController

marca_bp=Blueprint("marcas", __name__)

@marca_bp.route("/marcas/")
def get_all():
    try:
        marcas = MarcaController.get_all()
        if marcas:
            return jsonify(marcas), 200
        else:
            return jsonify({'mensaje': 'no se encontraron marcas'}),404
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500
@marca_bp.route("/marcas/<int:id>")
def get_one(id):
    try:
        marca = MarcaController.get_one(id)
        if marca:
            return jsonify(marca), 200
        else:
            return jsonify({'mensaje': 'no se encontro la marca'}),404
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500
@marca_bp.route("/marcas/", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        if data is None:
            return  jsonify({'mensaje': "no se recibieron datos"})
        result = MarcaController.crear(data)
        if result:
            marcas = MarcaController.get_all()
            return jsonify(marcas), 201
        else:
            return jsonify({'mensaje': 'error al crear una marca'}),500
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500
    
@marca_bp.route("/marcas/<int:id>", methods=["PUT"])
def modificar(id):
    try:
        data = request.get_json()
        data['id'] = id
        result = MarcaController.modificar(data)
        if result:
            marcas = MarcaController.get_all()
            return jsonify(marcas), 200
        else:
            return jsonify({'mensaje': 'error al modificar una marca'}),500
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500

@marca_bp.route("/marcas/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        result = MarcaController.eliminar(id)
        if result:
            marcas = MarcaController.get_all()
            return jsonify(marcas), 200
        return jsonify({'mensaje':"error al eliminar una marca"})
    except Exception as exc:
        return jsonify({'mensaje':f"error str{exc}"})
