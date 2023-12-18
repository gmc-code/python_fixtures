# Import the csv module
import csv

# Open the csv file as comma delimited with 5 to 6 elements in each row
with open("fixture.csv", "r", encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file, delimiter="\t")
    data = list(reader)

# Create 11 output files in which an item has that number is removed from each row
# @just do it now for 11
for i in range(11, 12):
    # Create a new file name with the number i
    output_file_name = f"fixture_{i}.csv"
    # Open the output file for writing
    with open(output_file_name, "w", newline='') as output_file:
        writer = csv.writer(output_file, delimiter="\t")
        # Loop through each row in the data
        for row in data:
            # Create a new row with the item that has the number i removed
            new_row = [item for item in row if str(i) not in item]
            # Write the new row to the output file
            writer.writerow(new_row)
