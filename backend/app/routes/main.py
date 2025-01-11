from flask import Blueprint
from app.models import User

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return "Welcome to Bounty Bug Project!"
@bp.route("/about")
def about():
    return "This is the About Page of Bounty Bug Project!"
@bp.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}! Welcome to Bounty Bug Project!"
@bp.route("/users")
def get_users():
    users = User.query.all()
    return {"users": [{"id": user.id, "username": user.username, "email": user.email} for user in users]}
