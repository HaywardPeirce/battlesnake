def conllisionCheck(location, checkPair, score):

    #location is static, checkPair is the moving point

    tempDirection = MoveChoices(score, score, score, score)
    #tempDirection.printMoves()

    #if the head shares the same x value as the element of the body
    #print("checkPair[0]: {}, location[0]: {}".format(checkPair[0],location[0]))
    if checkPair[0] == location[0]:

        #if moving one up will not hit the body
        if (checkPair[1] - 1) == location[1]:
            tempDirection.up = 0
            #print("moving up is not safe")


        #if moving one down will hit the body
        if (checkPair[1] + 1) == location[1]:
            tempDirection.down = 0
            #print("moving down is not safe")

    #if the head shares the same y value as the element of the body
    #print("checkPair[1]: {}, location[1]: {}".format(checkPair[1],location[1]))
    if checkPair[1] == location[1]:

        #if moving one to the right will hit the body
        if (checkPair[0] + 1) == location[0]:
            tempDirection.right = 0
            #print("moving right is not safe")

        #if moving one to the left will hit the body
        if (checkPair[0] - 1) == location[0]:
            tempDirection.left = 0
            #print("moving left is not safe")

    #tempDirection.printMoves("In `conllisionCheck`: ")
    return tempDirection

class Quadrant:
    def __init__(self, top, right, bottom, left):
        self.topBound = top
        self.rightBound = right
        self.bottomBound = bottom
        self.leftBound = left
        #self.occupancy = 0

    #check how many enemies are in a quadrant
    def checkOccupancy(self, enemies):

        occupancy = 0

        #use number of squares in quadrant to find average density,
        for enemy in enemies:
            for location in enemy.locations:

                if location[0] < self.rightBound and location[0] >= self.leftBound and location[1] < self.bottomBound and location[1] >= self.topBound:
                    occupancy += 1

        return occupancy
                # #if the pieces of the snake is in the first quadrant
                # if location[0] < xMid and location[1] < yMid: q1 += 1
                #
                # #if the pieces of the snake is in the second quadrant
                # if location[0] >= xMid and location[1] < yMid: q2 += 1
                #
                # #if the pieces of the snake is in the third quadrant
                # if location[0] >= xMid and location[1] >= yMid: q3 += 1
                #
                # #if the pieces of the snake is in the 4th quadrant
                # if location[0] < xMid and location[1] >= yMid: q4 += 1

    #which directions goes to a quadrant from a specific point
    def directionToQuadrant(self, point):
        #if the point is to the left of the quadrant
        if point[0] < self.leftBound:
            return "right"

        #if the point is to the right of the quadrant
        if point[0] >= self.rightBound:
            return "left"

        #if the point is above the quadrant
        if point[1] < self.topBound:
            return "down"

        #if the point is bellow the quadrant
        if point[1] >= self.bottomBound:
            return "up"

#-------
#|Q1|Q2|
#-------
#|Q4|Q3|
#-------

class Board:
    def __init__(self, height, width, food = []):
        self.height = height
        self.width = width
        self.q1 = Quadrant(0,(self.xMid() - 1), (self.yMid() - 1), 0)
        self.q2 = Quadrant(0, self.width, (self.yMid() - 1), self.xMid())
        self.q3 = Quadrant(self.yMid(), self.width, self.height, self.xMid())
        self.q4 = Quadrant(self.yMid(), (self.xMid() - 1), self.height, 0)
        self.food = food

    #read in the food for this turn
    def addFood(self, foodData):
        for item in foodData:
            self.food.append(tuple((item['x'],item['y'])))

    def xMid(self):
        #if the board is odd-sized
        if self.width % 2:
            return ((self.width - (self.width % 2))/2) + 1
        #if the board is even-sized
        else: return self.width/2

    def yMid(self):
        #if the board is odd-sized
        if self.height % 2:
            return ((self.height - (self.height % 2))/2) + 1
        #if the board is even-sized
        else: return self.height/2



    #directions to the emptiest quadrant
    def wayToMin(self, point, enemies, score):

        emptyQuadrantScore = score
        tempDirection = MoveChoices()

        #find what the lowest occupancy is
        minOccupancy = min(self.q1.checkOccupancy(enemies), self.q2.checkOccupancy(enemies), self.q3.checkOccupancy(enemies), self.q4.checkOccupancy(enemies))

        print("The minimum number of occupied spaces in a quadrant is {}".format(minOccupancy))

        if self.q1.checkOccupancy(enemies) == minOccupancy: tempDirection.translateMove(self.q1.directionToQuadrant(point), emptyQuadrantScore)
        if self.q2.checkOccupancy(enemies) == minOccupancy: tempDirection.translateMove(self.q2.directionToQuadrant(point), emptyQuadrantScore)
        if self.q3.checkOccupancy(enemies) == minOccupancy: tempDirection.translateMove(self.q3.directionToQuadrant(point), emptyQuadrantScore)
        if self.q4.checkOccupancy(enemies) == minOccupancy: tempDirection.translateMove(self.q4.directionToQuadrant(point), emptyQuadrantScore)

        tempDirection.printMoves("Directions to the emptiest quadrant: ")
        return tempDirection





class MoveChoices:
    def __init__(self, up=0, right=0, down=0, left=0):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    #return
    def bestDirection(self):
        #TODO: return which direction should be moved to, is two equal the same, return a list

        direction = []

        maxValue = max(self.up, self.right, self.down, self.left)


        sameScore = 0

        if self.up == maxValue: direction.append("up")
        if self.right == maxValue: direction.append("right")
        if self.down == maxValue: direction.append("down")
        if self.left == maxValue: direction.append("left")

        #print("the best direction to move is...")
        print("The best direction to move is: {}".format(direction))
        return direction

        #if the max value is 0, there isn't a good choice, return `None`

    #return a string version of the best direction
    #def stringifyDirection(self):

    #translate a string move into an actual direction, add it to direction
    def translateMove(self, move, value):
        if move == "up" or move =="top": self.up = value
        if move == "right": self.right = value
        if move == "down" or move == "bottom": self.down = value
        if move == "left": self.left = value

        # if move == "up" or move =="top": self.up += value
        # if move == "right": self.right += value
        # if move == "down" or move == "bottom": self.down += value
        # if move == "left": self.left += value

    def addMoves(self, toAdd):

        #TODO: maybe only add moves if the existing value isn't 0 (and other values aren't 0)?(means that it can still be moved to)
        self.left += toAdd.left
        self.right += toAdd.right
        self.up += toAdd.up
        self.down += toAdd.down

    #function to
    def boolDownMoves(self, otherMoves):
        if otherMoves.up < self.up:
            self.up = otherMoves.up
        if otherMoves.down < self.down:
            self.down = otherMoves.down
        if otherMoves.right < self.right:
            self.right = otherMoves.right
        if otherMoves.left < self.left:
            self.left = otherMoves.left

    def printMoves(self, info=""):
        print("{} Up: {}, Right: {}, Down: {}, Left: {}".format(info, self.up, self.right, self.down, self.left))

class Snake:
    def __init__(self, id, name):
        #TODO: do they have an ID we need to include here?
        self.id = id #name of the snake
        self.name = name #name of the snake
        self.isUs = False #boolean for whether this is snake our snake
        self.health = 100 #health of the snake
        self.length = 3 #length of the snake
        self.locations = [] #list of positions on the baord occupied by the snake

    #TODO: function for returning this snakes next move. Only if it's not our snake?

    #function for checking location of the snake's head
    def head(self):
        #print(len(self.locations))
        if not self.locations:
            print('this snake has no head')
            return None
        else:
            #print(self.locations[0])
            return self.locations[0]

    #return a list of coordinate pairs of where this snake might move
    def possibleMoves(self):

        tempMoves = []
        #directions = [(0,-1),(1,0),(0,1),(-1,0)]
        tempMoves.append(tuple((self.head()[0],(self.head()[1]-1))))
        tempMoves.append(tuple(((self.head()[0]+1),self.head()[1])))
        tempMoves.append(tuple((self.head()[0],(self.head()[1]+1))))
        tempMoves.append(tuple(((self.head()[0]-1),self.head()[1])))

        #print(tempMoves)

        return tempMoves

    #check the direction to a specific point from this snake's head
    def directionCheck(self, point, score):
        tempDirection = MoveChoices(0,0,0,0)

        head = self.head()

        #print(head[0], point[0], score)

        #the point is further to the right
        if point[0] > head[0]: tempDirection.right = score

        #the point is further to the left
        elif point[0] < head[0]: tempDirection.left = score

        #the point is on the same Y-axis
        #elif point[0] == head[0]: tempDirection.left = score

        #if the point is further down
        if point[1] > head[1]: tempDirection.down = score

        #if the point is further up
        elif point[1] < head[1]: tempDirection.up = score

        #tempDirection.printMoves()
        return tempDirection

    #TODO: function for checking if the head of a snake might move into the body of this snake
    def conllisionCheck(self, checkPair, score = 1):

        #weighted score to add if the direction will not run into this snake
        #freespaceScore = 1

        tempDirection = MoveChoices(score, score, score, score)

        print("Snake {}, head: {}, locations: {}".format(self.name, self.head(), self.locations))


        for location in self.locations:
            #for non-head location in squatchy
            #if location is not self.head():
            #print("location: {}".format(location))
            #print("checkPair: {}".format(checkPair))

            tempDirection.boolDownMoves(conllisionCheck(location, checkPair, score))
            #tempDirection.printMoves("After `boolDownMoves`: ")
        #print()

        return tempDirection
