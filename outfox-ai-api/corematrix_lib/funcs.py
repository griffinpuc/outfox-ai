#
# -----------------------------------------------------
#                       funcs.py
#           Holds some lonely functions
# -----------------------------------------------------
#
# LAST UPDATED: 13 SEPTEMBER 2021
# UPDATED BY: GCP
#

# SAVEFILE:
# saves a file given a path and string content
def saveFile(url, content):
    f = open(url, "a")
    f.write(content)
    f.close()

# CONVERT DOWN:
# converts case down
def convertDown(text):
    return text.lower()

# CONVERT UP:
# converts case up
def convertUp(text):
    return text.upper()

# SPLIT AND SPLICE:
# splits and edits rows to establish consistency
def splitAndSplice(text):
    text = str(text)
    text = text.replace(", ", ",")
    retval = ""

    for tag in text.split(","):
        tag = convertUp(tag)
        retval += (tag.replace(" ", "_")+",")

    print(retval)
    return retval