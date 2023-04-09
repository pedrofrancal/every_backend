import pytest
from app import create_app, db
from app.models import User, UserRole, Shop

# Define a fixture to create a test app and set the app context


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

# Define a fixture to create a test client for sending requests


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


def test_get_users(test_client):
    # Add test users to the database
    user1 = User(name="Test User 1", phone_number="1234567890")
    user2 = User(name="Test User 2", phone_number="2345678901")
    user3 = User(name="Test User 3",
                 phone_number="3456789012", is_deleted=True)

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Send a GET request to the /users/ endpoint
    response = test_client.get('/users/')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response contains the expected users
    users = response.get_json()
    assert len(users) == 2
    assert users[0]['name'] == "Test User 1"
    assert users[1]['name'] == "Test User 2"


def test_get_user(test_client):
    # Add a test user to the database
    user = User(name="Test User", phone_number="1234567890")
    db.session.add(user)
    db.session.commit()

    # Send a GET request to the /users/<user_id> endpoint
    response = test_client.get(f'/users/{user.id}')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response contains the expected user
    returned_user = response.get_json()
    assert returned_user['name'] == "Test User"
    assert returned_user['phone_number'] == "1234567890"


def test_create_user(test_client):
    # Prepare user data
    user_data = {"name": "New User", "phone_number": "1234567890"}

    # Send a POST request to the /users/ endpoint
    response = test_client.post('/users/', json=user_data)

    # Check if the response status code is 201 (Created)
    assert response.status_code == 201

    # Check if the user was created in the database
    new_user = User.query.filter_by(name="New User").first()
    assert new_user is not None
    assert new_user.phone_number == "1234567890"


def test_update_user(test_client):
    # Add a test user to the database
    user = User(name="Test User", phone_number="1234567890")
    db.session.add(user)
    db.session.commit()

    # Prepare updated user data
    updated_data = {"name": "Updated User", "phone_number": "0987654321"}

    # Send a PUT request to the /users/<user_id> endpoint
    response = test_client.put(f'/users/{user.id}', json=updated_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user was updated in the database
    updated_user = User.query.get(user.id)
    assert updated_user.name == "Updated User"
    assert updated_user.phone_number == "0987654321"


def test_delete_user(test_client):
    # Add a test user to the database
    user = User(name="Test User", phone_number="1234567890")
    db.session.add(user)
    db.session.commit()

    # Send a DELETE request to the /users/<user_id> endpoint
    response = test_client.delete(f'/users/{user.id}')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user is marked as deleted in the database
    deleted_user = User.query.get(user.id)
    assert deleted_user.is_deleted


def test_modify_user_role(test_client):
    # Add test user and shop to the database
    user = User(name="Test User", phone_number="1234567890")
    shop = Shop(name="Test Shop", latitude=0.0,
                longitude=0.0, phone_number="0987654321")
    db.session.add_all([user, shop])
    db.session.commit()

    # Prepare user role data
    user_role_data = {"shop_id": shop.id, "role": "staff"}

    # Send a PUT request to the /users/<user_id>/roles endpoint
    response = test_client.put(f'/users/{user.id}/roles', json=user_role_data)
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user role was created in the database
    user_role = UserRole.query.filter_by(
        user_id=user.id, shop_id=shop.id).first()
    assert user_role is not None
    assert user_role.role == "staff"
