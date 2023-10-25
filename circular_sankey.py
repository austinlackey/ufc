import pandas as pd
import numpy as np

fighters = pd.read_csv('Clean Data/fighters_clean.csv')
fights = pd.read_csv('Clean Data/fightInfo_clean.csv')
streaks = pd.read_csv('Test Data/winStreaks.csv')


# sort streaks by the streak column
streaks = streaks.sort_values(by=['streak'], ascending=False).reset_index(drop=True)
streaks = streaks.loc[streaks['streak'] >= 9].reset_index(drop=True)

#filter fights to only inlcude fights between jan 1 2022 and dec 31 2022
fights['Date'] = pd.to_datetime(fights['Date'])
# fights = fights.loc[(fights['Date'] >= '2022-01-01') & (fights['Date'] <= '2022-11-28')].reset_index(drop=True)
fights['Date'] = fights['Date'].dt.strftime('%Y-%m-%d')

# Split fights for each fighter
fights_A = fights.drop(columns=['Fighter_B'])
fights_B = fights.drop(columns=['Fighter_A'])
fights_A = fights_A.rename(columns={'Fighter_A': 'Fighter'})
fights_B = fights_B.rename(columns={'Fighter_B': 'Fighter'})
fights = pd.concat([fights_A, fights_B]).sort_values(by=['Date']).reset_index(drop=True)

# Filter fights to only include fights from streaks
fights = fights.loc[(fights['Fighter'].isin(streaks['fighter']))].reset_index(drop=True)

# Grouping by fighter and event
fights = fights.groupby(['Fighter', 'Event']).sum().reset_index().merge(fights.groupby(['Fighter']).size().reset_index(), on='Fighter', how='left').rename(columns={0: 'numFights'}).sort_values(by=['Date']).reset_index(drop=True)
fighters = fighters[fighters['Name'].isin(fights['Fighter'].unique())].reset_index(drop=True).reset_index()

# Adding Ranks
# return fights with rows for each event that are unique and sorted by date
fightsOriginal = pd.DataFrame(fights['Event'].unique(), columns=['Event']).reset_index().merge(fights[['Event', 'Date']].drop_duplicates(), on='Event', how='left').sort_values(by=['Date']).reset_index(drop=True)
fights = fights.merge(fighters[['index', 'Name']], left_on='Fighter', right_on='Name', how='left').drop(columns=['Name']).rename(columns={'index': 'fighterRank'})
fights['fighterRank'] = fights['fighterRank'].astype(pd.Int64Dtype())
fights = fights.merge(fightsOriginal[['Event', 'index']], on='Event', how='left').rename(columns={'index': 'eventRank'}).reset_index(drop=True)

# Data Densification
fights['one'] = 1
fights['numRecords'] = 1
df = pd.DataFrame({
    'one': 1,
    't': np.concatenate([np.arange(0, 1.01, 0.01), np.array([2,3])])
})
fights['winStatus'] = np.where(fights['Winner_Name'] == fights['Fighter'], 'Win', 'Loss')
print(fights)
print(df)

fights.to_csv('Test Data/radial_sankey_fights.csv', index=False)
df.to_csv('Test Data/radial_sankey_df.csv', index=False)
