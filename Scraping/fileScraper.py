#
# -----------------------------------------------------
#                       fileScraper.py
#           Scrapes and parses txt files into usable
#           tags
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
fileName = sys.argv[1]

outName = "file-tags.txt"


if os.path.exists(outName):
      os.remove(outName) # one file at a time





# Using readlines()
file1 = open(fileName, 'r')
Lines = file1.readlines()
nlp = spacy.load("en_core_web_sm")



        # Strips the newline character


tags = []
tagMap = {}
lineBuffer = []
for line in Lines:

    lineBuffer.append(line)
    if(len(lineBuffer) == 10 ):
        
        tBlock = ""
        for i in range(len(lineBuffer)):
            tBlock += lineBuffer[i]
            
        dSet = nlp(tBlock.decode('utf-8', 'ignore'))
        tagArr = numpy.asarray(dSet.ents)
        for j in range(len(tagArr)):
            
            if str(tagArr[j][0]) in tagMap:
                continue
            tags.append(str(tagArr[j][0]))
            tagMap[str(tagArr[j][0])] = len(tags)
        lineBuffer = []



file1 = open(outName, 'w+')
file1.write("{")
file1.write('"Tags" : [\n')
for i in range(len(tags)):
    file1.write(tags[i] + "\n")
        # file1.write(",")

file1.write("]}")
file1.close()
