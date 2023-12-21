from ORM import User
from flask_login import LoginManager
from db_mod import db

login_manager = LoginManager()

def init_app(app):
    login_manager.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SECRET_KEY"] = "super secret key"
    db.init_app(app)
    with app.app_context():
        db.create_all()

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
                return db.session.execute(db.select(User).filter_by(ID=user_id)).scalar_one()
    return None