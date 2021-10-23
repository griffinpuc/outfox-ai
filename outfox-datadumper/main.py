#!/usr/bin/python
import sys
import csvdata
import connect
    
#
#THROW ERROR FUNCTION
#TRIGGERS IF INVALID CMD ARGUMENT TOTAL
def throwCmdError():
    print('\nIncorrect command usage:')
    print('main.py <total entries> <password for accounts> <link to csv>\n')

#
#MAIN FUNCTION
#TAKES 3 ARGUMENTS: ENTRY TOTAL, GROUP TOTAL, AND CSV LINK
if __name__ == "__main__":

    if(len(sys.argv) != 4):
        throwCmdError()
    else:
        entryTotal = int(sys.argv[1])
        groupsTotal = int(sys.argv[2])
        csvLink = (sys.argv[3])

        connect.connect()
        csvdata.parseCSV(csvLink)
        connect.clearDatabase()
        connect.injectUsers(entryTotal, groupsTotal)