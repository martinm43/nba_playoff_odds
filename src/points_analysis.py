#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 22:03:48 2020

@author: martin

Script for calculating what the "difference over sum" distribution looks like
for the NBA, for later use in mathematical modelling.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler

from nba_database.nba_data_models import BballrefScores

# not ignoring warnings
# warnings.filterwarnings("ignore")
min_val = 1990
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
mean = parameters[0]
stddev = parameters[1]

mean_str = "%.5f" % mean
stddev_str = "%.5f" % stddev

print("logistic mean: "+mean_str)
print("logistic stddev: "+stddev_str)

cdf_x = np.linspace(-0.3,0.3,300)
z_default = 2*stats.logistic.cdf(cdf_x,mean,stddev)-1
plt.plot(cdf_x,z_default)
