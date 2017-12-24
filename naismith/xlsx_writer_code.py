#Rieslings from Alsace with low sugar content and price
#MA Miller Apr 24 2016

import os
cwd=os.getcwd()+'/'

import sqlite3

conn=sqlite3.connect(cwd+'lcbo_db.sqlite')
c=conn.cursor()

#get query
str_input='SELECT name,sugar_in_grams_per_liter,volume_in_milliliters,price_in_cents FROM PRODUCTS WHERE secondary_category="White Wine"\
           AND origin like "%alsa%" \
           AND name like "%ries%" \
           ORDER BY sugar_in_grams_per_liter ASC, price_per_liter_in_cents ASC'
#run query    
data=c.execute(str_input).fetchall()

#Write an xlsx
import xlsxwriter
workbook=xlsxwriter.Workbook('rieslings.xlsx')
worksheet=workbook.add_worksheet()

#bold format for headers and appropriate widths
bold14=workbook.add_format({'bold':True,'font_size':14})
bold14.set_align('center')
worksheet.set_column('A:A',70)
worksheet.set_column('B:B',20)
worksheet.set_column('C:C',20)

#Cash formatting
cashformat=workbook.add_format()
cashformat.set_num_format(0x2c)
cashformat.set_align('center')

#Centering
centformat=workbook.add_format()
centformat.set_align('center')

#Add headers to the xlsx.
worksheet.write('A1','Name',bold14)
worksheet.write('B1','Sugar (g/L)',bold14)
worksheet.write('C1','Volume (ml)',bold14)
worksheet.write('D1','Price',bold14)

row=1
col=0

#Write the data
for name,sugar,volume,price in (data):
  worksheet.write(row,col,name)
  worksheet.write(row,col+1,sugar,centformat)
  worksheet.write(row,col+2,volume,centformat)
  worksheet.write(row,col+3,price/100.0,cashformat)
  row += 1


workbook.close()

