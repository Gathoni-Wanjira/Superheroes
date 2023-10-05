#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, redirect, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

from models import db, Hero, Power, Hero_power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': "SuperHeroes Api"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    response_body = {
        "Message": "Welcome to the world of heroes"
    }
    return redirect(SWAGGER_URL), 200
class HeroesEndpoint(Resource):
    def get(self):
        heroes = Hero.query.all()
        serialized_heroes = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
        return jsonify(serialized_heroes)

class HeroesById(Resource):
    def get(self, id):
        hero = db.session.query(Hero).get(id)
        if hero:
            serialized_hero = hero.to_dict()
            return make_response(jsonify(serialized_hero))
        else:
            return {'error': 'Hero not found'}, 404

# Define routes for Power model
class PowersEndpoint(Resource):
    def get(self):
        powers = Power.query.all()
        serialized_powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
        return jsonify(serialized_powers)

class PowersById(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            serialized_power = {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            return jsonify(serialized_power)
        else:
            return {'error': 'Power not found'}, 404

# Define route for updating Power
class UpdatePower(Resource):
    def patch(self, id):
        power = Power.query.get(id)
        if power:
            data = request.get_json()
            if 'description' in data:
                power.description = data['description']

                try:
                    db.session.commit()
                    return jsonify({
                        'id': power.id,
                        'name': power.name,
                        'description': power.description
                    })
                except Exception as e:
                    return {'errors': ['Validation errors']}, 400

        return {'error': 'Power not found'}, 404

# Define route for creating HeroPower
class HeroPowersEndPoint(Resource):
    def get(self):
        hero_powers = Hero_power.query.all()
        serialized_hero_powers = [hero_power.to_dict() for hero_power in hero_powers]
        return serialized_hero_powers

    def post(self):
        data = request.get_json()
        new_hero_power = Hero_power(**data)

        try:
            db.session.add(new_hero_power)
            db.session.commit()
            return HeroesById().get(new_hero_power.hero_id)  # Return the related Hero data
        except Exception as e:
            return {'errors': ['Validation errors']}, 400
class HeroPowerById(Resource):
    def get(self, id):
        hero_power = Hero_power.query.get(id)
        if hero_power:
            serialized_hero_power = hero_power.to_dict()  # Assuming you have a to_dict() method in your Hero_power model
            return jsonify(serialized_hero_power)
        else:
            return {'error': 'Hero power not found'}, 404

# Add the route to the API
api.add_resource(HeroPowerById, '/hero_powers/<int:id>')
api.add_resource(HeroesEndpoint, '/heroes')
api.add_resource(HeroesById, '/heroes/<int:id>')
api.add_resource(PowersEndpoint, '/powers')
api.add_resource(PowersById, '/powers/<int:id>')
api.add_resource(HeroPowersEndPoint, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)