#all thanks to StackOverflow!
#minor edits made

def burke_calc(game,impmode='bballref',printing='off'):
   
  import math
  import datetime
  from pprint import pprint

  import csv 
  import numpy 
  try:
    import scipy.optimize
  except:
    print('Cannot import scipy optimization module.')
    return 
  if impmode=='bballref':
      game=[[g[2],g[0],g[3],g[1]] for g in game]
  # list of game,home,away,homescore,awayscore 
  numGames = len(game)
  numTeams = 30
 
  # Now, we have the NFL teams for 2002 and data on all games played. 
  # From this, we wish to forecast the score of future games. 
  # We are going to assume that each team has an inherent performance-factor, 
  # and that there is a bonus for home-field advantage; then the 
  # relative final score between a home team and an away team can be 
  # calculated as (home advantage) + (home team factor) - (away team factor) 
  # First we create a matrix M which will hold the data on # who played whom in each game and who had home-field advantage. 
  m_rows = numTeams + 1 
  m_cols = numGames 
  M = numpy.zeros( (m_rows, m_cols) ) 
  # Then we create a vector S which will hold the final # relative scores for each game. 
  s_cols = numGames 
  S = numpy.zeros(s_cols) 
  # Loading M and S with game data 
  for col,gamedata in enumerate(game):
    #print(col)
    #print(gamedata)     
    gameNum=col
    home,away,homescore,awayscore = gamedata 
    # In the csv data, teams are numbered starting at 1 
    # So we let home-team advantage be 'team 0' in our matrix 
    M[0, col] = 1.0 # home team advantage 
    M[int(home), col] = 1.0 
    M[int(away), col] = -1.0 
    #December 29, 2016: Maximum and Minimum MOV logic.
    diff_score=int(homescore) - int(awayscore)
    max_MOV=9.0
    if diff_score >max_MOV:
        diff_score=max_MOV
    elif diff_score < -max_MOV:
        diff_score=-max_MOV
    S[col] = diff_score
    

  # Now, if our theoretical model is correct, we should be able # to find a performance-factor vector W such that W*M == S 
  # 
  # In the real world, we will never find a perfect match, 
  # so what we are looking for instead is W which results in S' 
  # such that the least-mean-squares difference between S and S' 
  # is minimized. 
  # Initial guess at team weightings: 
  # 2.0 points home-team advantage, and all teams equally strong 
  init_W = numpy.array([2.0]+[0.0]*numTeams) 

  def errorfn(w,m,s): 
    return w.dot(m) - s 
  
  W = scipy.optimize.leastsq(errorfn, init_W, args=(M,S)) 
  homeAdvantage = W[0][0] # 2.2460937500005356 
  teamStrength = W[0][1:] # numpy.array([-151.31111318, -136.36319652, ... ]) 
  # Team strengths have meaning only by linear comparison; 
  # we can add or subtract any constant to all of them without 
  # changing the meaning. 
  # To make them easier to understand, we want to shift them 
  # such that the average is 0.0 
  teamStrength -= teamStrength.mean() 
  teamStrength.tolist()
  if printing=='on':
      for t in enumerate(teamStrength):
          print('Team '+str(t[0]+1)+' has a calculated Burke Score of '+str(t[1]))
  return teamStrength
  
if __name__=='__main__':
  
  print('this is main')
  from access_nba_data import epochtime, games_query
  #get list of games in format "home,away,homescore,awayscore"
  #start_date=raw_input('Start date: ')
  #end_date=raw_input('End date: ')
  start_secs=epochtime('oct 1 2015')
  end_secs=epochtime('may 1 2016')
  gameslist=games_query(start_secs,end_secs)
  #pprint(gameslist)
  #list comprehend this into the format required by the program
  game=[[g[2],g[0],g[3],g[1]] for g in gameslist]
  print(len(game))
  burke_calc(game, impmode=None)
