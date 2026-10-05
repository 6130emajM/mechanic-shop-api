from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.blueprints.inventory import inventory_bp
from application.models import db, Inventory
from .schemas import inventory_schema, inventories_schema

@inventory_bp.route("/", methods=['POST'])
def create_inventory_item():
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_item = Inventory(**data)
    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201

@inventory_bp.route("/", methods=['GET'])
def get_inventory_items():
    items = db.session.execute(select(Inventory)).scalars().all()
    return inventories_schema.jsonify(items)

@inventory_bp.route("/<int:id>", methods=['GET'])
def get_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    return inventory_schema.jsonify(item), 200

@inventory_bp.route("/<int:id>", methods=['PUT'])
def update_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return inventory_schema.jsonify(item), 200

@inventory_bp.route("/<int:id>", methods=['DELETE'])
def delete_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Inventory item id: {id} successfully deleted."}), 200
