# coding: utf-8
from prediction_table import playoff_odds_calc, playoff_odds_print
from datetime import datetime

start_datetime=datetime(2017,10,1) #start of data gathering period
end_datetime=datetime(2018,1,1) #end of data gathering period
season_year=2018 #year where data is gathered
input_predict_date=datetime(2016,1,23) #when to start the season being predicted
input_season_year=2017 #the season being predicted

results=playoff_odds_calc(start_datetime,end_datetime,\
        season_year,input_predict_date=input_predict_date,\
        input_season_year=input_season_year,auto='OFF')

results_table = playoff_odds_print(results)
print("Playoff odds for the "+str(season_year)+" season as of "+end_datetime.strftime("%b %d %Y"))
print(results_table)
print("Note that in 2014 and earlier, \n"+\
"division winners were automatically given a top-four seed\n"+\
          "and home court advantage for the first round. That logic has not yet been implemented in this progam")

    
