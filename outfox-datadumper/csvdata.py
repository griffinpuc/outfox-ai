import csv
from os import altsep

parsed_csv = []
last_row = -1

def parseCSV(csvLink):
    # open file in read mode
    with open(csvLink, 'r') as read_obj:
        reader = csv.reader(read_obj)
        header = next(reader)

        if header != None:
            for row in reader:
                parsed_csv.append(row)

def getRow():
    global last_row

    if(last_row + 1 <= len(parsed_csv)):
        pcsv = parsed_csv[last_row + 1]
        last_row += 1
        return pcsv