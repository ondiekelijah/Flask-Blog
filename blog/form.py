from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectField
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
import email_validator
import flask_login
from flask_login import current_user
from wtforms import ValidationError
from wtforms import validators
from models import User


class AddPost(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=8, max=200)])
    postImage = FileField(validators=[FileAllowed(["jpg", "png", "jpeg", "svg","webp"])])
    body = TextAreaField(validators=[InputRequired()])
    category = SelectField("Category", choices=[('Technology'),('Business')])
    s_category = SelectField("Sub Category", choices=[('Web Development'),('Android Development'),('UX Design'),('Other')])



class CommentPost(FlaskForm):
    comment = TextAreaField(validators=[InputRequired()])
    #Below are to allow for form submission,validation is therefore skipped
    email = StringField(validators=[Email(), Length(1, 64)])
    reply = TextAreaField(validators=[InputRequired()])

class ReplyComment(FlaskForm):
    reply = TextAreaField(validators=[InputRequired()])

class Subscribe(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    
class Search(FlaskForm):
    sval = StringField(validators=[InputRequired()])