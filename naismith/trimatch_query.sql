select * 
from bballref_scores as bbs 
inner join pro_api_games as pag, 
proline_data as pld on 
pag.away_score = bbs.away_pts and 
pag.home_score = bbs.home_pts and 
pag.away_score = pld.away_pts and 
pag.home_score = pld.home_pts and 
pag.season=pld.season and 
pag.season=bbs.season_year 
order by pag.id desc limit 30;