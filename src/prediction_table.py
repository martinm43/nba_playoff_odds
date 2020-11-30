"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django

"""

#Future import first


from nba_database.nba_data_models import ProApiTeams as Team
from datetime import datetime, timedelta

from pprint import pprint

def playoff_odds_calc(start_datetime, end_datetime, season_year,input_predict_date=None,input_season_year=None,auto='ON'):
        #Standard imports
        #from pprint import pprint
        #Third party imports
        #Library imports
        from predict.cython_mcss.mcss_ext2 import simulations_result_vectorized
        from analytics.SRS import SRS
        from analytics.morey import SRS_regress

        from nba_database.queries import games_query, games_won_query, future_games_query
        
        import numpy as np

        #Test results/inputs
        if end_datetime < start_datetime:
            print("Start date is after end date, please check inputs")
            return 1
        
        if auto == 'OFF':
            predict_date = input_predict_date
            predict_season_year = input_season_year
        elif auto == 'ON':
            predict_date = end_datetime
            predict_season_year = season_year
        else:
            print('Input for auto mode not valid')
            return 1

        # Get List Of Known Wins
        games_list = games_query(start_datetime,end_datetime)
        games_won_list_cpp = games_won_query(games_list,return_format="matrix").tolist()

        if auto == 'OFF':
            gwl = np.zeros((30,30))
            games_won_list_cpp = gwl.tolist()

        # Get Team Ratings (and create Team object list)
        ratings_list=SRS(games_query(start_datetime,end_datetime)).tolist() #get ratings for that time.
        #pprint(ratings_list)
        teams_list=Team.select().order_by(Team.bball_ref)
        teams_list=[[x.bball_ref, x.team_name, x.abbreviation,\
                            x.division, x.conf_or_league] for x in teams_list]
        for i, x in enumerate(teams_list):
            x.append(ratings_list[i])
            for j in range(1,5): #"all strings"
                x[j] = x[j].encode('utf-8')
                #print(type(x[j]))
        #pprint(teams_list)
 
        #Get future games (away_team, home_team, home_team_win_probability)
        #print(predict_date)
        #print(predict_season_year)
        future_games_list = future_games_query(predict_date, predict_season_year)
        for x in future_games_list:
            away_team_rating=teams_list[x[0]-1][5]
            home_team_rating=teams_list[x[1]-1][5]
            SRS_diff=home_team_rating-away_team_rating
            x.append(SRS_regress(SRS_diff))
        #pprint(future_games_list)
        
        #CALL THE FUNCTION!
        #pprint(games_won_list_cpp)
        #pprint(future_games_list)
        #pprint(teams_list)
        team_results = simulations_result_vectorized(games_won_list_cpp, future_games_list, teams_list)
        #pprint(team_results)
        team_results = [[x[0]*100.0, x[1]] for x in team_results]
        return team_results
    
def playoff_odds_print(team_results):
    """
    Prints table based on alphabetically ordered team results matrix
    """
    #Custom local function for formatting
    from tabulate import tabulate
    def format_percent(percent_float):
        return str(percent_float) + '%'
    #Format the results into a table
    teams = Team.select().order_by(Team.bball_ref)
    
    teams_dict = [
        dict(list(zip(['Team', 'Conference'], [i.abbreviation, i.conf_or_league]))) for i in teams]
    
    for i, d in enumerate(teams_dict):
        d['Avg. Wins'] = round(team_results[i][1], 1)
        d['Playoff %'] = round(team_results[i][0], 1)
        # Convert into percentages for printing
        d['Playoff %'] = format_percent(d['Playoff %'])
    
    teams_dict.sort(key=lambda x: (x['Conference'], -x['Avg. Wins']))
    
    team_tuples = [
        (d['Conference'],
         d['Team'],
         d['Avg. Wins'],
         d['Playoff %']) for d in teams_dict]
    
    results_table = tabulate(
        team_tuples,
        headers=[
            'Conference',
            'Team',
            'Avg. Wins',
            'Playoff %'],
        tablefmt='rst',
        numalign='left')
    return results_table


#Print your results:

if __name__=="__main__":

    start_datetime = datetime(1994,10,22) #start of season
    end_datetime = datetime(1994,12,1) #a few weeks or months in
    #in-season option: end_datetime = datetime.today()-timedelta(days=1)
    season_year = 1995 #year in which season ends

    results = playoff_odds_calc(start_datetime, end_datetime, season_year)
    results_table = playoff_odds_print(results)

    print("Playoff odds for the "+str(season_year)+" season as of "+end_datetime.strftime("%b %d %Y"))
    print(results_table)
    print("Note that in 2014 and earlier, division winners were automatically given a top-four seed\n"+\
          "and home court advantage for the first round. That logic has not yet been implemented in this progam")

