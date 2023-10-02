import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import re
import colors as c
from tqdm import tqdm
import string
import exception_handling as eh

print(c.Color.RED + "UFC Scraper v2.0" + c.Color.RESET)
domain = "https://www.ufc.com"

def extractEventStats(eventURL):
    pass

def extractFighterStats(fighterURL):
    # extract the p class "hero-profile__tag"
    page = requests.get(domain + fighterURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    name = eh.get_name(soup)
    print(name)

    # Fighter Nickname
    nickname = eh.get_nickname(soup)
    print(nickname)

    # Division
    division = eh.get_division(soup)
    print(division)

    # Fighter Record
    record = eh.get_record(soup)
    print(record)

    # Fighter Characteristics (Fighting Status, Birthplace, Age, Height, Weight, Octagon Debut)
    characteristics = eh.get_characteristics(soup)
    print(characteristics)

    # Significant Strikes
    sigStrikes = eh.get_sig_strikes(soup)
    print(sigStrikes)

    # numberCards (Significant Strikes Landed per Minute, Significant Strikes Absorbed per Minute, Take Down Average, Submission Average, 
    # Significant Strike Defense %, Take Down Defense %, Knockdown Average, Average Fight Time)
    numberCards = eh.get_number_cards(soup)
    print(numberCards)

    #Position Stats Significant Strikes per Position (Standing, Clinch, Ground)
    # Win by Method (Knockout/Technical Knockout, Decision, Submission)
    positionStats = eh.get_position_stats(soup)
    print(positionStats)
    
    #Takedown Stats
    takedownStats = eh.get_takedown_stats(soup)
    print("XXX")
    print(takedownStats)
    print("XXX")
    # Body Target Stats (Head, Body, Leg)
    bodyTargetStats = eh.get_target_body_stats(soup)
    print(bodyTargetStats)

def scrapeEvents(testPages = -1, testEvents = -1):
    eventListURL_Base = "https://www.ufc.com/events?page=0"
    eventListURL_start = "https://www.ufc.com/events"
    pass

def scrapeFighters(testPages = -1, testFighters = -1):
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
    pageBar = tqdm(np.arange(0, numPages + 1), desc="Pages", unit='pages') # progress bar
    # Loop through all pages
    for pageNum in pageBar:
        currentURL = fighterListURL_Base + str(pageNum)
        page = requests.get(currentURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', class_='e-button--black')] # extract href links from buttons
        if testFighters != -1:
            links = links[0:testFighters]
        for link in links:
            updateString = "Page: " + str(pageNum) + " - Fighter: " + link.split("/")[-1]
            pageBar.set_description(c.Color.BLUE + updateString.ljust(50) + c.Color.RESET)
            currentFighterData = extractFighterStats(link)
            # print(currentFighterData)


# CONTROL PANEL
scrapeFighters(testPages=1, testFighters=3)