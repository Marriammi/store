from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models.models import User

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/get_user_id', methods=['GET'])
@login_required
def get_user():
    if current_user.is_authenticated:
        user_id = current_user.user_id
        return jsonify({'user_id': user_id}), 200
    else:
        return jsonify({'error': 'User not authenticated'}), 401


@user_blueprint.route('/get_user_info', methods=['GET'])
@login_required
def get_user_information():
    if current_user.is_authenticated:
        user_info = {
            'username': current_user.username,
            'email': current_user.email,
            #'password': current_user.password
        }
        return jsonify(user_info), 200
    else:
        return jsonify({'error': 'User not authenticated'}), 401


@user_blueprint.route('/change_username', methods=['POST'])
@login_required
def change_username():
    data = request.get_json()
    new_username = data.get('newUsername')

    if not new_username:
        return jsonify({'error': 'New username is required'}), 401

    current_user.username = new_username
    db.session.commit()

    return jsonify({'message': 'Username changed successfully'}), 200

@user_blueprint.route('/change_email', methods=['POST'])
@login_required
def change_email():
    data = request.get_json()
    new_email = data.get('newEmail')

    if not new_email:
        return jsonify({'error': 'New email is required'}), 400

    current_user.email = new_email
    db.session.commit()

    return jsonify({'message': 'Email changed successfully'}), 200
