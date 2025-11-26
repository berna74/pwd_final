from flask import Blueprint, request, jsonify
from .articulo_controller import ArticuloController

articulos_bp=Blueprint("articulos", __name__)

@articulos_bp.route("/articulos/")
def get_all():
    try:
        articulos = ArticuloController.get_all()
        if articulos:
            return jsonify(articulos), 200
        else:
            return jsonify({'mensaje': 'no se encontraron artículos'}),404
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500
@articulos_bp.route("/articulos/<int:id>")
def get_one(id):
    try:
        articulo = ArticuloController.get_one(id)
        if articulo:
            return jsonify(articulo), 200
        else:
            return jsonify({'mensaje': 'no se encontro el artículo'}),404
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500
@articulos_bp.route("/articulos/", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        print(f"DEBUG - Datos recibidos en crear articulo: {data}")
        if data is None:
            return  jsonify({'mensaje': "no se recibieron datos"})
        result = ArticuloController.crear(data)
        if result:
            articulos = ArticuloController.get_all()
            return jsonify(articulos), 201
        else:
            return jsonify({'mensaje': 'error al crear un artículo'}),500
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500
    
@articulos_bp.route("/articulos/<int:id>", methods=["PUT"])
def modificar(id):
    try:
        data = request.get_json()
        data['id'] = id
        print(f"DEBUG - Datos recibidos en modificar articulo: {data}")
        result = ArticuloController.modificar(data)
        if result:
            articulos = ArticuloController.get_all()
            return jsonify(articulos), 200
        else:
            return jsonify({'mensaje': 'error al modificar un artículo'}),500
        
    except Exception as exc:
         return jsonify({'mensaje': f" error : {str(exc)}"}), 500

@articulos_bp.route("/articulos/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        print(f"DEBUG - Eliminando artículo con ID: {id}")
        result = ArticuloController.eliminar(id)
        if result:
            articulos = ArticuloController.get_all()
            return jsonify(articulos), 200
        return jsonify({'mensaje':"error al eliminar un artículo"}), 500
    except Exception as exc:
        return jsonify({'mensaje':f"error: {str(exc)}"}), 500
