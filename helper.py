import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch the API_KEY from the .env file
API_KEY = os.getenv("RIOT_API_KEY")

# Set the headers with the Riot API Key
HEADERS = {"X-Riot-Token": API_KEY}

# Region (can be adjusted based on where you play)
REGION = "americas"  # Change this to the appropriate region if needed

def get_puuid(game_name, tag_line):
    """
    Retrieve the PUUID for a given Riot ID (gameName and tagLine).
    """
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("puuid")
    else:
        print(f"Failed to get PUUID for {game_name}#{tag_line}: {res.status_code} - {res.text}")
        return None

def get_match_ids(puuid, count=20):
    """Retrieve a list of match IDs for a given PUUID."""
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to get match IDs for PUUID {puuid}: {res.status_code} - {res.text}")
        return None

def get_match_data(match_id):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to get match data for {match_id}: {res.status_code} - {res.text}")
        return None

