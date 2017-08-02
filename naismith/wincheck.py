# coding: utf-8
# %load srs_check
from access_nba_data import epochtime
from srscalc import srs_month_since_date
# %load srs_check
from access_nba_data import epochtime
from srscalc import srs_month_since_date
srs_month_since_date(epochtime('May 1 1997'),no_months=12)
srs_month_since_date(epochtime('May 1 2007'),no_months=12)
srs_month_since_date(epochdate('Oct 1 2007'),no_months=12)
from access_nba_data import epochdate
from access_nba_data import epochtime
srs_month_since_date(epochdate('Oct 1 2007'),no_months=12)
from access_nba_data import games_query
test_games_array=games_query(epochtime('Oct 1 2014'),epochtime('Oct 1 2015'))
winlist=[]
for i in test_games_array:
    if i[1]>i[3]:
        winlist.append(i[0])
    else:
        winlist.append(i[2])

for i in range(1,31):
    print(winlist.count(i))
    
winlist_totals=[]
for i in range(1,31):
    winlist_totals.append(i)
    
    
winlist_totals
del(winlist_totals)
winlist_totals=[]
for i in range(1,31):
    winlist_totals.append(winlist.count(i))
winlist_totals
