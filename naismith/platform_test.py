from platform import platform
from access_nba_data import epochtime
from srscalc import srs_month_since_date

date='May 1'
year='2016'
year_srs_date=date+' '+year

epoch_srs_date=epochtime(year_srs_date)

a=srs_month_since_date(epoch_srs_date)
print(a)
print(platform())
