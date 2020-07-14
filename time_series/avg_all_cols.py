import pandas as pd

working_dir = '/home/arthur/Dropbox/projects/greenland/sensor_intercompare/'
in_csv_name = working_dir + 'mcd_pts_3k_wgs84_extracted_values_MCD43A3.csv'
in_df = pd.read_csv(in_csv_name, index_col=0)

mean_df = pd.DataFrame()

mean_df['mean'] = in_df.mean(axis=1)
mean_df['sd'] = in_df.std(axis=1)

mean_df.to_csv(working_dir + 'mcd43a3_summary_stats.csv')
