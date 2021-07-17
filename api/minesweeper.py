from flask import Blueprint, jsonify, request
import mongoengine
from api.mongo import Players

bp = Blueprint('ms', __name__, url_prefix='/ms')

MAX_PLAYERS = 10

def format_players(players):
    formated = []

    for player in players:
        formated.append({
            'name': player.name,
            'level': player.level,
            'score': player.score,
            'date': format_date(player.date)
        })
    return formated

def format_date(date):
    return f'{date.day}-{date.month}-{date.year}'

def makes_the_top(top_players, player):
    made_it = False
    for i, top_player in enumerate(top_players):
        if int(player['score']) <= top_player['score']:
            made_it = True
            top_players.insert(i, player)
            break

    if len(top_players) < MAX_PLAYERS and made_it == False:
        top_players.append(player)
        made_it = True
    elif len(top_players) >= MAX_PLAYERS and made_it == True:
        top_players.pop()

    return (top_players, made_it)


@bp.route('/<level>', methods=['GET'])
def get_top_players(level):
    top_players = Players.objects(level=level)[:MAX_PLAYERS]
    top_players = format_players(top_players)
    return jsonify(top_players), 200

@bp.route('/<level>', methods=['POST'])
def post_top_players(level):
    top_players = Players.objects(level=level)[:MAX_PLAYERS]
    top_players = format_players(top_players)
    data = request.json

    top_players, made_the_top = makes_the_top(top_players, data)

    if made_the_top:
        player = Players(**data)
        player.save()

    return jsonify(top_players), 200

@bp.errorhandler(mongoengine.InvalidQueryError)
def handle_db_error(e):
    print(e)
    return 'Database error!', 404

@bp.errorhandler(mongoengine.InvalidDocumentError)
def handle_db_error(e):
    print(e)
    return 'Database error!', 404