# coding: utf-8
from access_nba_data import epochtime
from srscalc import srs_month_since_date
srs_month_since_date(epochtime('May 1 1997'),no_months=12)
srs_month_since_date(epochtime('May 1 2007'),no_months=12)
