from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.services import ServiceService, ValidationError
from app.models import Service

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def dashboard():
    user_id=current_user.id
    data = ServiceService.get_services_check(user_id=user_id)
    return render_template("dashboard.html", data=data)


@main_bp.route("/service/add", methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method=='POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        user_id = current_user.id
        try:
            service = ServiceService.create_service(data=data, user_id=user_id)
            if service:
                flash("service created successfully","success")
                return redirect(url_for('main.home'))
            else:
                flash("service has not been created", "error")
                return redirect(url_for('main.add_service'))
        except ValueError as v:
            flash(str(v),"error")
            return redirect(url_for('main.add_service'))
        except Exception as e:
            flash(str(e),"error")
            return redirect(url_for('main.add_service'))
    return render_template("create_service.html")

@main_bp.route("/service/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def edit_service(id):
    user_id=current_user.id
    service=Service.query.get(id)
    if service.user_id != user_id:
        flash("access denied for user","error")
        return redirect(url_for('main.dashboard'))
    if request.method=='POST':
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form.to_dict()
        if data:
            data_to_update={}
            for key,value in data.items():
                if key!='is_active':
                    if getattr(service, key)!=value:
                        data_to_update[key]=value
            is_active = True if (data.get('is_active') or data.get('is_active')=='true') else False
            if is_active!=service.is_active:
                data_to_update['is_active']= is_active 


                
            ServiceService.edit_service(data=data_to_update, id_service=id)

    return render_template(
        "edit_service.html", 
        service={
            "id":service.id,
            "url":service.url,
            "name":service.name,
            "check_interval_sec":service.check_interval_sec,
            "is_active":service.is_active,
        }
        )

@main_bp.post("/service/<int:id>/deactivate")
@login_required
def svc_deactivate(id):
    ServiceService.edit_service(
        data={"is_active":False},
        id_service=id
    )
    return redirect(url_for('main.dashboard'))

@main_bp.post("/service/<int:id>/activate")
@login_required
def svc_activate(id):
    ServiceService.edit_service(
        data={"is_active":True},
        id_service=id
    )
    return redirect(url_for('main.dashboard'))


@main_bp.route("/service/<int:id>/delete", methods=['GET','POST'])
@login_required
def svc_delete(id):
    if request.method=='POST':
        try:
            ServiceService.svc_delete(service_id=id, user_id=current_user.id)
            flash("the service is deleted")
            return redirect(url_for('main.dashboard'))
        except ValidationError as v:
            flash(str(v))
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('main.dashboard'))
    return render_template("confirmation_of_deletion.html",service_id=id)
