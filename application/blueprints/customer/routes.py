from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.blueprints.customer import customer_bp
from application.models import db, Customer
from .schemas import customer_schema, customers_schema

@customer_bp.route("/", methods=['POST'])
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing = db.session.execute(select(Customer).where(Customer.email == data['email'])).scalars().all()
    if existing:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customer_bp.route("/", methods=['GET'])
def get_customers():
    customers = db.session.execute(select(Customer)).scalars().all()
    return customers_schema.jsonify(customers)

@customer_bp.route("/<int:id>", methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    return customer_schema.jsonify(customer), 200

@customer_bp.route("/<int:id>", methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customer_bp.route("/<int:id>", methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer id: {id} successfully deleted."}), 200
