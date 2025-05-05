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
for name, puuid in name_to_puuid.items():
    print(f"Processing matches for {name}...")
    match_ids = get_match_ids(puuid, count=50)

    for match_id in match_ids:
        match = get_match_data(match_id)
        time.sleep(1.2)  # To avoid rate limits

        participants = match['metadata']['participants']
        info = match['info']

        shared_players = [p for p in participants if p in puuid_to_name]

        if len(shared_players) < 2:
            continue

        puuid_to_team = {}
        puuid_to_win = {}

        for participant in info['participants']:
            if participant['puuid'] in shared_players:
                puuid_to_team[participant['puuid']] = participant['teamId']
                puuid_to_win[participant['puuid']] = participant['win']

        for i in range(len(shared_players)):
            for j in range(i + 1, len(shared_players)):
                p1, p2 = shared_players[i], shared_players[j]
                if puuid_to_team[p1] == puuid_to_team[p2]:
                    name1, name2 = puuid_to_name[p1], puuid_to_name[p2]
                    same_team_win = puuid_to_win[p1] and puuid_to_win[p2]

                    winrate_data[name1][name2]['games'] += 1
                    winrate_data[name2][name1]['games'] += 1
                    if same_team_win:
                        winrate_data[name1][name2]['wins'] += 1
                        winrate_data[name2][name1]['wins'] += 1

# Step 4: Print result
print("\nWinrate Matrix:")
for name1 in name_to_puuid.keys():
    for name2 in name_to_puuid.keys():
        if name1 == name2:
            continue
        data = winrate_data[name1][name2]
        if data['games'] > 0:
            winrate = 100 * data['wins'] / data['games']
            print(f"{name1} + {name2}: {data['wins']}W / {data['games']}G ({winrate:.1f}%)")
