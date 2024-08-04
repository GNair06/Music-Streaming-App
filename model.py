from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

song_playlist = db.Table("song_playlist",
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    songs = db.relationship('Song', backref='user')
    playlists = db.relationship('Playlist', backref='user')
    albums = db.relationship('Album', backref='user')
    ratings = db.relationship('Rating', backref='user')
    avg_rating = db.Column(db.Integer, default=0)
    blacklist_id = db.Column(db.Integer, db.ForeignKey('blacklist.id'))

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=song_playlist, backref="playlists")

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    artist = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', backref='album')
    ratings = db.relationship('Rating', backref='album')
    avg_rating = db.Column(db.Integer, default=0)
    flag_id = db.Column(db.Integer, db.ForeignKey('flag.id'))

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    songs = db.relationship('Song', backref='genre')

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, default="whitelisted")
    users = db.relationship('User', backref='blacklist')

class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, default="not_flagged")
    songs = db.relationship('Song', backref='flag')
    albums = db.relationship('Album', backref='flag')

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False) 
    genre_name = db.Column(db.String(128))
    date = db.Column(db.String)
    lyrics = db.Column(db.String(10000), nullable=False)
    duration = db.Column(db.String(128))
    creator = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    ratings = db.relationship('Rating', backref='song')
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    avg_rating = db.Column(db.Integer, default=0)
    flag_id = db.Column(db.Integer, db.ForeignKey('flag.id'))

    