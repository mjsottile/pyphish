import os
import pickle
from pathlib import Path
from html.parser import HTMLParser
import requests
import pandas as pd

class Show:
    """
A show has a date, location, ID, tour, rating, and collection of sets.
"""
    def __init__(self, id, tour, date, rating, location):
        self.rating = rating
        self.date = date
        self.location = location
        self.id = id
        self.tour = tour
        self.sets = {}

    def add_set(self, name, setdata):
        self.sets[name] = setdata

class Song:
    """ A song has a name and ID. """
    def __init__(self, name, id):
        self.name = name
        self.id = id

class Database:
    """
A database holds a set of show and song objects, as well as auxiliary
data structures for helping look up data.  It also provides a set of
methods for querying and updating the contents.
"""
    def __init__(self):
        self.shows = {}
        self.songs = {}
        self.songs_by_id = {}
        self.song_id_counter = 1

    def add_show(self, show):
        self.shows[show.id] = show

    def contains_show(self, show_id):
        return show_id in self.shows

    def register_song(self, songname):
        if songname in self.songs:
            return self.songs[songname].id
        else:
            print('registering '+songname)
            s = Song(songname, self.song_id_counter)
            self.song_id_counter = self.song_id_counter + 1
            self.songs[songname] = s
            self.songs_by_id[s.id] = s
            return s.id

    def print_db(self):
        for show_id in self.shows:
            show = self.shows[show_id]
            print("SHOW: "+show.date+" - "+show.location+" ("+show.tour+")")
            for setname in show.sets:
                print("  "+setname+": "+str(show.sets[setname]))
        for song_id in self.songs_by_id:
            print("SONG: "+self.songs_by_id[song_id].name+" ("+str(song_id)+")")

##

def get_apikey():
    if os.environ.get('PHISHNET_APIKEY') is None:
        print("ERROR: Set PHISHNET_APIKEY to your Phish.net API key.")
        return None
    else:
        return os.environ.get('PHISHNET_APIKEY')

def get_show_string(show_id):
    apikey = get_apikey()
    return "https://api.phish.net/v3/setlists/get?apikey="+apikey+"&showid="+str(show_id)

def get_show_ids(year):
    apikey = get_apikey()
    return "https://api.phish.net/v3/shows/query?apikey="+apikey+"&year="+str(year)+"&order=DESC"

class SetlistHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_tag = None
        self.current_set = None
        self.setlists = {}

    def handle_starttag(self, tag, attrs):
        self.inside_tag = tag

    def handle_endtag(self, tag):
        self.inside_tag = None

    def handle_data(self, data):
        if self.inside_tag == 'span':
            self.setlists[data] = []
            self.current_set = data
        elif self.inside_tag == 'a':
            self.setlists[self.current_set].append(data)
        elif self.inside_tag is None:
            pass

def shows_for_year(year, artist='Phish'):
    """ Issue a request to the API to find the set of shows that
were performed in a given year by some artist (default is Phish).
The result is a list of (showID, tour name) pairs.
"""
    shows = []
    resp = (requests.get(get_show_ids(year)).json())['response']
    for show in resp['data']:
        if show['billed_as'] == artist:
            shows.append((show['showid'], show['tourname']))
    return shows

def parse_show(db, show):
    (showid, tourname) = show

    if showid in db.shows:
        print('show already known')
        return

    print("getting: "+str(show))

    resp = (requests.get(get_show_string(showid)).json())['response']
    if resp['count'] == 1:
        parser = SetlistHTMLParser()
        parser.feed(resp['data'][0]['setlistdata'])

        date = resp['data'][0]['showdate']
        rating = resp['data'][0]['rating']
        location = resp['data'][0]['location']

        s = Show(showid, tourname, date, rating, location)

        for setname in parser.setlists:
            setlist = []
            for song in parser.setlists[setname]:
                setlist.append(db.register_song(song))
            s.add_set(setname, setlist)
        db.add_show(s)
    else:
        print(resp)

########################################################################

def load_database(db_file):
    """
Load an existing database file or return a fresh empty
database if no file found.
"""
    f = Path(db_file)
    if f.is_file():
        filehandle = open(db_file, 'rb')
        db = pickle.load(filehandle)
        filehandle.close()
    else:
        db = Database()
    return db

def save_datebase(db_file, db):
    """ Serialize the database object to the given filename. """
    filehandle = open(db_file, 'wb')
    pickle.dump(db, filehandle)
    filehandle.close()

phish_artists = [
    'Phish',
    'Vida Blue',
    'Page McConnell',
    'Trey Anastasio',
    'Trey Anastasio & Don Hart',
    'Trey, Mike and The Duo',
    'The Dude of Life (with Phish)',
    'Mike Gordon',
    'Mike Gordon and Leo Kottke',
    'Ghosts of the Forest',
    'Amfibian']

def get_originals():
    res = pd.read_html('http://phish.net/song/')
    df = res[0]
    return sum([list(df[df['Original Artist'] == a]['Song Name']) for a in phish_artists], [])
