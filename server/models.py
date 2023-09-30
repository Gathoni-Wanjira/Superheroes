from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero (db.model):
    __tablename__ = "heroes"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    hero_powers = db.relationship('Hero_power', backref='hero', lazy=True)
    
    
class Hero_power (db.model):
    __tablename__ = "hero_powers"
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id= db.Column(db.Interger,db.ForeignKey('heroes.id'), nullable=False)
    power_id= db.Column(db.Interger,db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    hero = db.relationship('Hero', backref='hero_powers')
    power = db.relationship('Power', backref='hero_powers')
    
class Power (db.model):
    __tablename__ = "powers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    
    heroes = db.relationship('Hero_power', backref='power', lazy=True)