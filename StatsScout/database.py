from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import re


def update_league(league_data):

    load_dotenv()
    url = os.getenv("DB_URL")
    client = MongoClient(url, server_api=ServerApi('1'))

    db = client["players_database"]
    players = db["players"]

    for player in league_data:
        
        filter = {"name": player["name"]} #filters the player name
        existing_entry = players.find_one(filter) 

        #check if player already exists in database, if so update stats
        if existing_entry is not None:
            print("Player Already Exists: ", player["name"], ". Updating...")
            updated_entry = players.replace_one(filter,player)

        #add new player if they do not already exist
        else:
            print("Adding Player: ",player["name"])
            new_entry = players.insert_one(player)


def player_stats(player_name):

    load_dotenv()
    url = os.getenv("DB_URL")
    client = MongoClient(url, server_api=ServerApi('1'))

    db = client["players_database"]
    players = db["players"]
    
    player_info = players.find_one({'name': {"$regex": re.compile(player_name, re.IGNORECASE)}})
    return player_info



