from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import InputRequired, Optional, Length


class SendForm(FlaskForm):
    quantity = DecimalField(
        'Quantity',
        validators=[InputRequired()],
        render_kw={"placeholder": "Quantity to Send"}
    )
    receiver = StringField(
        'Receiver',
        validators=[InputRequired(), Length(min=58, max=58)],
        render_kw={"placeholder": "Receiver Address"}
    )
    note = StringField(
        'Note',
        validators=[Optional()],
        render_kw={"placeholder": "Note"})
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    passphrase = StringField('15-word Passphrase', validators=[InputRequired()])
    submit = SubmitField('Login')
