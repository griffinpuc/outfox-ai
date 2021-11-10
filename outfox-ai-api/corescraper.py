import os
import spacy
import numpy

nlp = spacy.load("en_core_web_sm") #setting up spacy nlp

def consumeResourceId(resourceId):
    print('test')

def scrapeTxt(filePath):

    # Using readlines()
    file1 = open(filePath, 'r')
    Lines = file1.readlines()

    tags = []
    tagMap = {} #used to avoid duplicates
    lineBuffer = []

    for line in Lines:

        lineBuffer.append(line)
        if(len(lineBuffer) == 1 ): #processing the text in blocks of 10 lines
            
            tBlock = ""
            for i in range(len(lineBuffer)):
                tBlock += lineBuffer[i]
                
            dSet = nlp(tBlock.decode('utf-8', 'ignore'))
            tagArr = numpy.asarray(dSet.ents)
            for j in range(len(tagArr)):
                
                if str(tagArr[j][0]) in tagMap: # avoiding duplicates by checking if the tag already exists before adding
                    continue
                tags.append(str(tagArr[j][0]))
                tagMap[str(tagArr[j][0])] = len(tags)
            lineBuffer = []
    
    return tags

def scraptTxt2(filePath):
    file1 = open(filePath, 'r', encoding="utf-8")
    txt = file1.read()

    return(nlp(txt).ents)

print(scraptTxt2("F:\Repositories\outfox-ai\TreeFrogsAssignment.txt"))