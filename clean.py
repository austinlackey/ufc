import pandas as pd
import numpy as np
import re

###############################
# ### Helper Functions ###   #
###############################
def extract_country(place_of_birth):
    place_of_birth = str(place_of_birth)
    if ',' in place_of_birth:
        return place_of_birth.split(',')[1].strip()
    else:
        return place_of_birth
def extract_city(place_of_birth):
    place_of_birth = str(place_of_birth)
    if ',' in place_of_birth:
        return place_of_birth.split(',')[0].strip()
    else:
        return np.nan
def time_to_seconds(time):
    if pd.isnull(time):
        return np.nan
    else:
        time = str(time)
        if ':' in time:
            minutes, seconds = time.split(':')
            return int(minutes) * 60 + int(seconds)
        else:
            return int(time)
################################
#        Clean Functions       #
################################
def clean_fighters(df):
    df['Nickname'] = df['Nickname'].str.replace('"', '')
    df['Country'] = df['Place_of_Birth'].apply(extract_country)
    df['City'] = df['Place_of_Birth'].apply(extract_city)
    df['Octagon_Debut'] = pd.to_datetime(df['Octagon_Debut'])
    df['Octagon_Debut_Year'] = df['Octagon_Debut'].dt.year
    df['Octagon_Debut_Month'] = df['Octagon_Debut'].dt.month
    df['Octagon_Debut_Day'] = df['Octagon_Debut'].dt.day
    df['Avg_Fight_Time_Seconds'] = df['Avg_Fight_Time'].apply(time_to_seconds)
    df['Avg_Fight_Time_Minutes'] = df['Avg_Fight_Time_Seconds'] / 60
    df['Sig_Str_Defense'] = df['Sig_Str_Defense'] / 100
    df['Takedown_Defense'] = df['Takedown_Defense'] / 100

    cols_to_int = ['Wins', 'Losses', 'Draws', 'Age', 'Sig_Str_Landed', 'Sig_Str_Attempted', 'Standing', 'Clinch', 'Ground', 'Head', 'Body', 'Leg', 'KO/TKO', 'DEC', 'SUB', 'Takedowns_Landed', 'Takedowns_Attempted']
    df[cols_to_int] = df[cols_to_int].astype('Int64')
    return df
def clean_fightInfo(df):
    pass
def clean_fightRounds(df):
    pass
def clean_fightTotals(df):
    pass

###############################
#         Raw Data           #
###############################
fighters_raw = pd.read_csv('Raw Data/fighters.csv')
# fightInfo_raw = pd.read_csv('Raw Data/fightInformation.csv')
# fightRounds_raw = pd.read_csv('Raw Data/fightRounds.csv')
# fightTotals_raw = pd.read_csv('Raw Data/fightTotals.csv')

###############################
#         Clean Data          #
###############################
fighters_clean = clean_fighters(fighters_raw)
# fightInfo_clean = clean_fightInfo(fightInfo_raw)
# fightRounds_clean = clean_fightRounds(fightRounds_raw)
# fightTotals_clean = clean_fightTotals(fightTotals_raw)

###############################
#         Save Data           #
###############################
fighters_clean.to_csv('Clean Data/fighters_clean.csv', index=False)
print(fighters_clean.iloc[:, 0:15])