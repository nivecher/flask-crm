from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    DecimalField,
)
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Donor
from typing import Any
from app.extensions import db
from app.utils import validate_address


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


class DonorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone")
    address = TextAreaField("Address")
    submit = SubmitField("Save Donor")
    original_email: str | None = None

    def validate_email(self, email: StringField) -> None:
        if self.obj and self.obj.email == email.data:
            return
        donor = db.session.scalar(db.select(Donor).filter_by(email=email.data))
        if donor is not None:
            raise ValidationError("This email is already registered.")

    def validate_address(self, address: TextAreaField) -> None:
        if address.data and not validate_address(address.data):
            raise ValidationError("The address appears to be invalid.")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(DonorForm, self).__init__(*args, **kwargs)
        self.obj = kwargs.get("obj")


class DonationForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired()], places=2)
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    type = StringField("Type", validators=[DataRequired()])
    submit = SubmitField("Save Donation")
