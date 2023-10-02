import re
import requests
from bs4 import BeautifulSoup
import string

def cleanString(string):
    # remove newlines and trailing spaces
    string = string.replace('\n', '').strip()
    return string

def cleanStrings(arr):
    # remove newlines and trailing spaces
    arr = [string.replace('\n', '').strip() for string in arr]
    # remove empty strings
    arr = [string for string in arr if string != '']
    return arr

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return None
    return wrapper

@handle_exceptions
def get_name(soup):
    return soup.find('h1', class_='hero-profile__name').text

@handle_exceptions
def get_nickname(soup):
    return soup.find('p', class_='hero-profile__nickname').text

@handle_exceptions
def get_division(soup):
    return soup.find('p', class_='hero-profile__division-title').text

@handle_exceptions
def get_record(soup):
    return soup.find('p', class_='hero-profile__division-body').text

@handle_exceptions
def get_characteristics(soup):
    return cleanStrings([char.text for char in soup.find_all('div', class_='c-bio__text')])

@handle_exceptions
def get_sig_strikes(soup):
    return cleanStrings([stat.text for stat in soup.find_all('dd', class_='c-overlap__stats-value')])

@handle_exceptions
def get_number_cards(soup):
    return cleanStrings([card.text.replace("%", "") for card in soup.find_all('div', class_='c-stat-compare__number')]) # Getting rid of the % in the text

@handle_exceptions
def get_position_stats(soup):
    return cleanStrings([re.sub(r'\(.*?\)', '', stat.text) for stat in soup.find_all('div', class_='c-stat-3bar__value')]) # Getting rid of the (x%) in the text

@handle_exceptions
def get_target_body_stats(soup):
    headStats = soup.find('text', id='e-stat-body_x5F__x5F_head_value').text
    bodyStats = soup.find('text', id='e-stat-body_x5F__x5F_body_value').text
    legStats = soup.find('text', id='e-stat-body_x5F__x5F_leg_value').text
    return cleanStrings([headStats, bodyStats, legStats])

@handle_exceptions
def get_takedown_stats(soup):
    print([stat.text for stat in soup.find_all('dd', class_='c-overlap__stats-value')])
    return cleanStrings([stat.text for stat in soup.find_all('dd', class_='c-overlap__stats-value')])