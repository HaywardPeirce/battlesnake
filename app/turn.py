from battlesnakeClasses import *

#import each of the component files running sections of the snake

def squatchyHitCheck(squatchy, securityScore):
    #get current squatchy head location
    print(squatchy.snakeHead)
    
    #get list of squatchy non-head locations
    #bodyLocations = 
    
    
    
#def wallHitCheck():
    
    #how wide is the board?
    
    #is our head going to hit the wall next turn?
    

#def enemyHitCheck():
    
    #loop through each enemy, `conllisionCheck` for our snake head


#return a string of which way squatchy should move
def turn(turnData, squatchy, enemies):
    
    #TODO: setup snakes based on the their initial positions
    
    myLocation = []
    for point in turnData['you']['body']['data']:
        myLocation.append(tuple((point.x,point.y)))
    
    squatchy.locations = myLocation
    squatchy.health = turnData['you']['health']
    squatchy.length = turnData['you']['length']
    
    #TODO: update positions, length, and health of each of the opponent snakes. Maybe check if it's turn 1 to initilize (name, ID...) the snakes, otherwise just update the values
    
    #first turn, setup opponent snakes
    if turnData['turn'] == 0:
        #TODO: setup initialization info about each snake 
        
        for snake in turnData['snakes']:
            print(snake)
    
    #non-first turn snake updates: positions, length, and health
    #else:
        #TODO: second turn+ snake info updates
    
    #initialize the security score for the turn as being zero
    securityScore = MoveChoices()
    
    #strategyScore = MoveChoices()
    
    #securityScore checks, to make sure this next turn's move is safe
    #TODO: check to see we wont hit ourself
    securityScore += squatchyHitCheck(squatchy, securityScore)
    
    #TODO: check to see we won't hit a wall
    
    #TODO: check to see we won't hit another snake
    
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
    