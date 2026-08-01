from app.extensions import db
from app.models import User
from app.extensions import login_manager
from flask_login import login_user

class ValidationError(Exception):
    pass


class AuthService:
    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    
    @staticmethod
    def create_user(user_data: dict):
        user = User(
            username=user_data['username'], 
            password=user_data['password'],
            f_name = user_data.get('f_name'),
            l_name = user_data.get('l_name')
            )
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    @staticmethod
    def login(user_data:dict):
        if 'username' not in user_data.keys() or 'password' not in user_data.keys():
            raise ValidationError("Some data is missing!")
        username = user_data.get('username')
        password = user_data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValidationError(f"{username} does not exist!")
        if user.password==password:
            login_user(user)
            return user
        else:
            return None
