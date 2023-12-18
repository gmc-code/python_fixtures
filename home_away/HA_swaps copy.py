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
                    {"round": index + 1, "team_id": teams[0], "home_team": teams[1]}
                )

    # Convert the processed data to a DataFrame
    processed_df = pd.DataFrame(processed_data)

    return processed_df


def suggest_swaps(df, team_id):
    team_games = df[df["team_id"] == team_id]
    swap_suggestions = []

    for i in range(1, len(team_games), 2):
        if team_games.iloc[i - 1]["home_team"] == team_games.iloc[i]["home_team"]:
            swap_suggestions.append(
                {
                    "round1": team_games.iloc[i - 1].name,
                    "round2": team_games.iloc[i].name,
                }
            )

    return swap_suggestions


def update_fixture(df, swap_info):
    temp_df = df.copy()
    (
        temp_df.loc[swap_info["round1"], "team_H"],
        temp_df.loc[swap_info["round2"], "team_H"],
    ) = (
        df.loc[swap_info["round2"], "team_H"],
        df.loc[swap_info["round1"], "team_H"],
    )
    (
        temp_df.loc[swap_info["round1"], "team_A"],
        temp_df.loc[swap_info["round2"], "team_A"],
    ) = (
        df.loc[swap_info["round2"], "team_A"],
        df.loc[swap_info["round1"], "team_A"],
    )

    return temp_df



# Read and analyze the fixture data
df = analyze_fixture("fixture.csv")

# Group by round and aggregate teams to match original format
grouped_df = df.groupby("round").apply(
    lambda x: "\t".join(x["team_id"] + " v " + x["home_team"])
)

# Convert the grouped DataFrame to a list
grouped_list = grouped_df.tolist()

# Save the updated fixture to a CSV file
with open("updated_fixture.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for line in grouped_list:
        writer.writerow([line])
