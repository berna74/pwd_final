from flask import Blueprint
from app.modules.pagos.pago_controller import PagoController

pago_bp = Blueprint('pago_bp', __name__)

@pago_bp.route('/pagos/', methods=['GET'])
def get_all_pagos():
    return PagoController.get_all()

@pago_bp.route('/pagos/<int:id>', methods=['GET'])
def get_pago(id):
    return PagoController.get_by_id(id)

@pago_bp.route('/pagos/', methods=['POST'])
def create_pago():
    return PagoController.create()

@pago_bp.route('/pagos/<int:id>', methods=['PUT'])
def update_pago(id):
    return PagoController.update(id)

@pago_bp.route('/pagos/<int:id>', methods=['DELETE'])
def delete_pago(id):
    return PagoController.delete(id)
