select b.id, b.away_team_id, b.away_pts-b.home_pts,
(select elo_rating from nba_team_elo_data 
	where b.datetime=nba_team_elo_data.datetime
	and b.away_team_id=nba_team_elo_data.bball_ref_id)
	from bballref_scores as b
	limit 5