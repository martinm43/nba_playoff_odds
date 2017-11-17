select b.id,b.away_pts-b.home_pts,
(select elo_rating from nba_team_elo_data 
		where b.datetime=nba_team_elo_data.datetime
		and b.away_team_id=nba_team_elo_data.bball_ref_id
		and elo_rating <> 1500) -
(select elo_rating from nba_team_elo_data 
		where b.datetime=nba_team_elo_data.datetime
		and b.home_team_id=nba_team_elo_data.bball_ref_id
		and elo_rating <> 1500)
from bballref_scores as b limit 10000;
--takes a very long time to run as written, but works as intended.
