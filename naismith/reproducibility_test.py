from platform import platform
from access_nba_data import epochtime
from srscalc import srs_month_since_date

date='May 1'
year='2016'
year_srs_date=date+' '+year

epoch_srs_date=epochtime(year_srs_date)

a=srs_month_since_date(epoch_srs_date,no_months=12)

#Report results in a text file
text_file=open('srstest'+'_'+platform()+'+_2ndrun.txt','w')

text_file.write('Test was conducted on platform '+platform()+'\n')
text_file.write('NBA year is: '+year+'\n')
for i in a:
    text_file.write('Team id '+str(i['team_id'])+' had a srs of '+str(i['srs'])+'\n')
text_file.close()