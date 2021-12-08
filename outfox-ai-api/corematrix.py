#
# -----------------------------------------------------
#                  OUTFOX AI
#                   main.py
#          Main base file for function
# -----------------------------------------------------
#
# LAST UPDATED: 29 NOV 2021
# UPDATED BY: GCP
#

import calc
import funcs
import os
import pandas as pd
from tqdm import tqdm
from lib import *
import json
import connect
import psycopg2

# VALUES:
# probably shouldnt change
#ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
#csvLink1 = ROOT_DIR+"\\csv\\raw_data.csv"
#csvLink2 = ROOT_DIR+"\\csv\\group_tags_bool.csv"
#csvLink3 = ROOT_DIR+"\\csv\\group_tags_corr_matrix.csv"



def generateDataframe():
    engine = psycopg2.connect("dbname='outfoxdb' user='griffin' host='pg.terramisha.com' password='alpineair'")
    sql = "select * from ai_correlation"
    return pd.read_sql_query(sql, engine).pivot(index='taga',columns='tagb',values='correlation')

mainDataframe = generateDataframe()

RESULTS_PR_TAG = 2
RECC_MODIFIER= 3
TAGS_PR_USR = 10
PR_PG = 5

##############################################################################################
##############################################################################################
#                                                                                            #
#      *             (        )   (              )                (        )      )  (       #
#    (  `     (      )\ )  ( /(   )\ )        ( /(    (     *   ) )\ )  ( /(   ( /(  )\ )    #
#    )\))(    )\    (()/(  )\()) (()/(    (   )\())   )\  ` )  /((()/(  )\())  )\())(()/(    #
#   ((_)()\((((_)(   /(_))((_)\   /(_))   )\ ((_)\  (((_)  ( )(_))/(_))((_)\  ((_)\  /(_))   #
#   (_()((_))\ _ )\ (_))   _((_) (_))_|_ ((_) _((_) )\___ (_(_())(_))    ((_)  _((_)(_))     #
#   |  \/  |(_)_\(_)|_ _| | \| | | |_ | | | || \| |((/ __||_   _||_ _|  / _ \ | \| |/ __|    #
#   | |\/| | / _ \   | |  | .` | | __|| |_| || .` | | (__   | |   | |  | (_) || .` |\__ \    #
#   |_|  |_|/_/ \_\ |___| |_|\_| |_|   \___/ |_|\_|  \___|  |_|  |___|  \___/ |_|\_||___/    #
#                                                                                            #
##############################################################################################
##############################################################################################                                 

# Trigger cache on user login
def triggerCache(userId):
    getUserRecsFromUser(userId,0,True)
    getGroupRecsFromUser(userId,0,True)
    getResourceRecsFromUser(userId,0,True)

# GET GROUP RECOMMENDATIONS
def getGroupRecsFromUser(userId, pageNum, bypass=False):
    
    groupListP = []
    groupList = []
    
    cache = connect.getRecsCache(userId,0 )
    if bypass:
        cache=""

    if(cache != ""):
        cache = json.loads(cache)
        cachestr=str(cache).replace("\'", "\"")
        groupList = json.loads(cachestr, object_hook=lambda d: Group(**d))
    else:
        userObj = User(userId, [])
        userObj.tags = connect.getUserTags(userId)

        tags = userObj.tags[:TAGS_PR_USR]

        i=0
        for tag in tags:
            for obj in calculateRecommendations(tag, RECC_MODIFIER, RESULTS_PR_TAG):
                if(connect.getOwner(obj.group) != userId):
                    groupList.insert(i, Group(obj.group, obj.tags))
                    i+=1

        connect.cacheRecs(userId, groupList, 0)

    groupListP = groupList[(int(pageNum)*PR_PG):(int(pageNum)*PR_PG)+PR_PG]
    return(' { "currentpg": '+str(pageNum)+', "pgcount": '+str(len(groupList)/PR_PG)+',"groups":' + json.dumps([Group.__dict__ for Group in groupListP]) + ' }')

# GET RESOURCE RECOMMENDATIONS
def getResourceRecsFromUser(userId, pageNum, bypass=False):

    resourceListP = []
    resourceList = []
    
    cache = connect.getRecsCache(userId,2)

    if bypass:
        cache=""
    if(cache != ""):
        cache = json.loads(cache)
        cachestr=str(cache).replace("\'", "\"")
        resourceList = json.loads(cachestr, object_hook=lambda d: Resource(**d))
    else:
        userObj = User(userId, [])
        userObj.tags = connect.getUserTags(userId)

        tags = userObj.tags[:TAGS_PR_USR]

        i=0
        for tag in tags:
            for obj in calculateRecommendations(tag, RECC_MODIFIER, RESULTS_PR_TAG):
                resourceList.insert(i, Resource(connect.getResourceFromGroup(obj.group, userId), obj.tags))
                i+=1

        connect.cacheRecs(userId, resourceList, 2)

    resourceListP = resourceList[(int(pageNum)*PR_PG):(int(pageNum)*PR_PG)+PR_PG]
    return(' { "pgcount": '+str(len(resourceList)/PR_PG)+', "resources":' + json.dumps([Resource.__dict__ for Resource in resourceListP]) + ' }')

# GET USER RECOMMENDATIONS
def getUserRecsFromUser(userId, pageNum, bypass=False):
    userListP = []
    userList = []
    
    cache = connect.getRecsCache(userId,1 )
    if bypass:
        cache=""
    if(cache != ""):
        cache = json.loads(cache)
        cachestr=str(cache).replace("\'", "\"")
        userList = json.loads(cachestr, object_hook=lambda d: User(**d))
    else:
        userObj = User(userId, [])
        userObj.tags = connect.getUserTags(userId)

        tags = userObj.tags[:TAGS_PR_USR]

        i=0
        for tag in tags:
            for obj in calculateRecommendations(tag, RECC_MODIFIER, RESULTS_PR_TAG):
                userList.insert(i, User(connect.getUserFromGroup(obj.group,userId), obj.tags))
                i+=1

        connect.cacheRecs(userId, userList, 1)

    userListP = userList[(int(pageNum)*PR_PG):(int(pageNum)*PR_PG)+PR_PG]
    return(' { "pgcount": '+str(len(userList)/PR_PG)+', "users":' + json.dumps([User.__dict__ for User in userListP]) + ' }')



##############################################################################################
##############################################################################################

# GENERATE BOOL MATRIX:
# generates a csv file with bool values corresponding to each category tag
def generateBoolMatrix():
    
    bool_df = calc.generateBools()
    return bool_df

# CALCULATE CORRELATIONAL MATRIX
# generates a correlational matrix for each category tag
def calculateCorrelationMatrix(boolDf):

    df = boolDf
    unique_tags = list(df.columns)
    unique_tags.pop(0)

    correlation_matrix_dict = {}
    conn = connect.openConnection()

    connect.clearRelations()

    for tag_a in tqdm(unique_tags):
        #correlation_matrix_dict[tag_a] = calc.correlate_with_every_tag(conn, df, tag_a)
        calc.correlate_with_every_tag(conn, df, tag_a)
        connect.commitCorrelations()
    
    
    conn.close()

    #df_corr_matrix = pd.DataFrame(correlation_matrix_dict)
    #df_corr_matrix.shape
    #df_corr_matrix.head()
    #df_corr_matrix["index"] = unique_tags
    #df_corr_matrix = df_corr_matrix.set_index("index")

    #funcs.saveFile(csvLink3, df_corr_matrix.to_csv())

# CALCULATE RECOMMENDATIONS
# calculates a list of recommended categories based on a category input
def calculateRecommendations(param, modifier, resultNo):
    #df = pd.read_csv(csvLink3, index_col = "index",encoding='cp1252')
    df = mainDataframe
    retObj = calc.get_recommendations(df, param,resultNo, modifier)
    sortedVals = sorted(retObj, key=lambda x: x.value, reverse=True)

    return sortedVals[:resultNo]

def calculateTags(param, resultNo):
    df = pd.read_csv(csvLink3, index_col = "index",encoding='cp1252')
    retObj = calc.get_only_tags(df, param, resultNo)

    return retObj

def buildMatrix():
    calculateCorrelationMatrix(generateBoolMatrix())

#buildMatrix()
#generateBoolMatrix()
#connect.generateMatrixTable()
#print(calculateRecommendations("CHEMISTRY", 3, 5)[0].tags)

#print(mainDataframe)
#print(getUserRecsFromUser(39, 0))
#print(getGroupRecsFromUser(39, 1))
