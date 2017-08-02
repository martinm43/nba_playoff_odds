# coding: utf-8
get_ipython().magic(u'load srs_check')
# %load srs_check
from access_nba_data import epochtime
from srscalc import srs_month_since_date
srs_month_since_date(epochtime('May 1 1997'),no_months=12)
srs_month_since_date(epochtime('May 1 2007'),no_months=12)
srs_month_since_date('Oct 1 2007',no_months=12)
srs_month_since_date(epochdate('Oct 1 2007'),no_months=12)
# %load srs_check
from access_nba_data import epochtime
from srscalc import srs_month_since_date
srs_month_since_date(epochtime('May 1 1997'),no_months=12)
srs_month_since_date(epochtime('May 1 2007'),no_months=12)
srs_month_since_date(epochdate('Oct 1 2007'),no_months=12)
from access_nba_data import epochdate
from access_nba_data import epochtime
srs_month_since_date(epochdate('Oct 1 2007'),no_months=12)
srs_month_since_date(epochtime('Oct 1 2007'),no_months=12)
srs_month_since_date(epochtime('Oct 1 2007'),no_months=11)
srs_month_since_date(epochtime('Oct 1 2007'),no_months=10)
srs_month_since_date(epochtime('May 1 2007'),no_months=10)
srs_month_since_date(epochtime('May 1 2015'),no_months=10)
from access_nba_data import games_query
games_query(epochtime('Oct 1 2014'),epochtime('Oct 1 2015'))
test_games_array=games_query(epochtime('Oct 1 2014'),epochtime('Oct 1 2015'))
test_games_array
type(test_games_array)
for i in test_games_array:
    print i
    
for i in test_games_array:
    print i[0]
    
    
winlist=[]
for i in test_games_array:
    if i[1]>i[3]:
        winlist.append(i[0])
    else
        winlist.append(i[2])

    
for i in test_games_array:
    if i[1]>i[3]:
        winlist.append(i[0])
    else:
        winlist.append(i[2])

    
winlist.count(30)
for i in range(1,31):
    print(winlist.count(i))
    
winlist_totals=[]
for i in range(1,31):
    winlist_totals.append(i)
    
    
winlist_totals
del(winlist_totals)
for i in range(1,31):
    winlist_totals.append(winlist.count(i))
    
    
    
winlist_totals=[]
for i in range(1,31):
    winlist_totals.append(winlist.count(i))
    
    
    
winlist_totals
get_ipython().magic(u'save wincheck 1-35')
