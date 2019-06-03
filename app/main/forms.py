from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required


class PostForm(FlaskForm):
    '''
    Class to create a wtf form for creating a post
    '''
    content = TextAreaField('YOUR POST')
    submit = SubmitField('SUBMIT')

class CommentForm(FlaskForm):
    '''
    Class to create a wtf form for creating a post
    '''
    opinion = TextAreaField('WRITE COMMENT')
    submit = SubmitField('SUBMIT')

class CategoryForm(FlaskForm):
    '''
    Class to create a wtf form for creating a post
    '''
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')

    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')