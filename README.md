
# StatScout

Evaluate players like you've never seen before: StatScout provides comprehensive player insights spanning Europe's top 5 football leagues. Input a player's name to receive an all-encompassing ChatGPT summary, accompanied by a visual overview that presents their performance statistics in full detail!

Here is the link to try the site: https://statscout.amanrajesh.me/

![StatScout Screenshot](https://i.imgur.com/g3tDb55.png)
## Supported Leagues and Players
Updated to 2020/21 League Season:
* Premier League (England)
* La Liga (Spain)
* Serie A (Italy)

Bundesliga and Ligue 1 in progress.


## How does it work?

**Data Retrieval and Cleaning**

The application uses the requests library to make API calls to API-Football. The get_stats function retrieves player statistics based on the provided league, season, and page parameters. The max_page function calculates the total number of pages of player data available for the specified league and season. The clean_data function processes the raw API response, combines player and statistics data, and returns a list of cleaned player data dictionaries.

**Data Storage and Database Updates**

The application utilizes MongoDB as its database to store player statistics. The update_league function updates player statistics in the database. It iterates through the cleaned player data list, checks if a player already exists in the database, and updates the data if necessary. If the player doesn't exist, a new entry is added to the database. The optimize_name function optimizes player names for better database search by removing accents and updating the complete_name field to aid the fuzzy search functionality.

**Text Generation**

The application employs the OpenAI GPT-3 API to generate short player summaries. The generate_bio function takes player statistics as input and constructs a prompt for GPT-3. The model then generates a short summary that includes the player's strengths and weaknesses.

**Web Interface using Flask**

The web interface is built using the Flask framework. The views blueprint defines routes for different pages. The / route is the homepage where users can enter a player's name to search for. Upon submission, the user is redirected to the /summary page. The /about route displays an about page.

**Player Summary Page**

The /summary route retrieves player statistics from the database using the player_stats function. It then generates a player summary by calculating ratings for various aspects of the player's performance, such as dribbling, defending, and shooting. The summary also includes detailed statistics such as appearances, goals, assists, and more. Additionally, the player's photo, club logo, and league logo are displayed. The GPT-3 generated player summary is also included. The Chart.js framework is used to create radar and bar graphs detailing the player's statistics in a visual format.

## Future Plans
* Update data to 2022/23 season
* Add Bundesliga and Ligue 1
* Improve search bar to show live drop-down while searching for a player
* Find another API with more comprehensive statistics and data
