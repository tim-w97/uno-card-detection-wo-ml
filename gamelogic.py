from enum import Enum

class Color(Enum):
    BLACK = 0
    YELLOW = 1
    RED = 2
    GREEN = 3
    BLUE = 4

class UnoCard:

    def __init__(self,number,color):
        self.number = number
        self.color = color
    
    def getNumber(self)->int:
        return self.number
    
    def getColor(self)->Color:
        return self.color
