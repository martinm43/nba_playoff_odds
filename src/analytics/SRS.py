def SRS(game, printing=False, max_MOV=100.0, home_team_adv=0.0, win_floor=0.0):
    """

    Inputs:

    game = list of games in standard format away_team,away_pts,home_team,home_pts
    impmode = file importation mode
    printing = debug printing optional
    max_MOV = maximum margin of victory
    home_team_adv = presumed home team advantage



    Outputs:
    An array of team ratings in the alphabetical order corresponding to the overall league.
    E.G in the NBA: ATL ... WAS

    """

    import math
    import datetime
    from pprint import pprint

    import csv
    import numpy
    import scipy.optimize

    game = [[g[2], g[0], g[3], g[1]] for g in game]
    # list of game,home,away,homescore,awayscore
    numGames = len(game)
    numTeams = 30

    # Now, we have the NFL teams for 2002 and data on all games played.
    # From this, we wish to forecast the score of future games.
    # We are going to assume that each team has an inherent performance-factor,
    # and that there is a bonus for home-field advantage; then the
    # relative final score between a home team and an away team can be
    # calculated as (home advantage) + (home team factor) - (away team factor)
    # First we create a matrix M which will hold the data on # who played whom
    # in each game and who had home-field advantage.
    m_rows = numTeams + 1
    m_cols = numGames
    M = numpy.zeros((m_rows, m_cols))
    # Then we create a vector S which will hold the final # relative scores
    # for each game.
    s_cols = numGames
    S = numpy.zeros(s_cols)
    # Loading M and S with game data
    for col, gamedata in enumerate(game):
        gameNum = col
        home, away, homescore, awayscore = gamedata
        # In the csv data, teams are numbered starting at 1
        # So we let home-team advantage be 'team 0' in our matrix
        M[0, col] = 1.0
        M[int(home), col] = 1.0
        M[int(away), col] = -1.0

        diff_score = int(homescore) - int(awayscore)
        if diff_score > max_MOV:
            diff_score = max_MOV
        elif diff_score < -max_MOV:
            diff_score = -max_MOV
        # Granting a bonus based on "actually winning the game". This is intended to account
        # for teams like Cleveland or GSW that can "win games when it counts". A crude adjustment
        # for teams with significantly different talent levels from other
        # teams.
        if diff_score > 0:  # bonuses for a win
            diff_score = max(win_floor, diff_score)
        else:  # demerits for a loss
            diff_score = min(-win_floor, diff_score)
        S[col] = diff_score

    # Now, if our theoretical model is correct, we should be able # to find a performance-factor vector W such that W*M == S
    #
    # In the real world, we will never find a perfect match,
    # so what we are looking for instead is W which results in S'
    # such that the least-mean-squares difference between S and S'
    # is minimized.

    init_W = numpy.array([home_team_adv] + [0.0] * numTeams)

    def errorfn(w, m, s):
        return w.dot(m) - s

    W = scipy.optimize.leastsq(errorfn, init_W, args=(M, S))
    homeAdvantage = W[0][0]

    teamStrength = W[0][1:]
    # Team strengths have meaning only by linear comparison;
    # we can add or subtract any constant to all of them without
    # changing the meaning.
    # To make them easier to understand, we want to shift them
    # such that the average is 0.0
    teamStrength -= teamStrength.mean()
    teamStrength.tolist()
    if printing == True:
        for t in enumerate(teamStrength):
            print(
                (
                    "Team "
                    + str(t[0] + 1)
                    + " has a calculated Burke Score of "
                    + str(t[1])
                )
            )
    return teamStrength
