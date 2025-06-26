from functools import wraps

from flask import Flask, abort
from flask_login import LoginManager, current_user
from flask_wtf import CSRFProtect

from models import User
from settings import DatabaseConfig

app = Flask(__name__)
app.config.from_object(DatabaseConfig)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    return user


def admin_required(f):
    @wraps(f)
    def decorate_func(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401)
        elif not current_user.is_admin:
            return abort(403)
        return f(*args, **kwargs)

    return decorate_func


from routes.administration import *
from routes.errors import *
from routes.main import *
from routes.menu import *
from routes.orders import *
from routes.users import *

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5050)