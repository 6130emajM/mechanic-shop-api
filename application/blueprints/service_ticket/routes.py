from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.blueprints.service_ticket import service_ticket_bp
from application.models import db, ServiceTicket, Mechanic
from .schemas import service_ticket_schema, service_tickets_schema
from application.utils import token_required

@service_ticket_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_ticket_bp.route("/", methods=['GET'])
def get_service_tickets():
    tickets = db.session.execute(select(ServiceTicket)).scalars().all()
    return service_tickets_schema.jsonify(tickets)

@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found."}), 404
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found."}), 404
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    tickets = db.session.execute(
        select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    ).scalars().all()
    return service_tickets_schema.jsonify(tickets)


@service_ticket_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404

    data = request.json or {}
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:inventory_id>", methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    from application.models import Inventory
    ticket = db.session.get(ServiceTicket, ticket_id)
    item = db.session.get(Inventory, inventory_id)
    if not ticket or not item:
        return jsonify({"error": "Ticket or Inventory item not found."}), 404
    if item not in ticket.inventory_items:
        ticket.inventory_items.append(item)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200
