import pandas as pd
import numpy as np
import itertools

fighters = pd.read_csv('Clean Data/fighters_clean.csv')
fightRounds = pd.read_csv('Clean Data/fightRounds_clean.csv')
info = pd.read_csv('Clean Data/fightInfo_clean.csv')

print(info.columns)

# Ensure that the 'Date' column is in datetime format
info['Date'] = pd.to_datetime(info['Date'])

# Set the date range
start_date = '1994-01-01'
end_date = '2023-12-31'

# Create a new DataFrame that includes all months in the range
all_months = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq='M'), columns=['Date'])

# Group the original data by month and count the number of rows for each month
monthly_counts = info.groupby(pd.Grouper(key='Date', freq='M')).size().reset_index(name='Count')

# Merge the new DataFrame with the original data
monthly_counts = pd.merge(all_months, monthly_counts, how='left', on='Date')

# Fill NaN values with 0
monthly_counts['Count'] = monthly_counts['Count'].fillna(0).astype(int)

print(monthly_counts)

monthly_counts.to_csv('Test Data/monthly_counts.csv', index=False)