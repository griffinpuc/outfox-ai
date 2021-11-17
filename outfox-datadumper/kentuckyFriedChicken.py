import wikipedia
import csvdata
import sys
import os
from pathlib import Path

#
#THROW ERROR FUNCTION
#TRIGGERS IF INVALID CMD ARGUMENT TOTAL
def throwCmdError():
    print('\nIncorrect command usage:')
    print('main.py <total entries> <total groups per user> <link to csv>\n')

def kfcMagicSeasoning(amount):
    for i in range(0, amount):
        while True:

            csvrow = csvdata.getRow()
            tag = csvrow[1].split(',')[0]
            path = "data/resources/"+tag
            if not os.path.exists(path):
                break
        

        print("TAG "+str(i)+": " + tag)
        Path(path).mkdir(parents=True, exist_ok=True)

        kfcMagicRecipe(tag)

#ANOTHER GOOD THING YES
def kfcMagicRecipe(tag):
    print(str(wikipedia.search(tag)))

    #random = wikipedia.random(1)
    #esult = wikipedia.page(random)

    #name = result.title+".txt"
    #content = result.content

    for string in wikipedia.search(tag):
        try:
            page = wikipedia.page(string)

            name = page.title
            content = page.content
            tag = tag
        finally:
            saveChickenBucket(name, content, tag)

#SAVE THE FILE
def saveChickenBucket(fileName, txtBody, tag):
    f = open("data/resources/"+tag+"/"+fileName+".txt", "w", encoding="utf-8")
    f.writelines(txtBody)
    print('Saved 1 file.')

#MAIN FUNCTION
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        throwCmdError()
    else:
        resourceTotal = int(sys.argv[1])

        csvdata.parseCSV("data\dataset1.csv")

        kfcMagicSeasoning(resourceTotal)