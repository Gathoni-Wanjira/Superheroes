from flask import Flask , jsonify , request, make_response
from models import db , Power , Hero , Hero_power
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow

# /heroes ,/heroes/:id, /powers , /powers/:id ,patch /powers/:id, post /hero_powers , 

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
ma = Marshmallow(app)


class HeroSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hero
        fields = ("id","name","super_name")
hero_schema = HeroSchema()
heroes_schema = HeroSchema(many = True)

class PowerSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Power
        fields = ("id","name","description")
power_schema = PowerSchema()
powers_schema = PowerSchema(many = True)

class Index (Resource):
    def get (self):
        return make_response(
            jsonify({"message": "Superheroes Api"})
        )
api.add_resource(Index, "/")
        
class Heroes(Resource):
    def get (self):
        heroes = heroes_schema.dump(Hero.query.all())
        return make_response(
            jsonify(heroes),
            200
        )
        

api.add_resource(Heroes, "/heroes")


class HeroById(Resource):
    def get (self,id):
        hero = Hero.query.filter_by(id = id).first()
        if not hero:
            return make_response(
                jsonify({ "error": "Hero not found"}), 
                200
            )
        hero_serial = hero_schema.dump(Hero.query.filter_by(id = id).first())
        hero_serial["powers"] = [power_schema.dump(power.power) for power in hero.powers]
        return make_response(
            jsonify(hero_serial),
            200
        )
        

api.add_resource(HeroById, "/heroes/<int:id>")

# class Heroes(Resource):
#     def get (self):
#         heroes = heroes_schema.dump(Hero.query.all())
#         return make_response(
#             jsonify(heroes),
#             200
#         )
        

# api.add_resource(Heroes, "/heroes")

# class Heroes(Resource):
#     def get (self):
#         heroes = heroes_schema.dump(Hero.query.all())
#         return make_response(
#             jsonify(heroes),
#             200
#         )
        

# api.add_resource(Heroes, "/heroes")

# class Heroes(Resource):
#     def get (self):
#         heroes = heroes_schema.dump(Hero.query.all())
#         return make_response(
#             jsonify(heroes),
#             200
#         )
        

# api.add_resource(Heroes, "/heroes")



# @app.route('/')
# def check():
#     return "Hello world"



if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
    
    