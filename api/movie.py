from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.movies import Movie

movie_api = Blueprint('movie_api', __name__,
                   url_prefix='/api/movies')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(movie_api)

class MovieAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            DateID = body.get('DateID')
            if DateID is None or len(DateID) < 2:
                return {'message': f'ID is missing, or is less than 2 characters'}, 210
            # validate uid
            ftitle = body.get('ftitle')
            if ftitle is None or len(ftitle) < 1:
                return {'message': f'Movie title is missing, or is less than 2 characters'}, 210
            commentary = body.get('commentary')
            if commentary is None or len(commentary) < 0:
                return {'message': f'commentary is missing, or is less than 0 characters'}, 210

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Movie(DateID=DateID, 
                      ftitle=ftitle,
                      commentary=commentary)
            
            ''' Additional garbage error checking '''
            # set password if provided
            
            # convert to date type
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            movie = uo.create()
            # success returns json of user
            if movie:
                return jsonify(movie.read())
            # failure returns error
            return {'message': f'Processed {ftitle}, either a format error or ID {DateID} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            movies = Movie.query.all()    # read/extract all users from database
            json_ready = [movie.read() for movie in movies]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')