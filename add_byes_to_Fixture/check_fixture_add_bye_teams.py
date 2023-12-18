# Import the csv module
import csv

# Open the csv file as comma delimited with 6 elements in each row
with open("fixture.csv", "r", encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file, delimiter="\t")
    data = list(reader)

with open("fixture_with_byes.csv", "w", newline='') as output_file:
    writer = csv.writer(output_file, delimiter='\t')
    # Loop through each row in the data
    for row in data:
        # Split the row into teams
        row_orig = row
        teams = set(map(int, ' '.join(row).replace('v', ' ').split()))
        # Find the bye teams
        bye_teams = set(range(1, 11)) - teams
        # Print the result
        bye_teams_tabbed = sorted(bye_teams)
        writer.writerow(row_orig + [str(team) for team in bye_teams_tabbed])
