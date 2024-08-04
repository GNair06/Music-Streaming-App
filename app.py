from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.figure import Figure
import base64
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from model import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.sqlite3"
db.init_app(app)
app.app_context().push()

# logout
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return redirect("/")

# statistics
@app.route("/statistics", methods=['GET', 'POST'])
def statistics():
    return render_template("statistics.html")

# song graph
@app.route("/song_graph", methods=['GET', 'POST'])
def song_graph():
    x, y = [], []
    for song in Song.query.all():
        x.append(song.title)
        y.append(song.avg_rating)
    xx = np.array(x)
    yy = np.array(y)
    # song avg rating
    all_songs = Song.query.all()
    if (len(all_songs) != 0):
        for song in all_songs:
            sum, count = 0, 0
            for rating in song.ratings:
                sum += rating.score
                count += 1
            if count == 0:
                song.avg_rating = 0
            else:
                song.avg_rating = sum / count
        db.session.commit()

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(xx, yy)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<br><h3>Song average rating</h3><img src='data:image/png;base64,{data}'/>"

# album graph
@app.route("/album_graph", methods=['GET', 'POST'])
def album_graph():
    x, y = [], []
    for album in Album.query.all():
        x.append(album.name)
        y.append(album.avg_rating)
    xx = np.array(x)
    yy = np.array(y)
    # song avg rating
    all_albums = Album.query.all()
    if (len(all_albums) != 0):
        for album in all_albums:
            sum, count = 0, 0
            for rating in album.ratings:
                sum += rating.score
                count += 1
            if count == 0:
                album.avg_rating = 0
            else:
                album.avg_rating = sum / count
        db.session.commit()

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(xx, yy)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<br><h3>Album average rating</h3><img src='data:image/png;base64,{data}'/>"

# creator graph
@app.route("/creator_graph", methods=['GET', 'POST'])
def creator_graph():
    x, y = [], []
    for user in User.query.all():
        if user.role == "creator":
            x.append(user.name)
            y.append(user.avg_rating)
    xx = np.array(x)
    yy = np.array(y)
    # user avg rating
    all_users = User.query.all()
    if (len(all_users) != 0):
        for user in all_users:
            sum, count = 0, 0
            for rating in user.ratings:
                sum += rating.score
                count += 1
            if count == 0:
                user.avg_rating = 0
            else:
                user.avg_rating = sum / count
        db.session.commit()

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(xx, yy)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<br><h3>Creator average rating</h3><img src='data:image/png;base64,{data}'/>"

# home page with dif login options
@app.route("/", methods=['GET', 'POST'])
def home():
    all_albums = Album.query.all()
    all_songs = Song.query.all()
    all_users = User.query.all()
    # song avg rating
    if (len(all_songs) != 0):
        for song in all_songs:
            sum, count = 0, 0
            for rating in song.ratings:
                sum += rating.score
                count += 1
            if count == 0:
                song.avg_rating = 0
            else:
                song.avg_rating = sum / count
        db.session.commit()

    # album avg rating
    if (len(all_albums) != 0):
        for album in all_albums:
            sum, count = 0, 0
            for rating in album.ratings:
                sum += rating.score
                count += 1
            if count == 0:
                album.avg_rating = 0
            else:
                album.avg_rating = sum / count
        db.session.commit()

    # user avg rating
    if (len(all_users) != 0):
        for user in all_users:
            rating_lst_len = len(user.ratings)
            sum, count = 0, 0
            for rating in user.ratings:
                sum = sum + rating.score
                if rating_lst_len == 0:
                    user.avg_rating = 0
                else:
                    user.avg_rating = sum / rating_lst_len
        db.session.commit()
    return render_template("index.html")

# top 5 songs
@app.route("/top_songs", methods=['GET', 'POST'])
def top_songs():
    # song avg rating
    all_songs = Song.query.all()
    for song in all_songs:
        sum, count = 0, 0
        for rating in song.ratings:
            sum += rating.score
            count += 1
        if count == 0:
            song.avg_rating = 0
        else:
            song.avg_rating = sum / count
    db.session.commit()
    # top 5 songs
    lst = []
    lst = Song.query.order_by(Song.avg_rating.desc()).limit(5).all()
    return render_template("top_songs.html", lst=lst)

# top albums
@app.route("/top_albums", methods=['GET', 'POST'])
def top_albums():
    # album avg rating
    all_albums = Album.query.all()
    for album in all_albums:
        sum, count = 0, 0
        for rating in album.ratings:
            sum += rating.score
            count += 1
        if count == 0:
            album.avg_rating = 0
        else:
            album.avg_rating = sum / count
    db.session.commit()
    # top 5 albums
    lst = []
    lst = Album.query.order_by(Album.avg_rating.desc()).limit(5).all()
    return render_template("top_albums.html", lst=lst)

# page with search links
@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template("search.html")

# search playlist using name
@app.route("/search_playlist", methods=['GET', 'POST'])
def search_playlist():
    if request.method == "POST":
        name = request.form.get('title')
        playlist = Playlist.query.filter_by(name=name).first()
        return render_template("search_playlist_view.html", playlist=playlist)
    return render_template("search_playlist_title.html")

# search song using avg_rating
@app.route("/search_song_rating", methods=['GET', 'POST'])
def search_song_rating():
    # song avg rating
    all_songs = Song.query.all()
    for song in all_songs:
        sum, count = 0, 0
        for rating in song.ratings:
            sum += rating.score
            count += 1
        if count == 0:
            song.avg_rating = 0
        else:
            song.avg_rating = sum / count
    db.session.commit()

    lst = []
    if request.method == "POST":
        score = request.form.get('score')
        for song in Song.query.all():
            if (song.avg_rating >= int(score)):
                lst.append(song)
        return render_template("search_rating_view.html", lst=lst)
    return render_template("search_song_rating.html")

# search album using avg_rating
@app.route("/search_album_rating", methods=['GET', 'POST'])
def search_album_rating():
    # album avg rating
    all_albums = Album.query.all()
    for album in all_albums:
        sum, count = 0, 0
        for rating in album.ratings:
            sum += rating.score
            count += 1
        if count == 0:
            album.avg_rating = 0
        else:
            album.avg_rating = sum / count
    db.session.commit()

    lst = []
    if request.method == "POST":
        score = request.form.get('score')
        for album in Album.query.all():
            if (album.avg_rating >= int(score)):
                lst.append(album)
        return render_template("album_rating_view.html", lst=lst)
    return render_template("search_album_rating.html")

# search song using title
@app.route("/search_song_title", methods=['GET', 'POST'])
def search_song_title():
    if request.method == "POST":
        title = request.form.get('title')
        song = Song.query.filter_by(title=title).first()
        return render_template("search_song_view.html", song=song)
    return render_template("search_song_title.html")

# search song using genre
@app.route("/search_song_genre", methods=['GET', 'POST'])
def search_song_genre():
    all_songs = Song.query.all()
    lst = []
    if request.method == "POST":
        genre = request.form.get('genre')
        for song in all_songs:
            if (song.genre_name==genre):
                lst.append(song)
        return render_template("search_genre_view.html", lst=lst)
    return render_template("search_song_genre.html")

# search song using using album
@app.route("/search_album_title", methods=['GET', 'POST'])
def search_album_title():
    if request.method == "POST":
        title = request.form.get('title')
        album = Album.query.filter_by(name=title).first()
        return render_template("search_album_view.html", album=album)
    return render_template("search_album_title.html")

# search song using using artist name
@app.route("/search_song_artist", methods=['GET', 'POST'])
def search_song_artist():
    all_songs = Song.query.all()
    lst = []
    if request.method == "POST":
        artist = request.form.get('artist')
        for song in all_songs:
            if (song.creator==artist):
                lst.append(song)
        return render_template("search_artist_view.html", lst=lst)
    return render_template("search_song_artist.html")

# admin dashboard
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    # user and creator lst
    ulst, clst = [], []
    all_users = User.query.all()
    for i in all_users:
        if i.role == "user":
            ulst.append(i)
        elif i.role == "creator":
            clst.append(i)
    # no. of general users
    user_len = len(ulst)
    # no. of creators
    creator_len = len(clst)
    # no. of songs
    song_len = len(Song.query.all())
    # no. of albums
    album_len = len(Album.query.all())
    # no. of genres
    genre_len = len(Genre.query.all())
    return render_template("admin_dashboard.html", genre_len=genre_len,  user_len=user_len, creator_len=creator_len, song_len=song_len, album_len=album_len)

# admin_users
@app.route("/admin_users")
def admin_users():
    all_users = User.query.all()
    return render_template("admin_users.html", all_users = all_users)

# display all songs
@app.route("/<int:id>/all_songs")
def all_songs(id):
    this_user = User.query.get(id)
    all_songs = Song.query.all()
    return render_template("all_songs.html", all_songs = all_songs, this_user=this_user)

# blacklist users
@app.route("/<int:id>/blacklist")
def blacklist(id):
    blacklist_lst = []
    this_user = User.query.get(id)
    if (this_user.blacklist_id == 2):
            return render_template("whitelist.html", this_user=this_user)
    else:
        this_user.blacklist_id = 2
        db.session.commit()
        blacklisted = Blacklist.query.get(2)
        blacklist_lst = blacklisted.users
        return render_template("blacklist.html", blacklist_lst=blacklist_lst)

# blacklisted users
@app.route("/blacklisted")
def blacklisted():
    blacklist_lst = []
    blacklisted = Blacklist.query.get(2)
    blacklist_lst = blacklisted.users
    return render_template("blacklist.html", blacklist_lst=blacklist_lst)

# whitelist users
@app.route("/<int:id>/whitelist")
def whitelist(id):
    this_user = User.query.get(id)
    this_user.blacklist_id = 1
    db.session.commit()
    return redirect("/admin_users")

# admin songs
@app.route("/admin_songs")
def admin_songs():
    all_songs = Song.query.all()
    return render_template("admin_songs.html", all_songs = all_songs)

# unflag songs
@app.route("/<int:id>/unflag")
def unflag(id):
    this_song = Song.query.get(id)
    this_song.flag_id = 1
    db.session.commit()
    return redirect("/admin_songs")

# flagged songs
@app.route("/flagged")
def flagged():
    flag_lst = []
    flagged = Flag.query.get(2)
    flag_lst = flagged.songs
    return render_template("flag.html", flag_lst=flag_lst)

# flag songs
@app.route("/<int:id>/flag_song")
def flag_songs(id):
    flag_lst = []
    this_song = Song.query.get(id)
    if (this_song.flag_id == 2):
            return render_template("unflag.html", this_song=this_song)
    else:
        this_song.flag_id = 2
        db.session.commit()
        flagged = Flag.query.get(2)
        flag_lst = flagged.songs
        return render_template("flag.html", flag_lst=flag_lst)
    
# ......................
# admin albums
@app.route("/admin_albums")
def admin_albums():
    all_albums = Album.query.all()
    return render_template("admin_albums.html", all_albums = all_albums)

# unflag albums
@app.route("/<int:id>/unflag_album")
def unflag_album(id):
    this_album = Album.query.get(id)
    this_album.flag_id = 1
    db.session.commit()
    return redirect("/admin_albums")

# flagged albums
@app.route("/flagged_albums")
def flagged_albums():
    flag_lst = []
    flagged = Flag.query.get(2)
    flag_lst = flagged.albums
    return render_template("flag_album.html", flag_lst=flag_lst)

# flag songs
@app.route("/<int:id>/flag_album")
def flag_album(id):
    flag_lst = []
    this_album = Album.query.get(id)
    if (this_album.flag_id == 2):
            return render_template("unflag_album.html", this_album=this_album)
    else:
        this_album.flag_id = 2
        db.session.commit()
        flagged = Flag.query.get(2)
        flag_lst = flagged.albums
        return render_template("flag_album.html", flag_lst=flag_lst)
# ......................

# display all albums
@app.route("/<int:id>/all_albums")
def all_albums(id):
    this_user = User.query.get(id)
    all_albums = Album.query.all()
    return render_template("all_albums.html", all_albums = all_albums, this_user=this_user)


# login page with users
@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        all_users = User.query.all()
        for user in all_users:
            if ((user.name == username) and (user.password == password)):
                print(user.name)
                this_user = User.query.get(user.id)
                if (user.role == "user"):
                    return render_template("user_dashboard.html", this_user=this_user)
                elif (user.role == "creator"):
                    song_lst_len = len(this_user.songs)
                    album_lst_len = len(this_user.albums)
                    rating_lst_len = len(this_user.ratings)
                    sum = 0
                    for rating in this_user.ratings:
                        sum = sum + rating.score
                    if rating_lst_len == 0:
                        avg_rating = 0
                    else:
                        avg_rating = sum / rating_lst_len
                    return render_template("creator_dashboard.html", this_user=this_user, song_lst_len=song_lst_len, album_lst_len=album_lst_len, avg_rating=avg_rating)
        return "INCORRECT CREDENTIALS"
    return render_template("user_login.html")

# login page for admin
@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if ((username == "admin") and (password == "admin")):
            return redirect("/admin_dashboard")
        else:
            return "INCORRECT CREDENTIALS"
    return render_template("admin_login.html")

# register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        role = "user"
        new_user = User(name = username, password=password, role=role, blacklist_id=1)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

# creator dashboard
@app.route("/<int:id>/creator", methods = ['Get', 'POST'])
def creator_dashboard(id):
    this_user = User.query.get(id)
    this_user.role = "creator"
    db.session.commit()
    song_lst_len = len(this_user.songs)
    album_lst_len = len(this_user.albums)
    rating_lst_len = len(this_user.ratings)
    sum = 0
    for rating in this_user.ratings:
        sum = sum + rating.score
    if rating_lst_len == 0:
        avg_rating = 0
    else:
        avg_rating = sum / rating_lst_len
        avg_rating = int(avg_rating)
    return render_template('creator_dashboard.html', this_user = this_user, song_lst_len=song_lst_len, album_lst_len=album_lst_len, avg_rating=avg_rating)

# add song
@app.route("/<int:id>/add_song", methods = ['Get', 'POST'])
def add_song(id):
    this_user = User.query.get(id)
    all_genres = Genre.query.all()
    if request.method == "POST":
        title = request.form.get('title')
        genre_name = request.form.get('genre_name')
        # if new genre, add into table
        l = []
        for i in all_genres:
            l.append(i.name)
        if genre_name not in l:
            new_genre = Genre(name=genre_name)
            db.session.add(new_genre)
            db.session.commit()
        # ..................................
        date = request.form.get('date')
        duration = request.form.get('duration')
        lyrics = request.form.get('lyrics')
        creator = this_user.name
        user_id = this_user.id
        this_genre = Genre.query.filter_by(name=genre_name).first()
        genre_id = this_genre.id
        new_song = Song(flag_id=1, genre_id=genre_id, duration=duration, title = title, genre_name=genre_name, date=date, lyrics=lyrics, creator=creator, user_id=user_id)
        db.session.add(new_song)
        db.session.commit()
        song_lst_len = len(this_user.songs)
        album_lst_len = len(this_user.albums)
        rating_lst_len = len(this_user.ratings)
        sum = 0
        for rating in this_user.ratings:
            sum = sum + rating.score
            rating_lst_len += 1
        if rating_lst_len == 0:
            avg_rating = 0
        else:
            avg_rating = sum / rating_lst_len
        return render_template('creator_dashboard.html', this_user = this_user, song_lst_len=song_lst_len, album_lst_len=album_lst_len, avg_rating=avg_rating)
    return render_template("add_song.html", this_user=this_user)

# all songs of the creator
@app.route("/<int:id>/my_songs", methods = ['Get', 'POST'])
def my_songs(id):
    this_user = User.query.get(id)
    lst = this_user.songs
    return render_template("my_songs.html", lst=lst, this_user=this_user)

# read lyrics
@app.route("/<int:id>/read_lyrics", methods = ['Get', 'POST'])
def read_lyrics(id):
    this_song = Song.query.get(id)
    lyrics = this_song.lyrics
    title = this_song.title
    return render_template("read_lyrics.html", lyrics=lyrics, title=title, this_song=this_song)

# edit a song
@app.route("/<int:idu>/<int:ids>/edit_song", methods = ['Get', 'POST'])
def edit_song(idu, ids):
    this_song = Song.query.get(ids)
    this_user = User.query.get(idu)
    lst = this_user.songs
    if request.method == "POST":
        title = request.form.get('title')
        genre = request.form.get('genre')
        lyrics = request.form.get('lyrics')
        this_song.title = title
        this_song.genre = genre
        this_song.lyrics = lyrics
        return render_template("my_songs.html", lst=lst, this_user=this_user)
    return render_template("edit_song.html", this_song=this_song, this_user=this_user)

# delete a song
@app.route("/<int:idu>/<int:ids>/delete_song", methods = ['Get', 'POST'])
def delete_song(idu, ids):
    this_song = Song.query.get(ids)
    play_lst = this_song.playlists
    idu = this_song.user_id
    this_user = User.query.get(idu)
    lst = this_user.songs
    for album in Album.query.all():
        for x in album.songs:
            if (this_song == x):
                album.songs.remove(this_song)
    for playlist in play_lst:
        playlist.songs.remove(this_song)
    this_user.songs.remove(this_song)
    db.session.delete(this_song)
    db.session.commit()
    return render_template("my_songs.html", lst=lst, this_user=this_user)

# delete a song by admin
@app.route("/<int:ids>/delete_song", methods = ['Get', 'POST'])
def delete_song_admin(ids):
    this_song = Song.query.get(ids)
    play_lst = this_song.playlists
    idu = this_song.user_id
    this_user = User.query.get(idu)
    this_song.flag_id = 1
    for playlist in play_lst:
        playlist.songs.remove(this_song)
    for album in Album.query.all():
        for x in album.songs:
            if (this_song == x):
                album.songs.remove(this_song)
        playlist.songs.remove(this_song)
    this_user.songs.remove(this_song)
    db.session.delete(this_song)
    db.session.commit()
    return redirect("/flagged")

# create playlist
@app.route("/<int:id>/playlist", methods = ['Get', 'POST'])
def playlist(id):
    this_user = User.query.get(id)
    user_id = this_user.id
    if request.method == "POST":
        name = request.form.get('name')
        new_playlist = Playlist(name=name, user_id=user_id)
        db.session.add(new_playlist)
        db.session.commit()
        return render_template("my_playlists.html", this_user=this_user)
    return render_template("create_playlist.html", this_user=this_user)

# all playlists of the user
@app.route("/<int:id>/my_playlist", methods = ['Get', 'POST'])
def my_playlist(id):
    this_user = User.query.get(id)
    return render_template("my_playlists.html", this_user=this_user)

# add to playlist
@app.route("/<int:id>/add_to_playlist", methods = ['Get', 'POST'])
def add_to_playlist(id):
    this_playlist = Playlist.query.get(id)
    this_user = User.query.get(this_playlist.user_id)
    if request.method == "POST":
        title = request.form.get('title')
        new_song = Song.query.filter_by(title=title).first()
        this_playlist.songs.append(new_song)
        db.session.commit()
        return render_template("my_playlists.html", this_user=this_user)
    return render_template("add_to_playlist.html", this_playlist=this_playlist)

# delete from playlist
@app.route("/<int:idp>/<int:ids>/delete_from_playlist", methods = ['Get', 'POST'])
def delete_from_playlist(idp, ids):
    this_playlist = Playlist.query.get(idp)
    this_user = User.query.get(this_playlist.user_id)
    this_song = Song.query.get(ids)
    this_playlist.songs.remove(this_song)
    db.session.commit()
    return render_template("my_playlists.html", this_user=this_user)

# delete a playlist
@app.route("/<int:idu>/<int:idp>/delete_playlist", methods = ['Get', 'POST'])
def delete_playlist(idu, idp):
    this_user = User.query.get(idu)
    this_playlist = Playlist.query.get(idp)
    this_user.playlists.remove(this_playlist)
    db.session.delete(this_playlist)
    db.session.commit()
    return render_template("my_playlists.html", this_user=this_user)

# create album
@app.route("/<int:id>/album", methods = ['Get', 'POST'])
def album(id):
    this_user = User.query.get(id)
    user_id = this_user.id
    if request.method == "POST":
        name = request.form.get('name')
        new_album = Album(name=name, user_id=user_id, flag_id=1)
        db.session.add(new_album)
        db.session.commit()
        return render_template("my_albums.html", this_user=this_user)
    return render_template("create_album.html", this_user=this_user)

# all albums of the creator
@app.route("/<int:id>/my_albums", methods = ['Get', 'POST'])
def my_albums(id):
    this_user = User.query.get(id)
    return render_template("my_albums.html", this_user=this_user)

# add to album
@app.route("/<int:id>/add_to_album", methods = ['Get', 'POST'])
def add_to_album(id):
    this_album = Album.query.get(id)
    this_user = User.query.get(this_album.user_id)
    if request.method == "POST":
        album_id = this_album.id
        title = request.form.get('title')
        genre_name = request.form.get('genre_name')
        date = request.form.get('date')
        duration = request.form.get('duration')
        lyrics = request.form.get('lyrics')
        creator = this_user.name
        user_id = this_user.id
        # if new genre, add into table
        l = []
        all_genres = Genre.query.all()
        for i in all_genres:
            l.append(i.name)
        if genre_name not in l:
            new_genre = Genre(name=genre_name)
            db.session.add(new_genre)
            db.session.commit()
        this_genre = Genre.query.filter_by(name=genre_name).first()
        genre_id = this_genre.id
        new_song = Song(flag_id=1, genre_id=genre_id, duration=duration, album_id=album_id, title = title, genre_name=genre_name, date=date, lyrics=lyrics, creator=creator, user_id=user_id)
        this_album.songs.append(new_song)
        db.session.commit()
        return render_template("my_albums.html", this_user=this_user)
    return render_template("add_to_album.html", this_album=this_album)

# delete from album
@app.route("/<int:idp>/<int:ids>/delete_from_album", methods = ['Get', 'POST'])
def delete_from_album(idp, ids):
    this_album = Album.query.get(idp)
    this_user = User.query.get(this_album.user_id)
    this_song = Song.query.get(ids)
    this_album.songs.remove(this_song)
    db.session.delete(this_song)
    db.session.commit()
    return render_template("my_albums.html", this_user=this_user)

# delete album
@app.route("/<int:idu>/<int:ida>/delete_album", methods = ['Get', 'POST'])
def delete_album(idu, ida):
    this_user = User.query.get(idu)
    this_album = Album.query.get(ida)
    # delete all songs of this albums
    for this_song in this_album.songs:
        this_song.flag_id = 1
        for playlist in this_song.playlists:
            playlist.songs.remove(this_song)
        for album in Album.query.all():
            for x in album.songs:
                if (this_song == x):
                    album.songs.remove(this_song)
        this_user.songs.remove(this_song)
        db.session.delete(this_song)
    # ...................................
    this_user.albums.remove(this_album)
    db.session.delete(this_album)
    db.session.commit()
    return render_template("my_albums.html", this_user=this_user)

# delete album by admin
@app.route("/<int:ida>/delete_album", methods = ['Get', 'POST'])
def delete_album_admin(ida):
    this_album = Album.query.get(ida)
    this_user = User.query.get(this_album.user_id)
    this_user.albums.remove(this_album)
    # delete all songs of this albums
    for this_song in this_album.songs:
        this_song.flag_id = 1
        for playlist in this_song.playlists:
            playlist.songs.remove(this_song)
        for album in Album.query.all():
            for x in album.songs:
                if (this_song == x):
                    album.songs.remove(this_song)
            playlist.songs.remove(this_song)
        this_user.songs.remove(this_song)
        db.session.delete(this_song)
    # ...................................
    db.session.delete(this_album)
    db.session.commit()
    return redirect("/flagged_albums")

# song rating
@app.route("/<int:ids>/song_rating", methods = ['Get', 'POST'])
def song_rating(ids):
    all_songs = Song.query.all()
    this_song = Song.query.get(ids)
    this_user = User.query.get(this_song.user_id)
    artist = this_user.name
    if request.method == "POST":
        score = request.form.get('ratings')
        new_rating = Rating(score=score, user_id=this_song.user_id, song_id=this_song.id, artist=artist)
        db.session.add(new_rating)
        db.session.commit()
        return render_template("all_songs.html", all_songs=all_songs, this_user=this_user)
    return render_template("song_rating.html", this_song=this_song, this_user=this_user, all_songs=all_songs)

# album rating
@app.route("/<int:ida>/album_rating", methods = ['Get', 'POST'])
def album_rating(ida):
    all_albums = Album.query.all()
    this_album = Album.query.get(ida)
    this_user = User.query.get(this_album.user_id)
    artist = this_user.name
    if request.method == "POST":
        score = request.form.get('ratings')
        new_rating = Rating(score=score, user_id=this_album.user_id, album_id=ida, artist=artist)
        db.session.add(new_rating)
        db.session.commit()
        return render_template("all_albums.html", all_albums = all_albums, this_user=this_user)
    return render_template("album_rating.html", this_album=this_album, this_user=this_user, all_albums = all_albums)

# play song
@app.route("/play", methods=["GET", "POST"])
def play():
    return send_file("song.mp3")

if __name__ == "__main__":
    app.run(debug=True)