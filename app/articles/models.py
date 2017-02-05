# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from sqlalchemy import ForeignKey, Integer, String, DateTime

from flask_login import UserMixin

from app.database import Column, Model, SurrogatePK, db, reference_col, relationship
from app.extensions import bcrypt

class Article(SurrogatePK, Model):
    """Article for blog"""
    __tablename__ = 'articles'
    title = Column(String(200))
    body = Column(String())
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    author = Column(Integer, ForeignKey('profiles.id'))
    comments = relationship('Comment', backref='article_link', cascade='delete')

    def __repr__(self):
        return '<Article title={}'.format(self.title)


class Comment(SurrogatePK, Model):
    __tablename__ = 'comments'
    body = Column(String(1000))
    author = Column(Integer, ForeignKey('profiles.id'))
    article = Column(Integer, ForeignKey('articles.id'))
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
