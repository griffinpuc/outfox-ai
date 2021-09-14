import string
import json
import spacy
import en_core_web_sm
import numpy
import pandas as pd
import os
fileName = "Course_Descriptions.txt"


if os.path.exists("CD_OUT.txt"):
      os.remove("CD_OUT.txt") # one file at a time


newFile = "CD_OUT.txt"


# Using readlines()
file1 = open(fileName, 'r')
Lines = file1.readlines()
nlp = spacy.load("en_core_web_sm")


class Class:
    def __init__(self, department, className, tagList):
        self.department = department
        self.className = className
        self.tagList = tagList


        # Strips the newline character

lineBuffer = []
classes = []
lastDept = ""
for line in Lines:

    lineBuffer.append(line)
    if(len(lineBuffer) > 3 and line == "\n"):

        
        table = string.maketrans("0123456789", '**********')
        res = lineBuffer[0].translate(table)
        
        
        
        
        if(len(lineBuffer[0]) - len(res)) < 2:
            className = lineBuffer[0]
            # do the nlp stuff here to get the list of tags
            description = ""
            for i in range(1, len(lineBuffer)-2):
                description += lineBuffer[i]
                
            dSet = nlp(description.decode('utf-8', 'ignore'))
            tagArr = numpy.asarray(dSet.ents)
            classes.append(Class(lastDept, className, tagArr))
            
           
            lastDept = lineBuffer[len(lineBuffer)-2]

        lineBuffer = []



file1 = open(newFile, 'w')
file1.write("{")
file1.write('"Classes" : [')
for i in range(len(classes)):
    mTArr = []
    
    for j in range(len(classes[i].tagList)):
        mTArr.append(str(classes[i].tagList[j][0]))
    
    classes[i].tagList = mTArr

    file1.writelines(json.dumps(classes[i].__dict__))
    if(i != len(classes)-1):
        file1.write(",")

file1.write("]}")
file1.close()
