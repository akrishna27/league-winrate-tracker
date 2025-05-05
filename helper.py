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
REGION = "na1"  # Change this to the appropriate region if needed

def get_puuid(summoner_name):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("puuid")


def get_match_ids(puuid, count=20):
    """Retrieve a list of match IDs for a given PUUID."""
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    res = requests.get(url, headers=HEADERS)
    return res.json()

def get_match_data(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to get match data for {match_id}: {res.status_code} - {res.text}")
        return None

