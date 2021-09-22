import spacy
import numpy as np
import os
import sys
nlp = spacy.load('en_core_web_lg')

def most_similar(word, topn=5):
    word = nlp.vocab[str(word)]
    queries = [
        w for w in word.vocab 
        if w.is_lower == word.is_lower and w.prob >= -15 and np.count_nonzero(w.vector)
    ]

    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return [(w.lower_,w.similarity(word)) for w in by_similarity[:topn+1] if w.lower_ != word.lower_]


inFile = "wordList-from-links.txt"
outFile = sys.argv[1]

file1 = open(inFile, 'r')
Lines = file1.readlines()

file2 = open(outFile, 'w+')


for line in Lines:
     tList = most_similar(line, topn=3)
     file2.write(str(tList))
    #  for i in range(len(tList)):
    #      file2.write(tList[i])
    #  for word in tList:
    #     file2.write(str(word) + "\n")
     
file1.close()
os.remove(inFile)
file2.close()