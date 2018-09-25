# coding: utf-8
from test_prediction_table import playoff_odds_calc, playoff_odds_print
from datetime import datetime
start_datetime=datetime(2018,2,1)
end_datetime=datetime(2018,5,1)
season_year=2018
input_predict_date=datetime(2017,10,1)
input_season_year=2018
results=playoff_odds_calc(start_datetime,end_datetime,\
        season_year,input_predict_date=input_predict_date,\
        input_season_year=input_season_year,auto='OFF')
results_table = playoff_odds_print(results)
print("Playoff odds for the "+str(season_year)+" season as of "+end_datetime.strftime("%b %d %Y"))
print(results_table)
print("Note that in 2014 and earlier, division winners were automatically given a top-four seed\n"+\
          "and home court advantage for the first round. That logic has not yet been implemented in this progam")

    
