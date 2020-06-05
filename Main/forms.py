# CREATED BY JOHN EARL COBAR

# lib imports
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask import Markup

######################################################################################
################################# FORMS INPUT #######################################
######################################################################################

class FormRegister(FlaskForm):

    formemail =EmailField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField(Markup('Register'))

class FormDelete(FlaskForm):

    formemail = EmailField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Delete')
