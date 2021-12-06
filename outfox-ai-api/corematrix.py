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



# Should be 0 at default, but here for testing porposes ;)
GRP_MODIFIER = 0
RES_MODIFIER = 0
USR_MODIFIER = 0

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

# GET GROUP RECOMMENDATIONS
def getGroupRecsFromUser(userId, pageNum):

    userObj = User(userId, [])
    userObj.tags = connect.getUserTags(userId)

    tags = userObj.tags[:10]

    groupList = []

    i=0
    for tag in tags:
        for obj in calculateRecommendations(tag, 3, 3):
            groupList.insert(i, Group(obj.group+GRP_MODIFIER, obj.tags))
            i+=1

    groupListP = groupList[(int(pageNum)*10):(int(pageNum)*10)+10]
    return(' { "groups":' + json.dumps([Group.__dict__ for Group in groupListP]) + ' }')

# GET RESOURCE RECOMMENDATIONS
def getResourceRecsFromUser(userId, pageNum):

    userObj = User(userId, [])
    userObj.tags = connect.getUserTags(userId)

    tags = userObj.tags

    resourceList = []
    
    i=0
    for tag in tags:
        for obj in calculateRecommendations(tag, 3, 3):
            resourceList.insert(i, Resource(connect.getResourceFromGroup(obj.group+RES_MODIFIER), obj.tags))
            i+=1

    resourceListP = resourceList[(int(pageNum)*10):(int(pageNum)*10)+10]

    return(' { "resources":' + json.dumps([Resource.__dict__ for Resource in resourceListP]) + ' }')

# GET USER RECOMMENDATIONS
def getUserRecsFromUser(userId, pageNum):

    userObj = User(userId, [])
    userObj.tags = connect.getUserTags(userId)

    tags = userObj.tags

    userList = []

    i=0
    for tag in tags:
        for obj in calculateRecommendations(tag, 3, 5):
            userList.insert(i, User(connect.getUserFromGroup(obj.group+RES_MODIFIER), obj.tags))
            i+=1

    userListP = userList[(int(pageNum)*10):(int(pageNum)*10)+10]
    return(' { "users":' + json.dumps([User.__dict__ for User in userListP]) + ' }')



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
    retObj = calc.get_recommendations(df, param, modifier)
    sortedVals = sorted(retObj, key=lambda x: x.value, reverse=True)

    return sortedVals[:resultNo]

def calculateTags(param, resultNo):
    df = pd.read_csv(csvLink3, index_col = "index",encoding='cp1252')
    retObj = calc.get_only_tags(df, param, resultNo)

    return retObj

def buildMatrix():
    calculateCorrelationMatrix(generateBoolMatrix())

#buildMatrix()
#print(getGroupRecsFromUser(669, 0))
#generateBoolMatrix()
#connect.generateMatrixTable()
#print(calculateRecommendations("CHEMISTRY", 3, 5)[0].tags)

#print(mainDataframe)
#print(getGroupRecsFromUser(39, 0))