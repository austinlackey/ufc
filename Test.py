import pandas as pd
import numpy as np
import itertools

fighters = pd.read_csv('Clean Data/fighters_clean.csv')
fightRounds = pd.read_csv('Clean Data/fightRounds_clean.csv')

# Unique fighters Names
fightersNames = fighters['Name'].unique()
# print(fightersNames)
fightersRoundsNames = fightRounds['Fighter'].unique()
# print(fightersRoundsNames)

# Return a list of the fightersNames that are not in fightersRoundsNames
names1 = np.setdiff1d(fightersNames, fightersRoundsNames)
print(names1)

names2 = np.setdiff1d(fightersRoundsNames, fightersNames)
print(names2)

# is Joe Jordan in fightersNames
print('Joe Jordan' in fightersNames, 'Joe Jordan' in fightersRoundsNames)