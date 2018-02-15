class MoveChoices:
    def __init__(self, up=0, right=0, down=0, left=0):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        
    #return 
    def bestDirection(self):
        #TODO: return which direction should be moved to, is two equal the same, return a list
        print("the best direction to move is...")
        
        #if the max value is 0, there isn't a good choice, return `None`
    
    #return a string version of the best direction
    #def stringifyDirection(self):

class Snake:
    def __init__(self, name, isUs):
        #TODO: do they have an ID we need to include here?
        self.name = name #name of the snake
        self.isUs = isUs #boolean for whether this is snake our snake
        self.length = None #length of the snake
        self.locations = [] #list of positions on the baord occupied by the snake
    
    #TODO: function for returning this snakes next move. Only if it's not our snake?
    
    #function for checking location of the snake's head
    def snakeHead(self):
        if self.locations: return self.locations[0]
        else: return None
    
    #TODO: function for checking if a coordinate pair is adjacent to this snake
    def conllisionCheck(self, checkPair):
        
        tempDirection = MoveChoices(1,1,1,1)
        #for non-head location in squatchy
        for location in self.locations:
            
            #if the head shares the same x value as the element of the body
            if checkPair[0] == location[0]:
                
                #if moving one up will hit the body
                if (checkPair[1] + 1) == location[1]:
                    tempDirection.up = 0
                
                #if moving one down will hit the body
                if (checkPair[1] - 1) == location[1]:
                    tempDirection.down = 0
            
            #if the head shares the same y value as the element of the body
            if checkPair[1] == location[1]:
                
                #if moving one to the right will hit the body
                if (checkPair[0] + 1) == location[0]:
                    tempDirection.right = 0
                
                #if moving one to the left will hit the body
                if (checkPair[0] - 1) == location[0]:
                    tempDirection.left = 0
                    
        return tempDirection.bestDirection
            
        

