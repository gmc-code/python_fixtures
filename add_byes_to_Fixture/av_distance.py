# Import the statistics module
import statistics
import csv

# Open the csv file as tab delimited
with open("byes.csv", "r", encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file, delimiter="\t")
    # Iterate over the reader object to get your data
    list_of_lists = [[int(num) for num in row] for row in reader]

data = list_of_lists

from collections import defaultdict

# Create a dictionary to store the indices
indices = defaultdict(list)

# Populate the dictionary
for i, row in enumerate(data):
    for num in row:
        indices[num].append(i)

# Calculate the average difference for each number
avg_diffs = {}
for num, idxs in indices.items():
    diffs = [b - a for a, b in zip(idxs, idxs[1:])]
    avg_diffs[num] = round(sum(diffs) / len(diffs),1) if diffs else 0

# Sort the dictionary by its values
sorted_d = dict(sorted(avg_diffs.items(), key=lambda item: item[1]))
print(sorted_d)


# Open the output file in write mode
with open('bye_distances.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file,  delimiter='\t')
    # Write the header
    writer.writerow(['Number', 'Average Difference'])
    # Write the data
    for key, value in sorted_d.items():
        writer.writerow([key, value])

# Calculate the average of the values
average = statistics.mean(sorted_d.values())

print(average)
