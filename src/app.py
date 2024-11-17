"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorites_planets, Favorites_peoples
#from models import Person importar todas las tablas

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_all_users():
    users= User.query.all()
    print(users)
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    return jsonify({'msg': 'ok', 'data': users_serialized}), 200
   

@app.route('/planets', methods=['GET'])
def get_planets():
    planets= Planet.query.all()
    print (planets)
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    return jsonify({'msg': 'ok', 'data': planets_serialized}), 200

@app.route('/people', methods=['GET'])
def get_people():
    peoples= People.query.all()
    print (peoples)
    peoples_serialized = []
    for people in peoples:
        peoples_serialized.append(people.serialize())
    return jsonify({'msg': 'ok', 'data': peoples_serialized}), 200

@app.route('/planets/<int:id>', methods=["GET"])
def get_planet_byId(id):
    planet = Planet.query.get(id)
    print (planet)
    planet_serialize = planet.serialize()
    return jsonify({'msg': 'ok', 'data': planet_serialize})

@app.route('/people/<int:id>', methods=["GET"])
def get_people_byId(id):
    people = People.query.get(id)
    print (people)
    people_serialize = people.serialize()
    return jsonify({'msg': 'ok', 'data': people_serialize})
    
@app.route('/planet', methods=["POST"])
def post_planet():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'El body no puede estar vacio'}), 400
    if 'name'  not in body:
        return jsonify({'msg': 'Debe ingresar un nombre'})
    if 'url' not in body: 
        return jsonify({'msg': 'Debe ingresar una url'})
    new_planet= Planet()
    new_planet.name = body['name']
    new_planet.url = body['url']
    new_planet.diameter= body.get('diameter',None)
    new_planet.rotation_period = body.get('rotation_period',None)
    new_planet.orbital_period = body.get('orbital_period')
    new_planet.gravity = body.get('gravity', None)
    new_planet.population = body.get ('population', None)
    new_planet.climate = body.get ('climate', None)
    new_planet. terrain  = body.get ('body', None)
    new_planet.surface_water = body.get ('surface_water', None)
    new_planet.created = body.get ('created', None)
    new_planet.edited = body.get ('edited', None)


@app.route('/people', methods=['POST'])
def post_people():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'El body no puede estar vacío'}), 400
    if 'name' not in body:
        return jsonify ({'msg':'Debe ingresar un nombre'}), 400
    if 'url' not in body:
        return jsonify ({'msg':'Debe ingresar un url'}), 400
    if 'homeworld' not in body:
        return jsonify ({'msg': 'Debe ingresar un homeworld'}), 400
    new_people = People()
    new_people_name = body['name']
    new_people_url = body['url']    
    new_people_homeworld = body['homeworld'] 
    new_people_height = body.get ('height', None)
    new_people_mass = body.get ('mass', None)
    new_people_hair_color = body.get('hair_color', None)
    new_people_skin_color = body.get ('skin_color', None)
    new_people_eye_color = body.get ('eye_color', None)
    new_people_birth_year = body.get ('birth_year', None)
    new_people_gender = body.get ('birth_year', None)
    new_people_created = body.get ('created', None)
    new_people_edited = body.get ('edited', None)
    new_people_species = body.get ('species', None)
    new_people_starships = body.get ('starships', None)
    new_people_vehicles = body.get ('vehicles', None)

##@app.route('/favorites/<int:user_id>', methods=['POST'])


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
