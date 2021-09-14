#
# -----------------------------------------------------
#                       linkParser.py
#           Parses text files derived from web pages
#           into usable tags
# -----------------------------------------------------
#
# LAST UPDATED: 14 SEPTEMBER 2021
# UPDATED BY: SA
#

import string
import json
import spacy
import en_core_web_sm
import numpy
import pandas as pd
import os
import sys
fileName = "temp-link-text.txt"

outName = sys.argv[1]


if os.path.exists(outName):
      os.remove(outName) 

file1 = open(fileName, 'r')
Lines = file1.readlines()
nlp = spacy.load("en_core_web_sm") #setting up spacy

tags = []
pageContent = ""
for line in Lines: #putting all of the text into one string
    nLine = " , "+ line
    pageContent = pageContent + nLine



dSet = nlp(pageContent) #running nlp on the content of the page to get tags
tagSet = numpy.asarray(dSet.ents)


tagMap = {}


for j in range(len(tagSet)):
    if str(tagSet[j][0])  not in tagMap:        #adding all distinct tags to the list
       
        tags.append(str(tagSet[j][0]))
        tagMap[str(tagSet[j][0]) ] = len(tags)





file1 = open(outName, 'w') #writing to a file

for i in range(len(tags)):
    file1.write(tags[i]+ "\n")
        # file1.write(",")


file1.close()