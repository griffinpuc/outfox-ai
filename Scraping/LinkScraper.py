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






from bs4 import BeautifulSoup
from urllib.request import urlopen

import string
import json
import os
import sys
import subprocess

url = sys.argv[1]
print(url)
outFile = "temp-link-text.txt"
page = urlopen(url + "/profiles")
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
pageData = soup.getText()


outName = "temp-link-text.txt"
if os.path.exists(outName):
      os.remove(outName) # one file at a time



file1 = open(outName, 'w+')
file1.write(pageData)


file1.close()



