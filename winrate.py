from dotenv import load_dotenv
import os
from helper import get_puuid, get_match_ids, get_match_data  # assuming these are defined
from collections import defaultdict
import time

# Load the Riot API key from the .env file
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": API_KEY}

# Replace this with your actual summoner list
summoner_riot_ids = [
    {"game_name": "AshyBoyy", "tag_line": "NA1"},
    {"game_name": "Gunyong", "tag_line": "0063"},
    {"game_name": "ChubbyPug", "tag_line": "NA1"}
]

# Step 1: Get PUUIDs
name_to_puuid = {
    f"{summoner['game_name']}#{summoner['tag_line']}": get_puuid(summoner['game_name'], summoner['tag_line'])
    for summoner in summoner_riot_ids
}
puuid_to_name = {v: k for k, v in name_to_puuid.items() if v is not None}

# Step 2: Track shared games and wins
winrate_data = defaultdict(lambda: defaultdict(lambda: {"games": 0, "wins": 0}))

# Step 3: Analyze matches
processed_matches = set()  # Cache to store processed match IDs

for name, puuid in name_to_puuid.items():
    print(f"Processing matches for {name}...")
    match_ids = get_match_ids(puuid, count=50)

    for match_id in match_ids:
        if match_id in processed_matches:
            continue  # Skip if the match has already been processed

        match = get_match_data(match_id)
        time.sleep(1.2)  # To avoid rate limits

        if not match:
            continue  # Skip if match data is invalid

        processed_matches.add(match_id)  # Mark this match as processed

        participants = match['metadata']['participants']
        info = match['info']

        # Find shared players in this match
        shared_players = [p for p in participants if p in puuid_to_name]

        if len(shared_players) < 2:
            continue  # Skip if fewer than 2 shared players are in the match

        puuid_to_team = {}
        puuid_to_win = {}

        # Process all relevant Riot IDs in this match
        for participant in info['participants']:
            if participant['puuid'] in shared_players:
                puuid_to_team[participant['puuid']] = participant['teamId']
                puuid_to_win[participant['puuid']] = participant['win']

        # Update winrate data for all pairs of shared players
        for i in range(len(shared_players)):
            for j in range(i + 1, len(shared_players)):
                p1, p2 = shared_players[i], shared_players[j]
                if puuid_to_team[p1] == puuid_to_team[p2]:  # Same team
                    name1, name2 = puuid_to_name[p1], puuid_to_name[p2]
                    same_team_win = puuid_to_win[p1] and puuid_to_win[p2]

                    winrate_data[name1][name2]['games'] += 1
                    winrate_data[name2][name1]['games'] += 1
                    if same_team_win:
                        winrate_data[name1][name2]['wins'] += 1
                        winrate_data[name2][name1]['wins'] += 1

# Step 4: Print result
print("\nWinrate Matrix:")
riot_ids = list(name_to_puuid.keys())  # Convert keys to a list for indexed iteration
processed_pairs = set()  # Track pairs that have already been printed

# Loop through all combinations of Riot IDs
for name1 in riot_ids:
    for name2 in riot_ids:
        if name1 == name2:  # Skip self-combinations
            continue

        # Ensure the pair is only processed once if winrates are identical
        pair = tuple(sorted([name1, name2]))  # Sort the pair to avoid duplicates
        if pair in processed_pairs:
            continue

        # Get winrate data for both perspectives
        data1 = winrate_data[name1][name2]
        data2 = winrate_data[name2][name1]

        # Check if winrate data is identical
        if data1 == data2:
            if data1['games'] > 0:
                winrate = 100 * data1['wins'] / data1['games']
                print(f"{name1} + {name2}: {data1['wins']}W / {data1['games']}G ({winrate:.1f}%)")
            processed_pairs.add(pair)  # Mark the pair as processed
        else:
            # Print both perspectives if winrate data differs
            if data1['games'] > 0:
                winrate1 = 100 * data1['wins'] / data1['games']
                print(f"{name1} + {name2}: {data1['wins']}W / {data1['games']}G ({winrate1:.1f}%)")
            if data2['games'] > 0:
                winrate2 = 100 * data2['wins'] / data2['games']
                print(f"{name2} + {name1}: {data2['wins']}W / {data2['games']}G ({winrate2:.1f}%)")
            processed_pairs.add(pair)  # Mark the pair as processed
