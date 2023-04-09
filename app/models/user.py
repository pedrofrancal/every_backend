from app import db

# Define the User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    # Define relationship
    roles = db.relationship('UserRole', back_populates='user')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "is_deleted": self.is_deleted
        }


# Define the UserRole model


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'staff' or 'admin'

    # Define relationships
    user = db.relationship('User', backref='user_roles')
    shop = db.relationship('Shop', backref='shop_roles')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shop_id": self.shop_id,
            "role": self.role
        }
