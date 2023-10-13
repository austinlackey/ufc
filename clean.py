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
def format_to_rounds(format):
    if pd.isnull(format):
        return np.nan
    else:
        match = re.search(r'\d+', format)
        if match:
            return int(match.group())
        else:
            return np.nan
def extract_att_landed(string):
    if pd.isnull(string):
        return pd.Series([np.nan, np.nan])
    else:
        landed, attempted = string.split(' of ')
        return pd.Series([int(landed), int(attempted)])
def replace_dashes(string):
    if pd.isnull(string):
        return np.nan
    if '-' in string:
        return None
    else:
        return string
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
    df['Time_Seconds'] = df['Time'].apply(time_to_seconds)
    df['Time_Minutes'] = df['Time_Seconds'] / 60
    df['Round_Format'] = df['Format'].apply(format_to_rounds)
    df['Unique_Fight_ID'] = df['Event'] + df['Fight'] + df['Date'].astype(str)
    return df
def clean_fightRounds(df):
    df['Sig_Str_Landed'] = df['Sig_Str'].apply(lambda x: extract_att_landed(x)[0])
    df['Sig_Str_Attempted'] = df['Sig_Str'].apply(lambda x: extract_att_landed(x)[1])
    df['Sig_Str_Perc'] = df['Sig_Str_Landed'] / df['Sig_Str_Attempted']
    df['Total_Str_Landed'] = df['Total_Str'].apply(lambda x: extract_att_landed(x)[0])
    df['Total_Str_Attempted'] = df['Total_Str'].apply(lambda x: extract_att_landed(x)[1])
    df['Total_Str_Perc'] = df['Total_Str_Landed'] / df['Total_Str_Attempted']
    df['TD_Landed'] = df['TD'].apply(lambda x: extract_att_landed(x)[0])
    df['TD_Attempted'] = df['TD'].apply(lambda x: extract_att_landed(x)[1])
    df['TD_Perc'] = df['TD_Landed'] / df['TD_Attempted']
    df['Ctrl'] = df['Ctrl'].apply(replace_dashes)
    df['Ctrl_Time_Seconds'] = df['Ctrl'].apply(time_to_seconds)
    df['Ctrl_Time_Minutes'] = df['Ctrl_Time_Seconds'] / 60
    df['Head_Landed'] = df['Head'].apply(lambda x: extract_att_landed(x)[0])
    df['Head_Attempted'] = df['Head'].apply(lambda x: extract_att_landed(x)[1])
    df['Head_Perc'] = df['Head_Landed'] / df['Head_Attempted']
    df['Body_Landed'] = df['Body'].apply(lambda x: extract_att_landed(x)[0])
    df['Body_Attempted'] = df['Body'].apply(lambda x: extract_att_landed(x)[1])
    df['Body_Perc'] = df['Body_Landed'] / df['Body_Attempted']
    df['Leg_Landed'] = df['Leg'].apply(lambda x: extract_att_landed(x)[0])
    df['Leg_Attempted'] = df['Leg'].apply(lambda x: extract_att_landed(x)[1])
    df['Leg_Perc'] = df['Leg_Landed'] / df['Leg_Attempted']
    df['Distance_Landed'] = df['Distance'].apply(lambda x: extract_att_landed(x)[0])
    df['Distance_Attempted'] = df['Distance'].apply(lambda x: extract_att_landed(x)[1])
    df['Distance_Perc'] = df['Distance_Landed'] / df['Distance_Attempted']
    df['Clinch_Landed'] = df['Clinch'].apply(lambda x: extract_att_landed(x)[0])
    df['Clinch_Attempted'] = df['Clinch'].apply(lambda x: extract_att_landed(x)[1])
    df['Clinch_Perc'] = df['Clinch_Landed'] / df['Clinch_Attempted']
    df['Ground_Landed'] = df['Ground'].apply(lambda x: extract_att_landed(x)[0])
    df['Ground_Attempted'] = df['Ground'].apply(lambda x: extract_att_landed(x)[1])
    df['Ground_Perc'] = df['Ground_Landed'] / df['Ground_Attempted']
    return df
def clean_fightTotals(df):
    df['Sig_Str_Landed'] = df['Sig_Str'].apply(lambda x: extract_att_landed(x)[0])
    df['Sig_Str_Attempted'] = df['Sig_Str'].apply(lambda x: extract_att_landed(x)[1])
    df['Sig_Str_Perc'] = df['Sig_Str_Landed'] / df['Sig_Str_Attempted']
    df['Total_Str_Landed'] = df['Total_Str'].apply(lambda x: extract_att_landed(x)[0])
    df['Total_Str_Attempted'] = df['Total_Str'].apply(lambda x: extract_att_landed(x)[1])
    df['Total_Str_Perc'] = df['Total_Str_Landed'] / df['Total_Str_Attempted']
    df['TD_Landed'] = df['TD'].apply(lambda x: extract_att_landed(x)[0])
    df['TD_Attempted'] = df['TD'].apply(lambda x: extract_att_landed(x)[1])
    df['TD_Perc'] = df['TD_Landed'] / df['TD_Attempted']
    df['Ctrl'] = df['Ctrl'].apply(replace_dashes)
    df['Ctrl_Time_Seconds'] = df['Ctrl'].apply(time_to_seconds)
    df['Ctrl_Time_Minutes'] = df['Ctrl_Time_Seconds'] / 60
    df['Head_Landed'] = df['Head'].apply(lambda x: extract_att_landed(x)[0])
    df['Head_Attempted'] = df['Head'].apply(lambda x: extract_att_landed(x)[1])
    df['Head_Perc'] = df['Head_Landed'] / df['Head_Attempted']
    df['Body_Landed'] = df['Body'].apply(lambda x: extract_att_landed(x)[0])
    df['Body_Attempted'] = df['Body'].apply(lambda x: extract_att_landed(x)[1])
    df['Body_Perc'] = df['Body_Landed'] / df['Body_Attempted']
    df['Leg_Landed'] = df['Leg'].apply(lambda x: extract_att_landed(x)[0])
    df['Leg_Attempted'] = df['Leg'].apply(lambda x: extract_att_landed(x)[1])
    df['Leg_Perc'] = df['Leg_Landed'] / df['Leg_Attempted']
    df['Distance_Landed'] = df['Distance'].apply(lambda x: extract_att_landed(x)[0])
    df['Distance_Attempted'] = df['Distance'].apply(lambda x: extract_att_landed(x)[1])
    df['Distance_Perc'] = df['Distance_Landed'] / df['Distance_Attempted']
    df['Clinch_Landed'] = df['Clinch'].apply(lambda x: extract_att_landed(x)[0])
    df['Clinch_Attempted'] = df['Clinch'].apply(lambda x: extract_att_landed(x)[1])
    df['Clinch_Perc'] = df['Clinch_Landed'] / df['Clinch_Attempted']
    df['Ground_Landed'] = df['Ground'].apply(lambda x: extract_att_landed(x)[0])
    df['Ground_Attempted'] = df['Ground'].apply(lambda x: extract_att_landed(x)[1])
    df['Ground_Perc'] = df['Ground_Landed'] / df['Ground_Attempted']
    return df

###############################
#         Raw Data           #
###############################
fighters_raw = pd.read_csv('Raw Data/fighters.csv')
fightInfo_raw = pd.read_csv('Raw Data/fightInformation.csv')
fightRounds_raw = pd.read_csv('Raw Data/fightRounds.csv')
fightTotals_raw = pd.read_csv('Raw Data/fightTotals.csv')

###############################
#         Clean Data          #
###############################
fighters_clean = clean_fighters(fighters_raw)
fightInfo_clean = clean_fightInfo(fightInfo_raw)
fightRounds_clean = clean_fightRounds(fightRounds_raw)
fightTotals_clean = clean_fightTotals(fightTotals_raw)

###############################
#         Save Data           #
###############################
fighters_clean.to_csv('Clean Data/fighters_clean.csv', index=False)
# print(fighters_clean.iloc[:, 13:23])

fightInfo_clean.to_csv('Clean Data/fightInfo_clean.csv', index=False)
# print(fightInfo_clean.iloc[:, 13:23])

fightRounds_clean.to_csv('Clean Data/fightRounds_clean.csv', index=False)
# print(fightRounds_clean.iloc[:, 16:22])

fightTotals_clean.to_csv('Clean Data/fightTotals_clean.csv', index=False)
# print(fightTotals_clean.iloc[:, 17:25])

print("Done!")