from battlesnakeClasses import *
import random

#import each of the component files running sections of the snake

#check if squatchy will hit himself
def squatchyHitCheck(squatchy):
    #get current squatchy head location
    print("------------------------------------------------")
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
    print("------------------------------------------------")
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
    print("------------------------------------------------")
    print("Check whether squatchy will hit any other snakes")
    #loop through each enemy, `conllisionCheck` for our snake head
    print("squatchy head: [{}]".format(squatchy.head()))

    enemyDirections = MoveChoices()

    #TODO: I think this is broken by the conllisionCheck function somehow...

    #loop through each enemy snake
    for enemy in enemies:
        print("------------------------")
        print("Checking whether squatchy will hit '{}'".format(enemy.name))
        tempDirection = enemy.conllisionCheck(squatchy.head(), 1)

        #tempDirection.printMoves()

        #if the scores for the hit checks againts this snake turn up new collisons, count out those moves. (less than means a new dangerous move)
        if tempDirection.up < enemyDirections.up:
            enemyDirections.up = tempDirection.up
        if tempDirection.down < enemyDirections.down:
            enemyDirections.down = tempDirection.down
        if tempDirection.right < enemyDirections.right:
            enemyDirections.right = tempDirection.right
        if tempDirection.left < enemyDirections.left:
            enemyDirections.left = tempDirection.left

        enemyDirections.printMoves("After `enemyDirections` for {}".format(enemy.name))


    return enemyDirections

def foodCheck(squatchy, food):
    print("------------------------------------------------")
    print("Check whether squatchy should head towards any food")

    foodDirections = MoveChoices()

    #TODO: calculate directions to closest food. Maybe see of we are the closest as well?



    return foodDirections


#return the direction of the quadant with the least other snakes in it
def findOpenSpace(squatchy, enemies, gameBoard):
    print("------------------------------------------------")
    print("Check which directions lead towards open space")
    tempDirection = MoveChoices()

    #q1, q2, q3, q4 = 0, 0, 0, 0

    #set the x and y values that the higher-numbered quadrants will start on

    tempDirection.addMoves(gameBoard.wayToMin(squatchy.head(), enemies))





    #TODO: check which quadrant has the least snake parts, move there. If there are two equally empty ones?



    #find min value
    #find which quadrants have this least value
    #find squatchy quadrants

    #return directionToQuadrant()


    return tempDirection

#return a string of which way squatchy should move
def turn(turnData, gameBoard, squatchy, enemies):

    #TODO: setup snakes based on the their initial positions

    #print('hello world')
    #print(turnData)

    # myLocation = []
    # for point in turnData['you']['body']['data']:
    #     myLocation.append(tuple((point['x'],point['y'])))
    #
    # squatchy.locations = myLocation
    # squatchy.health = turnData['you']['health']
    # squatchy.length = turnData['you']['length']



    #update positions, length, and health of each of the opponent snakes. Maybe check if it's turn 1 to initilize (name, ID...) the snakes, otherwise just update the values

    #first turn, setup opponent snakes
    #if turnData['turn'] == 0:
        #TODO: setup initialization info about each snake

    gameBoard.addFood(turnData['food']['data'])

    enemies = []

    for snake in turnData['snakes']['data']:

        tempSnake = Snake(snake['id'], snake['name'])

        tempLocations = []
        for location in snake['body']['data']:
            tempLocations.append(tuple((location['x'],location['y'])))

        tempSnake.locations = tempLocations

        tempSnake.length = snake['length']

        tempSnake.health = snake['health']

        if snake['id'] == turnData['you']['id']:
            print("Adding data in for snake: {} (squatchy)".format(snake['name']))
            squatchy = tempSnake
            squatchy.isUs = True

        else:
            print("Adding data in for snake: {}".format(snake['name']))
            enemies.append(tempSnake)





    #non-first turn snake updates: positions, length, and health
    # else:
    #     #TODO: second turn+ snake info updates
    #
    #     for snake in turnData['snakes']['data']:
    #
    #         for enemy in enemies:
    #             #print(enemy.id)
    #             #print(enemy.name)
    #
    #             if enemy.id == snake['id']:
    #                 print(snake['id'])
    #                 print(snake['name'])
    #
    #                 print(enemy.locations)
    #
    #                 tempLocations = []
    #                 for location in snake['body']['data']:
    #                     tempLocations.append(tuple((location['x'],location['y'])))
    #
    #                 enemy.locations = tempLocations
    #
    #                 enemy.length = snake['length']
    #
    #                 enemy.health = snake['health']




    #initialize the security score for the turn as being zero

    securityScore = MoveChoices()

    strategyScore = MoveChoices()

    #securityScore checks, to make sure this next turn's move is safe
    #TODO: check to see we wont hit ourself

    securityScore.addMoves(squatchyHitCheck(squatchy))
    securityScore.printMoves("After `squatchyHitCheck`: ")

    #TODO: check to see we won't hit a wall
    securityScore.addMoves(wallHitCheck(squatchy, gameBoard.height, gameBoard.width))
    securityScore.printMoves("After `wallHitCheck`: ")

    #TODO: check to see we won't hit another snake
    securityScore.addMoves(enemyHitCheck(squatchy, enemies))
    securityScore.printMoves("After `enemyHitCheck`: ")







    #if the `securityScore.bestDirection` is a list, move on to the strategyScore direction

    #returns a list of directions that should be moved in
    securityScoreDirections = securityScore.bestDirection()

    if len(securityScoreDirections) == 1:
        print("------------------------------------------------")
        print("The only safe direction to move is: {}".format(securityScoreDirections))
        #return the only element of the list of available moves
        return securityScoreDirections[0]


    #else, if the `securityScore.bestDirection` is only one direction, return that
    else:
        print("------------------------------------------------")
        print("There is more than one safe choice({}), moving on to us strategy choices".format(securityScoreDirections))

        #TODO: strategyScore calculations

        #TODO: check to see if we an eat next turn
        strategyScore.addMoves(foodCheck(squatchy, gameBoard.food))
        strategyScore.printMoves("After `foodCheck`: ")

        #TODO: simplest stategy play is moving to the empty quadrant
        strategyScore.addMoves(findOpenSpace(squatchy, enemies, gameBoard))
        strategyScore.printMoves("After `findOpenSpace`: ")

        #TODO: reconcile security and strategy scores

        strategyScoreDirections = strategyScore.bestDirection()

        #list of moves which are allowed from a security standpoint, and are optimal from a strategy standpoint
        finalDirectionList = []

        #loop through each of the good security moves, and better strategy moves
        for secureDirection in securityScoreDirections:
            for stratDirection in strategyScoreDirections:
                #if the move in strategy is also safe, add it to the final list of moves that could be made
                if secureDirection == stratDirection: finalDirectionList.append(secureDirection)

        print("------------------------------------------------")
        print("finalDirectionList: {}".format(finalDirectionList))
        #if there is only one "final" approved move, return that
        if len(finalDirectionList) == 1:
            return finalDirectionList[0]
        #if there are multiple options for safe and strategic moves, return a random one
        else:
            returnValue = random.choice(finalDirectionList)
            print("Returning instruction to move : {}".format(returnValue))
            return returnValue

    print("------------------------------------------------")
    print("couldn't work out a smart move to make, selecting a random direction")
    #fallback, return a random direction

    returnValue = random.choice(securityScoreDirections)
    print("Returning instruction to move : {}".format(returnValue))
    return returnValue
