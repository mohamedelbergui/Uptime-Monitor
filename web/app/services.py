from app.extensions import db
from app.models import User


class AuthService:
    @staticmethod
    def create_user(user_data: dict):
        user = User(username=user_data.get('username'), password=user_data.get('password'))
        if 'f_name' in user_data.keys() and 'l_name' in user_data.keys():
            user.f_name = user_data.get('f_name')
            user.l_name = user_data.get('l_name')
        db.session.add(user)
        db.session.commit