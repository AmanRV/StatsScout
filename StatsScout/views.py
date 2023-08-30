from flask import Blueprint, render_template, request, redirect, url_for
from .database import player_stats
from .gpt_description import generate_bio
import traceback

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        return redirect('/summary?player_name='+player_name)
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/summary', methods=['GET', 'POST'])
def summary():
    try:
        player_name = request.args.get('player_name')
        stats = player_stats(player_name)

        desc = generate_bio(str(stats))



        #setting player stats
        photo = stats["photo"]
        club = stats["team"]['logo']
        club_name = stats["team"]['name']
        player_name = stats["complete_name"]
        age = stats["age"]
        birthdate = stats["birth"]['date']
        nationality = stats["nationality"]
        height = stats["height"]
        weight = stats["weight"]
        league = stats["league"]['name']
        league_pic = stats["league"]['logo']
        season = stats["league"]['season']
        position = stats['games']['position']
        rating = round(float(stats['games']['rating']),2)
        rating = str(rating)

        # Games stats
        appearences = stats['games']['appearences']
        minutes = stats['games']['minutes']

        # Shots stats
        shotstotal = stats['shots']['total']
        shotsot = stats['shots']['on']

        # Goals stats
        goalstotal = stats['goals']['total']
        goalsconceded = stats['goals']['conceded']
        assists = stats['goals']['assists']
        saves = stats['goals']['saves']

        # Passes stats
        passes_total = stats['passes']['total']
        passes_key = stats['passes']['key']
        passes_accuracy = stats['passes']['accuracy']

        # Tackles stats
        tackles_total = stats['tackles']['total']
        tackles_blocks = stats['tackles']['blocks']
        tackles_interceptions = stats['tackles']['interceptions']

        # Duels stats
        duels_total = stats['duels']['total']
        duels_won = stats['duels']['won']

        # Dribbles stats
        dribbles_attempts = stats['dribbles']['attempts']
        dribbles_success = stats['dribbles']['success']
        dribbles_past = stats['dribbles']['past']

        # Fouls stats
        fouls_drawn = stats['fouls']['drawn']
        fouls_committed = stats['fouls']['committed']

        # Cards stats
        cards_yellow = stats['cards']['yellow']
        cards_yellowred = stats['cards']['yellowred']
        cards_red = stats['cards']['red']

        # Penalty stats
        penalty_won = stats['penalty']['won']
        penalty_committed = stats['penalty']['commited']
        penalty_scored = stats['penalty']['scored']
        penalty_missed = stats['penalty']['missed']
        penalty_saved = stats['penalty']['saved']
        #end

        #shooting calculations
        if goalstotal != None and shotsot != None:
            goalspercent = ((goalstotal/18)*100)*0.6
            shotpercent = ((shotsot/shotstotal)*100)*0.4
            shots_rating = goalspercent+shotpercent
        else:
            shots_rating = 0

        

        if shots_rating > 100:
            shots_rating = 100

        if assists != None:
            assistpercent = ((assists/10)*100)*0.6
            passpercent = (passes_accuracy)*0.60

            pass_rating = assistpercent+passpercent
        else:
            pass_rating = passes_accuracy

        if pass_rating > 100:
            pass_rating = 100

        if dribbles_success != None:
            dribble_rating = (dribbles_success/dribbles_attempts)*100
            dribble_rating = dribble_rating**1.1
        else:
            dribble_rating=0

        if dribble_rating > 100:
            dribble_rating = 100

        if duels_won != None and duels_total != None:
            defending_rating = ((duels_won/duels_total)*100)
        else:
            defending_rating = 0

        if defending_rating > 100:
            defending_rating = 100

        if position == 'Goalkeeper':
            goalkeeping_rating = -((goalsconceded*0.14 - 3)**2)+100
            defending_rating = defending_rating/2
            dribble_rating = dribble_rating/2
        else:
            goalkeeping_rating = 0

        if goalsconceded < 30 and position == 'Goalkeeper':
            goalkeeping_rating = 100
        
        
        
        
        
        if goalstotal != None:
            goal_ratio = round(((float(goalstotal)/float(minutes))*90),2)
            goal_ratio = str(goal_ratio)
        else:
            goal_ratio=0

        if assists != None:
            assist_ratio = round(((float(assists)/float(minutes))*90),2)
            assist_ratio = str(assist_ratio)
        else:
            assist_ratio=0



        

        #Sending stats to webpage to be displayed
        return render_template('summary.html',
                       photo=photo,
                       player_name=player_name,
                       league=league,
                       club=club,
                       club_name=club_name,
                       position=position,
                       rating=rating,
                       birthdate=birthdate,
                       goalkeeping_rating=goalkeeping_rating,
                       age=age,
                       dribble_rating=dribble_rating,
                       defending_rating=defending_rating,
                       height=height,
                       weight=weight,
                       nationality=nationality,
                       desc=desc,
                       appearences=appearences,
                       minutes=minutes,
                       shotstotal=shotstotal,
                       shotsot=shotsot,
                       goalstotal=goalstotal,
                       goalsconceded=goalsconceded,
                       pass_rating=pass_rating,
                       assists=assists,
                       saves=saves,
                       passes_total=passes_total,
                       passes_key=passes_key,
                       passes_accuracy=passes_accuracy,
                       tackles_total=tackles_total,
                       tackles_blocks=tackles_blocks,
                       tackles_interceptions=tackles_interceptions,
                       duels_total=duels_total,
                       duels_won=duels_won,
                       dribbles_attempts=dribbles_attempts,
                       dribbles_success=dribbles_success,
                       dribbles_past=dribbles_past,
                       fouls_drawn=fouls_drawn,
                       fouls_committed=fouls_committed,
                       cards_yellow=cards_yellow,
                       cards_yellowred=cards_yellowred,
                       cards_red=cards_red,
                       penalty_won=penalty_won,
                       penalty_committed=penalty_committed,
                       penalty_scored=penalty_scored,
                       penalty_missed=penalty_missed,
                       penalty_saved=penalty_saved,
                       goal_ratio=goal_ratio,
                       assist_ratio=assist_ratio,
                       shots_rating=shots_rating)

    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return render_template("home.html")