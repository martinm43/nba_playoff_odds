select 
bballref.away_pts-bballref.home_pts, 
burke.burke_ranking-burke2.burke_ranking 
from bballref_scores as bballref 
join burke_calc_data as burke,  
burke_calc_data as burke2 on 
burke.team = bballref.away_team_id 
and burke2.team = bballref.home_team_id 
and abs(burke.date - bballref.datetime)<86400;
