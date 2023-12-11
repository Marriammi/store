from flask import Blueprint, jsonify
from app.models.models import Product

prod = Blueprint('prod', __name__)

@prod.route('/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = [{'name': product.product_name, 'price': product.price, 'quantity': product.quantity_available, 'product_id': product.product_id} for product in products]
    return jsonify(products_list)