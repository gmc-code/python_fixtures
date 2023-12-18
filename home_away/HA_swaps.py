import pandas as pd
import csv


def analyze_fixture(data_file):
    df = pd.read_csv(data_file, header=None)

    # Create a list to hold the processed data
    processed_data = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Split the row into matches
        matches = row[0].split("\t")
        # Iterate over each match
        for match in matches:
            # Split the match into teams
            teams = match.split(" v ")
            # Check if there are two teams in the match
            if len(teams) == 2:
                # Add the match to the processed data
                processed_data.append(
                    {"round": index + 1, "team_H": teams[0], "team_A": teams[1]}
                )

    # Convert the processed data to a DataFrame
    processed_df = pd.DataFrame(processed_data)
    print(processed_df)
    return processed_df


def suggest_swaps(df, team_H):
    team_games = df[df["team_H"] == team_H].reset_index(drop=True)
    print(team_H, team_games)
    swap_suggestions = []
    # Iterate over the team's games
    for i in range(1, len(team_games) - 1):
        # Check if the current game and the next two games are home games
        if (
            team_games.iloc[i - 1]["team_H"] == team_H
            and team_games.iloc[i]["team_H"] == team_H
            and team_games.iloc[i + 1]["team_H"] == team_H
        ):
            # Find the next game
            if i + 2 < len(team_games):
                # Suggest swapping the middle game of the three with the next game
                swap_suggestions.append(
                    {
                        "round1": team_games.iloc[i].name,
                        "round2": team_games.iloc[i + 2].name,
                    }
                )
    print("suggest", swap_suggestions)
    return swap_suggestions


def update_fixture(df, swap_info):
    round1_index = swap_info["round1"]
    round2_index = swap_info["round2"]
    df.loc[round1_index, ["team_H", "team_A"]] = df.loc[round2_index][["team_H", "team_A"]]
    df.loc[round2_index, ["team_H", "team_A"]] = df.loc[round1_index][["team_H", "team_A"]]
    return df



# Read and analyze the fixture data
df = analyze_fixture("fixture.csv")

# Loop through each team
for team_H in df["team_H"].unique():
    # Suggest swaps for the team
    swaps = suggest_swaps(df, team_H)
    print(swaps)
    # If there are suggested swaps
    if swaps:
        # Choose a swap (this could be improved with some logic)
        swap = swaps[0]
        # Update the fixture with the chosen swap
        df = update_fixture(df, swap)

# Group by round and aggregate teams to match original format
grouped_df = df.groupby("round").apply(
    lambda x: "\t".join(x["team_H"] + " v " + x["team_A"])
)

# Convert the grouped DataFrame to a list
grouped_list = grouped_df.tolist()

# Save the updated fixture to a CSV file
with open("updated_fixture.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for line in grouped_list:
        writer.writerow([line])
