#!/usr/bin/python
import psycopg2
import datetime
import string
import random
import csvdata
from faker import Faker

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
#INJECT USERS FUNCTION
#CREATES USERS IN DATABASE
def injectUsers(entryTotal, groupsTotal):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        hashhPw = "$2b$10$z.NZ2Gdjkpqh.fcvHIoWGua3PHxZGg5oBdMmCztWXh1ALUpZ3PgPm" #Mark hamills! hamham123
        
        for i in range(0, entryTotal):
            fake = Faker()
            userNO = id_generator(10)
            fName = fake.name().split(' ')[0]
            lName = fake.name().split(' ')[1]

            sql = ('INSERT INTO users (username, firstname, lastname, email, hashpw) VALUES (\'{username}\', \'{firstname}\', \'{lastname}\', \'{email}\', \'{hashpw}\') RETURNING id')
            cur.execute(sql.format(username=userNO, firstname=fName, lastname=lName, email=userNO+'@gmail.com', hashpw=hashhPw))
            injectUserGroups(groupsTotal, cur.fetchone()[0], cur)

            #print(i)

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print('Completed data injection. Created entries.')
            conn.close()

#
#INJECT USER GROUPS FUNCTION
#CREATES GROUPS FOR USERS IN DATABASE
def injectUserGroups(groupsTotal, userId, cursor):
    conn = None
    try:
        cur = cursor
        
        for i in range(0, groupsTotal):
            
            csvrow = csvdata.getRow()
            groupNO = id_generator(10)
            sql = ('INSERT INTO groups (groupname, groupdescription, createdby, datetimeadd) VALUES (\'{groupname}\', \'{groupdescription}\', \'{createdby}\', \'{datetimeadd}\') RETURNING id')
            cur.execute(sql.format(groupname=csvrow[0]+" ["+groupNO + "]", groupdescription='AUTO GENERATED GROUP', createdby=userId, datetimeadd=datetime.datetime.now()))
            prevId = cur.fetchone()[0]

            sql = ('INSERT INTO tags (id, tag, createdate) VALUES (\'{id}\', \'{tags}\', \'{datetime}\')')
            cur.execute(sql.format(id=prevId, tags=csvrow[1],datetime=datetime.datetime.now()))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#
#CLEAR DATABASE FUNCTION
#CLEARS USERS AND GROUPS TABLES
def clearDatabases():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = ('DELETE FROM friends')
        cur.execute(sql)
        sql = ('DELETE FROM users WHERE ID != 669 & ID!=')
        cur.execute(sql)
        sql = ('DELETE FROM groups')
        cur.execute(sql)
        sql = ('DELETE FROM tags')
        cur.execute(sql)

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print('Completed database clear.')
            conn.close()

def clearDatabase():
    print('BOOYA!')

def poop():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        for i in range(0, 100):

            sql = ('INSERT INTO resources (type, title, description, mutable, creatorid) VALUES (\'{type}\', \'{title}\', \'{description}\', \'{mutable}\', \'{cid}\') RETURNING id')
            cur.execute(sql.format(type="Link", title="Test", description="Test test", mutable=False, cid=718))

            print('DOOOOOOOOOOOOOOONE')

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def poop2():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        fake = Faker()
        sql = ('UPDATE users where where firstname=\'Ad\' SET firstname='+fake.name().split(' ')[0]+' SET lastname='+fake.name().split(' ')[1])
        cur.execute(sql)

        print('DOOOOOOOOOOOOOOONE')

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

