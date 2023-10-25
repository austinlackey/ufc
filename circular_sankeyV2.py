import pandas as pd
import numpy as np

fighters = pd.read_csv('Clean Data/fighters_clean.csv')
fights = pd.read_csv('Clean Data/fightInfo_clean.csv')
streaks = pd.read_csv('Test Data/winStreaks.csv')
print(streaks)

# Formatting and Adding Date Columns
fights['Date'] = pd.to_datetime(fights['Date'])
fights['Date_Year'] = fights['Date'].dt.year
fights['Date_Month'] = fights['Date'].dt.month
fights['Date_M_Y'] = fights['Date'].dt.strftime('%Y-%m')
fights['Date'] = fights['Date'].dt.strftime('%Y-%m-%d')

# Splitting fights for each fighter
fights_A = fights.drop(columns=['Fighter_B'])
fights_B = fights.drop(columns=['Fighter_A'])
fights_A = fights_A.rename(columns={'Fighter_A': 'Fighter'})
fights_B = fights_B.rename(columns={'Fighter_B': 'Fighter'})
fights = pd.concat([fights_A, fights_B]).sort_values(by=['Date']).reset_index(drop=True)
fights = fights.sort_values(by=['Date', 'Fight']).reset_index(drop=True)

# Sorting Streaks
streaks = streaks.sort_values(by=['streak'], ascending=False).reset_index(drop=True)
streaks = streaks.loc[streaks['streak'] >= 8].reset_index(drop=True)
fights['streakFighter'] = np.where(fights['Fighter'].isin(streaks['fighter']), 1, 0)
fights['topStreak'] = fights['Fighter'].map(streaks.groupby('fighter')['streak'].max())

# Grouping
fights = fights.groupby(['Fighter', 'Event']).sum().reset_index().merge(fights.groupby(['Fighter']).size().reset_index(), on='Fighter', how='left').rename(columns={0: 'numFights'}).sort_values(by=['Date', 'Fight']).reset_index(drop=True)
fighters = fighters[fighters['Name'].isin(streaks['fighter'].unique())].reset_index(drop=True).reset_index()

# Adding Ranks
fightsOriginal = pd.DataFrame(fights['Event'].unique(), columns=['Event']).reset_index()
fights = fights.merge(fighters[['index', 'Name']], left_on='Fighter', right_on='Name', how='left').drop(columns=['Name']).rename(columns={'index': 'fighterRank'})
fights['fighterRank'] = fights['fighterRank'].astype(pd.Int64Dtype())
fights = fights.merge(fightsOriginal[['Event', 'index']], on='Event', how='left').rename(columns={'index': 'eventRank'}).reset_index(drop=True)

# Data Densification
fights['one'] = 1
fights['numRecords'] = 1
df = pd.DataFrame({
    'one': 1,
    't': np.concatenate([np.arange(0, 1.01, 0.01), np.array([2,3]), np.arange(4, 5.01, 0.01), np.array([6])])
})
fights['winStatus'] = np.where(fights['Winner_Name'] == fights['Fighter'], 'Win', 'Loss')

print(fights)
print(fights[fights['streakFighter'] == 1])

fights.to_csv('Test Data/radial_sankey_fights2.csv', index=False)
df.to_csv('Test Data/radial_sankey_df2.csv', index=False)