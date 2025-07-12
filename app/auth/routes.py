from flask import render_template, redirect, url_for, flash
from flask.typing import ResponseReturnValue
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.forms import LoginForm, RegistrationForm
from app.auth.services import create_user, authenticate_user


@bp.route("/login", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data is None or form.password.data is None:
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        user = authenticate_user(form.username.data, form.password.data)
        if user is None:
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main.dashboard"))
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout() -> ResponseReturnValue:
    logout_user()
    return redirect(url_for("main.dashboard"))


@bp.route("/register", methods=["GET", "POST"])
def register() -> ResponseReturnValue:
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data is None or form.email.data is None or form.password.data is None:
            flash("Invalid registration data")
            return redirect(url_for("auth.register"))
        create_user(form.username.data, form.email.data, form.password.data)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)

