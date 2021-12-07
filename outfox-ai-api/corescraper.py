#
# -----------------------------------------------------
#                    OUTFOX AI
#                  corescraper.py
#          Main scraping functionality
# -----------------------------------------------------
#
# LAST UPDATED: 29 NOV 2021
# UPDATED BY: GCP
#

import os
import spacy
import numpy as np
import connect
import config
import re
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api
import tqdm
import pathlib
from nltk import tokenize
from operator import itemgetter
import math
from pathlib import Path
import nltk
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

# INITIAL SETUP
# PERFORMS DOWNLOADS NECESSARY FOR COMPUTATION
def initialSetup():

    print("[LOAD MODEL] NLTK STOPWORDS...")
    nltk.download('stopwords')
    print("Done.")

    print("[LOAD MODEL] NLTK PUNKT...")
    nltk.download('punkt')
    print("Done.")

    print("[LOAD MODEL] " + str(model_file))
    #model = api.load("word2vec-google-news-300") #choose from multiple models https://github.com/RaRe-Technologies/gensim-data
    model = api.load("glove-wiki-gigaword-300") #choose from multiple models https://github.com/RaRe-Technologies/gensim-data
    model.save("gigaword-model.d2v")
    print("Done.")

# CHECK MODEL FILE
model_file = Path(str(pathlib.Path().resolve())+"\gigaword-model.d2v")
if model_file.exists():
    print('Loading ' + str(model_file))
else:
    print('Running intial setup...')
    initialSetup()
    print('Loading ' + str(model_file))

# Initialize db connection
connect.connect()
# Initialize loaded model
model = KeyedVectors.load("gigaword-model.d2v")
# Initialize stop word set
stop_words = set(stopwords.words('english'))
# Initialize spacy
nlp = spacy.load("en_core_web_lg") #setting up spacy nlp
# INITIALIZE KEYWORD LIST
keywords = connect.getDistinctTags()

def updateGroup(groupId):
    connect.calculateGroupTags(groupId)

# CONSUME RESOURCE ID
# CONSUMES A RESOURCE ID AND RETURNS THE TOP KEYWORDS
def consumeResourceId(resourceId):
    # PULLS FILE URI FROM RESOURCE ID
    fileUri = "C:/Users/Administrator/Desktop/outfox/server/dist" + connect.getResourcePath(resourceId)
    print(fileUri)

    # SCRAPE AND GENERATE TOP KEYWORDS
    topKeywords = scrapetTxt(fileUri)
    # GENERATE TOP TAGS FROM THOSE KEYWORDS
    topTags = magicMatch(keywords, topKeywords)
    print(topKeywords)

    # SAVE TAGS TO RESOURCE TAGS TABLE
    connect.saveResourceTags(resourceId, topTags)


# SCRAPE TEXT
# SCRAPES TEXT GIVEN A FILEPATH
def scrapetTxt(filePath):
    file1 = open(filePath, 'r', encoding="utf-8")
    txt = file1.read()
    
    return(scrape(re.sub('[^A-Za-z0-9\s]+', '', txt)))


# CHECK SENTENCE
# CHECKS SENTENCE FOR WORD
def checkSent(word, sentences): 
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))


# GET TOP N
# GETS TOP N OF DICT ELEM
def getTopN(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result


# SCRAPE
# SCRAPES A STRING RETURNING KEYWORDS
def scrape(string):

    # return nlp(string).ents
    total_words = string.split()
    total_word_length = len(total_words)
    total_sentences = tokenize.sent_tokenize(string)
    total_sent_len = len(total_sentences)

    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = checkSent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}

    return getTopN(tf_idf_score, 10)


# MAGIC MATCH
# THE MAGICAL FUNCTION THAT MATCHES GENERATED KEYWORDS TO TAGS IN OUR BANK
# TAKES A TOLERANCE: 0<x<1 (default 0.65)
def magicMatch(tags, keywords, tolerance=0.65):
    tagList = []
    
    for tag in tags:
        for keyword in keywords:
            if not keyword.isdigit():
                try:
                    val = model.similarity(tag.lower(), keyword.lower())
                    if(val > tolerance):
                        tagList.append(tag)
                except KeyError:
                    pass

    return(list(set(tagList)))


# TESTING/DEMO USAGE (leave commented!)
#print(magicMatch(keywords, scrapetTxt("F:\Repositories\outfox-ai\outfox-datadumper\data\\resources\PAINTING\Chinese painting.txt")))
#consumeResourceId(5)
def test():
    directory = r'F:\Repositories\outfox-ai\outfox-datadumper\data\resources\MANAGEMENT'
    for filename in os.listdir(directory):
        print(filename)
        print(magicMatch(keywords, scrapetTxt(os.path.join(directory, filename))))

#for i in range (10,232):
    #consumeResourceId(i)
#def scrapeTest():

#updateGroup(37)
consumeResourceId(242)

