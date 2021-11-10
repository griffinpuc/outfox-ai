#!/usr/bin/python
import psycopg2
import datetime
import string
import random

from config import config

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#
#CONNECT FUNCTION
#ESTABLISHES AND TESTS INTIAL DB CONNECTION
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#
def getResourcePath(resourceId):
    conn = None
    resourcePath = ""

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        
        sql = ('SELECT * from resources where id={resourceId}')
        cur.execute(sql.format(resourceId=resourceId))

        row = cur.fetchone()
        
        resourceUrl = row[4]
        resourcePath = row[5]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print('Recieved resource upload')
            conn.close()

            return resourcePath
