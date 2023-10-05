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

def extractFighterStats(fighterURL):
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
    # print(fighterData)
    # print(len(fighterData))
    return fighterData
            
def extractEventStats(eventURL):
    domain = "https://www.ufc.com"
    page = requests.get(domain + eventURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    eventName = cleanEventName(soup.find('div', class_='c-hero__header'))
    print(eventName)
    eventInfo = cleanString(soup.find('div', class_='c-hero__bottom-text').find('div', class_='c-hero__headline-suffix tz-change-inner').text)
    eventDate, eventTime = eventInfo.split(' / ')
    print(eventDate)
    print(eventTime)
    # Extract section elements with the tag "l-listing--stacked--full-width"
    mainCard = soup.find('div', class_='main-card', id='main-card')
    stacks = mainCard.find('section', class_='l-listing--stacked--full-width')
    fights = stacks.find_all('li', class_='l-listing__item')

    for fight in fights:
        redCornerOutcome = cleanString(fight.find('div', class_='c-listing-fight__corner--red').find('div', class_='c-listing-fight__outcome-wrapper').text)
        fightOutcome = 'Red' if redCornerOutcome == 'Win' else 'Blue' if redCornerOutcome == 'Loss' else 'Draw'
        print("Winner:", fightOutcome)
        redCornerName = cleanName(fight.find('div', class_='c-listing-fight__corner-name c-listing-fight__corner-name--red').text)
        blueCornerName = cleanName(fight.find('div', class_='c-listing-fight__corner-name c-listing-fight__corner-name--blue').text)
        print(redCornerName + " vs " + blueCornerName)
        round = fight.find('div', class_='c-listing-fight__result-text round').text
        time = fight.find('div', class_='c-listing-fight__result-text time').text
        method = fight.find('div', class_='c-listing-fight__result-text method').text
        print(round + " " + time + " " + method)
        oddsWrapper = fight.find('div', class_='c-listing-fight__odds-wrapper')
        odds = oddsWrapper.find_all('span', class_='c-listing-fight__odds-amount')
        odds = [odd.text for odd in odds]
        redOdds, blueOdds = odds
        print(odds)


def scrapeEvents(testPages = -1, testEvents = -1):
    eventListURL_Base = "https://www.ufc.com/events?page="
    eventListURL_start = "https://www.ufc.com/events"
    page = requests.get(eventListURL_start)
    soup = BeautifulSoup(page.content, 'html.parser')
    eventData = []
    # Number of events/pages
    if testPages == -1:
        numEvents = int(re.findall(r'\d+', soup.find_all('div', class_='althelete-total')[1].text)[0]) # number of events
        numPages = (numEvents // 8) - 1 if (numEvents % 8) == 0 else (numEvents // 8 ) # 12 events per page (starting at pg 0)
        print(str(numEvents) + " events\n" + str(numPages) + " pages")
    else:
        print("Testing " + str(testPages) + " pages")
        numPages = testPages - 1
    pageBar = tqdm(np.arange(0, numPages + 1), desc="Pages", unit='pages') # progress bar
    # Loop through all pages
    for pageNum in pageBar:
        currentURL = eventListURL_Base + str(pageNum)
        page = requests.get(currentURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = [link.get('href') for link in soup.select('h3.c-card-event--result__headline a[href]')] # extract href links from buttons
        if pageNum == 0: # first page contains 7 upcoming events that have not happened yet
            links = links[7:]
        if testEvents != -1:
            links = links[:testEvents]
        for link in links:
            updateString = "Page: " + str(pageNum) + " - Event: " + link.split("/")[-1].upper()
            pageBar.set_description(c.Color.BLUE + updateString.ljust(50) + c.Color.RESET)
            eventData.append(extractEventStats(link))
    return pd.DataFrame(eventData)

def scrapeFighters(testPages = -1, testFighters = -1):
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
            fighterData.append(extractFighterStats(link))
    return pd.DataFrame(fighterData)


# CONTROL PANEL
# Fighters_DF = scrapeFighters(testPages=3, testFighters=-1)
# print(Fighters_DF)

Events_DF = scrapeEvents(testPages=1, testEvents=2)