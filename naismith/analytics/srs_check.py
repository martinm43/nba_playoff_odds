# coding: utf-8
def year_win_totals(year):
    from access_nba_data import epochtime, games_query
    test_games_array=games_query(epochtime('Oct 1 '+str(year-1)),epochtime('Oct 1 '+str(year)))
    winlist=[]
    for i in test_games_array:
        if i[1]>i[3]:
            winlist.append(i[0])
        else:
            winlist.append(i[2])
    
    for i in range(1,31):
        print(winlist.count(i))
        
    winlist_totals=[]
    for i in range(1,31):
        winlist_totals.append(i)
            
    winlist_totals
    del(winlist_totals)
    winlist_totals=[]
    for i in range(1,31):
        winlist_totals.append(winlist.count(i))
    return winlist_totals

def year_pts_for(year,ngames=82):
    import numpy as np
    from access_nba_data import epochtime, games_query
    test_games_array=games_query(epochtime('Oct 1 '+str(year-1)),epochtime('Oct 1 '+str(year)))
    ptslist=np.zeros(30)
    for i in test_games_array:
    	for j in range(0,30):
        	if i[0]==j+1:
            	   ptslist[j]+=i[1]
        	if i[2]==j+1:
            	   ptslist[j]+=i[3]
    return ptslist/ngames

def year_pts_against(year,ngames=82):
    import numpy as np
    from access_nba_data import epochtime, games_query
    test_games_array=games_query(epochtime('Oct 1 '+str(year-1)),epochtime('Oct 1 '+str(year)))
    ptslist=np.zeros(30)
    for i in test_games_array:
    	for j in range(0,30):
        	if i[0]==j+1:
            	   ptslist[j]+=i[3]
        	if i[2]==j+1:
            	   ptslist[j]+=i[1]
    return ptslist/ngames


if __name__=="__main__":
    from sys import argv
    print(year_win_totals(int(argv[1])))
    print(year_pts_for(int(argv[1])))
    print(year_pts_against(int(argv[1])))
    
