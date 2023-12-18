import pandas as pd
import numpy as np
import csv

# Open the csv file as tab delimited
with open("byes.csv", "r", encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file, delimiter="\t")
    # Iterate over the reader object to get your data
    list_of_lists = [[int(num) for num in row] for row in reader]

df = pd.DataFrame(list_of_lists)

# Add an index column to the DataFrame
df['index'] = df.index

def check_distance(df, min_distance):
    # Create a dictionary to store the last occurrence of each number
    last_occurrence = {}
    # Iterate over the rows in the DataFrame
    for i, row in df.iterrows():
        # Iterate over the numbers in the row
        for num in row.drop('index'):
            # If the number has occurred before and the distance is less than the minimum distance, return False
            if num in last_occurrence and i - last_occurrence[num] < min_distance:
                return False
            # Update the last occurrence of the number
            last_occurrence[num] = i
    # If no numbers are within the minimum distance of each other, return True
    return True

counter = 0
row_to_keep = 0
row_to_keep_next = row_to_keep + 1
# Shuffle the rows until they satisfy the condition or the counter reaches 10000
while not check_distance(df, 3) and counter < 10000:
    df_except_row5 = df.drop(row_to_keep).sample(frac=1).reset_index(drop=True)
    df = pd.concat([df_except_row5.iloc[:row_to_keep], df.iloc[row_to_keep:row_to_keep_next], df_except_row5.iloc[row_to_keep:]], ignore_index=True)
    counter += 1

# Print the DataFrame with the original index numbers in their new order
print(df.sort_values(by='index').to_string(header=False))
