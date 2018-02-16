import bottle
import os
import random
from turn import turn
from battlesnakeClasses import *

#TODO: declare information you want to reference across turns here?




#initialize our snake
#squatchy = Snake("","squatchy")
#squatchy['isUs'] = True
squatchy = None

#initialize the list of opponent snakes
enemies = []
#TODO: loop through returned list of compenitors and add a new snake entry for them.


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    print("hello world")
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: initialize squatchy info from info being returned

    return {
        'name': 'SaaSquatch',
        'color': '#003b45',
        'secondary_color': '#65DB60',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'head_type': 'fang',
        'tail_type': 'small-rattle',
    }


@bottle.post('/move')
def move():
    data = bottle.request.json


    #print(data)

    #return the direction to move.
    move = turn(data, squatchy, enemies)

    #directions = ['up', 'down', 'left', 'right']

    return {
        #'move': random.choice(directions),
        'move': move,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
    #bottle.run(application, host='localhost', port=os.getenv('PORT', '8080'))
