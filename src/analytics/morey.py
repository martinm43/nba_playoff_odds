"""
Logistic functions that take differences
in calculated analytical values (Elo and SRS)
and returns a one-game probability of
winning.

"""


def Elo_regress(dElo):
    """


    Parameters
    ----------
    dElo : difference in elo rating, defined as "home versus away".

    Returns
    -------
    the odds of the home team beating the away team.

    Define the binomial odds of the home team winning using the formula
    We = 1/(10^z+1)
    where We is the win expectancy
    and z is equal to -1*(delta+h)/F
    where F is a scaling factor for Elo
    and h is the home field advantage between two neutral teams.

    Solve for the cases where
    1) delta is zero, and home field advantage is some given % based on
    historical data
    2) delta is a large Elo difference, and the expected win percentage is high
    to obtain the coefficients that are used below.

    """
    max_elo_diff = 400
    f = max_elo_diff / 1.10266
    h = 0.17609 * f  # this value comes from 60% HFA, or h = -log(1/0.6-1)
    return 1 / (1 + 10 ** ((-1 * (dElo + h) / f)))


def SRS_regress(dSRS):

    """
    See analysis performed for Elo_regress.
    """
    import math

    max_srs_diff = 20  # should be nominally 15, but has to be tuned for 'sanity check'
    f = max_srs_diff / 2.539
    h = 0.405465 * f
    return 1 / (1 + math.exp(-1 * (h + dSRS) / f))  # .3


if __name__ == "__main__":
    max_delo = 400
    print(Elo_regress(max_delo))
    max_dsrs = 15
    print(SRS_regress(max_dsrs))
