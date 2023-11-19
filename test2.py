import pandas as pd

# Example date strings
date_strings = ["November 11, 2023", "1994-03-11"]

# Convert to datetime with the correct format, handling multiple formats
formatted_dates = pd.to_datetime(date_strings, errors='coerce')

# Extract NaT (Not a Time) entries
na_entries = formatted_dates[formatted_dates.isna()]

# Replace NaT entries with the alternate format
formatted_dates.update(pd.to_datetime(na_entries, format='%Y-%m-%d'))

print(formatted_dates)
