from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planet = db.relationship('Favorites_planets', back_populates='user_relationship')
    favorite_people = db.relationship('Favorites_peoples', back_populates = 'user_relationship')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__= "planet"
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String(50), unique=True, nullable=False )
    url = db.Column(db.String(50), unique= True )
    climate = db.Column (db.String(30))
    population = db.Column (db.Integer)
    terrain  = db.Column (db.String(30))
    surface_water = db.Column (db.Integer)
    diameter= db.Column(db.Integer)
    rotation_period =db.Column (db.Integer)
    orbital_period = db.Column (db.Integer)
    gravity = db.Column (db.String(20))
    created = db.Column (db.Date)
    edited = db.Column(db.Date)
    planet_favorite = db.relationship('Favorites_planets', back_populates='planet_relationship')
    people = db.relationship('People', back_populates = 'homeworld_relationship')
    
    def __repr__(self):
        return f'Planet: {self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "climate" : self.climate,
            "population" : self.population,
            "terrain" : self.terrain,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period" : self.orbital_period,
            "gravity" : self.gravity,
            "terrain" : self.terrain,
            "surface_water": self.surface_water,
            "created" : self.created, 
            "edited" : self.edited
    }

    def basic_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "climate" : self.climate,
            "population" : self.population
        }

class People(db.Model):
    __tablename__= "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(30), unique=True, nullable=False)
    url= db.Column (db.String(50), unique=True, nullable=False )     
    homeworld = db.Column (db.Integer, db.ForeignKey('planet.id'))
    homeworld_relationship = db.relationship('Planet', back_populates ='people')
    height= db.Column (db.Integer)
    mass = db.Column (db.Integer)
    hair_color = db.Column (db.String(10))
    skin_color = db.Column (db.String(10))
    eye_color = db.Column (db.String(10))
    birth_year = db.Column (db.Date)
    gender = db.Column (db.String(10), nullable=False)
    created = db.Column (db.Date)
    edited = db.Column (db.Date)
    species = db.Column (db.String(50))
    starships = db.Column (db.String(50))
    vehicles = db.Column (db.String(50))
    people_favorite = db.relationship('Favorites_peoples', back_populates = 'people_relationship')

    def __repr__(self):
        return f'Personaje: {self.name}'

    def serialize(self):
         return{ 
            "id ":  self.id,
            "name" : self.name,
            "url" : self.url,    
            "homeworld" : self.homeworld_relationship.basic_serialize(), 
            "height" : self.height,
            "mass" : self.mass,
            "hair_color" : self.hair_color,
            "skin_color" : self.skin_color,
            "eye_color" : self.eye_color,
            "birth_year" : self.birth_year,
            "gender" : self.birth_year,
            "created" : self.created,
            "edited" : self.edited,
            "species" : self.species,
            "starships" : self.starships,
            "vehicles" : self.vehicles,
        }

class Favorites_planets(db.Model):
    __tablename__ = "favorites_planets"
    id= db.Column (db.Integer, primary_key=True)
    user_id = db.Column (db.Integer,  db.ForeignKey('user.id'))
    user_relationship = db.relationship('User', back_populates='favorite_planet')
    planet_id = db.Column(db.Integer,  db.ForeignKey('planet.id'))
    planet_relationship = db.relationship('Planet', back_populates='planet_favorite')

    def __repr__(self):
        return f'Favorite_planet: {self.planet_id}'
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id
        } 
    
class Favorites_peoples(db.Model):
    __tablename__ = "favorites_peoples"
    id= db.Column (db.Integer, primary_key=True)
    user_id = db.Column (db.Integer,  db.ForeignKey('user.id'))
    user_relationship = db.relationship('User', back_populates='favorite_people')
    people_id = db.Column(db.Integer,  db.ForeignKey('people.id'))
    people_relationship = db.relationship('People', back_populates='people_favorite')

    def __repr__(self):
        return f'Favorite_people: {self.people_id}'
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.people_id
        }