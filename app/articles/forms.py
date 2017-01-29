# -*- coding: utf-8 -*-
"""Article forms."""
from flask_wtf import Form, FlaskForm
from wtforms import PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class NewArticleForm(FlaskForm):
    title = StringField('Article title', validators=[DataRequired(), Length(min=5, max=200)])
    body = TextAreaField('Article body', validators=[DataRequired(), Length(min=50)])


class NewCommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
