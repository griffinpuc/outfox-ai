#
# -----------------------------------------------------
#                       linkScraper.py
#           Scrapes web pages for text
#           
# -----------------------------------------------------
#
# LAST UPDATED: 14 SEPTEMBER 2021
# UPDATED BY: SA
#

import requests
from bs4 import BeautifulSoup
import sys
import os
import re
url = sys.argv[1]


page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
cleanStuff = soup.getText()
cleanedCleanStuff = re.sub('[^0-9a-zA-Z]+', ' ', cleanStuff)




outName = "temp-link-text.txt"
if os.path.exists(outName):
      os.remove(outName) # one file at a time



file1 = open(outName, 'w+')
file1.write(cleanedCleanStuff)
file1.close()