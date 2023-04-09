from flask import Blueprint, request, jsonify
from app.models import Shop, ShopHours, Product, Category
from app import db

bp = Blueprint('shop', __name__, url_prefix='/shops')


@bp.route('/', methods=['GET'])
def get_shops():
    shops = Shop.query.filter_by(is_deleted=False).all()
    return jsonify([shop.to_dict() for shop in shops])


@bp.route('/<int:shop_id>', methods=['GET'])
def get_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404
    return jsonify(shop.to_dict())


@bp.route('/', methods=['POST'])
def create_shop():
    data = request.get_json()
    is_valid, error_message = validate_shop_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    shop = Shop(
        name=data["name"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        phone_number=data["phone_number"],
    )
    db.session.add(shop)
    db.session.commit()

    return jsonify(shop.to_dict()), 201


@bp.route('/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404

    data = request.get_json()
    is_valid, error_message = validate_shop_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    shop.name = data["name"]
    shop.latitude = data["latitude"]
    shop.longitude = data["longitude"]
    shop.phone_number = data["phone_number"]
    db.session.commit()

    return jsonify(shop.to_dict())


@bp.route('/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404
    shop.is_deleted = True
    db.session.commit()
    return jsonify({"message": "Shop deleted"})


def validate_shop_data(data):
    if not data:
        return False, "No data provided"

    required_fields = ["name", "latitude", "longitude", "phone_number"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None


def validate_shop_hours_data(data):
    if not data:
        return False, "No data provided"

    required_fields = ["day_of_week", "open_time", "close_time"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None


@bp.route('/<int:shop_id>/hours', methods=['POST'])
def add_shop_hours(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404

    data = request.get_json()
    is_valid, error_message = validate_shop_hours_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    existing_hours = ShopHours.query.filter_by(
        shop_id=shop_id, day_of_week=data["day_of_week"]
    ).first()

    if existing_hours:
        return jsonify({"error": "Hours already exist for this day of the week"}), 400

    shop_hours = ShopHours(
        shop_id=shop_id,
        day_of_week=data["day_of_week"],
        open_time=data["open_time"],
        close_time=data["close_time"],
    )
    db.session.add(shop_hours)
    db.session.commit()

    return jsonify(shop_hours.to_dict()), 201


def validate_product_data(data):
    if not data:
        return False, "No data provided"

    required_fields = ["name", "amount", "price", "category_id"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None


@bp.route('/<int:shop_id>/products', methods=['POST'])
def create_product(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404

    data = request.get_json()
    is_valid, error_message = validate_product_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    product = Product(
        shop_id=shop_id,
        category_id=data["category_id"],
        name=data["name"],
        amount=data["amount"],
        price=data["price"],
    )
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@bp.route('/<int:shop_id>/products/<int:product_id>', methods=['PUT'])
def update_product(shop_id, product_id):
    product = Product.query.get_or_404(product_id)
    if product.shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404

    data = request.get_json()
    is_valid, error_message = validate_product_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    product.category_id = data["category_id"]
    product.name = data["name"]
    product.amount = data["amount"]
    product.price = data["price"]
    db.session.commit()

    return jsonify(product.to_dict())


@bp.route('/<int:shop_id>/products', methods=['GET'])
def list_products(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.is_deleted:
        return jsonify({"error": "Shop not found"}), 404

    products = Product.query.filter_by(shop_id=shop_id).all()
    return jsonify([product.to_dict() for product in products])


def validate_category_data(data):
    if not data:
        return False, "No data provided"

    required_fields = ["name"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None


@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    is_valid, error_message = validate_category_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    category = Category(
        name=data["name"],
    )
    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201


@bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])
