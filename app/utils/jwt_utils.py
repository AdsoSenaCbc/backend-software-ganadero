import jwt
from flask import current_app, request, jsonify
from functools import wraps
from datetime import datetime, timedelta

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message": "Invalid token!"}), 401
        
        return f(*args, **kwargs)
    return decorated