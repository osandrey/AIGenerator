from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    response = Column(String(3200), nullable=False)
    question = Column(String(200), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), default=None)
    user = relationship("User", backref='questions')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)

    # contacts = relationship("Contact", backref='user', foreign_keys=[Contact.user_id])