import Levenshtein

def calculateSimilarity(tagArray1, tagArray2):
    return Levenshtein.distance(tagArray1, tagArray2)