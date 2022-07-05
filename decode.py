# Decode tests
from bs4 import BeautifulSoup
import requests, snowflake.connector, random, datetime

####################### Snowflake connector ###############################
conn = snowflake.connector.connect(
        user = "BrendanDV",
        password = "bMSmG@qWxTP7lZ2tEzkN#0!h$",
        account = "ym30263.ca-central-1.aws",
        warehouse = 'COMPUTE_WH',
        database = 'FNB_CHECK',
        schema = 'PUBLIC',
        role = 'ACCOUNTADMIN'
    )
###########################################################################

#Input parameters - need to keep in mind how the data will be received
inp = str(input('Please specify the name of the person you are interested in searching:\n'))
inp = inp.lstrip().rstrip()
inp = inp.replace(' ', '+')
lower_inp = inp.lower()
url = "https://google.com/search?q=" + "\"" + inp + "\""


try:
    with conn.cursor() as curs:
        name = curs.execute("select distinct lower(poi_name) from FNB_CHECK.PUBLIC.HEADER where lower(poi_name) = '{}';".format(lower_inp)).fetchall()
        name = name[0]
        name = str(name[0])
        
        
        
        
        if lower_inp == name:
            uid = curs.execute("select distinct uid from FNB_CHECK.PUBLIC.HEADER where lower(poi_name) = '{}'".format(lower_inp)).fetchall()
            print(uid)
            print(type(uid))
            uid = uid[0]
            uid = uid[0]
            print(uid)
            
            
            
            
        else:
            print('Get wrecked') 
            snow_uids = curs.execute('select distinct uid from FNB_CHECK.PUBLIC.HEADER;')
            snow_uids = curs.fetchall()
            print(snow_uids)
            if uid in snow_uids:
                uid_gen()
            else:
                uid = uid 
                
          
    curs.close()
except Exception as e:
    print(e)