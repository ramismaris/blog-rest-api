from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    is_superuser = Column(Boolean)
    is_active = Column(Boolean, default=True)
    data_joined = Column(DateTime, default=datetime.now)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    text = Column(String)
    is_archived = Column(Boolean, default=False)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    text = Column(String)

    created_at = Column(DateTime, default=datetime.now)


class UserToken(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    key = Column(String)
