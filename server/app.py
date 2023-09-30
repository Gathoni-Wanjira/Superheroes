from flask import Flask
from models import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def check():
    return "Hello world"

if __name__ == '__main__':
    app.run(port=5555, debug=True)