from flask import Flask, render_template, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@127.0.0.1:5436/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from app.models.models import User, Product, Order

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and session.get('is_admin', False)

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and session.get('is_admin', False)

admin = Admin(app, name='Store', template_mode='bootstrap4', index_view=CustomAdminIndexView())
admin.add_view(ModelView(User, db.session, name='Users'))
admin.add_view(ModelView(Product, db.session, name='Products'))
admin.add_view(ModelView(Order, db.session, name='Orders'))


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/start-page')
@login_required
def start():
    return render_template('start.html')

@app.route('/start-account_page')
@login_required
def account_page():
    return render_template('account_page.html')



from app.models.auth import auth
app.register_blueprint(auth)
from app.models.products import prod
app.register_blueprint(prod)
from app.models.order import order_blueprint
app.register_blueprint(order_blueprint)
from app.models.user import user_blueprint
app.register_blueprint(user_blueprint)


if __name__ == '__main__':
    app.run(debug=True)