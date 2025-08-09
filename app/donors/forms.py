from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Email, Optional
from wtforms import FormField
from app.utils import validate_phone, validate_donor_email
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from flask_wtf import FlaskForm  # noqa: F811


class AddressForm(FlaskForm):
    class Meta:
        csrf = False  # covered by parent form

    address_line1 = StringField("Address Line 1", validators=[DataRequired()])
    address_line2 = StringField("Address Line 2", validators=[Optional()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[Optional()])
    postal_code = StringField("Postal Code", validators=[Optional()])
    country = StringField("Country", validators=[DataRequired()])


class DonorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email", validators=[DataRequired(), Email(), validate_donor_email]
    )
    phone = TelField("Phone", validators=[Optional(), validate_phone])
    current_address = FormField(AddressForm)
    submit = SubmitField("Save Donor")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(DonorForm, self).__init__(*args, **kwargs)
        self.obj = kwargs.get("obj")
