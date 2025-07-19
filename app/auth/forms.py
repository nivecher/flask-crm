from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from app.extensions import db


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username: StringField) -> None:
        user = db.session.scalar(db.select(User).filter_by(username=username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email: StringField) -> None:
        user = db.session.scalar(db.select(User).filter_by(email=email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")
