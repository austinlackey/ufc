import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import re
import colors as c
from tqdm import tqdm

print(c.Color.RED + "UFC Scraper" + c.Color.RESET)

def scrape(numTestEvents=-1, numTestFights=-1, printData=False, update=False):
    # Initialize Dataframes
    fighterData = pd.DataFrame() # Fighter Specific Data
    overallFightData = pd.DataFrame() # Overall Fight Data
    roundByRoundFightData = pd.DataFrame() # Round by Round Fight Data
    fightInformation = pd.DataFrame() # Basic Fight Data
    updatedEvents = None
    if update:
        print(c.Color.GREEN + "UPDATING UFC DATA" + c.Color.RESET)
        numTestEvents = -1
        numTestFights = -1
        overallFightData = pd.read_csv('Data/overallFightData.csv')
        roundByRoundFightData = pd.read_csv('Data/roundByRoundFightData.csv')
        fightInformation = pd.read_csv('Data/fightInformation.csv')
        updatedEvents = 0
    elif numTestEvents < 0 or numTestFights < 0:
        print(c.Color.YELLOW + "SCRAPING ALL FIGHTS: THIS WILL TAKE A LONG TIME" + c.Color.RESET)
    else:
        print(c.Color.YELLOW + "SCRAPING " + str(numTestEvents) + " EVENTS WITH " + str(numTestFights) + " FIGHTS EACH" + c.Color.RESET)
    eventsPage = 'http://www.ufcstats.com/statistics/events/completed?page=all'
    fightersPage = 'http://www.ufcstats.com/statistics/fighters?char=a&page=all'

    # Event Page Information
    page = requests.get(eventsPage)
    soup = BeautifulSoup(page.content, 'html.parser')
    eventLinks = soup.find_all('a', class_='b-link b-link_style_black') # Link Tag
    eventLinks = [link.get('href') for link in eventLinks] # Link Information

    if numTestEvents < 1: # Testing
        numTestEvents = len(eventLinks)
    eventBar = tqdm(eventLinks[0:numTestEvents], desc='Events', unit='events')
    for eventLink in eventBar:
        page = requests.get(eventLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        eventTitle = soup.find('span', class_='b-content__title-highlight').get_text().strip() # Event Title
        eventBar.set_description(c.Color.BLUE + eventTitle + c.Color.RESET)
        eventInfo = soup.find_all('li', class_='b-list__box-list-item')
        eventInfo = [info.get_text().replace('\n', '').replace('Date:', '').replace('Location:', '').strip() for info in eventInfo]
        eventDate = datetime.strptime(eventInfo[0], '%B %d, %Y') # Event Date
        eventLocation = eventInfo[1] # Event Location
        # SKIP IF EVENT IS TODAY
        if eventDate == datetime.combine(date.today(), time.min):
            print(c.Color.YELLOW + "WARNING: SKIPPING EVENT: " + eventTitle + " (Today's Event)" + c.Color.RESET)
            continue
        if update:
            if eventTitle in fightInformation['Event'].unique():
                print(c.Color.YELLOW + "FOUND EXISTING EVENT:" + eventTitle + " (Already Scraped) - Terminating Update." + c.Color.RESET)
                print(c.Color.GREEN + "DONE - SUCCESSFULLY UPDATED UFC DATA" + c.Color.RESET)
                print(c.Color.MAGENTA + str(updatedEvents) + " Events Updated" + c.Color.RESET)
                return overallFightData.reset_index(drop=True), roundByRoundFightData.reset_index(drop=True), fightInformation.reset_index(drop=True)
            else:
                print(c.Color.YELLOW + "UPDATING EVENT:" + eventTitle + c.Color.RESET)
                updatedEvents += 1
        # print(c.Color.BLUE + eventTitle + c.Color.RESET)

        # Fight Page Information
        fightLinks = soup.find_all('a', class_='b-flag b-flag_style_green')
        fightLinks = [link.get('href') for link in fightLinks]
        if numTestFights < 1: # Testing
            numTestFights = len(fightLinks)
        fightBar = tqdm(fightLinks[0:numTestFights], desc='Fights', unit='fights', leave=False)
        for fightLink in fightBar:
            # Extracting Information from Fight Page
            page = requests.get(fightLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            # Fighter Names
            fighterNames = soup.find_all('h3', class_='b-fight-details__person-name') # Fighter Name Tag
            fighterNames = [name.get_text().strip() for name in fighterNames] # Grab Fighter Names from Tag
            fighterA_Name, fighterB_Name = fighterNames # Split Fighter Names into A/B
            fightTitle = fighterA_Name + ' vs. ' + fighterB_Name # Concatenate Fighter Names for Fight Title
            fightBar.set_description(c.Color.CYAN + fightTitle + c.Color.RESET)
            # print(c.Color.LIGHT_BLUE + "    " + fightTitle + c.Color.RESET)
            # Fight Information
            fightBout = soup.find('i', class_='b-fight-details__fight-title').get_text().strip() # Fight Bout (Light/Heavyweight, etc.)
            fightInfoRaw = soup.find_all('p', class_='b-fight-details__text') # Fight Info Tag
            fightInfoRaw = ''.join(info.get_text() for info in fightInfoRaw).replace('\n', '') # Remove new lines from Tag
            fightInfoRaw = re.sub(' +', ' ', fightInfoRaw) # Remove trailing spaces from Tag

            splitTags = ['Method:', 'Round:', 'Time:', 'Time format:', 'Referee:', 'Details:'] # Split Tags used to extract information
            fightInfoClean = [] # Extracted Information for Fight Info
            for i in range(len(splitTags)): # Loop through split tags and extract information
                if i == len(splitTags)-1: # Last Tag
                    pattern = re.escape(splitTags[i]) + r'(.*)' # Match everything after the last tag
                else: # Not Last Tag
                    pattern = re.escape(splitTags[i]) + r'(.*?)' + re.escape(splitTags[i+1]) # Match everything between the current tag and the next tag
                match = re.search(pattern, fightInfoRaw) # Search for pattern
                if match: # If pattern is found
                    fightInfoClean.append(match.group(1).strip()) # Append to fightInfoClean

            # Extracting Information from Fight Totals and Strikes
            cells = soup.find_all('p', class_='b-fight-details__table-text')
            cells = [cell.get_text().strip() for cell in cells]
            
            # Count how many times the fighter's name appears in the fightInfoRaw
            numRounds = (cells.count(fighterA_Name) - 2)/2
            fighterA_Totals = pd.DataFrame(np.reshape(cells[0:int((numRounds+1)*20):2], (-1, 10)))
            fighterB_Totals = pd.DataFrame(np.reshape(cells[1:int((numRounds+1)*20):2], (-1, 10)))
            fighterA_Strikes = pd.DataFrame(np.reshape(cells[int((numRounds+1)*20)::2], (-1, 9)))
            fighterB_Strikes = pd.DataFrame(np.reshape(cells[int((numRounds+1)*20)+1::2], (-1, 9)))
            fighterA_Totals.columns = ['Fighter', 'KD', 'SigStr', 'SigStrPct', 'TotStr', 'TD', 'TdPct', 'SubAtt', 'Rev', 'CtrlTime']
            fighterB_Totals.columns = ['Fighter', 'KD', 'SigStr', 'SigStrPct', 'TotStr', 'TD', 'TdPct', 'SubAtt', 'Rev', 'CtrlTime']
            fighterA_Strikes.columns = ['Fighter', 'SigStr', 'SigStrPct', 'Head', 'Body', 'Leg', 'Distance', 'Clinch', 'Ground']
            fighterB_Strikes.columns = ['Fighter', 'SigStr', 'SigStrPct', 'Head', 'Body', 'Leg', 'Distance', 'Clinch', 'Ground']

            overallTotals = pd.concat([fighterA_Totals.iloc[0], fighterB_Totals.iloc[0]], axis=1).T
            overallStrikes = pd.concat([fighterA_Strikes.iloc[0], fighterB_Strikes.iloc[0]], axis=1).T

            roundByRoundTotals = pd.concat([fighterA_Totals.iloc[1::], fighterB_Totals.iloc[1::]], axis=0)
            roundByRoundStrikes = pd.concat([fighterA_Strikes.iloc[1::], fighterB_Strikes.iloc[1::]], axis=0)
            roundByRoundTotals.insert(1, 'Round', np.tile(np.arange(1, numRounds+1), 2).astype(int))
            roundByRoundStrikes.insert(1, 'Round', np.tile(np.arange(1, numRounds+1), 2).astype(int))

            overallTotals.drop(['SigStr', 'SigStrPct'], axis=1, inplace=True)
            roundByRoundTotals.drop(['SigStr', 'SigStrPct'], axis=1, inplace=True)
            overall = pd.merge(overallTotals, overallStrikes, how='outer', on=['Fighter'])
            round_by_round = pd.merge(roundByRoundTotals, roundByRoundStrikes, how='outer', on=['Fighter', 'Round'])

            overall.insert(0, 'Event', eventTitle)
            round_by_round.insert(0, 'Event', eventTitle)
            overall.insert(1, 'Fight', fightTitle)
            round_by_round.insert(1, 'Fight', fightTitle)

            fight_information = pd.DataFrame(fightInfoClean).T
            fight_information.columns = ['Method', 'Round', 'Time', 'Time Format', 'Referee', 'Details']
            fight_information.insert(0, 'Event', eventTitle)
            fight_information.insert(1, 'Fight', fightTitle)
            fight_information.insert(2, 'Date', eventDate)
            fight_information.insert(3, 'Location', eventLocation)
            fight_information.insert(4, 'Fighter_A', fighterA_Name)
            fight_information.insert(5, 'Fighter_B', fighterB_Name)
            fight_information.insert(8, 'Fight_Bout', fightBout)
            if printData:
                print("Overall")
                print(overall)
                print("Round by Round")
                print(round_by_round)
                print("Fight Information")
                print(fight_information)
            fight_information['Date'] = fight_information['Date'].astype('object')
            # print(c.Color.GREEN + str(fight_information['Date'].dtype))
            # print(c.Color.GREEN + str(fightInformation['Date'].dtype))
            overallFightData = pd.concat([overallFightData, overall], axis=0)
            roundByRoundFightData = pd.concat([roundByRoundFightData, round_by_round], axis=0)
            fightInformation = pd.concat([fightInformation, fight_information], axis=0)
    print(c.Color.MAGENTA + "DONE - SCRAPED ALL UFC DATA" + c.Color.RESET)
    print(len(fightInformation), "Fights Scraped")
    print(len(roundByRoundFightData['Event'].unique()), "Events Scraped")
    return overallFightData.reset_index(drop=True), roundByRoundFightData.reset_index(drop=True), fightInformation.reset_index(drop=True)
def saveData(overallFightData, roundByRoundFightData, fightInformation):
    print(c.Color.GREEN + "SAVING DATA" + c.Color.RESET)
    overallFightData.to_csv('Data/overallFightData.csv', index=False)
    roundByRoundFightData.to_csv('Data/roundByRoundFightData.csv', index=False)
    fightInformation.to_csv('Data/fightInformation.csv', index=False)
def removeFightInformation(eventTitle):
    overallFightData = pd.read_csv('Data/overallFightData.csv')
    roundByRoundFightData = pd.read_csv('Data/roundByRoundFightData.csv')
    fightInformation = pd.read_csv('Data/fightInformation.csv')
    print(c.Color.MAGENTA + "REMOVING " + str(len(eventTitle)) + " EVENTS" + c.Color.RESET)
    for event in eventTitle:
        print(c.Color.YELLOW + "REMOVING EVENT: " + event + " from data." + c.Color.RESET)
        overallFightData = overallFightData[overallFightData['Event'] != event]
        roundByRoundFightData = roundByRoundFightData[roundByRoundFightData['Event'] != event]
        fightInformation = fightInformation[fightInformation['Event'] != event]
    saveData(overallFightData, roundByRoundFightData, fightInformation)
def loadData():
    print(c.Color.YELLOW + "LOADING DATA" + c.Color.RESET)
    overallFightData = pd.read_csv('Data/overallFightData.csv')
    roundByRoundFightData = pd.read_csv('Data/roundByRoundFightData.csv')
    fightInformation = pd.read_csv('Data/fightInformation.csv')
    return overallFightData, roundByRoundFightData, fightInformation

# CONTROL PANEL
removeFightInformation(['UFC Fight Night: Fiziev vs. Gamrot', 'UFC Fight Night: Grasso vs. Shevchenko 2'])
overallFightData, roundByRoundFightData, fightInformation = scrape(numTestEvents=10, numTestFights=-1, printData=False, update=False)
print(fightInformation)
saveData(overallFightData, roundByRoundFightData, fightInformation)
overallFightData, roundByRoundFightData, fightInformation = loadData()

print(c.Color.GREEN + "Overall Fight Data" + c.Color.RESET)
print(overallFightData)
print(c.Color.GREEN + "Round by Round Fight Data" + c.Color.RESET)
print(roundByRoundFightData)
print(c.Color.GREEN + "Fight Information" + c.Color.RESET)
print(fightInformation)
