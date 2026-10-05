from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.blueprints.customer import customer_bp
from application.models import db, Customer
from .schemas import customer_schema, customers_schema, login_schema
from application.extensions import limiter 
from application.utils import encode_token
from application.utils import token_required

@customer_bp.route("/", methods=['POST'])
@limiter.limit("5 per hour")
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
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        customers = db.paginate(select(Customer), page=page, per_page=per_page)
        return customers_schema.jsonify(customers.items)
    except:
        customers = db.session.execute(select(Customer)).scalars().all()
        return customers_schema.jsonify(customers)

@customer_bp.route("/<int:id>", methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    return customer_schema.jsonify(customer), 200
@customer_bp.route("/<int:id>", methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    if int(customer_id) != id:
        return jsonify({"error": "You are not authorized to update this account."}), 403
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
@token_required
def delete_customer(customer_id, id):
    if int(customer_id) != id:
        return jsonify({"error": "You are not authorized to delete this account."}), 403
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer id: {id} successfully deleted."}), 200


@customer_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.execute(select(Customer).where(Customer.email == email)).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401
