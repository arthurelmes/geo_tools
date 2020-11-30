import pandas as pd

# read in two csvs as pandas dfs
# also define that 'Date' is the index
df1 = pd.read_csv('/home/arthur/Dropbox/projects/greenland/station_data/appears_extraction/noaa_summit/'
                  'combined_manual_location/noaa-summit-manual-location-mcd2/'
                  'summit-manual-location-mcd2-MCD43A3-006-results.csv', index_col='Date')

df2 = pd.read_csv('/home/arthur/Dropbox/projects/greenland/station_data/appears_extraction/noaa_summit/'
                  'combined_manual_location/noaa-summit-manual-location-vnp/'
                  'noaa-summit-manual-location-VNP-MCD-VNP43MA3-001-results.csv', index_col='Date')

# specify join field name (should be same for both for now)
join_field = 'Date'

# join on join field to new df
df3 = df1.join(df2,
               how='left',
               lsuffix='_mcd',
               rsuffix='_vnp')
print(df3)

# export new df to csv
df3.to_csv('/home/arthur/Dropbox/projects/greenland/station_data/appears_extraction/noaa_summit/'
                  'combined_manual_location/summit-manual-location-joined.csv')