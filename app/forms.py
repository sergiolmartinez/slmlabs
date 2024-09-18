from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Optional


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone (optional)', validators=[
                        Optional()])  # Optional phone field
    message = TextAreaField('Message', validators=[DataRequired()])
    # Checkbox for user to receive a copy
    send_copy = BooleanField('Send me a copy of this message')
    submit = SubmitField('Send')
