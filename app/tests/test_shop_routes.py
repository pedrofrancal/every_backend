import pytest
from app import create_app, db
from app.models import Shop, ShopHours, Product, Category


@pytest.fixture
def test_app():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    app_context = app.app_context()
    app_context.push()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

    app_context.pop()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

# Test create_shop


def test_create_shop(test_client):
    data = {
        "name": "Test Shop",
        "latitude": 10.0,
        "longitude": 10.0,
        "phone_number": "1234567890",
    }
    response = test_client.post("/shops/", json=data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data["name"] == "Test Shop"

    # Cleanup
    shop = Shop.query.get(json_data["id"])
    db.session.delete(shop)
    db.session.commit()

# Test update_shop


def test_update_shop(test_client):
    shop = Shop(name="Test Shop", latitude=10.0,
                longitude=10.0, phone_number="1234567890")
    db.session.add(shop)
    db.session.commit()

    update_data = {
        "name": "Updated Test Shop",
        "latitude": 20.0,
        "longitude": 20.0,
        "phone_number": "0987654321",
    }
    response = test_client.put(f"/shops/{shop.id}", json=update_data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["name"] == "Updated Test Shop"

    # Cleanup
    db.session.delete(shop)
    db.session.commit()

# Test delete_shop


def test_delete_shop(test_client):
    shop = Shop(name="Test Shop", latitude=10.0,
                longitude=10.0, phone_number="1234567890")
    db.session.add(shop)
    db.session.commit()

    response = test_client.delete(f"/shops/{shop.id}")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["message"] == "Shop deleted"

    # Cleanup
    shop.is_deleted = False
    db.session.commit()

# Test add_shop_hours


def test_add_shop_hours(test_client):
    shop = Shop(name="Test Shop", latitude=10.0,
                longitude=10.0, phone_number="1234567890")
    db.session.add(shop)
    db.session.commit()

    data = {
        "day_of_week": 1,
        "open_time": "9:00",
        "close_time": "18:00",
    }
    response = test_client.post(f"/shops/{shop.id}/hours", json=data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data["day_of_week"] == 1
    assert json_data["open_time"] == "9:00"
    assert json_data["close_time"] == "18:00"

    # Cleanup
    shop_hours = ShopHours.query.get(json_data["id"])
    db.session.delete(shop_hours)
    db.session.delete(shop)
    db.session.commit()

# Test create_product


def test_create_product(test_client):
    shop = Shop(name="Test Shop", latitude=10.0,
                longitude=10.0, phone_number="1234567890")
    db.session.add(shop)
    db.session.commit()

    category = Category(name="Test Category")
    db.session.add(category)
    db.session.commit()

    data = {
        "category_id": category.id,
        "name": "Test Product",
        "amount": 100,
        "price": 9.99,
    }
    response = test_client.post(f"/shops/{shop.id}/products", json=data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data["name"] == "Test Product"

    # Cleanup
    product = Product.query.get(json_data["id"])
    db.session.delete(product)
    db.session.delete(category)
    db.session.delete(shop)
    db.session.commit()


# Test update_product
def test_update_product(test_client):
    shop = Shop(name="Test Shop", latitude=10.0,
                longitude=10.0, phone_number="1234567890")
    db.session.add(shop)
    db.session.commit()

    category = Category(name="Test Category")
    db.session.add(category)
    db.session.commit()

    product = Product(shop_id=shop.id, category_id=category.id,
                      name="Test Product", amount=100, price=9.99)
    db.session.add(product)
    db.session.commit()

    update_data = {
        "category_id": category.id,
        "name": "Updated Test Product",
        "amount": 50,
        "price": 14.99,
    }
    response = test_client.put(
        f"/shops/{shop.id}/products/{product.id}", json=update_data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["name"] == "Updated Test Product"

    # Cleanup
    db.session.delete(product)
    db.session.delete(category)
    db.session.delete(shop)
    db.session.commit()


# Test list_products
def test_list_products(test_client):
    shop = Shop(name="Test Shop", latitude=10.0,
                longitude=10.0, phone_number="1234567890")
    db.session.add(shop)
    db.session.commit()

    category = Category(name="Test Category")
    db.session.add(category)
    db.session.commit()

    product = Product(shop_id=shop.id, category_id=category.id,
                      name="Test Product", amount=100, price=9.99)
    db.session.add(product)
    db.session.commit()

    response = test_client.get(f"/shops/{shop.id}/products")
    json_data = response.get_json()

    assert response.status_code == 200
    assert len(json_data) == 1
    assert json_data[0]["name"] == "Test Product"

    # Cleanup
    db.session.delete(product)
    db.session.delete(category)
    db.session.delete(shop)
    db.session.commit()
