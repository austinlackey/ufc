import pandas as pd

# Generate the dates
dates = pd.date_range(start='1990-01-01', end='2030-12-31')

# Create the DataFrame
df = pd.DataFrame(dates, columns=['Date'])

# Extract the week number, month number, and year
df['Week'] = df['Date'].dt.isocalendar().week
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

print(df.head())
df.to_csv('Test Data/dates.csv', index=False)