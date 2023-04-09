from flask import Blueprint, request, jsonify
from app.models import User, UserRole
from app import db

bp = Blueprint('user', __name__, url_prefix='/users')

# Endpoint to get all non-deleted users


@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.filter_by(is_deleted=False).all()
    return jsonify([user.to_dict() for user in users])

# Endpoint to get a specific user by user_id


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_deleted:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

# Endpoint to create a new user


@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    is_valid, error_message = validate_user_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    user = User(
        name=data["name"],
        phone_number=data["phone_number"],
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

# Endpoint to update an existing user by user_id


@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_deleted:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    is_valid, error_message = validate_user_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    user.name = data["name"]
    user.phone_number = data["phone_number"]
    db.session.commit()

    return jsonify(user.to_dict())

# Endpoint to delete a user by user_id


@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_deleted:
        return jsonify({"error": "User not found"}), 404
    user.is_deleted = True
    db.session.commit()
    return jsonify({"message": "User deleted"})

# Endpoint to modify the user role for a specific user and shop


@bp.route('/<int:user_id>/roles', methods=['PUT'])
def modify_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_deleted:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    is_valid, error_message = validate_user_role_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    user_role = UserRole.query.filter_by(
        user_id=user_id, shop_id=data["shop_id"]).first()

    if not user_role:
        user_role = UserRole(
            user_id=user_id, shop_id=data["shop_id"], role=data["role"])
        db.session.add(user_role)
    else:
        user_role.role = data["role"]

    db.session.commit()

    return jsonify(user_role.to_dict())

# Validate user data for creation or update


def validate_user_data(data):
    if not data:
        return False, "No data provided"

    required_fields = ["name", "phone_number"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None


# Validate user role data for modification
def validate_user_role_data(data):
    if not data:
        return False, "No data provided"

    required_fields = ["shop_id", "role"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    if data["role"] not in ["staff", "admin"]:
        return False, "Invalid role value"

    return True, None
