import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import db, setup_db, Movies, Actors
from auth import AuthError, requires_auth
from datetime import datetime

def create_app(is_drop=False):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, is_drop=is_drop)
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    # Controller
    @app.route('/movies') 
    @requires_auth('get:movies')
    def get_movies(self):
        data = []
        try:
            movies = db.session.query(Movies).join(Actors, isouter=True).all()
            for movie in movies:
                actors = []
                for actor in movie.actors:
                    actors.append({
                        "id": actor.id,
                        "name": actor.name,
                        "age": actor.age,
                        "gender": actor.gender
                    })
                data.append({
                    "id": movie.id,
                    "title": movie.title,
                    "release_date": movie.release_date,
                    "actors": actors
                })
            return jsonify({
                "success": True,
                "movies": data
            })
        except Exception as e:
            print(e)
            abort(500, "Error fetching movies")
    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(self):
        body = request.get_json()
        title=body.get('title', None)
        release_date=body.get('release_date', None)
        if title is None or release_date is None:
            abort(400, "Missing required fields")
        new_movie = Movies(title=title, release_date=release_date)
        try:
            db.session.add(new_movie)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Movie created",
                "movie": new_movie.format()
            }), 201
        except Exception as e:
            db.session.rollback()
            print(e) 
            abort(500, "Error creating movie")
        finally:
            db.session.close()
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(self, movie_id):
        movie = db.session.query(Movies).filter(Movies.id == movie_id).first()
        if not movie:
            abort(404, "Movie not found")
        
        body = request.get_json()
        if 'title' in body:
            movie.title = body.get('title')
        if 'release_date' in body:
            movie.release_date = format_date(body.get('release_date'))
        
        try:
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Movie updated",
                "movie": movie.format()
            })
        except Exception as e:
            print(e)
            abort(500, "Error updating movie")
        finally:
            db.session.close()

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(self, movie_id):
        movie = db.session.query(Movies).filter(Movies.id == movie_id).first()
        if not movie:
            abort(404, "Movie not found")
        
        try:
            db.session.delete(movie)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Movie deleted"
            })
        except Exception as e:
            print(e)
            abort(500, "Error deleting movie")
        finally:
            db.session.close()

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(self):
        try:
            actors = db.session.query(Actors).all()
            return jsonify({
                "success": True,
                "actors": [actor.format() for actor in actors]
            })
        except Exception as e:
            print(e)
            abort(500, "Error fetching actors")

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(self):
        body = request.get_json()
        name=body.get('name', None)
        age=body.get('age', None)
        gender=body.get('gender', None)
        if body is None or name is None or age is None or gender is None:
            abort(400, "Missing required fields")
        new_actor = Actors(name=name, age=age, gender=gender)

        try:
            db.session.add(new_actor)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Actor created",
                "actor": new_actor.format()
            }), 201
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(500, "Error creating actor")
        finally:
            db.session.close()

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(self, actor_id):
        actor = db.session.query(Actors).filter(Actors.id == actor_id).first()
        if not actor:
            abort(404, "Actor not found")       
        
        body = request.get_json()
        if 'name' in body:
            actor.name = body.get('name')
        if 'age' in body:
            actor.age = body.get('age')
        if 'gender' in body:
            actor.gender = body.get('gender')
        
        try:
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Actor updated",
                "actor": actor.format()
            })
        except Exception as e:
            print(e)
            abort(500, "Error updating actor")
        finally:
            db.session.close()

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(self, actor_id):
        actor = db.session.query(Actors).filter(Actors.id == actor_id).first()
        if not actor:
            abort(404, "Actor not found")       
        
        try:
            db.session.delete(actor)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Actor deleted"
            })
        except Exception as e:
            print(e)
            abort(500, "Error deleting actor")
        finally:
            db.session.close()

    def format_date(date): 
        if isinstance(date, str): 
            return datetime.strptime(date, "%Y-%m-%d").date() 
        else: 
            return date

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "message": error.error.get('description'),
            "error": error.status_code
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": error.description if error.description else "Bad request",
            "error": 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": error.description if error.description else "Resource not found",
            "error": 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "message": error.description if error.description else "Internal server error",
            "error": 500
        }), 500

    return app

APP = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=port)
