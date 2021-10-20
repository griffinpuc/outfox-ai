import os
import csv
import Levenshtein
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
csvLink1 = ROOT_DIR+"\\csv\\raw_data.csv"

def calculateAll(tagArray):
    calculateSimAll(tagArray)
    #i = 0
    #for row in reader:
    #    if(i>0):
    #        val = calculateSimilarity(tagArray, row[2].split(','))
    #        print(row[2] + ": " + str(val))
    #    i+=1

def calculateSimAll(tagArray):
    file = open(csvLink1)
    reader = csv.reader(file, delimiter=',')

    grouparray = [''] * 194
    
    i = 0
    for row in reader:
        if(i>0):
            grouparray[i-1] = ' '.join(str(row[2]).split(', '))
        i+=1
    
    vect = CountVectorizer().fit_transform(grouparray)
    vectors = vect.toarray()
    csim = cosine_similarity(vectors)

    print(str(cosineCompVecter(vectors[0], vectors[20])))


def calculateSimilarity(tagArray1, tagArray2):
    tagArray1 = ' '.join(tagArray1)
    tagArray2 = ' '.join(tagArray2)
    
    return Levenshtein.distance(tagArray1, tagArray2)

def cosineCompVecter(vect1, vect2):
    vect1 = vect1.reshape(1,-1)
    vect2 = vect2.reshape(1,-1)

    return cosine_similarity(vect1, vect2)[0][0]