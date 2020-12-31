"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django

"""

#Future import first


from nba_database.nba_data_models import ProApiTeams as Team
from nba_database.queries import elo_ratings_list,epochtime
from datetime import datetime, timedelta

from pprint import pprint

def playoff_odds_calc(start_datetime, end_datetime, season_year,\
                      input_predict_date=None,input_season_year=None,\
                          zero_out_wins=False,ratings_mode="Elo"):
        """
    
        Given a start, end, season_year, and a ratings calculation method 
        with some other factors, determine the odds of every team of making
        the playoffs at any given time.

        Parameters
        ----------
        start_datetime : start of period to be used for analysis (Unix timestamp)
        end_datetime : end of period to be used for analysis (Unix timestamp)
        season_year : year that season nominally ends in
                    (e.g. if season ends in 2021, use 2021)
        input_predict_date : to be deprecated
        input_season_year : to be deprecated
        zero_out_wins : to be deprecated
        ratings_mode : Elo or SRS. Default mode is Elo.
    
        Returns
        -------
        a list of 2-item lists for each team (first item ATL, last item WAS)
        each list consists of [playoff odds,average wins]

        """
        #Standard imports
        #from pprint import pprint
        #Third party imports
        #Library imports
        from predict.cython_mcss.mcss_ext2 import simulations_result_vectorized
        from analytics.SRS import SRS
        from analytics.morey import SRS_regress, Elo_regress

        from nba_database.queries import games_query, games_won_query, future_games_query
        
        import numpy as np

        #Test results/inputs
        if end_datetime < start_datetime:
            print("Start date is after end date, please check inputs")
            return 1
        
        if zero_out_wins == True:
            predict_date = input_predict_date
            predict_season_year = input_season_year
        elif zero_out_wins == False:
            predict_date = end_datetime
            predict_season_year = season_year
        else:
            print('Input for auto mode not valid')
            return 1

        # Get List Of Known Wins
        games_list = games_query(start_datetime,end_datetime)
        games_won_list_cpp = games_won_query(games_list,return_format="matrix").tolist()

        if zero_out_wins == True:
            gwl = np.zeros((30,30))
            games_won_list_cpp = gwl.tolist()
            
        #Get team data.
        teams_list=Team.select().order_by(Team.bball_ref)
        teams_list=[[x.bball_ref, x.team_name, x.abbreviation,\
                            x.division, x.conf_or_league] for x in teams_list]

        #Get future games (away_team, home_team, home_team_win_probability)
	
        future_games_list = future_games_query(predict_date, predict_season_year)
        

        if ratings_mode == "SRS":
            # Get Team Ratings (and create Team object list)
            ratings_list=SRS(games_query(start_datetime,end_datetime)).tolist() #get ratings for that time.
            
            for i, x in enumerate(teams_list):
                x.append(ratings_list[i])
                for j in range(1,5): #"all strings"
                    x[j] = x[j].encode('utf-8')
    
     
            for x in future_games_list:
                away_team_rating=teams_list[x[0]-1][5]
                home_team_rating=teams_list[x[1]-1][5]
                SRS_diff=home_team_rating-away_team_rating
                x.append(SRS_regress(SRS_diff))
                
        if ratings_mode == "Elo":
            ratings_list = elo_ratings_list(epochtime(end_datetime))
            for i, x in enumerate(teams_list):
                x.append(ratings_list[i])
                for j in range(1,5): #"all strings"
                    x[j] = x[j].encode('utf-8')
            
            for x in future_games_list:
                away_team_rating=teams_list[x[0]-1][5]
                home_team_rating=teams_list[x[1]-1][5]
                Elo_diff=home_team_rating-away_team_rating
                x.append(Elo_regress(Elo_diff))
        
        #Call the C++ module
        #What is passed to the C++ function?
        #A matrix of team wins against every other team - games_won_list_cpp
        #
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

    season_year = 1991 #year in which season ends
    start_datetime = datetime(season_year-1,10,15) #start of season
    end_datetime = datetime(season_year-1,11,1) #a few weeks or months in
    #in-season option: end_datetime = datetime.today()-timedelta(days=1)


    results = playoff_odds_calc(start_datetime, end_datetime, season_year,\
                                ratings_mode="Elo")
    results_table = playoff_odds_print(results)

    print("Playoff odds for the "+str(season_year)+" season as of "+end_datetime.strftime("%b %d %Y"))
    print(results_table)
    print("Note that in 2014 and earlier, division winners were automatically given a top-four seed\n"+\
          "and home court advantage for the first round. That logic has not yet been implemented in this progam")

    print("For 2020 please note that:\n"+ 
          "* Play-in tournament has also not yet been implemented.\n"+
          "* League is releasing schedule in two halves; first half has 37 games")
