from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
import email_validator
import flask_login
from flask_login import current_user
from wtforms import ValidationError
from wtforms import validators


class Message(FlaskForm):
    name = StringField(
        validators=[
            InputRequired(),
            Length(3, 100, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Names must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    message = TextAreaField(validators=[InputRequired()])

class Subscribe(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])





