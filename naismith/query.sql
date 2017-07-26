select case 
when away_standard_id=28 then away_pts-home_pts+2 
when home_standard_id=28 then home_pts-away_pts-2 
end 
from nba_py_api_data 
where (away_standard_id=28 or home_standard_id=28);
