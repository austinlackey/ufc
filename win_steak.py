import pandas as pd
import numpy as np
import itertools

fights = pd.read_csv('Clean Data/fightInfo_clean.csv')

fights['Date'] = pd.to_datetime(fights['Date'])
fighterA = fights['Fighter_A'].unique()
fighterB = fights['Fighter_B'].unique()
union = np.union1d(fighterA, fighterB)
winStreaks = []
def filterFights(fighter):
    return fights.loc[(fights['Fighter_A'] == fighter) | (fights['Fighter_B'] == fighter)]

def winStreak(fighter, print=False):
    global allFights
    fighterFights = filterFights(fighter) # Get all fights for fighter
    fighterFights = fighterFights.sort_values(by=['Date'], ascending=True).reset_index(drop=True) # Sort by date
    fighterFights['Win'] = np.where(fighterFights['Winner_Name'] == fighter, 1, 0) # Add win column
    #concat fighterFights with allFights
    if sum(fighterFights['Win']) == 0: # If no wins, then no win streak
        return
    fighterFights['Prev_Win'] = fighterFights['Win'].shift(1) # Add previous win column
    fighterFights = fighterFights[~((fighterFights['Win'] == 0) & (fighterFights['Prev_Win'] == 0))] # Remove consecutive losses
    fighterFights = fighterFights.drop(columns=['Prev_Win']).reset_index(drop=True) # Remove previous win column

    if fighterFights['Win'].iloc[0] == 0: # If first fight is a loss, then remove it
        fighterFights = fighterFights.iloc[1:].reset_index(drop=True)
    loss_locations = fighterFights.index[fighterFights['Win'] == 0].tolist() # Get all loss locations
    if len(loss_locations) == 0: # If no losses, then current win streak
        winStreaks.append(dict(fighter=fighter, streak=len(fighterFights), startDate=fighterFights['Date'].iloc[0], endDate=fighterFights['Date'].iloc[-1], current=True))
        return
    loss_locations = [x+1 for x in loss_locations]
    loss_locations.insert(0, 0)
    if loss_locations[-1] != len(fighterFights):
        loss_locations.append(len(fighterFights))
    if print:
        print(fighterFights)
        print(loss_locations)
    for i in np.arange(0, len(loss_locations)-1):
        sub = fighterFights.iloc[loss_locations[i]:loss_locations[i+1]]
        if print:
            print(sub)
        if 0 in sub['Win'].values:
            winStreaks.append(dict(fighter=fighter, streak=len(sub)-1, startDate=sub['Date'].iloc[0], endDate=sub['Date'].iloc[-2], current=False))
        else:
            winStreaks.append(dict(fighter=fighter, streak=len(sub), startDate=sub['Date'].iloc[0], endDate=sub['Date'].iloc[-1], current=True))
for fighter in union:
    print(fighter)
    winStreak(fighter, print=False)
# winStreak('Aalon Cruz')
winStreaks = pd.DataFrame(winStreaks).sort_values(by=['streak'], ascending=False).reset_index(drop=True)
print(winStreaks)
winStreaks.to_csv('Test Data/winStreaks.csv', index=False)
