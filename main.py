import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

numTestEvents = 1
numTestFights = 1

eventsPage = 'http://www.ufcstats.com/statistics/events/completed?page=all'
fightersPage = 'http://www.ufcstats.com/statistics/fighters?char=a&page=all'

# Event Page Information
page = requests.get(eventsPage)
soup = BeautifulSoup(page.content, 'html.parser')
eventLinks = soup.find_all('a', class_='b-link b-link_style_black') # Link Tag
eventLinks = [link.get('href') for link in eventLinks] # Link Information
if numTestEvents < 1: # Testing
    numTestEvents = len(eventLinks)
for eventLink in eventLinks[0:numTestEvents]:
    page = requests.get(eventLink)
    soup = BeautifulSoup(page.content, 'html.parser')
    eventTitle = soup.find('span', class_='b-content__title-highlight').get_text().strip() # Event Title
    eventInfo = soup.find_all('li', class_='b-list__box-list-item')
    eventInfo = [info.get_text().replace('\n', '').replace('Date:', '').replace('Location:', '').strip() for info in eventInfo]
    eventDate = datetime.strptime(eventInfo[0], '%B %d, %Y') # Event Date
    eventLocation = eventInfo[1] # Event Location
    print(eventTitle)

    # Fight Page Information
    fightLinks = soup.find_all('a', class_='b-flag b-flag_style_green')
    fightLinks = [link.get('href') for link in fightLinks]
    if numTestFights < 1: # Testing
        numTestFights = len(fightLinks)
    for fightLink in fightLinks[0:numTestFights]:
        page = requests.get(fightLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        fighterNames = soup.find_all('h3', class_='b-fight-details__person-name')
        fighterNames = [name.get_text().strip() for name in fighterNames]
        fighterNicknames = soup.find_all('p', class_='b-fight-details__person-title')
        fighterNicknames = [nickname.get_text().strip() for nickname in fighterNicknames]
        fighterA_Name, fighterB_Name = fighterNames
        fighterA_Nickname, fighterB_Nickname = fighterNicknames
        fightTitle = soup.find('i', class_='b-fight-details__fight-title').get_text().strip()
        fightInfo = soup.find_all('p', class_='b-fight-details__text')
        fightInfo = ''.join(info.get_text() for info in fightInfo).replace('\n', '')
        fightInfo = re.split(r'\s{2,}', fightInfo)
        removeTags = ['', 'Method:', 'Round:', 'Time:', 'Time format:', 'Referee:', 'Details:']
        fightInfo = [info for info in fightInfo if info not in removeTags]
        print(fightInfo)
        cells = soup.find_all('p', class_='b-fight-details__table-text')
        cells = [cell.get_text().strip() for cell in cells]
        
        # Count how many times the fighter's name appears in the fightInfo
        numRounds = (cells.count(fighterA_Name) - 2)/2
        fighterA_Totals = pd.DataFrame(np.reshape(cells[0:int((numRounds+1)*20):2], (-1, 10)))
        fighterB_Totals = pd.DataFrame(np.reshape(cells[1:int((numRounds+1)*20):2], (-1, 10)))
        fighterA_Strikes = pd.DataFrame(np.reshape(cells[int((numRounds+1)*20)::2], (-1, 9)))
        fighterB_Strikes = pd.DataFrame(np.reshape(cells[int((numRounds+1)*20)+1::2], (-1, 9)))
        print(fighterB_Strikes)
        # Reshape the overallStats into a dataframe with 10 column and whatever number of rows
        print(overallStats)
        overallStats = pd.DataFrame(np.reshape(overallStats, (-1, 10)))
        overallStats.columns = ['Fighter', 'KD', 'SigStr', 'SigStrPct', 'TotalStr', 'TD', 'TDPct', 'SubAtt', 'Rev', 'Ctrl']
