import api

# assumes the database has already been cached
db_file = "phishdb.pickle"
db = api.load_database(db_file)

# simple query: count all shows with at least two sets, and track all
# that have less set 1 songs than set 2 songs
data = []
count = 0
for _,s in db.shows.items():
    if 'Set 1' in s.sets and 'Set 2' in s.sets:
        s1 = s.sets['Set 1']
        s2 = s.sets['Set 2']
        if len(s1) < len(s2):
            data.append((s.date, len(s1), len(s2)))
        count += 1

# print count and proportion
print(len(data))
print(len(data)/count)
