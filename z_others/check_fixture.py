import csv
from collections import defaultdict

# Initialize a dictionary to store the matches
matches = defaultdict(int)

# Open the CSV file
with open('fixture.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the header row

    # Read each row in the CSV file
    for row in reader:
        # For each table in the row
        for table in row[:]:
            # Skip if the table is empty
            if not table:
                continue

            # Split the teams
            team1, team2 = map(int, table.split(' v '))

            # Increment the count of matches for the pair of teams
            matches[frozenset([team1, team2])] += 1

# Check if each team plays each other team twice
for teams, count in matches.items():
    if count != 2:
        print(f'Teams {teams} do not play each other twice, they play {count} times.')
    else:
        print(f'Teams {teams} play each other {count} times.')
