import os
import csv
import collections

from numpy import cos
from numpy.core.fromnumeric import sort
import Levenshtein
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from lib import *

groupNum = 912

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is the Project Root
csvLink1 = ROOT_DIR+"\\csv\\raw_data.csv"

def calculateAll(tagArray):
    file = open(csvLink1)
    reader = csv.reader(file, delimiter=',')

    grouparray = [''] * groupNum
    namearray = [''] * groupNum
    
    i = 0
    for row in reader:
        grouparray[i] = ' '.join(str(tagArray).split(', '))
        if(i>0):
            grouparray[i] = ' '.join(str(row[1]).split(', '))
            namearray[i] = str(row[0])
        i+=1
    
    vect = CountVectorizer().fit_transform(grouparray)
    vectors = vect.toarray()
    csim = cosine_similarity(vectors)

    cosineVectors = []

    x=0
    for group in grouparray:
        if(x>0):
            val = cosineCompVecter(vectors[0], vectors[x])
            cosineVectors.append(CosineObj(namearray[x], val))
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