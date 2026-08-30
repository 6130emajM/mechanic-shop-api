from flask import Flask
from application.models import db
from application.extensions import ma, limiter, cache
from application.blueprints.customer import customer_bp
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.service_ticket import service_ticket_bp

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    return app
