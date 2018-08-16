update nba_team_elo_data
set bball_ref_id=
(select t.bball_ref_id 
from pro_api_teams as t 
where nba_team_elo_data.team_abbreviation=t.abbreviation)