import urllib2
import json
from pprint import pprint

#Create the lcbo db
def create_db(dbname,table_name,factory_mode=False):
  import sqlite3
  
  sqlite_file = dbname # name of the sqlite database file # name of the table to be created 
  
  #ALWAYS HAVE PRIMARY KEYS
  new_field = 'id' # name of the column 
  field_type = 'INTEGER' # column data type 
  
  # Connecting to the database file 
  conn = sqlite3.connect(sqlite_file) 
  
  if factory_mode=='str':
    conn.text_factory=str
  
  c = conn.cursor() 
  
   #Remove old table
  try:
    c.execute('DROP TABLE '+table_name)
  except:
    print 'Initalizing table' 
  # Creating a new SQLite table with 1 column 
  
  # Creating a table with 1 column and set it as PRIMARY KEY 
  # note that PRIMARY KEY column must consist of unique values! 
  try:
    c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
  	         .format(tn=table_name, nf=new_field, ft=field_type))
  except sqlite3.OperationalError:
    print table_name + ' already exists'
  try:
    # Committing changes and closing the connection to the database file 
    conn.commit() 
    conn.close()
    print 'ok'
  except:
    print 'dberror!'

#get datatype for sqlite3
#and return it with the value given
#while handling 
#NoneTypes will be stored as NULL
#can be used for other lcboapi databases
def sqldatahandler(val):
  
  if (type(val) is int):
    return 'INTEGER'  
  elif(type(val) is bool): 
    return 'INTEGER'  
  elif(type(val) is float):  
    return 'REAL'  
  elif(type(val) is long):
    return 'REAL'  
  elif(type(val) is str):  
    return 'TEXT'  
  elif(type(val) is unicode):
    return 'TEXT'
  else: #NoneType - have as a "general handler"
    return 'NUMERIC'   

 
def col_creator(dbname,table_name,entry_dict):
  import sqlite3  

  sqlite_file = dbname # name of the sqlite database file 
 
  conn = sqlite3.connect(sqlite_file) 
  c = conn.cursor()
  
  #for each key in sample dictionary
  
  for i in entry_dict.keys():
    print i
    if i != 'id': 
      column_type=sqldatahandler(entry_dict[i]) #we need the variable type, hand the variable type to another program
      print column_type
      #print type(column_type)
      #print column_type
      print 'Adding column ' + i + ' as ' + column_type
      try:
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        	   .format(tn=table_name, cn=i, ct=column_type))
      except:
        print 'Error inserting column ' + i
      
  conn.commit()
  conn.close()
  return

def insert_data(dbname,table_name,entry_dict,factory_mode=False):
  import sqlite3
  conn = sqlite3.connect(dbname)
  if factory_mode=='str':
    conn.text_factory=str
  cursor = conn.execute('select * from '+table_name)
  names = [description[0] for description in cursor.description]
  conn.execute('PRAGMA journal_mode=OFF')
  #print names
  from strgen import insertstr
  
  try: 
    #Use a generator to return an array containing the list values in the 
    #order of the array. 
    conn.execute(insertstr(table_name,len(names)),[entry_dict[i] for i in names])
    
    #Confirm output somehow - id is arbitrary for inv
    if table_name != 'inventories':  
      print 'Added '+str(entry_dict['id'])
  
  except sqlite3.IntegrityError:
      print 'Error inserting record id '+str(entry_dict['id'])+', key is not unique!'
    #handling and error logging here
    #use the logging module
  
  conn.commit()
  conn.close()
  return

##The next step in development
def table_initializer(_dblink,_tablename,_sampledict,_dictlist,automode='off'):
  
    #Shitty error handling < no error handling
    #On error resume next is awful.
    if automode=='off':
    	flag=raw_input('YES to delete existing table/create new table '+_tablename+':')
    	if flag=='YES':
      		create_db(_dblink,_tablename)
    
    col_creator(_dblink,_tablename,_sampledict)
  
    for d in _dictlist:
      insert_data(_dblink,_tablename,d)
    
    print('Operation completed successfully!')
    return 0
    
 
  
  

