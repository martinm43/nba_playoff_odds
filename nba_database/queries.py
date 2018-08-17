#-*-coding:utf8;-*-
#qpy:2
#qpy:console

#Choose working directory.
from nba_data_models import BballrefScores
import time, datetime

def epochtime(str_time):
  """
  Convert time in MON DAY YEAR format to a UNIX timestamp
  """
  datetime_obj=datetime.datetime.strptime(str_time,"%b %d %Y")
  return time.mktime(datetime_obj.timetuple())

def games_query(start_datetime,end_datetime,return_format="list"):
    """
    Returns the number of games won to date in either a straight
    numerical list, a list of dicts, or a head to head matrix
    """
    played_games = Game.select().where(
        Game.scheduled_date < end_datetime,
        Game.scheduled_date > start_datetime).order_by(Game.scheduled_date)

    played_games = [[g.away_team, g.away_runs, g.home_team, g.home_runs]
                    for g in played_games]
    winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
    winrows = []
    if return_format == 'list_of_lists':
        winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
        winrows = []
        for i in range(1, 31):
            winrows.append([winlist.count(i)])
        return_value = winrows
    elif return_format == 'list':
        winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
        winrows = []
        for i in range(1, 31):
            winrows.append(winlist.count(i))
        return_value = winrows
    elif return_format == 'matrix':
        win_matrix = np.zeros((30, 30))
        for x in played_games:
            if x[1] > x[3]:
                win_matrix[x[0] - 1, x[2] - 1] += 1
            elif x[3] > x[1]:
                win_matrix[x[2] - 1, x[0] - 1] += 1
        return win_matrix
    else:
        print('invalid option')
        return_value = 0
    return return_value

"""
