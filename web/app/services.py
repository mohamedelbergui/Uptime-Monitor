from app.extensions import db
from app.models import User, Service, CheckResult
from app.extensions import login_manager
from flask_login import login_user
from sqlalchemy import desc


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

class ServiceService:
    @staticmethod
    def create_service(data:dict, user_id:int):
        if 'url' not in data.keys():
            raise ValidationError("URL is missing!")
        if 'check_interval_sec' not in data.keys():
            raise ValidationError("check interval is missing!")
        service = Service(
            user_id = user_id,
            url = data['url'],
            check_interval_sec = data['check_interval_sec'],
            name = data.get('name')
        )
        db.session.add(service)
        try:
            db.session.commit()
            return service
        except Exception as e:
            raise Exception(str(e))
            
    @staticmethod
    def edit_service(data:dict, id_service:int):
        service = db.session.get(Service,id_service)
        for key, value in data.items():
            setattr(service,key, value)
        db.session.commit()
        return service

    @staticmethod
    def get_services_check(user_id:int):
        services=Service.query.filter_by(user_id=user_id).all()
        services_list=[]
        for service in services:
            check_last = CheckResult.query.filter_by(id_service=service.id).order_by(desc(CheckResult.timestamp)).first()
            if check_last:
                services_list.append(
                    {
                        "id": service.id,
                        "url": service.url,
                        "name": service.name,
                        "is_active":service.is_active,
                        "check_interval_sec": service.check_interval_sec,
                        "is_checked":True,
                        "status_code": check_last.status_code,
                        "response_time_ms": check_last.response_time_ms,
                        "message": check_last.message,
                        "timestamp": check_last.timestamp
                    }
                )
            else:
                services_list.append(
                                    {
                                        "id": service.id,
                                        "url": service.url,
                                        "name": service.name,
                                        "is_active":service.is_active,
                                        "check_interval_sec": service.check_interval_sec,
                                        "is_checked":False,
                                    }
                                )
        return services_list
    
    @staticmethod
    def svc_delete(service_id, user_id):
        service=db.session.get(Service,ident=service_id)
        if service.user_id==user_id:
            db.session.delete(service)
            db.commit()
        else:
            raise ValidationError("access to this feature is denied")


        
