import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import re
import colors as c
from tqdm import tqdm

print(c.Color.RED + "UFC Scraper v2.0" + c.Color.RESET)
domain = "https://www.ufc.com"

def cleanName(string):
    string = string.replace('\n', ' ').strip()
    return string

def cleanEventName(arr):
    arr = [arr.text for arr in arr]
    arr = [arr.replace('\n', ' ').strip() for arr in arr]
    arr = [arr for arr in arr if arr != '']
    arr = [re.sub(r'\s+', ' ', arr) for arr in arr]
    arr = ': '.join(arr)
    return arr

def cleanString(string):
    # remove newlines and trailing spaces
    string = string.replace('\n', '').strip()
    return string
def cleanStrings(arr):
    # remove newlines and trailing spaces
    arr = [string.replace('\n', '').strip() for string in arr]
    # remove empty strings
    # arr = [string for string in arr if string != '']
    return arr
def downloadImage (url, name):
    # print("Downloading " + name + "'s" + " image")
    name = 'images/' + name + '.jpg'
    response = requests.get(url)
    with open(name, 'wb') as f:
        f.write(response.content)
def extractFighterBio(bioElements, fighterData):
    bioElements = [bio.text.split('\n') for bio in bioElements] # split by newlines
    bioElements = [item for sublist in bioElements for item in sublist] # flatten the list
    bioElements = [bio.strip() for bio in bioElements] # remove trailing spaces
    for bioNum in range(0, len(bioElements)):
        if bioElements[bioNum] == 'Status':
            fighterData.update({'Status': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Place of Birth':
            fighterData.update({'Place_of_Birth': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Age':
            fighterData.update({'Age': bioElements[bioNum + 2]})
        if bioElements[bioNum] == 'Height':
            fighterData.update({'Height': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Weight':
            fighterData.update({'Weight': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Octagon Debut':
            fighterData.update({'Octagon_Debut': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Reach':
            fighterData.update({'Reach': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Leg Reach':
            fighterData.update({'Leg_Reach': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Trains at':
            fighterData.update({'Trains_at': bioElements[bioNum + 1]})
        if bioElements[bioNum] == 'Fighting style':
            fighterData.update({'Fighting_Style': bioElements[bioNum + 1]})
    return bioElements, fighterData
def extractFighterStats(fighterURL, downloadImages = False):
    # extract the p class "hero-profile__tag"
    page = requests.get(domain + fighterURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    fighterData = {}
    fighterData.update({'URL': fighterURL})
    # INFO Elements at the top of the page
    infoElements = soup.find('div', class_='hero-profile__info')
    infoElements = [info.text.split('\n') for info in infoElements] # split by newlines
    infoElements = [item for sublist in infoElements for item in sublist] # flatten the list
    infoElements = [info.strip() for info in infoElements] # remove trailing spaces
    for infoNum in range(0, len(infoElements)):
        if 'Division' in infoElements[infoNum]:
            fighterData.update({'Division': infoElements[infoNum]})
        if infoElements[infoNum] == "Dana White's Contender Series":
            fighterData.update({'Dana_White_Contender_Series': True})
    try:
        fighterData.update({'Nickname': soup.find('p', class_='hero-profile__nickname').text})
    except AttributeError:
        pass
    try:
        fighterData.update({'Name': soup.find('h1', class_='hero-profile__name').text})
    except AttributeError:
        pass
    try:
        record = soup.find('p', class_='hero-profile__division-body').text
        record = record.split('(')[0].split('-')
        fighterData.update({'Wins': record[0].strip()})
        fighterData.update({'Losses': record[1].strip()})
        fighterData.update({'Draws': record[2].strip()})
    except AttributeError:
        pass

    # BIO Elements at the bottom of the page
    bioElements = soup.find('div', class_='c-tabs__panes')
    bioElements, fighterData = extractFighterBio(bioElements, fighterData)


    # STAT Elements in the middle of the page
    stat_cards = soup.find_all('div', class_=['stats-records stats-records--two-column', 'stats-records stats-records--three-column'])
    stat_cards = [stat.text.split('\n') for stat in stat_cards] # split by newlines
    stat_cards = [item for sublist in stat_cards for item in sublist] # flatten the list
    stat_cards = [stat.strip() for stat in stat_cards] # remove trailing spaces
    for cardNum in range(0, len(stat_cards)):
        if stat_cards[cardNum] == 'Sig. Strikes Landed':
            fighterData.update({'Sig_Str_Landed': stat_cards[cardNum + 1]})
        if stat_cards[cardNum] == 'Sig. Strikes Attempted':
            fighterData.update({'Sig_Str_Attempted': stat_cards[cardNum + 1]})
        if stat_cards[cardNum] == 'Takedowns Landed':
            fighterData.update({'Takedowns_Landed': stat_cards[cardNum + 1]})
        if stat_cards[cardNum] == 'Takedowns Attempted':
            fighterData.update({'Takedowns_Attempted': stat_cards[cardNum + 1]})
        if stat_cards[cardNum] == 'Sig. Str. Landed':
            fighterData.update({'Sig_Str_Landed_PM': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Sig. Str. Absorbed':
            fighterData.update({'Sig_Str_Absorbed_PM': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Takedown avg':
            fighterData.update({'Takedown_Avg_P15': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Submission avg':
            fighterData.update({'Submission_Avg_P15': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Sig. Str. Defense':
            fighterData.update({'Sig_Str_Defense': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Takedown Defense':
            fighterData.update({'Takedown_Defense': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Knockdown Avg':
            fighterData.update({'Knockdown_Avg_P15': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Average fight time':
            fighterData.update({'Avg_Fight_Time': stat_cards[cardNum - 2]})
        if stat_cards[cardNum] == 'Standing':
            fighterData.update({'Standing': stat_cards[cardNum + 1].split('(')[0].strip()})
        if stat_cards[cardNum] == 'Clinch':
            fighterData.update({'Clinch': stat_cards[cardNum + 1].split('(')[0].strip()})
        if stat_cards[cardNum] == 'Ground':
            fighterData.update({'Ground': stat_cards[cardNum + 1].split('(')[0].strip()})
        if stat_cards[cardNum] == 'Head':
            fighterData.update({'Head': stat_cards[cardNum - 1]})
        if stat_cards[cardNum] == 'Body':
            fighterData.update({'Body': stat_cards[cardNum - 1]})
        if stat_cards[cardNum] == 'Leg':
            fighterData.update({'Leg': stat_cards[cardNum - 1]})
        if stat_cards[cardNum] == 'KO/TKO':
            fighterData.update({'KO/TKO': stat_cards[cardNum + 1].split('(')[0].strip()})
        if stat_cards[cardNum] == 'DEC':
            fighterData.update({'DEC': stat_cards[cardNum + 1].split('(')[0].strip()})
        if stat_cards[cardNum] == 'SUB':
            fighterData.update({'SUB': stat_cards[cardNum + 1].split('(')[0].strip()})
    # if there is a div with the class hero-profile__image-wrap then find the img tag and extract the src attribute, otherwise set to None
    fighterProfileImage = soup.find('div', class_='hero-profile__image-wrap')
    if fighterProfileImage != None:
        fighterProfileImage = fighterProfileImage.find('img', class_='hero-profile__image')['src']
        if downloadImages:
            downloadImage(fighterProfileImage, fighterData['Name'])
        fighterData.update({'hasImage': True})
    else:
        fighterProfileImage = None
        fighterData.update({'hasImage': False})
    return fighterData
def scrapeEvents(testEvents = -1, testFights = -1, update=False):
    URL = "http://www.ufcstats.com/statistics/events/completed?page=all"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    upcomingEvents = soup.find_all('img', class_='b-statistics__icon') # List of upcoming events
    eventLinks = [link.get('href') for link in soup.find('table', class_='b-statistics__table-events').find_all('a')] # All event links
    eventLinks = eventLinks[len(upcomingEvents):] # Remove upcoming events from list
    if update:
        pastLinks = pd.read_csv('Raw Data/fightInformation.csv')['Event_Link'].unique().tolist()
        eventLinks = [link for link in eventLinks if link not in pastLinks]
        if len(eventLinks) == 0:
            print(c.Color.GREEN + "No new events to update" + c.Color.RESET)
            return None, None, None
        print(c.Color.ORANGE + "Updating " + str(len(eventLinks)) + " events" + c.Color.RESET)
    elif testEvents == -1:
        numEvents = len(eventLinks)
        print(str(numEvents) + " events")
    else:
        print("Testing " + str(testEvents) + " pages")
        eventLinks = eventLinks[:testEvents]
    eventBar = tqdm(eventLinks, desc="Events", unit='events') # progress bar
    eventFightInformation, eventFightTotals, eventFightRounds = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for event in eventBar:
        soup = BeautifulSoup(requests.get(event).content, 'html.parser')
        eventTitle = cleanString(soup.find('span', class_='b-content__title-highlight').text)
        eventBar.set_description(c.Color.BLUE + eventTitle.ljust(50) + c.Color.RESET)
        eventInfo = soup.find('div', class_='b-list__info-box b-list__info-box_style_large-width')
        eventInfo = [info.text.split('\n') for info in eventInfo] # split by newlines
        eventInfo = cleanStrings([item for sublist in eventInfo for item in sublist]) # flatten the list
        eventInfo = [info for info in eventInfo if info != ''] # remove empty strings
        eventDate, eventLocation = None, None
        for item in np.arange(0, len(eventInfo)):
            if eventInfo[item] == 'Date:':
                eventDate = eventInfo[item + 1]
            if eventInfo[item] == 'Location:':
                eventLocation = eventInfo[item + 1]
        fightLinks = [link.get('href') for link in soup.find_all('a', class_='b-flag b-flag_style_green')]
        if testFights != -1:
            fightLinks = fightLinks[:testFights]
        for fight in fightLinks:
            soup = BeautifulSoup(requests.get(fight).content, 'html.parser')
            if "Round-by-round stats not currently available." in soup.text:
                continue
            nameSection = soup.find('div', class_='b-fight-details__persons clearfix')
            winner = nameSection.find_all('div', class_='b-fight-details__person')[0].find('i', class_='b-fight-details__person-status b-fight-details__person-status_style_gray')
            winner = "A" if winner == None else "B"
            names = nameSection.find_all('h3', class_='b-fight-details__person-name')
            nicknames = nameSection.find_all('p', class_='b-fight-details__person-title')
            fighterA_nickname, fighterB_nickname = [cleanName(nickname.text) for nickname in nicknames]
            fighterA_nickname = None if fighterA_nickname == '' else fighterA_nickname
            fighterB_nickname = None if fighterB_nickname == '' else fighterB_nickname
            fighterA_name, fighterB_name = [cleanName(name.text) for name in names]
            winnerName = fighterA_name if winner == "A" else fighterB_name
            fightTitle = fighterA_name + " vs. " + fighterB_name
            print(fightTitle)
            fightBout = cleanString(soup.find('i', class_='b-fight-details__fight-title').text)
            fightInfo = soup.find('div', class_='b-fight-details__content')
            fightInfo = [info.text.split('\n') for info in fightInfo] # split by newlines
            fightInfo = cleanStrings([item for sublist in fightInfo for item in sublist]) # flatten the list
            fightInfo = [info for info in fightInfo if info != ''] # remove empty strings
            fightMethod, fightRound, fightTime, fightFormat, fightReferee, fightDetails = None, None, None, None, None, None
            for item in np.arange(0, len(fightInfo)):
                if fightInfo[item] == 'Method:':
                    fightMethod = fightInfo[item + 1]
                if fightInfo[item] == 'Round:':
                    fightRound = fightInfo[item + 1]
                if fightInfo[item] == 'Time:':
                    fightTime = fightInfo[item + 1]
                if fightInfo[item] == 'Time format:':
                    fightFormat = fightInfo[item + 1]
                if fightInfo[item] == 'Referee:':
                    fightReferee = fightInfo[item + 1]
                if fightInfo[item] == 'Details:':
                    fightDetails = ' '.join(fightInfo[item + 1:])
            # Stats
            tableData = soup.find_all('p', class_='b-fight-details__table-text')
            tableData = [data.text.split('\n') for data in tableData] # split by newlines
            tableData = cleanStrings([item for sublist in tableData for item in sublist]) # flatten the list
            tableData = [data for data in tableData if data != ''] # remove empty strings
            numberOfRows = tableData.count(tableData[0])
            # Fight Totals
            fightTotals = tableData[:(numberOfRows*10)]
            fighterA_Totals = pd.DataFrame(np.array(fightTotals[::2]).reshape(-1, 10))
            fighterA_Totals_Rnds = fighterA_Totals.iloc[1:]
            fighterA_Totals_Rnds.insert(0, 'Round', np.arange(1, len(fighterA_Totals_Rnds) + 1))
            fighterA_Totals = fighterA_Totals.iloc[[0]]
            fighterB_Totals = pd.DataFrame(np.array(fightTotals[1::2]).reshape(-1, 10))
            fighterB_Totals_Rnds = fighterB_Totals.iloc[1:]
            fighterB_Totals_Rnds.insert(0, 'Round', np.arange(1, len(fighterB_Totals_Rnds) + 1))
            fighterB_Totals = fighterB_Totals.iloc[[0]]
            fightTotals = pd.concat([fighterA_Totals, fighterB_Totals], axis=0).reset_index(drop=True)
            fightTotals.columns = ['Fighter', 'KD', 'Sig_Str', 'Sig_Str_Perc', 'Total_Str', 'TD', 'TD_Perc', 'Sub_Att', 'Rev', 'Ctrl']
            fightTotals.insert(0, 'Fight', fightTitle)
            fightTotals.insert(0, 'Event', eventTitle)
            fightTotals_Rnds = pd.concat([fighterA_Totals_Rnds, fighterB_Totals_Rnds], axis=0).reset_index(drop=True)
            fightTotals_Rnds.columns = ['Round', 'Fighter', 'KD', 'Sig_Str', 'Sig_Str_Perc', 'Total_Str', 'TD', 'TD_Perc', 'Sub_Att', 'Rev', 'Ctrl']
            fightTotals_Rnds.insert(0, 'Fight', fightTitle)
            fightTotals_Rnds.insert(0, 'Event', eventTitle)
            # Significant Strikes
            sigStrikes = tableData[(numberOfRows*10):]
            fighterA_SigStrikes = pd.DataFrame(np.array(sigStrikes[::2]).reshape(-1, 9))
            fighterA_SigStrikes_Rnds = fighterA_SigStrikes.iloc[1:]
            fighterA_SigStrikes_Rnds.insert(0, 'Round', np.arange(1, len(fighterA_SigStrikes_Rnds) + 1))
            fighterA_SigStrikes = fighterA_SigStrikes.iloc[[0]]
            fighterB_SigStrikes = pd.DataFrame(np.array(sigStrikes[1::2]).reshape(-1, 9))
            fighterB_SigStrikes_Rnds = fighterB_SigStrikes.iloc[1:]
            fighterB_SigStrikes_Rnds.insert(0, 'Round', np.arange(1, len(fighterB_SigStrikes_Rnds) + 1))
            fighterB_SigStrikes = fighterB_SigStrikes.iloc[[0]]
            sigStrikes = pd.concat([fighterA_SigStrikes, fighterB_SigStrikes], axis=0).reset_index(drop=True)
            sigStrikes.columns = ['Fighter', 'Sig_Str', 'Sig_Str_Perc', 'Head', 'Body', 'Leg', 'Distance', 'Clinch', 'Ground']
            sigStrikes.insert(0, 'Fight', fightTitle)
            sigStrikes.insert(0, 'Event', eventTitle)
            sigStrikes_Rnds = pd.concat([fighterA_SigStrikes_Rnds, fighterB_SigStrikes_Rnds], axis=0).reset_index(drop=True)
            sigStrikes_Rnds.columns = ['Round', 'Fighter', 'Sig_Str', 'Sig_Str_Perc', 'Head', 'Body', 'Leg', 'Distance', 'Clinch', 'Ground']
            sigStrikes_Rnds.insert(0, 'Fight', fightTitle)
            sigStrikes_Rnds.insert(0, 'Event', eventTitle)
            fightTotals = pd.concat([fightTotals, sigStrikes[['Head', 'Body', 'Leg', 'Distance', 'Clinch', 'Ground']]], axis=1)
            fightRounds = pd.concat([fightTotals_Rnds, sigStrikes_Rnds[['Head', 'Body', 'Leg', 'Distance', 'Clinch', 'Ground']]], axis=1)
            # Fight Info
            fightInfo = pd.DataFrame([[eventTitle, eventDate, eventLocation, fightTitle, fighterA_name, fighterB_name, fightBout, fightMethod, fightRound, fightTime, fightFormat, fightReferee, fightDetails, winner, winnerName, event]], columns=['Event', 'Date', 'Location', 'Fight', 'Fighter_A', 'Fighter_B', 'Bout', 'Method', 'Round', 'Time', 'Format', 'Referee', 'Details', 'Winner', 'Winner_Name', 'Event_Link'])
            eventFightInformation = pd.concat([eventFightInformation, fightInfo], axis=0).reset_index(drop=True)
            eventFightTotals = pd.concat([eventFightTotals, fightTotals], axis=0).reset_index(drop=True)
            eventFightRounds = pd.concat([eventFightRounds, fightRounds], axis=0).reset_index(drop=True)
    if update:
        oldFightInformation = pd.read_csv('Raw Data/fightInformation.csv')
        oldFightTotals = pd.read_csv('Raw Data/fightTotals.csv')
        oldFightRounds = pd.read_csv('Raw Data/fightRounds.csv')
        eventFightInformation = pd.concat([oldFightInformation, eventFightInformation], axis=0).reset_index(drop=True)
        eventFightTotals = pd.concat([oldFightTotals, eventFightTotals], axis=0).reset_index(drop=True)
        eventFightRounds = pd.concat([oldFightRounds, eventFightRounds], axis=0).reset_index(drop=True)
    return eventFightInformation, eventFightTotals, eventFightRounds
def scrapeFighters(testPages = -1, testFighters = -1, downloadImages = False):
    fighterListURL_Base = "https://www.ufc.com/athletes/all?gender=All&search=&page="
    fighterListURL_start = "https://www.ufc.com/athletes/all"
    page = requests.get(fighterListURL_start)
    soup = BeautifulSoup(page.content, 'html.parser')
    fighterData = []
    # Number of fighters/pages
    if testPages == -1:
        numFighters = int(re.findall(r'\d+', soup.find('div', class_='althelete-total').text)[0]) # number of fighters
        numPages = (numFighters // 11) - 1 if (numFighters % 11) == 0 else (numFighters // 11 ) # 11 fighters per page (starting at pg 0)
        print(str(numFighters) + " fighters\n" + str(numPages) + " pages")
    else:
        print("Testing " + str(testPages) + " pages")
        numPages = testPages - 1
    pageBar = tqdm(np.arange(0, numPages + 1), desc="Pages", unit='pages') # progress bar
    # Loop through all pages
    for pageNum in pageBar:
        currentURL = fighterListURL_Base + str(pageNum)
        page = requests.get(currentURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', class_='e-button--black')] # extract href links from buttons
        if testFighters != -1:
            links = links[:testFighters]
        for link in links:
            updateString = "Page: " + str(pageNum) + " - Fighter: " + link.split("/")[-1]
            pageBar.set_description(c.Color.BLUE + updateString.ljust(50) + c.Color.RESET)
            fighterData.append(extractFighterStats(link, downloadImages))
    return pd.DataFrame(fighterData)


# CONTROL PANEL
fightInformation, fightTotals, FightRounds = scrapeEvents(testEvents=-1, testFights=-1, update=True)
if fightInformation is not None and fightTotals is not None and FightRounds is not None:
    print(fightInformation)
    print(fightTotals)
    print(FightRounds)
    print(c.Color.CYAN + "Saving data..." + c.Color.RESET)
    fightInformation.to_csv('Raw Data/fightInformation.csv', index=False)
    fightTotals.to_csv('Raw Data/fightTotals.csv', index=False)
    FightRounds.to_csv('Raw Data/fightRounds.csv', index=False)
    print(c.Color.GREEN + "Data saved." + c.Color.RESET)
# Fighters_DF = scrapeFighters(testPages=-1, testFighters=-1, downloadImages=False)
# Fighters_DF.to_csv('Raw Data/fighters.csv', index=False)