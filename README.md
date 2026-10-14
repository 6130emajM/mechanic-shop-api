# Mechanic Shop API

A Flask REST API for managing a mechanic shop's customers, mechanics, and service tickets, built with SQLAlchemy (MySQL locally, PostgreSQL in production) and Marshmallow, using the Application Factory Pattern.

## Features
- Customer, Mechanic, and Service Ticket management (full CRUD)
- Many-to-many relationship between Service Tickets and Mechanics
- Application Factory Pattern with modular blueprints

## Setup
1. Clone this repo and cd into it
2. Create and activate a virtual environment: python3 -m venv venv && source venv/bin/activate
3. Install dependencies: pip install -r requirements.txt
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

## Live Deployment

- API: https://mechanic-shop-api-fqzh.onrender.com
- Swagger docs: https://mechanic-shop-api-fqzh.onrender.com/api/docs/
- Hosted on Render (web service plus managed PostgreSQL). The free instance sleeps when idle, so the first request can take about 50 seconds.

## Configuration

Set these environment variables (locally in a gitignored .env file, in production on Render):

- SQLALCHEMY_DATABASE_URI: database connection string
- SECRET_KEY: secret used to sign tokens

## Running Tests

    python -m unittest discover tests

## CI/CD Pipeline

GitHub Actions (.github/workflows/main.yaml) runs on every push to main:

1. build: installs dependencies
2. test: runs the unit test suite
3. deploy: triggers a Render deploy only if build and test pass (Render Auto-Deploy is turned off)

Required GitHub secrets: RENDER_API_KEY and SERVICE_ID.
