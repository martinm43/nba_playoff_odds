select count(*) from bballref_scores as b, 
proline_data as p where 
p.away_pts=b.away_pts and 
p.home_pts=b.home_pts and 
p.away_team_id=b.away_team_id and 
b.home_team_id=p.home_team_id and 
abs(b.datetime-p.unix_date)<172800; --within 48 h
