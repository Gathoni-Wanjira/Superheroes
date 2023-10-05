#!/usr/bin/env python3

from random import choice as rc, randint
from app import app
from models import db, Hero, Hero_power, Power

# Delete existing data
with app.app_context():
    db.drop_all()
    db.create_all()

hero_list = [
    { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
    { "name": "Doreen Green", "super_name": "Squirrel Girl" },
    { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
    { "name": "Janet Van Dyne", "super_name": "The Wasp" },
    { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
    { "name": "Jean Grey", "super_name": "Dark Phoenix" },
    { "name": "Ororo Munroe", "super_name": "Storm" },
    { "name": "Kitty Pryde", "super_name": "Shadowcat" },
    { "name": "Elektra Natchios", "super_name": "Elektra" }
]

power_list = [
    { "name": "super strength", "description": "gives the wielder super-human strengths" },
    { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
    { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
    { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }
]

strengths = ['Strong', 'Weak', 'Average']

with app.app_context():
    heroes = []
    for hero_data in hero_list:
        hero = Hero(name=hero_data['name'], super_name=hero_data['super_name'])
        heroes.append(hero)
        db.session.add(hero)

    powers = []
    for power_data in power_list:
        power = Power(name=power_data['name'], description=power_data['description'])
        powers.append(power)
        db.session.add(power)

    db.session.commit()

    hero_powers = []
    for hero in heroes:
        power = rc(powers)
        strength = rc(strengths)
        hero_power = Hero_power(hero=hero, power=power, strength=strength)
        hero_powers.append(hero_power)
        db.session.add(hero_power)

    db.session.commit()