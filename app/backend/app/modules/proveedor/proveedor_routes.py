from flask import Blueprint, request, jsonify
from .proveedor_controller import ProveedorController

proveedor_bp = Blueprint('proveedores', __name__)

@proveedor_bp.route("/proveedores/", methods=["GET"])
def get_all():
    try:
        proveedores = ProveedorController.get_all()
        if proveedores:
            return jsonify(proveedores), 200
        else:
            return jsonify({'mensaje': 'no se encontraron proveedores'}), 404
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@proveedor_bp.route("/proveedores/<int:id>", methods=["GET"])
def get_one(id):
    try:
        proveedor = ProveedorController.get_one(id)
        if proveedor:
            return jsonify(proveedor), 200
        else:
            return jsonify({'mensaje': 'no se encontró el proveedor'}), 404
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@proveedor_bp.route("/proveedores/", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        print(f"DEBUG - Datos recibidos en crear proveedor: {data}")
        if data is None:
            return jsonify({'mensaje': "no se recibieron datos"})
        result = ProveedorController.crear(data)
        if result:
            proveedores = ProveedorController.get_all()
            return jsonify(proveedores), 201
        else:
            return jsonify({'mensaje': 'error al crear el proveedor'}), 500
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@proveedor_bp.route("/proveedores/<int:id>", methods=["PUT"])
def modificar(id):
    try:
        data = request.get_json()
        data['id'] = id
        result = ProveedorController.modificar(data)
        if result:
            return jsonify({'mensaje': 'proveedor modificado correctamente'}), 200
        else:
            return jsonify({'mensaje': 'error al modificar el proveedor'}), 500
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"}), 500

@proveedor_bp.route("/proveedores/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        result = ProveedorController.eliminar(id)
        if result:
            return jsonify({'mensaje': "proveedor eliminado con éxito"})
        return jsonify({'mensaje': "error al eliminar el proveedor"})
    except Exception as exc:
        return jsonify({'mensaje': f"error: {str(exc)}"})