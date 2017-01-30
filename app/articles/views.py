# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Article
from app.user.models import User
from app.articles.models import Comment
from app.articles.forms import NewArticleForm, NewCommentForm
from app.utils import flash_errors

blueprint = Blueprint('articles', __name__, url_prefix='/articles', static_folder='../static')


@blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def add_article():
    form = NewArticleForm(request.form, csrf_enabled=True)
    if form.validate_on_submit():
        article = Article.create(title=form.title.data, body=form.body.data, author=current_user.profile.id)
        flash('Article with title "{}" will be added!'.format(article.title), 'success')
        return redirect(url_for('user.members', user_id=current_user.id))
    else:
        flash_errors(form)
    return render_template('articles/new_article.html', form=form, user=current_user)


@blueprint.route('/detail/<article_id>', methods=['GET', 'POST'])
@login_required
def detail_article(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    comments = Comment.query.filter(Comment.article == article_id).order_by(Comment.created_at.desc())
    form = NewCommentForm(csrf_enabled=True)
    return render_template('articles/detail_article.html', form=form, user=current_user, article=article, comments=comments)


@blueprint.route('/edit/<article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    if article.author != current_user.profile.id:
        return render_template('404.html')
    form = NewArticleForm(request.form, csrf_enabled=True, title=article.title, body=article.body)
    if form.validate_on_submit():
        article = article.update(title=form.title.data, body=form.body.data)
        flash('Article was be editing.', 'success')
        return redirect(url_for('user.members', user_id=current_user.id))
    else:
        flash_errors(form)
    return render_template('articles/new_article.html', form=form, user=current_user, article=article)


@blueprint.route('/delete/<article_id>')
@login_required
def delete_article(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    if article.author != current_user.profile.id:
        return render_template('404.html')
    article.delete()
    return redirect(url_for('user.members', user_id=current_user.id))


@blueprint.route('/add_comment/<article_id>', methods=['POST'])
@login_required
def add_comment(article_id):
    form = NewCommentForm(request.form, csrf_enabled=True)
    if form.validate_on_submit():
        article = Article.query.filter(Article.id == article_id).first()
        comment = Comment.create(body=form.body.data, author=current_user.profile.id, article=article.id)
        dict = {
            'body': comment.body,
            'author': comment.profile.user.username,
            'created_at': comment.created_at
        }
        return jsonify(dict)
    else:
        flash_errors(form)
    return redirect(url_for('articles.detail_article', article_id=article_id))

