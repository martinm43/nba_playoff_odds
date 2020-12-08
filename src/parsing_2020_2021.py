from datetime import datetime
from nba_database.nba_data_models import ProApiTeams
from nba_database.queries import full_name_to_id

file1 = open("december_schedule.txt","r")
Lines = file1.readlines()
days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

count = 1
        
for line in Lines:
    line = line.strip()
    
    #set the days
    for d in days:
        if d in line:
            print(line)
            date_object = datetime.strptime(line+" 2020","%A, %B %d %Y")
            print(date_object)
            
    #set home and away teams, away is always first
    if(full_name_to_id(line)>0):
        if count % 2 == 1:
            print("Away Team")
            print(full_name_to_id(line))
            count+=1
        else:
            print("Home Team")
            print(full_name_to_id(line))
            count+=1

    

