from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gstno = db.Column(db.String(15), nullable=False)
    businessregno = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, default=0)
    phoneno = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    deals = db.relationship('Deal', backref='seller', lazy=True)

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phoneno = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    ongoing_deals = db.relationship('Deal', secondary='buyer_deals', backref=db.backref('buyers', lazy='dynamic'))

buyer_deals = db.Table('buyer_deals',
    db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id'), primary_key=True),
    db.Column('deal_id', db.Integer, db.ForeignKey('deal.id'), primary_key=True))

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Add category field
    price = db.Column(db.Float, nullable=False)  # Add price field

    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    terms = db.relationship('Term', backref='deal', lazy=True)

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    is_accepted = db.Column(db.Boolean, default=False)  # Indicates whether the term is accepted
    is_declined = db.Column(db.Boolean, default=False)  # Indicates whether the term is declined
    is_countered = db.Column(db.Boolean, default=False) # Indicates whether the term is countered
    counter_term = db.Column(db.String(200))  # Stores the counter term if any
    # Other fields...