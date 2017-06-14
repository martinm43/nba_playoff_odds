
def insertstr(table_name,num_col):
  #generate a SQLite insert statement based off 
  #table name and number of columns
  l='INSERT INTO '+table_name+' VALUES (?'
  for i in range(1,num_col-1):
    l=l+',?'
  l=l+',?)'

  return l



def invkey(d):
  i=1
  for d_i in d:
    d_i['id']=i
    i=i+1
    
  return d

if __name__ == '__main__':
  print insertstr('products',6)