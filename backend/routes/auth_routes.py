from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Blueprint
auth_bp = Blueprint('auth', __name__)

# Secret key from .env
SECRET_KEY = os.getenv("SECRET_KEY")
from flask import current_app

SECRET_KEY = current_app.config["SECRET_KEY"]

# Temporary DB (replace with MongoDB later)
users_db = []

# -----------------------------
# TOKEN REQUIRED DECORATOR
# -----------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# -----------------------------
# SIGNUP
# -----------------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validation
    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    # Check user exists
    for user in users_db:
        if user['email'] == email:
            return jsonify({"error": "User already exists"}), 400

    # Hash password
    hashed_password = generate_password_hash(password)

    # Save user
    users_db.append({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Signup successful"}), 201


# -----------------------------
# LOGIN
# -----------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Find user
    user = None
    for u in users_db:
        if u['email'] == email:
            user = u
            break

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check password
    if not check_password_hash(user['password'], password):
        return jsonify({"error": "Wrong password"}), 401

    # Generate token
    token = jwt.encode({
        "email": user['email'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token
    })


# -----------------------------
# PROTECTED ROUTE
# -----------------------------
@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        "message": "Profile fetched",
        "user": current_user
    })