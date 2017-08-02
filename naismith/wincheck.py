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

if __name__=="__main__":
    print(year_win_totals(2000))
    