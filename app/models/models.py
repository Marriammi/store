from app import db

class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def init(self, is_active=True):
        self.is_active = is_active

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

class Product(db.Model):
    __tablename__ = 'Products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    price = db.Column(db.Numeric(10, 2))
    quantity_available = db.Column(db.Integer)

class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'))
    status = db.Column(db.String)

    user = db.relationship('User', back_populates='orders')
    product = db.relationship('Product', back_populates='orders')

User.orders = db.relationship('Order', back_populates='user')
Product.orders = db.relationship('Order', back_populates='product')
