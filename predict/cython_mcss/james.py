"""
Regression functions for calculating
binomial win percentages

Named after the pioneer Bill James.

"""
from __future__ import print_function, division

# Selection of mathematical models for MLB win predictions


def runs_regress(dpts):
    """
    Performs regression based on team run differential'
    """
    import math
    return 1 / (1 + math.exp(-1 * (0.15 + dpts * 0.2)))


def SRS_regress(dSRS, dSRS_coeff=0.15):
    """
    Performs regression based on team 'SRS' incorporating strength of schedule
    """
    import math
    return 1 / (1 + math.exp(-1 * (-0.15 + dSRS * dSRS_coeff)))


if __name__ == '__main__':
    print(SRS_regress(2))
