def team_abbreviation(team_alphabetical_id):
  """ This program converts team alphabetical ids into team abbreviations. e.g. 1 -> ATL"""
  from dbtools.nba_data_models import ProApiTeams
  s=ProApiTeams.select(ProApiTeams.abbreviation).where(ProApiTeams.bball_ref==team_alphabetical_id)
  i=s[0]
  return i.abbreviation

if __name__=="__main__":
  for i in range(1,31):
    print('Team '+str(i)+' is team '+team_abbreviation(i))
