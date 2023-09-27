import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import re
import colors as c
from tqdm import tqdm
import string

print(c.Color.RED + "UFC Scraper v2.0" + c.Color.RESET)

testPages = 3

fighterListURL_Base = "https://www.ufc.com/athletes/all?gender=All&search=&page="
fighterListURL_start = "https://www.ufc.com/athletes/all"
fighterURL_Base = "https://www.ufc.com"
page = requests.get(fighterListURL_start)
soup = BeautifulSoup(page.content, 'html.parser')

# Number of fighters/pages
if testPages == -1:
    numFighters = int(re.findall(r'\d+', soup.find('div', class_='althelete-total').text)[0]) # number of fighters
    numPages = (numFighters // 11) - 1 if (numFighters % 11) == 0 else (numFighters // 11 ) # 11 fighters per page (starting at pg 0)
    print(str(numFighters) + " fighters\n" + str(numPages) + " pages")
else:
    print("Testing " + str(testPages) + " pages")
    numPages = testPages - 1

# Loop through all pages
for pageNum in np.arange(0, numPages + 1):
    currentURL = fighterListURL_Base + str(pageNum)
    print(currentURL)
    page = requests.get(currentURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', class_='e-button--black')] # extract href links from buttons
    for link in links:
        print(fighterURL_Base + link)
