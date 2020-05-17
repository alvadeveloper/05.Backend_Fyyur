#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import date

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#-------------------------------------------------------#
#Global Variables.
today = str(date.today())
#-------------------------------------------------------#

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Shows = db.Table('Shows',
#   db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id')),
#   db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id')),
#   db.Column('start_time', db.String(100))
# )

class Shows(db.Model):
  __tablename__='all_shows'

  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
  venue_id =  db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
  start_time = db.Column(db.String(100))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    shows = db.relationship('Venue', secondary='all_shows', backref=db.backref('allshows',  lazy='dynamic'))
   

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# class Shows(db.Model):
#     __tablename__ = 'Shows'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     artistid = db.Column(db.Integer)
#     venueid = db.Column(db.Integer)
#     date = db.Column(db.String) 

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venuelocation = Venue.query.all(),
  return render_template('pages/venues.html', venuelocation=venuelocation);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_venue')
  results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  count = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).count()

  return render_template('pages/search_venues.html', results=results, search_term=search_term, count=count)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venueall=Venue.query.filter_by(id=venue_id).all()
  venue = venueall[0]

  showsbefore = db.session.query(Artist, Venue, Shows)\
                    .join(Artist, Artist.id == Shows.artist_id)\
                    .join(Venue, Venue.id == Shows.venue_id).filter(Shows.start_time <= today).filter(Venue.id == venue_id)

  showsafter = db.session.query(Artist, Venue, Shows)\
                    .join(Artist, Artist.id == Shows.artist_id)\
                    .join(Venue, Venue.id == Shows.venue_id).filter(Shows.start_time >= today).filter(Venue.id == venue_id)


  comingshows = showsafter.count()
  pastshows = showsbefore.count()

  return render_template('pages/show_venue.html', venue=venue, showsbefore=showsbefore, showsafter=showsafter, comingshows=comingshows, pastshows=pastshows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  name = form.name.data
  city = form.city.data
  state = form.state.data
  address = form.address.data
  phone = form.phone.data
  image_link = form.image_link.data
  website = form.website.data
  genres = form.genres.data
  facebook_link = form.facebook_link.data


  venue = Venue(name=name, city=city, state=state, address=address, phone=phone, website=website, genres=genres, image_link=image_link, facebook_link=facebook_link)
  db.session.add(venue)
  db.session.commit()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists=Artist.query.all()
  return render_template('pages/artists.html',  artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_artist')
  results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  count = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).count()

  return render_template('pages/search_artists.html', results=results, search_term=search_term, count=count )

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artistall=Artist.query.filter_by(id=artist_id).all()
  artist = artistall[0]

  showsbefore = db.session.query(Artist, Venue, Shows)\
                    .join(Artist, Artist.id == Shows.artist_id)\
                    .join(Venue, Venue.id == Shows.venue_id).filter(Shows.start_time <= today).filter(Artist.id == artist_id)

  showsafter = db.session.query(Artist, Venue, Shows)\
                    .join(Artist, Artist.id == Shows.artist_id)\
                    .join(Venue, Venue.id == Shows.venue_id).filter(Shows.start_time >= today).filter(Artist.id == artist_id)


  comingshows = showsafter.count()
  pastshows = showsbefore.count()
  

  return render_template('pages/show_artist.html', artist=artist, showsafter=showsafter, showsbefore=showsbefore, comingshows=comingshows, pastshows=pastshows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artistall=Artist.query.filter_by(id=artist_id).all()
  artist = artistall[0]
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  artistall=Artist.query.filter_by(id=artist_id).all()
  artist = artistall[0]
  name = form.name.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  genres = form.genres.data
  image_link = form.image_link.data
  website = form.website.data
  facebook_link = form.facebook_link.data

  # try:
  artist = Artist.query.get(artist_id)
  artist.name = name
  artist.city = city
  artist.image_link = image_link
  artist.genres = genres
  artist.state = state
  artist.phone = phone
  artist.facebook_link = facebook_link
  artist.website = website
  db.session.commit()

  # except:
  #       db.session.rollback()
  # finally:
  #       session.expunge_all()
  #       db.session.close()

  return render_template('pages/show_artist.html', artist_id=artist_id, artist=artist)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  name = form.name.data
  city = form.city.data
  state = form.state.data
  address = form.address.data
  phone = form.phone.data
  genres = form.genres.data
  image_link = form.image_link.data
  website = form.website.data
  facebook_link = form.facebook_link.data
  venuelocation = Venue.query.all(),
    
  venue = Venue.query.get(venue_id)
  venue.name = name
  venue.city = city
  venue.state = state
  venue.genres = genres
  venue.image_link = image_link
  venue.website = website
  venue.address = address
  venue.phone = phone
  venue.facebook_link = facebook_link
  db.session.commit()

  return render_template('pages/show_venue.html', venuelocation=venuelocation, venue_id=venue_id, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  name = form.name.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  genres = form.genres.data
  image_link = form.image_link.data
  website = form.website.data
  facebook_link = form.facebook_link.data

  try:
        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website=website)
        db.session.add(artist)
        db.session.commit()

  except:
        db.session.rollback()
  finally:
        db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(Artist, Venue, Shows)\
                    .join(Artist, Artist.id == Shows.artist_id)\
                    .join(Venue, Venue.id == Shows.venue_id).all();

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  artist_id = form.artist_id.data
  venue_id = form.venue_id.data
  start_time = form.start_time.data

  try:
        shows = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(shows)
        db.session.commit()
  except:
        db.session.rollback()
  finally:
        db.session.close()



  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
