from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired


class DonationForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired()], places=2)
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    type = StringField("Type", validators=[DataRequired()])
    submit = SubmitField("Save Donation")
