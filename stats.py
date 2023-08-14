import os
import requests
import json
import time
from dotenv import load_dotenv

def get_stats(league, season,page):
    load_dotenv()

    url = "https://v3.football.api-sports.io/players"

    #the parameters: football league, the season (year), and the page
    querystring = {"league":league, "season":season, "page":page}

    headers = {
	    "X-RapidAPI-Key": os.getenv('API_KEY'),
	    "X-RapidAPI-Host": "v3.football.api-sports.io"
    }

    #Getting the raw stats from api-football
    api_response = requests.get(url, headers=headers, params=querystring)
    stats_json = api_response.text
    parsed_json = json.loads(stats_json)

    return parsed_json

def max_page(league,season,page):
    #finds how many pages of players there are
    data = get_stats(league, season, page)
    total_pages = data["paging"]["total"]
    return total_pages

def clean_data(parsed_json):
    cleaned_data = []

    #cleaning up unwanted keys
    del parsed_json["get"]
    del parsed_json["parameters"]
    del parsed_json["errors"]
    del parsed_json["results"]
    del parsed_json["paging"]

    #combines "player" and "statistics" key and adds it to cleaned data list
    for i in parsed_json["response"]:
        player = {}
        player.update(i["player"])
        player.update(i["statistics"][0])
        cleaned_data.append(player)
    
    #returns a list of player data dictionaries
    return cleaned_data


def get_league(league, season):
    league_data = []
    final_page = max_page(league, season, "1")
    rate_limit = [8,16,24,32,40,48]

    for i in range(final_page):

        #get, parse, and clean league data
        page = i+1
        parsed_data = get_stats(league, season, page)
        cleaned_data = clean_data(parsed_data)

        #append each individual player as a list item in league_data
        for j in cleaned_data:
            league_data.append(j)

        #due to api request limit, wait 1 minute every 8 requests
        if i in rate_limit:
            time.sleep(65)
    
    return league_data #returns full list of every player from that league







    