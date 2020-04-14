# Phish.net Python API Interface

This is some Python code that I wrote for accessing the phish.net
API.  It implements client-side caching so that repeated data accesses
don't hammer the server excessively, and also makes it easier and faster to work
offline.  Note that caching the data has issues:

- Your cache may go silently stale if the server data is updated.
- You shouldn't share the cached data or make it available to others to
  avoid running afoul of the phish.net API usage rules.

# Usage

You need the requests package and pandas.  I recommend using Anaconda Python
which includes these.  Get an API key and set the PHISHNET_APIKEY environment
variable:

```
$ export PHISHNET_APIKEY='thekeyhere'
```

On the first run you should populate your cache.  Set your Python path to
make sure the code from this API can be found.  Assuming you are in the root
of the repository, just run:

```
$ export PYTHONPATH=$PYTHONPATH:`pwd`/src
```

Now, run the database updater:

```
$ python3 src/db_updater.py
```

You should get a pickled database that contains the cache.  You can then
run the examples:

```
$ python3 examples/simple.py
```

# Design

The goal of the library is to take data available on phish.net and
import it into a set of Python data structures for performing computations.
There are three simple objects involved:

## Shows

A show has:

- An ID
- A rating
- A location
- A tour
- A date
- A collection of sets

A show ID is a unique identifier as used by phish.net.  The rating,
location, and date are also drawn from the API.  These are left in the
form returned by the HTML parser (e.g., strings).  The setlist collection
is a dictionary where the keys are the setlist names (e.g., "Set 1")
and the values are ordered lists of songs.

## Songs

A song has:

- An ID
- A name

Songs are unfortunately not first-class objects like shows in the
phish.net database.  They are represented as strings in the setlist data
for shows.  As such, the code internally generates an identifier for
songs such that two songs sharing the same name map to the same ID.
The ID is maintained and generated by the Database object.

## Database

When querying the API, songs and shows are not returned directly.  Instead,
the query returns an instance of the database object.  This object is what
is serialized to disk for caching.

The database has:

- A dictionary of shows keyed by show ID
- A dictionary of songs keyed by name
- A dictionary of songs keyed by song ID

### Serialization

Serialization is performed in the simplest possible way - pickling.
Countless other methods exist (and even more opinions on them), but
the goal was simplicity and avoidance of dependencies.  Given that the
serialized database is intended solely to act as an opaque cache,
extensibility and interoperability with other tools is not a requirement.

### Why not a database?

I'd do SQLite since it's thin and trivial to install, and would support flexible queries.  For the purposes that this was originally created for, I went the route of least effort.  If enough people ask, I can map it to a proper SQLite DB for caching instead of piclking.

# Packaging (or lack thereof)

I don't use packages if I can avoid it.  If someone else wants to package the bits up, feel free to contribute.
