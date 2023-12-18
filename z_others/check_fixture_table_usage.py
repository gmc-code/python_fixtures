import csv
from collections import defaultdict

# Initialize dictionaries to store the matches and table counts
matches = defaultdict(int)
table_counts = defaultdict(lambda: defaultdict(int))

# Open the CSV file
with open('fixture.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    headers = next(reader)  # Get the header row

    # Read each row in the CSV file
    for row in reader:
        # For each table in the row
        for i, table in enumerate(row[1:], start=1):
            # Skip if the table is empty
            if not table:
                continue

            # Split the teams
            team1, team2 = map(int, table.split(' v '))

            # Increment the count of matches for the pair of teams
            matches[frozenset([team1, team2])] += 1

            # Increment the count of matches for each team on the table
            table_counts[team1][headers[i]] += 1
            table_counts[team2][headers[i]] += 1

# Check if each team plays each other team twice
for teams, count in matches.items():
    if count != 2:
        print(f'Teams {teams} do not play each other twice, they play {count} times.')

# Output the table counts for each team
for team, counts in table_counts.items():
    print(f'Team {team} played on:')
    for table, count in counts.items():
        print(f'  {table}: {count} matches')
