import os
import requests
import json
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

def sort_data(parsed_json):
    name_list = []
    #cleaning up unwanted keys
    del parsed_json["get"]
    del parsed_json["parameters"]
    del parsed_json["errors"]
    del parsed_json["results"]
    del parsed_json["paging"]




    