from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Area
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(usernamelowercase=username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username, this one is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(emaillowercase=email.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different email address, this one is already used.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(usernamelowercase=self.username.data.lower()).first()
            if user is not None:
                raise ValidationError('Please use a different username, this one is already taken.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(emaillowercase=email.data.lower()).first()
            if user is not None:
                raise ValidationError('Please use a different email address, this one is already used.')

class EditProfileAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    # TODO: Add validation for email address and username

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ActivityForm(FlaskForm):
    activitytitle = StringField('Activity title', validators=[
        DataRequired(), Length(min=1, max=140)])
    activitylocation = SelectField(u'Location', choices = [],
        validators = [DataRequired()])
    activitybody = TextAreaField('Describe the activity.', validators=[
        DataRequired(), Length(min=1, max=14000)])
    submit = SubmitField('Submit')

    # Call items for the drop-down from a database.
    def __init__(self):
        super(ActivityForm, self).__init__()
        self.activitylocation.choices = Area.query.all()
        # self.activitylocation.choices = Area.query.filter_by(city='Dublin').all()

class EditActivityForm(FlaskForm):
    activitytitle = StringField('Activity title', validators=[
        DataRequired(), Length(min=1, max=140)])
    activitylocation = SelectField(u'Location', choices = [],
        validators = [DataRequired()])
    activitybody = TextAreaField('Describe the activity.', validators=[DataRequired(), Length(min=1, max=14000)])
    submit = SubmitField('Submit')

    def __init__(self):
        super(EditActivityForm, self).__init__()
        # self.activitylocation.choices = Area.query.filter_by(city='Dublin').all()
        self.activitylocation.choices = Area.query.all()

    
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class Filter(FlaskForm):
    activitylocation = SelectField(u'Location', choices = [],
        validators = [DataRequired()])
    submit = SubmitField('Filter')

    def __init__(self):
        super(Filter, self).__init__()
        # self.activitylocation.choices = Area.query.filter_by(city='Dublin').all()
        self.activitylocation.choices = Area.query.all()

    