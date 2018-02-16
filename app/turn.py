from battlesnakeClasses import *

#import each of the component files running sections of the snake

#check if squatchy will hit himself
def squatchyHitCheck(squatchy):
    #get current squatchy head location
    print("Checking whether squatchy will hit himself")
    print("squatchy head: [{}]".format(squatchy.head()))

    tempDirection = squatchy.conllisionCheck(squatchy.head())

    #print(tempDirection)

    tempDirection.printMoves()

    return tempDirection

    #get list of squatchy non-head locations
    #bodyLocations =


#check if squatchy will run into a wall
def wallHitCheck(squatchy, height, width):

    print("Checking whether squatchy will hit the wall")
    print("squatchy head: [{}]".format(squatchy.head()))

    #how wide is the board?

    freespaceScore = 1

    tempDirection = MoveChoices()

    #if squatchy isnt right up againts to left side of the board
    if squatchy.head()[0] > 0:
        tempDirection.left = freespaceScore

    #if squatchy isn't right up againt the right side (assuming board locations are indexed starting at 0)
    if squatchy.head()[0] < (width - 1):
        tempDirection.right = freespaceScore

    if squatchy.head()[1] > 0:
        tempDirection.up = freespaceScore

    if squatchy.head()[1] < (height - 1):
        tempDirection.down = freespaceScore

    return tempDirection


def enemyHitCheck(squatchy, enemies):
    print("Check whether squatchy will hit any other snakes")
    #loop through each enemy, `conllisionCheck` for our snake head
    print("squatchy head: [{}]".format(squatchy.head()))

    enemyDirections = MoveChoices()

    #loop through each enemy snake
    for enemy in enemies:
        print("Checking whether squatchy will hit '{}'".format(enemy.name))
        tempDirection = enemy.conllisionCheck(squatchy.head())

        tempDirection.printMoves()

        if tempDirection.up > enemyDirections.up:
            enemyDirections.up = tempDirection.up
        if tempDirection.down > enemyDirections.down:
            enemyDirections.down = tempDirection.down
        if tempDirection.right > enemyDirections.right:
            enemyDirections.right = tempDirection.right
        if tempDirection.left > enemyDirections.left:
            enemyDirections.left = tempDirection.left

        enemyDirections.printMoves()


    return enemyDirections


#return a string of which way squatchy should move
def turn(turnData, squatchy, enemies):

    #TODO: setup snakes based on the their initial positions

    #print('hello world')
    print(turnData)

    # myLocation = []
    # for point in turnData['you']['body']['data']:
    #     myLocation.append(tuple((point['x'],point['y'])))
    #
    # squatchy.locations = myLocation
    # squatchy.health = turnData['you']['health']
    # squatchy.length = turnData['you']['length']



    #TODO: update positions, length, and health of each of the opponent snakes. Maybe check if it's turn 1 to initilize (name, ID...) the snakes, otherwise just update the values

    #first turn, setup opponent snakes
    if turnData['turn'] == 0:
        #TODO: setup initialization info about each snake

        for snake in turnData['snakes']['data']:
            print(snake['name'])
            tempSnake = Snake(snake['id'], snake['name'])

            tempLocations = []
            for location in snake['body']['data']:
                tempLocations.append(tuple((location['x'],location['y'])))

            tempSnake.locations = tempLocations

            if snake['id'] == turnData['you']['id']:
                squatchy = tempSnake
                squatchy.isUs = True

            else:
                enemies.append(tempSnake)



    #non-first turn snake updates: positions, length, and health
    else:
        #TODO: second turn+ snake info updates

        for snake in turnData['snakes']['data']:

            for enemy in enemies:
                #print(enemy.id)
                #print(enemy.name)

                if enemy.id == snake['id']:
                    print(snake['id'])
                    print(snake['name'])

                    print(enemy.locations)

                    tempLocations = []
                    for location in snake['body']['data']:
                        tempLocations.append(tuple((location['x'],location['y'])))

                    enemy.locations = tempLocations

                    enemy.length = snake['length']

                    enemy.health = snake['health']




    #initialize the security score for the turn as being zero

    securityScore = MoveChoices()

    #strategyScore = MoveChoices()

    #securityScore checks, to make sure this next turn's move is safe
    #TODO: check to see we wont hit ourself

    securityScore.addMoves(squatchyHitCheck(squatchy))
    securityScore.printMoves()

    #TODO: check to see we won't hit a wall
    securityScore.addMoves(wallHitCheck(squatchy, turnData['height'], turnData['width']))
    securityScore.printMoves()

    #TODO: check to see we won't hit another snake
    securityScore.addMoves(enemyHitCheck(squatchy, enemies))
    securityScore.printMoves()

    #TODO: check to see if we an eat next turn


    #TODO: MOVE TO OPEN SPACE!!!




    #if the `securityScore.bestDirection` is a list, move on to the strategyScore direction

    tempDirection = securityScore.bestDirection()

    if len(tempDirection) == 1:
        print("The only safe direction to move is: {}".format(tempDirection))
        return tempDirection

    #else, if the `securityScore.bestDirection` is only one direction, return that
    else:
        print("There are more than one safe choice, moving on to strategy choices")

        #TODO: strategyScore calculations

        #TODO: simplest stategy play is moving to the empty quadrant

            #TODO: best way to loop through each coordinate for each enemy?

    return None
