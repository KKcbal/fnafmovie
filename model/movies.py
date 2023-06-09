""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Movie(db.Model):
    __tablename__ = 'movies'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _DateID = db.Column(db.Integer, unique=True)
    _ftitle = db.Column(db.String(255), unique=False, nullable=False)
    _commentary = db.Column(db.String, unique=False, nullable=False)
    _likes = db.Column(db.Integer, unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, DateID, ftitle, commentary, likes):
        self._DateID = DateID
        self._ftitle = ftitle    # variables with self prefix become part of the object, 
        self._commentary = commentary
        self._likes = likes

    @property
    def DateID(self):
        return self._DateID
    
    # a setter function, allows name to be updated after initial object creation
    @DateID.setter
    def DateID(self, DateID):
        self._DateID = DateID
    
    # a name getter method, extracts name from object
    @property
    def ftitle(self):
        return self._ftitle
    
    # a setter function, allows name to be updated after initial object creation
    @ftitle.setter
    def ftitle(self, ftitle):
        self._ftitle = ftitle
    
    # a getter method, extracts commentary from object
    @property
    def commentary(self):
        return self._commentary
    
    # a setter function, allows name to be updated after initial object creation
    @commentary.setter
    def commentary(self, commentary):
        self._commentary = commentary
        
    @property
    def likes(self):
        return self._likes
    
    # a setter function, allows name to be updated after initial object creation
    @likes.setter
    def likes(self, likes):
        self._likes = likes
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "DateID": self.DateID,
            "ftitle": self.ftitle,
            "commentary": self.commentary,
            "likes": self.likes
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, DateID="", ftitle="", commentary="", likes=""):
        """only updates values with length"""
        if len(DateID) > 0:
            self.DateID = DateID
        if len(ftitle) > 0:
            self.ftitle = ftitle
        if len(commentary) > 0:
            self.commentary = commentary
        if len(likes) > 0:
            self.likes = likes
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initMovies():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = Movie(DateID="97812", ftitle='Joker', commentary='I\'m the joker baby', likes=0)
    u2 = Movie(DateID="123", ftitle='fnaf', commentary='it was soo cool', likes=0)
    u3 = Movie(DateID="3", ftitle='Back to the Future', commentary='doc browno', likes=0)
    u4 = Movie(DateID="4", ftitle='BlacKkKlansman', commentary='adam driver your line was "keep driving asshole"', likes=0)
    u5 = Movie(DateID="5", ftitle='Willy\'s Wonderland', commentary='I love Nicholas Cage', likes=0)

    movies = [u1, u2, u3, u4, u5]

    """Builds sample user/note(s) data"""
    for movie in movies:
        try:
            movie.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist or error: {movie.DateID}")
            