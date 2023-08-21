from flask import Blueprint, render_template, request, redirect, url_for
from .database import player_stats
from .gpt_description import generate_bio

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
        player_name = stats["name"]
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
        #end


        return render_template('summary.html', photo=photo, player_name=player_name,club=club,league=league,position=position,rating=rating, birthdate=birthdate, age=age,height=height,weight=weight, nationality=nationality, desc=desc)
    
    except:
        return render_template("home.html")