"""
Dump the database to CSV files: the list of shows with songs listed by
ID, and a song table mapping song ID to name.  Analysis is much easier
for shows with songs listed as IDs not strings.
"""
import api

db_file = "phishdb.pickle"
db = api.load_database(db_file)

with open("songs.csv","w") as f_out:
  for s in db.songs_by_id:
    x = f"{str(s)},\"{db.songs_by_id[s].name}\"\n"
    f_out.write(x)

with open("shows.csv","w") as f_out:
  for s in db.shows:
    show = db.shows[s]
    prefix = f"{str(s)},{str(show.date)}"
    for setname in show.sets:
      ids = ",".join([str(i) for i in show.sets[setname]])
      x = f"{prefix},\"{setname}\",{ids}\n"
      f_out.write(x)
