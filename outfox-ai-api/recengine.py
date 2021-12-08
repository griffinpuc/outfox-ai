import os
import csv
import collections

from numpy import cos
from numpy.core.fromnumeric import sort
import Levenshtein
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from lib import *
import connect

mstrgrouparray = connect.getDistinctGroups(0)
mstrtagarray = [''] *len(mstrgrouparray)

x=0
for group in mstrgrouparray:
    mstrtagarray[x] = group.tags
    x+=1

def calculateAll(tagArray, userId):

    global mstrgrouparray
    global mstrtagarray

    grouparray = [' '.join(tagArray)] + mstrtagarray
    vect = CountVectorizer().fit_transform(grouparray)
    vectors = vect.toarray()
    csim = cosine_similarity(vectors)
    cosineVectors = []

    x=0
    
    for group in mstrgrouparray:
        if(x>0):
            val = cosineCompVecter(vectors[0], vectors[x])
            cosineVectors.append(CosineObj(group.id, val, tagArray))
        x+=1

    return cosineVectors
    #print("RECOMMENDED GROUP: " + topgroup + ": " + str(topval) + "\n\n====================================\n")
    


def calculateSimilarity(tagArray1, tagArray2):
    tagArray1 = ' '.join(tagArray1)
    tagArray2 = ' '.join(tagArray2)
    
    return Levenshtein.distance(tagArray1, tagArray2)

def cosineCompVecter(vect1, vect2):
    vect1 = vect1.reshape(1,-1)
    vect2 = vect2.reshape(1,-1)

    return cosine_similarity(vect1, vect2)[0][0]