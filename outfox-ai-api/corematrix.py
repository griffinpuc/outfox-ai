#
# -----------------------------------------------------
# OUTFOX-AI: CM3 (CORRELATIONAL-MATRIX-MODEL-MANAGER)
#                  main.py
#          Main base file for function
# -----------------------------------------------------
#
# LAST UPDATED: 12 SEPTEMBER 2021
# UPDATED BY: GCP
#

import calc
import funcs
import os
import pandas as pd
from tqdm import tqdm
from lib import *
import json

# VALUES:
# probably shouldnt change
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
csvLink1 = ROOT_DIR+"\\csv\\raw_data.csv"
csvLink2 = ROOT_DIR+"\\csv\\group_tags_bool.csv"
csvLink3 = ROOT_DIR+"\\csv\\group_tags_corr_matrix.csv"



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
    userObj.tags = ["CHEMISTRY", "CREATIVITY", "PARTICLES", "DIGITALMEDIA", "PAINTING","LIFE", "LANGUAGESTUDY", "COMMUNICATIONS", "TECHNOLOGY"]

    tags = userObj.tags

    groupList = []

    i=0
    for tag in tags:
        for obj in calculateRecommendations(tag, 3, 5):
            groupList.insert(i, Group(obj.group+3655, obj.tags))
            i+=1

    groupListP = groupList[(int(pageNum)*10):(int(pageNum)*10)+10]
    return(' { "groups":' + json.dumps([Group.__dict__ for Group in groupListP]) + ' }')

# GET RESOURCE RECOMMENDATIONS
def getResourceRecsFromUser(userId, pageNum):

    userObj = User(userId, [])
    userObj.tags = ["CHEMISTRY", "CHILDREN", "PARTICLES", "CREATIVE", "PAINTING","LIFE", "LANGUAGESTUDY", "SOCIETY", "TECHNOLOGY"]

    tags = userObj.tags

    resourceList = []
    
    i=0
    for tag in tags:
        for obj in calculateRecommendations(tag, 3, 5):
            resourceList.insert(i, Resource(i+332, obj.tags))
            i+=1

    print(i)

    resourceListP = resourceList[(int(pageNum)*10):(int(pageNum)*10)+10]

    return(' { "resources":' + json.dumps([Resource.__dict__ for Resource in resourceListP]) + ' }')

# GET USER RECOMMENDATIONS
def getUserRecsFromUser(userId, pageNum):

    userObj = User(userId, [])
    userObj.tags = ["PHYSICAL", "NUTRITION", "PARTICLES", "DIGITALMEDIA", "ANIMALS","LIFE", "LANGUAGESTUDY", "PHOTOGRAPHY", "PAINTING"]

    tags = userObj.tags

    userList = []

    i=0
    for tag in tags:
        for obj in calculateRecommendations(tag, 3, 5):
            userList.insert(i, User(i+731, obj.tags))
            i+=1

    userListP = userList[(int(pageNum)*10):(int(pageNum)*10)+10]
    return(' { "users":' + json.dumps([User.__dict__ for User in userListP]) + ' }')



##############################################################################################
##############################################################################################

# GENERATE BOOL MATRIX:
# generates a csv file with bool values corresponding to each category tag
def generateBoolMatrix():
    try:
        os.remove(csvLink2)
    except OSError:
        pass
    
    funcs.saveFile(csvLink2, calc.generateBools(csvLink1,  "tags_bool"))
    print(('EXPORT TO: {path}').format(path=csvLink2))

# CALCULATE CORRELATIONAL MATRIX
# generates a correlational matrix for each category tag
def calculateCorrelationMatrix():
    try:
        os.remove(csvLink3)
    except OSError:
        pass
    df = calc.returnDf(csvLink2)
    unique_tags = list(df.columns)
    unique_tags.pop(0)

    correlation_matrix_dict = {}

    for tag_a in tqdm(unique_tags):
        correlation_matrix_dict[tag_a] = calc.correlate_with_every_tag(df, tag_a, dict_mode = False)

    df_corr_matrix = pd.DataFrame(correlation_matrix_dict)
    df_corr_matrix.shape
    df_corr_matrix.head()
    df_corr_matrix["index"] = unique_tags
    df_corr_matrix = df_corr_matrix.set_index("index")
    funcs.saveFile(csvLink3, df_corr_matrix.to_csv())

# CALCULATE RECOMMENDATIONS
# calculates a list of recommended categories based on a category input
def calculateRecommendations(param, modifier, resultNo):
    df = pd.read_csv(csvLink3, index_col = "index",encoding='cp1252')
    retObj = calc.get_recommendations(df, param, modifier)

    sortedVals = sorted(retObj, key=lambda x: x.value, reverse=True)

    return sortedVals[:resultNo]

def calculateTags(param, resultNo):
    df = pd.read_csv(csvLink3, index_col = "index",encoding='cp1252')
    retObj = calc.get_only_tags(df, param, resultNo)

    return retObj

print(getGroupRecsFromUser(669, 0))
