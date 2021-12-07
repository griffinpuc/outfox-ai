#
# -----------------------------------------------------
#                       calc.py
#           Holds all calculation functions
# -----------------------------------------------------
#
# LAST UPDATED: 12 SEPTEMBER 2021
# UPDATED BY: GCP
#

# todo:
# - change from csv to sql table:
#   - https://pandas.pydata.org/docs/reference/api/pandas.read_sql_table.html

import pandas as pd
import funcs
import recengine
from tqdm import tqdm
import connect
import sqlalchemy
import psycopg2

connect.connect()

# RETURN DATA FRAME:
# returns a data frame from a csv file
def returnDf(csvLink):
    return pd.read_csv(csvLink,encoding='cp1252')

# GENERATE BOOLS:
# generates a boolean tables based on categorys
def generateBools():

    #df = pd.read_csv(csvLink)
    
    engine = psycopg2.connect("dbname='outfoxdb2' user='griffin' host='pg.terramisha.com' password='alpineair'")
    sql = "select * from resourcetags"
    df = pd.read_sql_query(sql, engine)

    # create empty list
    tag_lists = []

    # loop through
    print("Generating boolean matrix...")
    for string in df["tags"]:
        subtag_list = []
        for substring in str(string).split(","):
            subtag_list.append(substring.strip())
        tag_lists.append(subtag_list)
        
    df["tags"] = tag_lists

    unique_tags = get_all_unique(df["tags"])
    df_bool = create_boolean_df(unique_tags, df["tags"])
    df_bool.shape
    df_bool.info()
    df_bool = df_bool.set_index(df["id"])

    print(df_bool.info())

    print('\n==========================================\n')
    print('      BOOL TABLE GENERATION COMPLETE')
    print('\n==========================================\n')

    return df_bool

# CORRELATION:
# returns correlation value between 0 and 1
def correlation(df, tag_a, tag_b):
    
    # Get all rows where a == True
    a = df[df[tag_a]]
    # Get all rows where b == True
    b = df[df[tag_b]]
    
    # Find all rows where a AND b == True
    a_and_b = df[ (df[tag_a]) & (df[tag_b]) ]
    
    # Find all rows where a == True AND b != True
    a_not_b = df[ (df[tag_a]) & ~ (df[tag_b]) ]
    # Find all rows where b == True AND a != True
    b_not_a = df[ (df[tag_b]) & ~ (df[tag_a]) ]
    
    # Calculate the number of possitive and possible outcomes using the shape attribute
    possible_outcomes = a_and_b.shape[0] + a_not_b.shape[0] + b_not_a.shape[0] # shape[0] returns the number of rows
    positive_outcomes = a_and_b.shape[0]
    
    # Calculate the final correlation coefficient
    r = positive_outcomes / possible_outcomes
    
    return r

# CORRELATION WITH EVERY TAG:
# generates correlation values for a tag against every tag
def correlate_with_every_tag(conn, df, tag_a): 
    
    unique_tags = list(df.columns)
    unique_tags.pop(0)

    # Loop through every tag and store the correlation in a list
    correlation_list = []
    for tag_b in unique_tags:
        val = correlation(df, tag_a, tag_b)
        #correlation_list.append(val)
        connect.addRelation(tag_a, tag_b, val)
        #connect.insertRelation(conn, tag_a, tag_b, val)
    #return correlation_list

# CREATE BOOLEAN DF:
# generate a boolean data frame
def create_boolean_df(unique_tags, group_taglists):
    # Create new df with a column for every tag
    boolean_df = pd.DataFrame(columns = unique_tags)
    boolean_df.shape
    
    # Create an empty dict
    data_dict = {}
    
    # Loop through the columns (tags) in the boolean_df and add them to the dict
    for col in boolean_df:
        data_dict[col] = []
        
        # Loop through the taglists in the old dataframe
        for taglist in group_taglists:
            
            # Check if the column (tag) is in the tracks taglist. If yes append True else append False
            data_dict[col].append(col in taglist)
    
    # Use the boolean lists as values for the boolean_df's columns
    for col in boolean_df:
        boolean_df[col] = data_dict[col]
        
    return boolean_df

# GET ALL UNIQUE:
# gets all unique tags in a dataframe of groups
def get_all_unique(dataframe_of_lists):
    # Create empty list
    unique_tags = []
    
    # Loop through the dataframe rows (lists) and each item inside
    for row in dataframe_of_lists:
        for item in row:
            
            # Add item to all_tags if it's not already in it
            if item not in unique_tags:
                unique_tags.append(item)
                
    return unique_tags

# FIND CORRELATIONS:
# finds correlations in dataframe from list of tags
def find_correlations(df, tag):
    
    # Setup empty list
    correlations = []
    columns = []

    # Loop through all column at the row with the tag as its index
    try:
        for i, corr in enumerate(df.loc[tag,:]):
            # Find the column
            col = df.columns[i]
            
            # Append the correlation to the list
            correlations.append(corr)
            columns.append(col)
    except KeyError:
        print("INVALID CATEGORY TAG")
        pass

    # Create a df out of the lists
    results_df = pd.DataFrame({"tag" : columns,
                              "correlation" : correlations})
    
    return results_df

# FIND HIGHEST CORRELATION:
# finds highest correlation tags from a tag
def find_highest_correlations(corr_df, num_of_values):
    
    # Sort the input df
    corr_df_sorted = corr_df.sort_values(by = ["correlation"], ascending = False)
    
    # Extract the relevant correlations
    corr_df_sliced = corr_df_sorted.iloc[1:num_of_values+1]
    
    return corr_df_sliced

# BASE LEVEL GET RECOMMENDATION:
# takes dataframe, tag, and rec count
def get_recommendations(df, tag, num_of_recommendations, modifier):
    
    corr_df = find_correlations(df, tag)
    
    recommendations_df = find_highest_correlations(corr_df, num_of_recommendations)
    
    #print("\n====================================\n\nRECOMMENDED TAGS: " + str(list(recommendations_df["tag"])))
    rtags = list(recommendations_df["tag"])[:modifier]
    return recengine.calculateAll(rtags)

def get_only_tags(df, tag, num_of_recommendations):
    corr_df = find_correlations(df, tag)
    
    recommendations_df = find_highest_correlations(corr_df, num_of_recommendations)
    return list(recommendations_df["tag"])