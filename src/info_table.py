
#Standard imports
import sys
from datetime import datetime, timedelta
from pprint import pprint
#Third Party Imports
from tabulate import tabulate
#Query imports
from nba_database.queries import games_query, team_abbreviation, games_won_query, epochtime
from nba_database.nba_data_models import BballrefScores as Game
#Analytics imports
from analytics.SRS import SRS
from analytics.pythag import pythagorean_wins, league_pythagorean_wins
#Wins script import
from analytics.wins_script import get_wins

#Query Testing
start_datetime = datetime(2019,10,1)
end_datetime = datetime.today()-timedelta(days=1)
season_year = 2020
#start_datetime_str = input('Please enter the start date in %b %d %Y format, e.g. Oct 1 2010): ')
#end_datetime_str = input('Please enter the end date in %b %d %Y format, e.g. May 1 2011): ')
#season_year_str = input('Please enter the season year (e.g. 2011): ')


#try:
#    start_datetime = datetime.strptime(start_datetime_str,'%b %d %Y')
#    end_datetime = datetime.strptime(end_datetime_str,'%b %d %Y')
#    season_year = int(season_year_str)
#except ValueError:
#    print('Error parsing entered values. Please review dates and season year entered.')
#    sys.exit(1)


games_list=games_query(start_datetime,end_datetime)

#Custom SRS calculation options
max_MOV = 100 # no real max MOV
home_team_adv = 0
win_floor = 0

wins_dict_list = [get_wins(i,season_year,start_datetime,end_datetime) for i in range(1,31)]
wins_list = [[x['away_record'],x['home_record'],x['record']] for x in wins_dict_list] 

#Pythagorean Wins
lpw_results = league_pythagorean_wins(Game,mincalcdatetime=epochtime(start_datetime),\
            maxcalcdatetime=epochtime(end_datetime))

srs_list = SRS(games_list, max_MOV = max_MOV, home_team_adv = home_team_adv, win_floor = win_floor)

lpw_results.sort(key = lambda x:x[0])

#results = zip(lpw_results,srs_list)
results = list(zip(lpw_results,srs_list,wins_list))

results = [[x[0][0],x[0][1],x[1],x[2][0],x[2][1],x[2][2]] for x in results]

results_tuples = [(team_abbreviation(x[0]),round(x[1],0),round(x[2]*100.0/100.0,3),\
                   x[3],x[4],x[5]) for x in results]

results_tuples.sort(key = lambda x: x[5])

results_table = tabulate(
        results_tuples,
        headers=[
            'Team',
            'Pythag. Wins',
            'Est. SRS',
            'Away Record',
            'Home Record',
            'Overall Record'],
        tablefmt='rst',
        numalign='left')

print("Pythagorean Win Expectations, Est. SRS, and Records \n"+\
        "Based on Games Played Between: "+start_datetime.strftime('%b %d %Y')+\
        " and "+end_datetime.strftime('%b %d %Y'))
print(results_table)
