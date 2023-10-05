from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates 

metadata = MetaData(naming_convention={
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db =SQLAlchemy(metadata = metadata)

db = SQLAlchemy()

class Hero (db.Model, SerializerMixin):
    __tablename__ = "heroes"
    serialize_rules = ('-powers.hero',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    powers = db.relationship('Hero_power', back_populates='hero', lazy=True)
    
    
class Hero_power (db.Model, SerializerMixin):
    __tablename__ = "hero_powers"
    
    serialize_rules = ('-hero.powers', '-power.heroes')
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id= db.Column(db.Integer,db.ForeignKey('heroes.id'), nullable=False)
    power_id= db.Column(db.Integer,db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, value):
        # Ensure that 'strength' is one of the allowed values
        allowed_strengths = ['Strong', 'Weak', 'Average']
        if value not in allowed_strengths:
            raise ValueError("Strength must be one of 'Strong', 'Weak', 'Average'")
        return value
    
class Power (db.Model, SerializerMixin):
    __tablename__ = "powers"
    
    serialize_rules = ('-heroes.power',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    
    heroes = db.relationship('Hero_power', back_populates='power', lazy=True)
    
    @validates('description')
    def validate_description(self, key, value):
        # Ensure that 'description' is present and at least 20 characters long
        if not value:
            raise ValueError("Description must be present")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value