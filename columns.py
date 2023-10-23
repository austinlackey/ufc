import pandas as pd
import numpy as np

fighters_clean = pd.read_csv('Clean Data/fighters_clean.csv')
fightInfo_clean = pd.read_csv('Clean Data/fightInfo_clean.csv')

# union of both column sets
cols = np.union1d(fighters_clean.columns, fightInfo_clean.columns)

print(cols)