#!/usr/bin/python
from os import X_OK
import psycopg2
import datetime
import string
from lib import *
import random
from collections import Counter

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


def getResourceFromGroup(groupId):
    conn = None
    resourceId = 0

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select id from resources where \"GroupId\"={groupId} order by RANDOM() limit 1')
        cur.execute(sql.format(groupId=groupId))

        row = cur.fetchone()
        resourceId = row[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return resourceId

def getUserTags(userId):
    conn = None
    userTags = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        
        sql = ('(select string_agg(tags,\',\') from resourcetags where resourceid in(select id from resources where "GroupId" in (select groupid from favoritegroup where userid = {userId})))')
        cur.execute(sql.format(userId=userId))

        row = cur.fetchone()
        counter = Counter(row[0].split(","))

        
        userTags = list(set(row[0].split(",")))
        userTags = counter.most_common()
        userTags = [x[0] for x in userTags]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return userTags

def getUserFromGroup(groupId):
    conn = None
    userId = 0

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select id from users where id in (select * from groups where \"GroupId\"={groupId}) order by RANDOM() limit 1')
        cur.execute(sql.format(groupId=groupId))

        row = cur.fetchone()
        resourceId = row[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return userId

def saveResourceTags(resourceId, tags):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        tags = ",".join(tags)

        sql = ("INSERT INTO resourcetags (resourceid, tags) VALUES ({resourceId}, '{tags}')")
        cur.execute(sql.format(resourceId=resourceId, tags=tags))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def getDistinctGroups():
    conn = None
    distinctGn = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select id from groups where id in (select \"GroupId\" from resources)')
        cur.execute(sql)

        ids = [item[0] for item in cur.fetchall()]
        distinctGn = [''] *len(ids)
        i = 0
        for id in ids:
            dTags = calculateGroupTags(id)
            dTags = list(filter(None, dTags))

            newGroup = Group(id,' '.join(dTags))
            distinctGn[i] = newGroup
            i+=1

        cur.close()
        return(distinctGn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def getDistinctTags():
    conn = None
    distinctTags = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select distinct taga from ai_correlation')
        cur.execute(sql)

        distinctTags = [item[0] for item in cur.fetchall()]
        return(distinctTags)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def updateGroupTags(groupId):
    conn = None
    distinctTags = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select id from resources where GroupId={groupId}')
        cur.execute(sql)

        distinctTags = [item[0] for item in cur.fetchall()]
        

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
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

strng="INSERT INTO ai_correlation (taga, tagb, correlation) VALUES "
def addRelation(tagA, tagB, correlation):
    global strng
    strng+="('"+tagA+"','"+tagB+"',"+str(correlation)+"),"

def commitCorrelations():
    global strng
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print("Executing SQL INSERT...")
        sql = (strng[:-1])
        cur.execute(sql)

        strng="INSERT INTO ai_correlation (taga, tagb, correlation) VALUES "

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def calculateGroupTags(groupId):
    conn = None
    tags = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        sql = '(select string_agg(tags,\',\') from resourcetags where resourceid in(select id from resources where "GroupId" = {groupId}))'
        cur.execute(sql.format(groupId=groupId))

        row = cur.fetchone()
        tags = list(set(row[0].split(",")))

        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

            return tags



def clearRelations():
    try:
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ("DELETE FROM ai_correlation")
        cur.execute(sql)

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def openConnection():
    params = config()
    return psycopg2.connect(**params)

def generateMatrixTable():

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    

    # DYNAMICALLY GETS TAG NAMES AND FORCES TO LIST
    sql1 = """select
                overlay
                (
                    (select string_agg(distinct taga, ',ai_correlation.') from ai_correlation) placing '' from 1 for 1
            );"""

    cur.execute(sql1)
    colspivot = cur.fetchone()[0]

    sql2 = """select taga, """+str(colspivot)+"""
             from crosstab
             (
               select taga taga, tagb tagb, correlation
               from ai_correlation
               union all
               select tagb, taga, correlation
               from ai_correlation
               union all
               select distinct taga, taga, 1.0
               from ai_correlation
              ) x
              pivot
              (
                max(correlation) 
                for tagb in ("""+str(colspivot)+""")
            ) p"""
    #print(sql2)
    #cur.execute(sql2)