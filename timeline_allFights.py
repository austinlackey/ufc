import pandas as pd
import numpy as np
import itertools

fights = pd.read_csv('Clean Data/fightInfo_clean.csv')

fighterA = fights['Fighter_A'].unique()
fighterB = fights['Fighter_B'].unique()
union = np.union1d(fighterA, fighterB)
allFights = pd.DataFrame()
def filterFights(fighter):
    return fights.loc[(fights['Fighter_A'] == fighter) | (fights['Fighter_B'] == fighter)].reset_index(drop=True)
# union = union[0:3]
for fighter in union:
    print(fighter)
    fighterFights = filterFights(fighter) # Get all fights for fighter
    fighterFights['Opponent'] = fighterFights.apply(lambda row: row['Fighter_A'] if row['Fighter_A'] != fighter else row['Fighter_B'], axis=1)
    fighterFights['Fighter'] = fighter
    fighterFights['Win'] = np.where(fighterFights['Winner_Name'] == fighter, 1, 0) # Add win column
    fighterFights = fighterFights.drop(columns=['Fighter_A', 'Fighter_B', 'Winner_Name', 'Winner'])
    allFights = pd.concat([allFights, fighterFights], ignore_index=True)
print(allFights)
allFights.to_csv('Test Data/timeline_allFights.csv', index=False)