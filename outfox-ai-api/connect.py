#!/usr/bin/python
from os import X_OK
import psycopg2
from datetime import datetime,timezone
import string
from lib import *
import random
import json
import time
from collections import Counter

from config import config

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# CONNECT FUNCTION# ESTABLISHES AND TESTS INTIAL DB CONNECTION
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
        pass
    finally:
        if conn is not None:
            conn.close()

def isFile(resourceId):
    conn = None
    retval=False

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select type from resources where id = {resourceId}')
        cur.execute(sql.format(resourceId=resourceId))

        row = cur.fetchone()
        ftype = row[0]

        if ftype == "txt":
            return True

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            pass
    finally:
        if conn is not None:
            conn.close() 
        return retval

def cacheRecs(userId, objlist, type):
    conn = None
    table = ""

    if type==0:
        table = "ai_grouprec_cache"
    elif type == 1:
        table = "ai_userrec_cache"
    elif type == 2:
        table = "ai_resourcerec_cache"

    try:

        json_string = ""
        if type==0:
            json_string = json.dumps([Group.__dict__ for Group in objlist])
        elif type == 1:
            json_string = json.dumps([User.__dict__ for User in objlist])
        elif type == 2:
            json_string = json.dumps([Resource.__dict__ for Resource in objlist])

        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('insert into '+table+' (userid, rec, lastchanged) ')
        sql += ("values ({userId},'{objlist}','{timeStamp}') ")
        sql += ('on conflict (userid) do update ')
        sql += ('set userid=excluded.userid,')
        sql += ('rec=excluded.rec,')
        sql += ('lastchanged=excluded.lastchanged;')

        cur.execute(sql.format(userId=userId,objlist=json_string,timeStamp=datetime.now(timezone.utc)))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            pass
    finally:
        if conn is not None:
            conn.close()  

def getOwner(groupId):
    conn = None
    ownerid=0

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select createdby from groups where id = {groupId}')
        cur.execute(sql.format(groupId=groupId))

        row = cur.fetchone()
        ownerid = row[0]

        return ownerid

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            pass
    finally:
        if conn is not None:
            conn.close() 
            
def isFav(groupId, userId):
    conn = None
    isfav=False

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select userid from favoritegroup where groupid = {groupId}')
        cur.execute(sql.format(groupId=groupId))

        row = cur.fetchone()
        for item in row:
            if item == userId:
                return True

        return isfav

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            pass
    finally:
        if conn is not None:
            conn.close()  

def getRecsCache(userId, type):
    conn = None
    recString=""
    table = ""

    if type==0:
        table = "ai_grouprec_cache"
    elif type == 1:
        table = "ai_userrec_cache"
    elif type == 2:
        table = "ai_resourcerec_cache"

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select lastchanged from '+table+' where userid = {userId}')
        cur.execute(sql.format(userId=userId))

        row = cur.fetchone()
        timestamp = row[0]

        fmt = '%H:%M:%S.%f'
        d1 = datetime.strptime(str(datetime.now(timezone.utc).time()), fmt)
        d2 = datetime.strptime(str(timestamp), fmt)
        
        diff = d1-d2
        diff = int(diff.total_seconds())
        
        if((diff <= (5*60))):
            sql = ('select rec from '+table+' where userid = {userId}')
            cur.execute(sql.format(userId=userId))

            row = cur.fetchone()
            recString = row[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            pass
    finally:
        if conn is not None:
            conn.close()
        
        return recString   

def getResourceFromGroup(groupId, userId):
    conn = None
    resourceId = 0

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select id from resources where \"GroupId\"={groupId} AND creatorid != {userId} order by RANDOM() limit 1')
        cur.execute(sql.format(groupId=groupId,userId=userId))

        row = cur.fetchone()
        resourceId = row[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
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

        if row[0] is not None:
            counter = Counter(row[0].split(","))
        else:
            sql = ('(select string_agg(tags,\',\') from resourcetags) order by RANDOM() limit 15')
            cur.execute(sql.format(userId=userId))

            row = cur.fetchone()
            counter = Counter(row[0].split(","))
        
        userTags = list(set(row[0].split(",")))
        userTags = counter.most_common()
        userTags = [x[0] for x in userTags]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()

        return userTags

def getUserFromGroup(groupId, userId):
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select userid from favoritegroup where groupid = {groupId} AND userid != {userId} order by RANDOM() limit 1')
        cur.execute(sql.format(groupId=groupId, userId=userId))

        row = cur.fetchone()

        if row:
            userId = row[0]

        else:
            sql = ('select createdby from groups where id = {groupId}')
            cur.execute(sql.format(groupId=groupId))

            row = cur.fetchone()
            userId = row[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
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
        pass

def getDistinctGroups(userId=0):
    conn = None
    distinctGn = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('select id from groups where id in (select \"GroupId\" from resources) AND createdby != {userId} AND id not in (select groupid from favoritegroup where userid={userId})')
        cur.execute(sql.format(userId=userId))

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
        pass

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
        pass

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
        pass
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
        pass
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
        pass


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
        pass

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