from app import db

# Define the Shop model


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    # Define relationships
    hours = db.relationship('ShopHours', backref='shop', lazy=True)
    roles = db.relationship('UserRole', back_populates='shop')
    products = db.relationship('Product', back_populates='shop', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone_number": self.phone_number,
            "is_deleted": self.is_deleted
        }

# Define the ShopHours model


class ShopHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False, unique=True)
    open_time = db.Column(db.String(5), nullable=False)
    close_time = db.Column(db.String(5), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "shop_id": self.shop_id,
            "day_of_week": self.day_of_week,
            "open_time": self.open_time,
            "close_time": self.close_time
        }

# Define the Category model


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Define relationship
    products = db.relationship('Product', back_populates='category', lazy=True)

    # Method to return dictionary representation of the category
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Define the Product model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define relationships
    shop = db.relationship('Shop', back_populates='products')
    category = db.relationship('Category', back_populates='products')

    # Method to return dictionary representation of the product
    def to_dict(self):
        return {
            "id": self.id,
            "shop_id": self.shop_id,
            "category_id": self.category_id,
            "name": self.name,
            "amount": self.amount,
            "price": self.price
        }
