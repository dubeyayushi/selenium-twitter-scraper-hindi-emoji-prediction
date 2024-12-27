import pandas as pd

# List of the specific CSV filenames
csv_files = [
    'tweets/2024-12-26_23-13-48_tweets_1-30.csv',
    'tweets/2024-12-26_23-29-44_tweets_1-250.csv',
    'tweets/2024-12-26_23-30-52_tweets_1-24.csv',
    'tweets/2024-12-26_23-45-04_tweets_1-136.csv',
    'tweets/2024-12-26_23-45-33_tweets_1-11.csv',
    'tweets/2024-12-26_23-59-47_tweets_1-127.csv',
    'tweets/2024-12-27_00-01-23_tweets_1-30.csv',
    'tweets/2024-12-27_00-02-30_tweets_1-73.csv',
    'tweets/2024-12-27_00-15-56_tweets_1-69.csv',
    'tweets/2024-12-27_02-20-38_tweets_1-3.csv',
    'tweets/2024-12-27_02-22-15_tweets_1-45.csv',
    'tweets/2024-12-27_02-23-49_tweets_1-25.csv',
    'tweets/2024-12-27_02-37-12_tweets_1-68.csv',
    'tweets/2024-12-27_02-37-28_tweets_1-1.csv',
    'tweets/2024-12-27_02-37-59_tweets_1-3.csv',
    'tweets/2024-12-27_02-51-25_tweets_1-67.csv',
    'tweets/2024-12-27_03-06-38_tweets_1-138.csv',
    'tweets/2024-12-27_03-09-16_tweets_1-6.csv',
    'tweets/2024-12-27_03-10-16_tweets_1-21.csv',
    'tweets/2024-12-27_03-10-43_tweets_1-13.csv',
    'tweets/2024-12-27_03-24-05_tweets_1-199.csv',
    'tweets/2024-12-27_03-25-36_tweets_1-24.csv',
    'tweets/2024-12-27_03-26-04_tweets_1-4.csv',
    'tweets/2024-12-27_03-37-00_tweets_1-12.csv',
    'tweets/2024-12-27_03-42-15_tweets_1-204.csv',
    'tweets/2024-12-27_03-55-33_tweets_1-102.csv',
    'tweets/2024-12-27_04-10-38_tweets_1-156.csv',
    'tweets/2024-12-27_04-11-59_tweets_1-44.csv',
    'tweets/2024-12-27_04-12-39_tweets_1-27.csv',
    'tweets/2024-12-27_04-28-07_tweets_1-183.csv',
    'tweets/2024-12-27_04-41-23_tweets_1-80.csv',
    'tweets/2024-12-27_04-46-20_tweets_1-176.csv',
    'tweets/2024-12-27_04-56-48_tweets_1-30.csv',
    'tweets/2024-12-27_04-57-17_tweets_1-7.csv',
    'tweets/2024-12-27_05-11-58_tweets_1-156.csv',
    'tweets/2024-12-27_05-27-28_tweets_1-178.csv',
    'tweets/2024-12-27_05-27-47_tweets_1-2.csv',
    'tweets/2024-12-27_13-36-13_tweets_1-3.csv',
    'tweets/2024-12-27_13-37-30_tweets_1-9.csv',
    'tweets/2024-12-27_13-37-45_tweets_1-1.csv',
    'tweets/2024-12-27_14-14-00_tweets_1-5.csv',
    'tweets/2024-12-27_14-20-24_tweets_1-163.csv',
    'tweets/2024-12-27_14-20-51_tweets_1-7.csv',
    'tweets/2024-12-27_14-21-27_tweets_1-8.csv',
    'tweets/2024-12-27_14-36-18_tweets_1-226.csv',
    'tweets/2024-12-27_14-50-53_tweets_1-191.csv',
    'tweets/2024-12-27_14-56-20_tweets_1-172.csv',
    'tweets/2024-12-27_14-56-36_tweets_1-2.csv',
    'tweets/2024-12-27_17-10-28_tweets_1-97.csv',
    'tweets/2024-12-27_17-49-43_tweets_1-7.csv',
    'tweets/2024-12-27_17-50-18_tweets_1-8.csv',
    'tweets/2024-12-27_18-04-57_tweets_1-228.csv',
    'tweets/2024-12-27_18-05-41_tweets_1-18.csv'
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
combined_df.to_csv('hinglish_tweets1.csv', index=False)
