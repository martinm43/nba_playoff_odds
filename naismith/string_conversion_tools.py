"""
This module will contain scripts for converting team names.
Also a test of PEP conformance
"""

def team_abbreviation(team_alphabetical_id):
    """
    Converts team numerical ids into team names.
    """
    from dbtools.nba_data_models import ProApiTeams
    s_query = ProApiTeams.select(ProApiTeams.abbreviation).\
      where(ProApiTeams.bball_ref == team_alphabetical_id)
    s_result = s_query[0]
    return s_result.abbreviation

if __name__ == "__main__":
    for i in range(1, 31):
        print 'Team '+str(i)+' is team '+team_abbreviation(i)
