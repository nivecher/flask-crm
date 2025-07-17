from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    DecimalField,
    DateField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from app.utils import validate_user_email
from app.extensions import db
from typing import Any



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(), validate_user_email])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username: StringField) -> None:
        user = db.session.scalar(db.select(User).filter_by(username=username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")





class DonationForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired()], places=2)
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    type = StringField("Type", validators=[DataRequired()])
    submit = SubmitField("Save Donation")

