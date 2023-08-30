from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import unicodedata
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
    
    # Split the player name into individual words
    name_parts = player_name.split()

    # Create a list of regex patterns for each part of the name
    name_patterns = [re.escape(part) for part in name_parts]

    # Combine the patterns into a single regex with optional spaces and any characters
    combined_pattern = r"\s*.*".join(name_patterns)

    # Use the combined pattern to search for the name in the database
    player_info = players.find_one({'complete_name': {"$regex": re.compile(combined_pattern, re.IGNORECASE)}})

    return player_info

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def optimize_name():
    load_dotenv()

    url = os.getenv("DB_URL")
    client = MongoClient(url, server_api=ServerApi('1'))

    db = client["players_database"]
    players = db["players"]

    for documents in players.find():
        filtere = {'name': documents['name']}
        complete_name = (documents['firstname'] + " " + documents['lastname'])
        complete_name = strip_accents(complete_name)
        update = {'$set': {'complete_name': complete_name}}

        if documents['complete_name'] == complete_name:
            print(documents['complete_name'] + ' already up to date.')
        else:
            players.update_one(filtere, update)
            print(documents['complete_name'] + ' updated.')
    
    print('Done')










