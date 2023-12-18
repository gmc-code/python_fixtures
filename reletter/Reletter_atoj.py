import csv

def replace_letters(fixture, old_letters, new_letters):
    # Create a translation table
    trans = str.maketrans(old_letters, new_letters)
    
    # Use the translation table to replace the letters
    return fixture.translate(trans)

# Original letters from A to J
old_letters = 'ABCDEFGHIJ'

# Specific order of new letters from A to J
specific_order = 'CDFEGHJIAB'

# Read the letters from a CSV file
with open('letter_fixture.csv', 'r') as file:
    reader = csv.reader(file)
    fixtures = list(reader)

# Replace the letters and write to a new CSV file
with open('new_letter_fixture.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for fixture in fixtures:
        fixture = replace_letters(fixture[0], old_letters, specific_order)
        writer.writerow([fixture])
