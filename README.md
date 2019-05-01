# NBA Playoff Odds

A set of scripts to calculate ratings for teams, based on point differential
and strength of schedule, and then use those ratings to determine playoff odds
over a given season. 

Project structure - folders:
1. nba_database - access and process data, holds data model
2. analytics - perform analyses (SRS calculations and determining wins)
3. predictions - perform predictions, contains C++ monte carlo model
4. extract - for temporary extractions
and the nba_data.sqlite database (not hosted here as it is a binary file/exceeds Github individual size reqs, available on request)

Main scripts:

update_nba_api - use nba_api in order to access data from stats.nba.com for use

plot_season_odds - plots odds of getting to the playoffs, rolling across the season

prediction_table - produces basic table of instantaneous to that date playoff odds

info_table - shows basic home, away, wins, losses, and adjusted SRS



