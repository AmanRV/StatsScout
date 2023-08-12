import os
import requests
import json
from dotenv import load_dotenv

def get_stats(league, season,page):
    load_dotenv()

    url = "https://v3.football.api-sports.io/players"
    querystring = {"league":league, "season":season, "page":page}

    headers = {
	    "X-RapidAPI-Key": os.getenv('api_key'),
	    "X-RapidAPI-Host": "v3.football.api-sports.io"
    }

    #Getting the raw stats from api-football
    api_response = requests.get(url, headers=headers, params=querystring)
    stats_json = api_response.text
    parsed_json = json.loads(stats_json)

    print(parsed_json['response'][0]['player']['name'])

get_stats("39","2020","1")

    