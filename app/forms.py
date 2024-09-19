from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Optional, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(message="Name is required.")])

    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address.")
    ])

    phone = StringField('Phone (optional)', validators=[
        Optional(),
        # Simple phone number validation
        Regexp(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
    ])

    message = TextAreaField('Message', validators=[
        DataRequired(message="Message is required."),
        Length(min=10, message="Message must be at least 10 characters long.")
    ])

    send_copy = BooleanField('Receive a copy of the email?')
    submit = SubmitField('Send')
