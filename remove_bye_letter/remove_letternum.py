# Import the csv module
import csv

# Open the csv file as comma delimited with 6 elements in each row
with open("letter_fixture.csv", "r", encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file, delimiter=",")
    data = list(reader)

# Create a list of letters from A to K
letters = list("ABCDEFGHIJK")

# Create a dictionary to map letters to numbers
letter_to_number = {letter: i+1 for i, letter in enumerate(letters)}

# Create 11 output files in which an item has that number or a letter from A to K is removed from each row
for i in range(1, 12):
    # Create a new file name with the number i
    output_file_name = f"FixtureTemplate12_2b_{i}.csv"
    # Open the output file for writing with newline=''
    with open(output_file_name, "w", newline='') as output_file:
        writer = csv.writer(output_file, delimiter="\t")
        # Loop through each row in the data
        for row in data:
            # Create a new row with the item that has the number i or a letter from A to K removed
            new_row = [item for item in row if str(i) not in item and letters[i-1] not in item]
            # Write the new row to the output file
            writer.writerow(new_row)
    
    # Create another file name with the number i and _num suffix
    output_file_name_num = f"FixtureTemplate12_2b_{i}.txt"
    # Open the output file for writing with newline=''
    with open(output_file_name_num, "w", newline='') as output_file_num:
        writer_num = csv.writer(output_file_num, delimiter="\t")
        # Loop through each row in the data
        for row in data:
            # Create a new row with the item that has the number i or a letter from A to K removed
            new_row = [item for item in row if str(i) not in item and letters[i-1] not in item]
            # Convert the letters to numbers and insert " v " between them
            new_row = [" v ".join(str(letter_to_number[letter]) for letter in item) for item in new_row]
            # Write the new row to the output file
            writer_num.writerow(new_row)
