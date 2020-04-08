"""
Update the database to download any missing shows over all time from
1980 to 2030.  This will stop being correct in around 10 years...
"""
import phishnet.api

db_file = "phishdb.pickle"

db = phishnet.api.load_database(db_file)

for year in range(1980,2030):
    #print(year)
    shows = api.shows_for_year(db, year)

    for show in shows:
        api.parse_show(db, show)
        api.save_datebase(db_file, db)
