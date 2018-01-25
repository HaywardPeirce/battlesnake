from plzEatFood import plzEatFood
from dontDie import dontDie
from plzEatFood import myClosestFoodCheck
from combineMoves import combineMoves


import bottle
import os
import random
import math
import json
import taunt

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    # Different Start Taunts
    tauntStart = ['GL HF!', 'No wards, gg', 'Mid or feed']

    head_url = '%s://%s/static/RS.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'secondary_color': '#65DB60',
        'color': '#003b45',
        'taunt': random.choice(tauntStart),
        'head_url': head_url,
        'head_type': 'fang',
        'tail_type': 'small-rattle',
        'name': 'Squatchy'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    #returns a list of moves that wont kill you
    isSafeMove = dontDie(data)

    #eatMoves = myClosestFoodCheck(data['food'], data)
    
    #move = combineMoves(isSafeMove, eatMoves)

    return {
        #'move': random.choice(directions),
        'move': random.choice(isSafeMove),
        'taunt': taunt.taunt("MAD")
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
