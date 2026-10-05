from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from flask import current_app, request, jsonify
from functools import wraps

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

from functools import wraps
from flask import request, jsonify
from jose import JWTError

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split()[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            customer_id = data['sub']
        except JWTError:
            return jsonify({"error": "Token is invalid or expired"}), 401

        return f(customer_id, *args, **kwargs)
    return decorated
