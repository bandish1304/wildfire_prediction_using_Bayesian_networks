import pandas as pd
import numpy as np
weather_df = pd.read_csv('data/raw/weatherData.csv')
print('Weather Data Sample:')
print(weather_df.head())
print('\nColumns:', weather_df.columns.tolist())
print('\nMissing values per column:')
print(weather_df.isnull().sum())
weather_cols = ['DATE', 'TAVG', 'TMAX', 'TMIN', 'AWND', 'PRCP']
weather_clean = weather_df[weather_cols].copy()
for col in ['TAVG', 'TMAX', 'TMIN', 'AWND', 'PRCP']:
	weather_clean[col] = pd.to_numeric(weather_clean[col], errors='coerce')
weather_clean = weather_clean[weather_clean['PRCP'].notnull() & weather_clean['DATE'].notnull()].copy()
weather_clean.to_csv('data/processed/weather_processed.csv', index=False)
print('\nCleaned weather data saved to data/processed/weather_processed.csv')
weather_categorized = weather_clean.copy()
def make_category(series, labels=['Low', 'Medium', 'High']):
	if series.nunique() >= 3:
		bins = list(series.quantile([0, 1/3, 2/3, 1]).values)
		bins = sorted(set(bins))
		if len(bins) == 4:
			return pd.cut(series, bins=bins, labels=labels, include_lowest=True)
	return 'Unknown'
weather_categorized['TAVG_CAT'] = make_category(weather_clean['TAVG'])
weather_categorized['TMAX_CAT'] = make_category(weather_clean['TMAX'])
weather_categorized['TMIN_CAT'] = make_category(weather_clean['TMIN'])
if weather_clean['PRCP'].nunique() > 1:
	prcp_bins = [weather_clean['PRCP'].min()-1, 0, weather_clean['PRCP'].median(), weather_clean['PRCP'].max()+1]
	prcp_labels = ['Dry', 'Light', 'Wet']
	if len(set(prcp_bins)) == len(prcp_bins):
		weather_categorized['PRCP_CAT'] = pd.cut(weather_clean['PRCP'], bins=prcp_bins, labels=prcp_labels, include_lowest=True)
	else:
		# Not enough variation, assign all as 'Dry'
		weather_categorized['PRCP_CAT'] = 'Dry'
else:
	weather_categorized['PRCP_CAT'] = 'Unknown'


# --- Date Feature Extraction for Weather ---
weather_categorized['DATE'] = pd.to_datetime(weather_categorized['DATE'], errors='coerce')
weather_categorized['MONTH'] = weather_categorized['DATE'].dt.month
weather_categorized['DAY_OF_WEEK'] = weather_categorized['DATE'].dt.dayofweek
weather_categorized['SEASON'] = weather_categorized['MONTH'].map({12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',6:'Summer',7:'Summer',8:'Summer',9:'Fall',10:'Fall',11:'Fall'})

# Save categorized weather data
weather_categorized.to_csv('data/processed/weather_categorized.csv', index=False)
print('\nCategorized weather data saved to data/processed/weather_categorized.csv')


# --- Wildfire Data Cleaning ---
wildfire_df = pd.read_csv('data/raw/mapdataall.csv')

# Inspect the first few rows
print('\nWildfire Data Sample:')
print(wildfire_df.head())

# Show columns and missing values
print('\nWildfire Columns:', wildfire_df.columns.tolist())
print('\nWildfire missing values per column:')
print(wildfire_df.isnull().sum())


# Select relevant columns for wildfire data (customize as needed)
wildfire_cols = ['incident_name', 'incident_dateonly_created', 'incident_county', 'incident_acres_burned', 'incident_latitude', 'incident_longitude']
wildfire_clean = wildfire_df[wildfire_cols].copy()

# Convert acres burned and coordinates to numeric
for col in ['incident_acres_burned', 'incident_latitude', 'incident_longitude']:
	wildfire_clean[col] = pd.to_numeric(wildfire_clean[col], errors='coerce')

# Drop rows with missing values in these columns
wildfire_clean = wildfire_clean.dropna()


# --- Date Feature Extraction for Wildfire ---
wildfire_clean['incident_dateonly_created'] = pd.to_datetime(wildfire_clean['incident_dateonly_created'], errors='coerce')
wildfire_clean['MONTH'] = wildfire_clean['incident_dateonly_created'].dt.month
wildfire_clean['DAY_OF_WEEK'] = wildfire_clean['incident_dateonly_created'].dt.dayofweek
wildfire_clean['SEASON'] = wildfire_clean['MONTH'].map({12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',6:'Summer',7:'Summer',8:'Summer',9:'Fall',10:'Fall',11:'Fall'})

# Categorize incident_acres_burned into Small/Medium/Large
def fire_size_category(series):
	if series.nunique() >= 3:
		bins = list(series.quantile([0, 1/3, 2/3, 1]).values)
		bins = sorted(set(bins))
		if len(bins) == 4:
			return pd.cut(series, bins=bins, labels=['Small', 'Medium', 'Large'], include_lowest=True)
	return 'Unknown'

wildfire_clean['FIRE_SIZE_CAT'] = fire_size_category(wildfire_clean['incident_acres_burned'])


# Save cleaned wildfire data
wildfire_clean.to_csv('data/processed/wildfire_processed.csv', index=False)
print('\nCleaned wildfire data saved to data/processed/wildfire_processed.csv (with fire size category)')

# --- Merge Weather and Wildfire Data ---

print('\nMerging wildfire events with closest previous weather date (as-of join)...')
# Reload processed files to ensure all features are present
weather = pd.read_csv('data/processed/weather_categorized.csv')
wildfire = pd.read_csv('data/processed/wildfire_processed.csv')

# Standardize date columns to datetime
weather['DATE'] = pd.to_datetime(weather['DATE'], errors='coerce')
wildfire['incident_dateonly_created'] = pd.to_datetime(wildfire['incident_dateonly_created'], errors='coerce')

# Sort both DataFrames by date for merge_asof

# Ensure both date columns are datetime64[ns] for merge_asof compatibility

weather['DATE'] = weather['DATE'].astype('datetime64[ns]')
wildfire['incident_dateonly_created'] = wildfire['incident_dateonly_created'].astype('datetime64[ns]')

# Filter wildfire events to only those on or after the earliest weather date
min_weather_date = weather['DATE'].min()
wildfire = wildfire[wildfire['incident_dateonly_created'] >= min_weather_date].copy()

# Sort both DataFrames by date for merge_asof
weather = weather.sort_values('DATE')
wildfire = wildfire.sort_values('incident_dateonly_created')

# Perform as-of join: for each wildfire, get the most recent weather on or before the fire date
merged = pd.merge_asof(
	wildfire,
	weather,
	left_on='incident_dateonly_created',
	right_on='DATE',
	direction='backward',
	suffixes=('_fire', '_weather')
)

# Save merged dataset
merged.to_csv('data/processed/merged_weather_wildfire.csv', index=False)
print(f"Merged dataset saved to data/processed/merged_weather_wildfire.csv. Rows: {len(merged)}")
