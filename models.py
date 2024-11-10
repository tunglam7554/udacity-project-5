import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import config

database_path = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy()

def setup_db(app, database_path=database_path, is_drop=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    app.app_context().push()
    db.init_app(app)
    if is_drop is True:
        db.drop_all()
    db.create_all()    

    # db.session.add(Movies(title="Avenger Endgame", release_date="2024-11-11"))
    # db.session.add(Actors(name="Chris Evans", age=43, gender="Male", movie_id=1))
    # db.session.commit()

class Movies(db.Model):  
    __tablename__ = 'Movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = Column(db.Date)
    actors = db.relationship("Actors", backref=db.backref("movie", lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.set_release_date(release_date)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_release_date(self, release_date): 
        if isinstance(release_date, str): 
            self.release_date = datetime.strptime(release_date, "%Y-%m-%d").date() 
        else: 
            self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat()
        }

class Actors(db.Model):
    __tablename__ = 'Actors'
    
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    gender = Column(db.String)
    movie_id = Column(db.Integer, db.ForeignKey('Movies.id'), nullable=True)

    def __init__(self, name, age, gender, movie_id=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }