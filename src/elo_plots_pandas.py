import pandas as pd
import sqlite3

conn = sqlite3.connect('population.db')
query = "SELECT country FROM Population WHERE population > 50000000;"

df = pd.read_sql_query(query,conn)

for country in df['country']:
    print(country)
