import pandas as pd

# List of the specific CSV filenames
csv_files = [
    'tweets/2024-12-02_17-46-23_tweets_1-258.csv',
    'tweets/2024-12-03_21-44-51_tweets_1-497.csv',
    'tweets/2024-12-05_00-54-25_tweets_1-575.csv',
    'tweets/2024-12-02_18-04-40_tweets_1-390.csv',
    'tweets/2024-12-03_22-00-39_tweets_1-170.csv',
    'tweets/2024-12-05_00-58-01_tweets_1-159.csv',
    'tweets/2024-12-02_18-29-23_tweets_1-280.csv',
    'tweets/2024-12-03_22-01-41_tweets_1-41.csv',
    'tweets/2024-12-05_01-12-42_tweets_1-316.csv',
    'tweets/2024-12-02_18-35-16_tweets_1-531.csv',
    'tweets/2024-12-03_22-02-00_tweets_1-2.csv',
    'tweets/2024-12-05_01-28-08_tweets_1-242.csv',
    'tweets/2024-12-02_18-49-56_tweets_1-349.csv',
    'tweets/2024-12-03_22-15-01_tweets_1-95.csv',
    'tweets/2024-12-05_01-43-46_tweets_1-309.csv',
    'tweets/2024-12-02_19-04-26_tweets_1-486.csv',
    'tweets/2024-12-03_22-15-25_tweets_1-5.csv',
    'tweets/2024-12-05_01-58-10_tweets_1-306.csv',
    'tweets/2024-12-02_19-18-12_tweets_1-316.csv',
    'tweets/2024-12-03_22-17-03_tweets_1-46.csv',
    'tweets/2024-12-05_02-12-52_tweets_1-229.csv',
    'tweets/2024-12-02_19-35-57_tweets_1-296.csv',
    'tweets/2024-12-03_22-30-15_tweets_1-220.csv',
    'tweets/2024-12-05_02-27-48_tweets_1-470.csv',
    'tweets/2024-12-02_19-50-08_tweets_1-292.csv',
    'tweets/2024-12-03_22-46-30_tweets_1-199.csv',
    'tweets/2024-12-05_02-33-14_tweets_1-477.csv',
    'tweets/2024-12-02_20-05-57_tweets_1-429.csv',
    'tweets/2024-12-03_23-00-35_tweets_1-184.csv',
    'tweets/2024-12-05_02-45-06_tweets_1-207.csv',
    'tweets/2024-12-02_20-13-59_tweets_1-203.csv',
    'tweets/2024-12-03_23-15-41_tweets_1-171.csv',
    'tweets/2024-12-05_02-45-58_tweets_1-44.csv',
    'tweets/2024-12-02_20-19-58_tweets_1-192.csv',
    'tweets/2024-12-03_23-31-02_tweets_1-262.csv',
    'tweets/2024-12-05_02-46-24_tweets_1-21.csv',
    'tweets/2024-12-02_20-38-54_tweets_1-395.csv',
    'tweets/2024-12-04_23-49-37_tweets_1-287.csv',
    'tweets/2024-12-05_02-49-35_tweets_1-215.csv',
    'tweets/2024-12-02_20-51-54_tweets_1-303.csv',
    'tweets/2024-12-05_00-03-35_tweets_1-278.csv',
    'tweets/2024-12-02_21-07-36_tweets_1-441.csv',
    'tweets/2024-12-05_00-04-19_tweets_1-24.csv',
    'tweets/2024-12-03_21-11-42_tweets_1-8.csv',
    'tweets/2024-12-05_00-20-53_tweets_1-335.csv',
    'tweets/2024-12-03_21-14-12_tweets_1-587.csv',
    'tweets/2024-12-05_00-21-20_tweets_1-4.csv',
    'tweets/2024-12-03_21-28-56_tweets_1-319.csv',
    'tweets/2024-12-05_00-39-49_tweets_1-64.csv'
]

# Initialize an empty list to store dataframes
dfs = []

# Loop through each CSV file and read it into a DataFrame
for file in csv_files:
    df = pd.read_csv(file)  # Read each CSV file
    dfs.append(df)  # Add the DataFrame to the list

# Concatenate all dataframes into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('hindi_tweets1.csv', index=False)
