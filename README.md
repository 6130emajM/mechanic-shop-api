# Mechanic Shop API

A Flask REST API for managing a mechanic shop's customers, mechanics, and service tickets, built with SQLAlchemy (MySQL) and Marshmallow, using the Application Factory Pattern.

## Features
- Customer, Mechanic, and Service Ticket management (full CRUD)
- Many-to-many relationship between Service Tickets and Mechanics
- Application Factory Pattern with modular blueprints

## Setup
1. Clone this repo and cd into it
2. Create and activate a virtual environment: python3 -m venv venv && source venv/bin/activate
3. Install dependencies: pip install flask flask-sqlalchemy mysql-connector-python flask-marshmallow marshmallow-sqlalchemy
4. Create a MySQL database named mechanic_shop_db
5. Update the connection string in config.py with your own MySQL username/password
6. Run the app: python app.py
7. API available at http://127.0.0.1:5000

## Endpoints
- POST/GET /customers/, GET/PUT/DELETE /customers/<id>
- POST/GET /mechanics/, PUT/DELETE /mechanics/<id>
- POST/GET /service-tickets/
- PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>
- PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>
