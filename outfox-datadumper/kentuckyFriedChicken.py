import wikipedia
import sys

#
#THROW ERROR FUNCTION
#TRIGGERS IF INVALID CMD ARGUMENT TOTAL
def throwCmdError():
    print('\nIncorrect command usage:')
    print('main.py <total entries> <total groups per user> <link to csv>\n')

def kfcMagicSeasoning(amount):
    

#ANOTHER GOOD THING YES
def kfcMagicRecipe(amount):
    for i in range(0, amount):

        print(str(wikipedia.search("chemistry")))

        random = wikipedia.random(1)
        result = wikipedia.page(random)

        name = result.title+".txt"
        content = result.content

        saveChickenBucket(name, content)


def saveChickenBucket(fileName, txtBody):
    f = open("data/resources/"+fileName, "w", encoding="utf-8")
    f.writelines(txtBody)
    print('Saved 1 file.')

#MAIN FUNCTION
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        throwCmdError()
    else:
        resourceTotal = int(sys.argv[1])
        kfcMagicRecipe(resourceTotal)