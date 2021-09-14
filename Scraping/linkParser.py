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
nlp = spacy.load("en_core_web_sm")

tags = []
pageContent = ""
for line in Lines:
    nLine = " , "+ line
    pageContent = pageContent + nLine



dSet = nlp(pageContent)
tagSet = numpy.asarray(dSet.ents)


tagMap = {}


for j in range(len(tagSet)):
    if str(tagSet[j][0])  not in tagMap:
        print("new thing:"+ str(tagSet[j][0]))
        tags.append(str(tagSet[j][0]))
        tagMap[str(tagSet[j][0]) ] = len(tags)





file1 = open(outName, 'w')
file1.write("{")
file1.write('"Tags" : [')
for i in range(len(tags)):
    file1.write(tags[i]+ "\n")
        # file1.write(",")

file1.write("]}")
file1.close()