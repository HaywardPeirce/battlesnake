from battlesnakeClasses import *
import random, math

#import each of the component files running sections of the snake

#check if squatchy will hit himself
def squatchyHitCheck(squatchy, score):
    #get current squatchy head location
    print("------------------------------------------------")
    print("Checking whether squatchy will hit himself")
    print("squatchy head: [{}]".format(squatchy.head()))

    #see if squatchy's head will hit his body
    tempDirection = squatchy.conllisionCheck(squatchy.head(), score)

    #print(tempDirection)

    tempDirection.printMoves()

    return tempDirection

    #get list of squatchy non-head locations
    #bodyLocations =


#check if squatchy will run into a wall
def wallHitCheck(squatchy, height, width, freespaceScore):
    print("------------------------------------------------")
    print("Checking whether squatchy will hit the wall")
    print("squatchy head: [{}]".format(squatchy.head()))

    #how wide is the board?

    #freespaceScore = 1

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

    tempDirection.printMoves()
    return tempDirection


def enemyHitCheck(squatchy, enemies, score):
    print("------------------------------------------------")
    print("Check whether squatchy will hit any other snakes")
    #loop through each enemy, `conllisionCheck` for our snake head
    print("squatchy head: [{}]".format(squatchy.head()))

    #value to use when weighting enemy detection
    #score = 1

    #set initial enemy direction to "safe" as hit detection will set unsafe options to 0
    enemyDirections = MoveChoices(score, score, score, score)



    #loop through each enemy snake
    for enemy in enemies:
        print("------------------------")
        print("Checking whether squatchy will hit '{}'".format(enemy.name))

        #see if squatchy's head will collide with any part of this enemy snake
        tempDirection = enemy.conllisionCheck(squatchy.head(), score)

        tempDirection.printMoves()

        enemyDirections.boolDownMoves(tempDirection)

        #if the scores for the hit checks againts this snake turn up new collisons, count out those moves. (less than means a new dangerous move)
        # if tempDirection.up < enemyDirections.up:
        #     enemyDirections.up = tempDirection.up
        # if tempDirection.down < enemyDirections.down:
        #     enemyDirections.down = tempDirection.down
        # if tempDirection.right < enemyDirections.right:
        #     enemyDirections.right = tempDirection.right
        # if tempDirection.left < enemyDirections.left:
        #     enemyDirections.left = tempDirection.left

        enemyDirections.printMoves("After `enemyDirections` for {}".format(enemy.name))


    return enemyDirections

def moveToSameCheck(squatchy, enemies, score):
    print("------------------------------------------------")
    print("Check whether squatchy might be moving to the same square as another snake")

    enemyDirections = MoveChoices(score, score, score, score)
    directions = [(0,-1),(1,0),(1,1),(-1,0)]
    #TODO:

    squatchyNextTurn = squatchy.possibleMoves()

    print("squatchy head: [{}]".format(squatchy.head()))

    #loop through each enemy
    for enemy in enemies:
        print("------------------------")
        print("Checking whether squatchy might move into '{}'".format(enemy.name))
        #print("{} head: [{}]".format(enemy.name, enemy.head()))

        enemyNextTurn = enemy.possibleMoves()

        #loop through the enemies possible moves, and check if it would collide with where squatchy would be
        for position in enemyNextTurn:
            tempDirection = conllisionCheck(position, squatchy.head(), score)

            #tempDirection.printMoves()

            enemyDirections.boolDownMoves(tempDirection)

            #if the scores for the hit checks againts this snake turn up new collisons, count out those moves. (less than means a new dangerous move)
            # if tempDirection.up < enemyDirections.up:
            #     enemyDirections.up = tempDirection.up
            # if tempDirection.down < enemyDirections.down:
            #     enemyDirections.down = tempDirection.down
            # if tempDirection.right < enemyDirections.right:
            #     enemyDirections.right = tempDirection.right
            # if tempDirection.left < enemyDirections.left:
            #     enemyDirections.left = tempDirection.left


        enemyDirections.printMoves("After `enemyDirections` for {}".format(enemy.name))

    return enemyDirections


def foodCheck(squatchy, height, width, food, score):
    print("------------------------------------------------")
    print("Check whether squatchy should head towards any food")

    #TODO: work out scaling/weighting factor based on how hungry squatchy is
    if squatchy.health > 20:
        score = 0

    foodDirections = MoveChoices()

    bestDist = max(height, width)
    bestFood = []

    #calculate directions to closest food. Maybe see of we are the closest as well?

    for nibble in food:

        #tempDistance = math.sqrt( ((squatchy.head()[0]-nibble[0])**2)+((squatchy.head()[1]-nibble[1])**2) )

        #just sum each component of the distance rather than finding the diagonal route
        tempDistance = abs(squatchy.head()[0]-nibble[0]) + abs(squatchy.head()[1]-nibble[1])

        if tempDistance < bestDist:
            bestFood = [tuple((nibble[0],nibble[1]))]
            bestDist = tempDistance

        elif tempDistance == bestDist:
            bestFood.append(tuple((nibble[0],nibble[1])))

    #TODO: work out direction to nearest food pieces

    #loop through the food items that are closest
    for item in bestFood:
        tempDirection = squatchy.directionCheck(item, score)

        #take all the directions which lead to the closest foods, but don't go above the value of `score`
        if tempDirection.up > foodDirections.up:
            foodDirections.up = tempDirection.up
        if tempDirection.down > foodDirections.down:
            foodDirections.down = tempDirection.down
        if tempDirection.right > foodDirections.right:
            foodDirections.right = tempDirection.right
        if tempDirection.left > foodDirections.left:
            foodDirections.left = tempDirection.left

    return foodDirections


#return the direction of the quadant with the least other snakes in it
def findOpenSpace(squatchy, enemies, gameBoard, score):
    print("------------------------------------------------")
    print("Check which directions lead towards open space")
    tempDirection = MoveChoices()

    #q1, q2, q3, q4 = 0, 0, 0, 0

    #set the x and y values that the higher-numbered quadrants will start on

    #tempDirection.addMoves(gameBoard.wayToMin(squatchy.head(), enemies))
    tempDirection.boolDownMoves(gameBoard.wayToMin(squatchy.head(), enemies, 100))





    #TODO: check which quadrant has the least snake parts, move there. If there are two equally empty ones?



    #find min value
    #find which quadrants have this least value
    #find squatchy quadrants

    #return directionToQuadrant()

    tempDirection.printMoves("After `findOpenSpace`(inside): ")
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

    #add food points into game boad declaration
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

    securityScore = MoveChoices(100,100,100,100)

    strategyScore = MoveChoices()

    #list of moves which are allowed from a security standpoint, and are optimal from a strategy standpoint
    finalDirectionList = []

    #securityScore checks, to make sure this next turn's move is safe

    #check to see we wont hit ourself
    #securityScore.addMoves(squatchyHitCheck(squatchy, 100))
    securityScore.boolDownMoves(squatchyHitCheck(squatchy, 100))
    securityScore.printMoves("After `squatchyHitCheck`: ")

    #check to see we won't hit a wall
    #securityScore.addMoves(wallHitCheck(squatchy, gameBoard.height, gameBoard.width, 100))
    securityScore.boolDownMoves(wallHitCheck(squatchy, gameBoard.height, gameBoard.width, 100))
    securityScore.printMoves("After `wallHitCheck`: ")

    #check to see we won't hit another snake
    #securityScore.addMoves(enemyHitCheck(squatchy, enemies, 100))
    securityScore.boolDownMoves(enemyHitCheck(squatchy, enemies, 100))
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
    elif len(securityScoreDirections) > 1:
        print("------------------------------------------------")
        print("There is more than one safe choice({}), moving on to use strategy choices".format(securityScoreDirections))

        #strategyScore calculations

        #TODO: check to see if another snake might move into the same spot as us next turns
        strategyScore.addMoves(moveToSameCheck(squatchy, enemies, 100))
        strategyScore.printMoves("After `moveToSameCheck`: ")

        #TODO: check to see if the snake will have moved away from a spot next turn. maybe have this and `moveToSameCheck` in security check?

        #TODO: check if they are moving into an enclosed space, don't do that (flood fill?)

        #TODO: check to see if we an eat next turn
        print("------------------------------------------------")
        #print(gameBoard.food)
        if gameBoard.food:
            if squatchy.health < 50:
                strategyScore.addMoves(foodCheck(squatchy, gameBoard.height, gameBoard.width, gameBoard.food, 100))
                strategyScore.printMoves("After `foodCheck`: ")
            else: print("Squatchy's health is above 50, so no food moves will be recommended")
        else: print("There is no food on the board")

        # simplest stategy play is moving to the empty quadrant
        strategyScore.addMoves(findOpenSpace(squatchy, enemies, gameBoard, 100))
        print("------------------------------------------------")
        strategyScore.printMoves("After `findOpenSpace`: ")

        #TODO: advanced strategy move checks

        #reconcile security and strategy scores
        print("------------------------------------------------")
        print("strategyScore bestDirection:")
        strategyScoreDirections = strategyScore.bestDirection()

        #loop through each of the good security moves, and better strategy moves
        for secureDirection in securityScoreDirections:
            for stratDirection in strategyScoreDirections:
                #if the move in strategy is also safe, add it to the final list of moves that could be made
                if secureDirection == stratDirection: finalDirectionList.append(secureDirection)
    else:
        print("------------------------------------------------")
        print("No safe move available, returning totally random direction")
        #fallback, return a random direction

        returnValue = random.choice("up", "right", "down", "left")
        print("Returning totally random direction: {}".format(returnValue))
        return returnValue


    print("------------------------------------------------")
    print("finalDirectionList: {}".format(finalDirectionList))
    #if there is only one "final" approved move, return that
    if len(finalDirectionList) == 1:
        return finalDirectionList[0]
    #if there are multiple options for safe and strategic moves, return a random one
    elif len(finalDirectionList) > 1:
        returnValue = random.choice(finalDirectionList)
        print("Returning random move from multiple finalDirectionList options: {}".format(returnValue))
        return returnValue
    else:
        print("------------------------------------------------")
        print("couldn't work out a strategic move to make, falling back to random safe move")
        #fallback, return a random direction

        returnValue = random.choice(securityScoreDirections)
        print("Returning random safe move: {}".format(returnValue))
        return returnValue
