#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 21:41:02 2020

@author: martin
"""

import matplotlib.pyplot as plt

from nba_database.queries import prettytime
from nba_database.nba_data_models import NbaTeamEloData

season_year = 2007
abbrev = "CLE"

x = NbaTeamEloData.select().where(NbaTeamEloData.team_abbreviation == abbrev)
ratings = [z.elo_rating for z in x]
date = [prettytime(z.datetime) for z in x]
plt.plot(date,ratings)
plt.xlabel('Date')
plt.ylabel('Elo Rating')
plt.title('Historical Elo Rating of '+abbrev)
 