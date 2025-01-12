from flask import Blueprint, jsonify
from app.models import User

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    """
    Ruta principal que muestra un mensaje de bienvenida.
    """
    return "Welcome to Bounty Bug Project!"

@bp.route("/about")
def about():
    """
    Ruta para la página de información sobre el proyecto.
    """
    return "This is the About Page of Bounty Bug Project!"

@bp.route("/greet/<name>")
def greet(name):
    """
    Ruta dinámica que saluda al usuario.
    """
    if not name:
        return jsonify({"error": "Name is required"}), 400
    return f"Hello, {name}! Welcome to Bounty Bug Project!"

@bp.route("/users", methods=["GET"])
def get_users():
    """
    Recupera todos los usuarios de la base de datos y los devuelve en formato JSON.
    """
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found"}), 404

    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            for user in users
        ]
    }
from flask import request, jsonify
from app.models import User
from app import db

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=data["username"], email=data.get("email", ""))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": f"Welcome, {user.username}"}), 200
