from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero (db.Model):
    __tablename__ = "heroes"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    powers = db.relationship('Hero_power', back_populates='hero', lazy=True)
    
    
class Hero_power (db.Model):
    __tablename__ = "hero_powers"
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id= db.Column(db.Integer,db.ForeignKey('heroes.id'), nullable=False)
    power_id= db.Column(db.Integer,db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')
    
class Power (db.Model):
    __tablename__ = "powers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    
    heroes = db.relationship('Hero_power', back_populates='power', lazy=True)
    
    