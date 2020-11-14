#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 22:03:48 2020

@author: martin
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler

from nba_database.nba_data_models import BballrefScores

# not ignoring warnings
# warnings.filterwarnings("ignore")
min_val = 2000
max_val = 2020

z = BballrefScores.select().where(BballrefScores.season_year >= min_val, BballrefScores.season_year < max_val)
mov = [x.home_pts-x.away_pts for x in z]
dos = [(x.home_pts-x.away_pts)/(x.home_pts+x.away_pts) for \
                 x in z if x.home_pts+x.away_pts > 0]

monitored_variable = pd.DataFrame(dos)

#description = monitored_variable.describe()
#print(description)

size = len(monitored_variable)

df_fit = np.asarray(monitored_variable)

dist_name = 'logistic'

#Fitting distribution
dist = getattr(stats,dist_name)
parameters = dist.fit(df_fit)

print(parameters)