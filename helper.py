import requests

API_KEY = "RIOT_API_KEY"
HEADERS = {"X-Riot-Token": API_KEY}
REGION = "na1"  # Change to your region

def get_puuid(summoner_name, headers):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    res = requests.get(url, headers=headers)
    return res.json().get("puuid")

def get_match_ids(puuid, count=20):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    res = requests.get(url, headers=HEADERS)
    return res.json()

def get_match_data(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json()

