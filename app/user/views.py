# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from app.articles.models import Article, Comment
from app.utils import flash_errors

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

@blueprint.route('/<user_id>')
@login_required
def members(user_id):
    """List members."""
    user = User.query.filter(User.id == user_id).first()
    page = request.args.get('page', type=int, default=1)
    articles = Article.query.filter(Article.author == user.profile.id).order_by(Article.created_at.desc()).paginate(page, 5, False)
    return render_template('users/user_page.html', user=user, articles=articles)



