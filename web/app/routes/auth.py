from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='POST':
        if request.is_json:
            user_data=request.get_json()
        else:
            user_data=request.form.to_dict()
        try:
            AuthService.create_user(user_data=user_data)
            flash("Sign UP!","success")
            redirect(url_for('auth.signup'))
        except Exception as e:
            flash(str(e),"error")
            redirect(url_for('auth.signup'))
    return render_template("signup.html")