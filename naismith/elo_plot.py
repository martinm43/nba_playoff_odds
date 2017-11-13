#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Quick script for plotting calculated ELO ranking for teams

Created on Wed Nov  8 19:58:43 2017

"""

from dbtools.nba_data_models import NbaTeamEloData
import matplotlib.pyplot as plt

team_abbreviation = 'GSW'
season_year=2017

query=NbaTeamEloData.select().where(NbaTeamEloData.team_abbreviation == team_abbreviation, \
                             NbaTeamEloData.season_year == season_year)

query_y=[i.elo_rating for i in query]
query_x=[i.datetime for i in query]

plt.plot(query_x,query_y)

#Team two
team_abbreviation = 'TOR'

query=NbaTeamEloData.select().where(NbaTeamEloData.team_abbreviation == team_abbreviation, \
                             NbaTeamEloData.season_year == season_year)

query_y=[i.elo_rating for i in query]
query_x=[i.datetime for i in query]

plt.plot(query_x,query_y)

#Team three
team_abbreviation = 'PHI'

query=NbaTeamEloData.select().where(NbaTeamEloData.team_abbreviation == team_abbreviation, \
                             NbaTeamEloData.season_year == season_year)

query_y=[i.elo_rating for i in query]
query_x=[i.datetime for i in query]

plt.plot(query_x,query_y)

plt.title('Team Performances over '+str(season_year))
plt.ylabel('ELO rating')
plt.xlabel('Date')
plt.axis([min(query_x),max(query_x),0,2000])
plt.legend(('GSW','TOR','PHI'))
plt.show()