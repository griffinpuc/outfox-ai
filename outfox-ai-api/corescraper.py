import os
import spacy
import numpy

nlp = spacy.load("en_core_web_sm") #setting up spacy nlp

def consumeResourceId(resourceId):
    print('test')

def scrapetTxt(filePath):
    file1 = open(filePath, 'r', encoding="utf-8")
    txt = file1.read()

    return(nlp(txt).ents)

print(scrapetTxt("F:\Repositories\outfox-ai\TreeFrogsAssignment.txt"))