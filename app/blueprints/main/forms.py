from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[DataRequired(message="Please enter your name."), Length(max=120)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter your email."), Email(), Length(max=254)],
    )
    subject = StringField(
        "Subject",
        validators=[DataRequired(message="Please enter a subject."), Length(max=150)],
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(message="Please enter a message."), Length(min=10, max=5000)],
    )
    subscribe_opt_in = BooleanField(
        "Keep me posted on drops and news (optional)", validators=[Optional()]
    )
    submit = SubmitField("Send Message")
