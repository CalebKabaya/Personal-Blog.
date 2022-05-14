from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import DataRequired

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')
class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Technology','Technology'),('Health','Health'),('Food','Food '),('Lifestyle','lifestyle'),],validators=[DataRequired()])
    post = TextAreaField('Your Story', validators=[DataRequired()])
    submit = SubmitField('Post Blog')    