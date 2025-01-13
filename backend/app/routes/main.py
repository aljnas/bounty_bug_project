from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


bp = Blueprint("main", __name__)

# Rutas informativas
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

from flask_jwt_extended import jwt_required

@bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """
    Recupera todos los usuarios de la base de datos solo si el token es válido.
    """
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found"}), 404

    return {
        "users": [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]
    }


# Rutas para autenticación
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(username=data["username"], email=data.get("email", ""))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/login_basic', methods=['POST'])  # RENOMBRADO
def login_basic():
    """
    Login básico sin token. Renombrado para evitar conflicto de endpoint
    """
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": f"Welcome, {user.username}"}), 200

@bp.route('/login_with_token', methods=['POST'])
def login_with_token():
    """
    Login que genera un token JWT
    """
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

@bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful"}), 200

@bp.route('/protected', methods=['GET'])
@jwt_required()  # Decorador que asegura que esta ruta requiere autenticación
def protected():
    """
    Ruta protegida que requiere un token JWT válido para acceder.
    """
    current_user = get_jwt_identity()  # Obtiene la identidad del usuario desde el token
    return jsonify({"message": f"Welcome to the protected route, user {current_user}!"}), 200
