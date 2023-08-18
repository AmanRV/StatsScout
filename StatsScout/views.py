from flask import Blueprint, render_template, request, redirect, url_for
from .database import player_stats

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
        photo = player_stats(player_name)["photo"]
        print(player_stats(player_name) is None)
        return render_template('summary.html', photo=photo)
    
    except:
        return render_template("home.html")