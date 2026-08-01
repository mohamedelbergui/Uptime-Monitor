from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services import AuthService, ValidationError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='POST':
        if request.is_json:
            user_data=request.get_json()
        else:
            user_data=request.form.to_dict()
        try:
            user=AuthService.create_user(user_data=user_data)
            if user:
                flash("Sign UP!","success")
                redirect(url_for('auth.login'))
            else:
                flash("error","error")
                redirect(url_for('auth.signup'))
        except Exception as e:
            flash(str(e),"error")
            redirect(url_for('auth.signup'))
    return render_template("signup.html")


@auth_bp.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.is_json:
            user_data=request.get_json()
        else:
            user_data=request.form.to_dict()
        try:
            user=AuthService.login(user_data=user_data)
            if user:
                flash(f"Bonjour {user.username}","success")
                redirect(url_for('auth.login'))
            else:
                flash(f"Mot de passe incorrect","error")
                redirect(url_for('auth.login'))
        except ValidationError as v:
            flash(str(v),"error")
            redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e),"error")
            redirect(url_for('auth.login'))
    return render_template("login.html")