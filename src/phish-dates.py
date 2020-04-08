"""
Pre-defined date ranges for different interesting phases in Phish
time.
"""
from datetime import date

#
# major eras
#
era_1 = ('1983-01-01', '2000-12-31')
era_2 = ('2002-01-01', '2004-12-31')
era_3 = ('2009-01-01', '2030-01-01')

#
# festivals
#
fest_clifford_ball = ('1996-08-16', '1996-08-17')
fest_great_went    = ('1997-08-16', '1997-08-17')
fest_lemonwheel    = ('1998-08-15', '1998-08-16')
fest_camp_oswego   = ('1999-07-17', '1999-07-18')
fest_big_cypress   = ('1999-12-30', '1999-12-31')
fest_it            = ('2003-08-02', '2003-08-03')
fest_coventry      = ('2004-08-13', '2004-08-15')
fest_festival_8    = ('2009-10-30', '2009-11-01')
fest_super_ball    = ('2011-07-01', '2011-07-03')
fest_magnaball     = ('2015-08-21', '2015-08-23')

festivals = [fest_clifford_ball, fest_great_went, fest_lemonwheel,
             fest_camp_oswego, fest_big_cypress, fest_it,
             fest_coventry, fest_festival_8, fest_super_ball,
             fest_magnaball]

#
# halloweens
#
halloween_beatles            = ('1994-10-31', '1994-10-31')
halloween_who                = ('1995-10-31', '1995-10-31')
halloween_talking_heads      = ('1996-10-31', '1996-10-31')
halloween_velvet_underground = ('1998-10-31', '1998-10-31')
halloween_rolling_stones     = ('2009-10-31', '2009-10-31')
halloween_little_feat        = ('2010-10-31', '2010-10-31')
halloween_wingsuit           = ('2013-10-31', '2013-10-31')
halloween_disney             = ('2014-10-31', '2014-10-31')
halloween_david_bowie        = ('2016-10-31', '2016-10-31')
halloween_kasvot_vaxt        = ('2018-10-31', '2018-10-31')

halloweens = [halloween_beatles, halloween_who, halloween_talking_heads,
              halloween_velvet_underground, halloween_rolling_stones,
              halloween_little_feat, halloween_wingsuit, halloween_disney,
              halloween_david_bowie, halloween_kasvot_vaxt]

#
# notable tours
#
bakers_dozen = ('2017-07-21', '2017-08-06')
island_tour = ('1998-04-02', '1998-04-05')

#
# dates
#
def between_dates(lo,hi):
    dlo = date.fromisoformat(lo)
    dhi = date.fromisoformat(hi)

    def f(show):
        d = date.fromisoformat(show.date)
        if dlo<=d and d<=dhi:
            return True
        else:
            return False
    return f

def between_many_dates(ds):
    tests = []
    for (lo,hi) in ds:
        tests.append(between_dates(lo,hi))
        
    def f(show):
        return any([t(show) for t in tests])
    return f
