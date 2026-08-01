from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.services import ServiceService

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def home():
    return "Hello, Flask is running!"


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