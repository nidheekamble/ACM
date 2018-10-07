from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError
from Unholify.models import User, AboveUser

class SelectForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    type = RadioField('Let us know something about your age',choices=[('A','I am older than 21 years'),('B','I am not yet 21')])
    submit = SubmitField('Proceed')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Tha email is taken. Please choose a different one.')


class RegistrationFormAbove(FlaskForm):
    above_choices = [('D','Occasionally a day'),('M', 'Occasionally a month'),('Y', 'Occasionally a year')]
    above_type = RadioField('How frequently do you drink?', choices=above_choices, validators=[Required()])
    above_friend = StringField('Frequently Contacted Friend', validators=[DataRequired(), Length(max=120) ,Email()])
    above_family = StringField('Frequently Contacted Family Member', validators=[DataRequired(), Length(max=120) ,Email()])
    above_colleague =  StringField('Frequently Contacter Colleague', validators=[DataRequired(), Length(max=120) ,Email()])
    above_submit = SubmitField('Sign Up')

class StressForm(FlaskForm):
    above_stress=IntegerField('On the scale of 1 to 10, how stressed do you feel at the moment, 10 being the most?',validators=[DataRequired(),NumberRange(min=1, max= 10)])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountFormAboveUser(FlaskForm):
    above_choices = [('D','Occasionally a day'),('M', 'Occasionally a month'),('Y', 'Occasionally a year')]
    above_type = SelectField('How frequently do you drink?', choices=above_choices, validators=[Required()])
    above_friend = StringField('Frequently Contacted Friend', validators=[DataRequired(), Length(max=120) ,Email()])
    above_family = StringField('Frequently Contacted Family Member', validators=[DataRequired(), Length(max=120) ,Email()])
    above_colleague =  StringField('Frequently Contacter Colleague', validators=[DataRequired(), Length(max=120) ,Email()])
    submit = SubmitField('Sign Up')
