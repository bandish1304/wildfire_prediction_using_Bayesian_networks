import pandas as pd

# Load merged data
df = pd.read_csv('data/processed/merged_weather_wildfire.csv')

# Step 1: Check for missing values in key columns
key_columns = ['TAVG_CAT', 'TMAX_CAT', 'TMIN_CAT', 'PRCP_CAT', 'SEASON_weather']
print('Missing values per key column:')
print(df[key_columns].isnull().sum())

# Step 2: Drop rows with missing values in key columns
df = df.dropna(subset=key_columns)

# Step 3: Ensure all variables are categorical
df['TAVG_CAT'] = df['TAVG_CAT'].astype(str)
df['TMAX_CAT'] = df['TMAX_CAT'].astype(str)
df['TMIN_CAT'] = df['TMIN_CAT'].astype(str)
df['PRCP_CAT'] = df['PRCP_CAT'].astype(str)
df['SEASON_weather'] = df['SEASON_weather'].astype(str)

# Step 4: Create WILDFIRE_OCCURRENCE (1 if a fire occurred, else 0)
df['WILDFIRE_OCCURRENCE'] = 1  # All rows in merged data have a fire event

# Save the prepared data for modeling
df.to_csv('data/processed/model_data.csv', index=False)
print('Prepared data saved to data/processed/model_data.csv')
