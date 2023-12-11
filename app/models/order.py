from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models.models import Product, Order

order_blueprint = Blueprint('order_blueprint', __name__)

@order_blueprint.route('/place_order', methods=['POST'])
@login_required
def place_order():
    # Отримайте дані замовлення, включаючи product_id та кількість units
    data = request.get_json()
    product_id = data.get('product_id')  # Змінив на product_id
    units = data.get('units')

    # Знайдіть товар в базі даних
    product = Product.query.get(product_id)

    # Перевірте, чи доступна достатня кількість товару
    if product and product.quantity_available >= units:
        # Оновіть кількість доступних і проданих одиниць товару
        product.quantity_available -= units

        # Створіть новий запис у таблиці Orders
        order = Order(user_id=current_user.user_id, product_id=product_id, status='Accepted')
        db.session.add(order)
        db.session.commit()

        return jsonify({'message': 'Order placed successfully'}), 201
    else:
        return jsonify({'error': 'Not enough stock available'}), 400


@order_blueprint.route('/get_user_orders', methods=['GET'])
@login_required
def get_orders():
    try:
        # Assuming you have a relationship between User and Order models
        user_id = current_user.user_id
        user_orders = Order.query.filter_by(user_id=user_id).all()

        orders_data = []

        for order in user_orders:
            prod_name = Product.query.get(order.product_id).product_name
            orders_data.append({'order_id': order.order_id, 'name': prod_name, 'status': order.status})

        return jsonify({'orders': orders_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@order_blueprint.route('/delete_order/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    try:
        # Find the order by ID
        order = Order.query.get(order_id)

        # If order not found or does not belong to the current user, return an error
        if not order or order.user_id != current_user.user_id:
            return jsonify({'error': 'Order not found or unauthorized'}), 403

        # Find the associated product
        product = Product.query.get(order.product_id)

        # Increase the quantity in the Product table
        if product:
            product.quantity_available += 1
            db.session.delete(order)  # Delete the order
            db.session.commit()

            return jsonify({'message': 'Order deleted successfully'}), 200
        else:
            return jsonify({'error': 'Associated product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500