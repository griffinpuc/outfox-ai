import os
import spacy
import numpy
import connect
import config

connect.connect()
nlp = spacy.load("en_core_web_sm") #setting up spacy nlp

def consumeResourceId(resourceId):
    fileUri = connect.getResourcePath(resourceId)

    print(scrapetTxt(fileUri))

def scrapetTxt(filePath):
    file1 = open(filePath, 'r', encoding="utf-8")
    txt = file1.read()

    return(nlp(txt).ents)

#consumeResourceId(5)
#print(scrapetTxt("F:\Repositories\outfox-ai\TreeFrogsAssignment.txt"))