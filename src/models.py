from . import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(500))
    estimated_cost = db.Column(db.Integer)
    estimated_revenue = db.Column(db.Integer)
    date_start = db.Column(db.Date(), nullable=False)
    date_end = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_rel = relationship("User", foreign_keys="[Business.user_id]")


class Expense(db.Model):
    amount = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    date_transaction = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_rel = relationship("User", foreign_keys="[Expense.user_id]")
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    business_rel = relationship("Business", foreign_keys="[Expense.business_id]")


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date_transaction = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_rel = relationship("User", foreign_keys="[Sale.user_id]")
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    business_rel = relationship("Business", foreign_keys="[Sale.business_id]")
