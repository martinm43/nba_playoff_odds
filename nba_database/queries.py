#-*-coding:utf8;-*-
#qpy:2
#qpy:console

#Choose working directory.
from nba_data_models import BballrefScores as Game
import time, datetime

def epochtime(str_time):
  """
  Convert time in MON DAY YEAR format to a UNIX timestamp
  """
  datetime_obj=datetime.datetime.strptime(str_time,"%b %d %Y")
  return time.mktime(datetime_obj.timetuple())

def games_query(start_datetime,end_datetime):
    """
    Input: datetime objects
    Output: [away_team, away_pts, home_team, home_pts] list
    """
    start_epochtime=time.mktime(start_datetime.timetuple())
    end_epochtime=time.mktime(end_datetime.timetuple())
    played_games = Game.select().where(
        Game.datetime < end_epochtime,
        Game.datetime > start_epochtime).order_by(Game.datetime)

    played_games = [[g.away_team_id, g.away_pts, g.home_team_id, g.home_pts]
                    for g in played_games]
    return played_games

def team_abbreviation(team_alphabetical_id):
    """
    Converts team numerical ids into team names.
    """
    from nba_data_models import ProApiTeams
    s_query = ProApiTeams.select(ProApiTeams.abbreviation).\
      where(ProApiTeams.bball_ref == team_alphabetical_id)
    s_result = s_query[0]
    return s_result.abbreviation

