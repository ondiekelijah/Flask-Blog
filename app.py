import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_msearch import Search
# from .config import Config
from dotenv import load_dotenv

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_cartegory = "info"
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
bcrypt = Bcrypt()
search = Search()
env_configs = load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config['ADMIN_EMAIL'] = os.getenv("ADMIN_EMAIL")


    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    bcrypt.init_app(app)
    search.init_app(app)
    bcrypt.init_app(app)

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    class MyModelView(ModelView):
        def is_accessible(self):
            access = current_user.is_authenticated and current_user.is_administrator()
            return access
        
    admin = Admin(app,name='Infokit Admin', template_mode='bootstrap3')
    from models import User,Post,Comments,Role,Replies
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))
    admin.add_view(MyModelView(Comments, db.session))
    admin.add_view(MyModelView(Replies, db.session))
    admin.add_view(MyModelView(Role, db.session))


    from auth.routes import auth
    from blog.routes import bp

    app.register_blueprint(auth)
    app.register_blueprint(bp)

    return app
