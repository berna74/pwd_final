from flask import Blueprint, request, jsonify
from .categoria_controller import CategoriaController

categoria_bp = Blueprint('categorias', __name__)

@categoria_bp.route("/categorias/", methods=["GET"])
def get_all():
    try:
        categorias = CategoriaController.get_all()
        if categorias:
            return jsonify(categorias), 200
        else:
            return jsonify({'mensaje': 'no se encontraron categorías'}), 404
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@categoria_bp.route("/categorias/<int:id>", methods=["GET"])
def get_one(id):
    try:
        categoria = CategoriaController.get_one(id)
        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({'mensaje': 'no se encontró la categoría'}), 404
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@categoria_bp.route("/categorias/", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        print(f"DEBUG - Datos recibidos en crear categoria: {data}")
        if data is None:
            return jsonify({'mensaje': "no se recibieron datos"})
        result = CategoriaController.crear(data)
        if result:
            categorias = CategoriaController.get_all()
            return jsonify(categorias), 201
        else:
            return jsonify({'mensaje': 'error al crear la categoría'}), 500
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@categoria_bp.route("/categorias/<int:id>", methods=["PUT"])
def modificar(id):
    try:
        data = request.get_json()
        data['id'] = id
        result = CategoriaController.modificar(data)
        if result:
            return jsonify({'mensaje': 'categoría modificada correctamente'}), 200
        else:
            return jsonify({'mensaje': 'error al modificar la categoría'}), 500
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@categoria_bp.route("/categorias/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        result = CategoriaController.eliminar(id)
        if result:
            return jsonify({'mensaje': "categoría eliminada con éxito"})
        return jsonify({'mensaje': "error al eliminar la categoría"})
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"})