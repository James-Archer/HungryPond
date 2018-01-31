from organism import *
from pondConstants import *
from math import sqrt, atan, pi

class Pond():

    def __init__(self, n):

        self.orgs = []
        self.eggs = []
        self.dimensions = DIMENSIONS
        self.food = []
        self.t = 0

        for i in range(0,n):
            newOrg = Organism(self)
            newOrg.pos = randomPos()
            self.orgs.append(newOrg)

        for i in range(0, INITIAL_FOOD):
            self.food.append(Food())

    def step():

        for org in self.orgs:
            org.think()
            for food in self.food:
                if getDistance(org, food) < 0.1:
                    org.eat(food.food)
                    food.food = 0
        
        return

    def getNearestFood(self, organism):

            nearestFood = self.food[0]
            nearestDist = getDistance(organism, self.food[0])
            for food in self.food:
                d = getDistance(organism, food)
                if d < nearestDist:
                    nearestDist = d
                    nearestFood = food
            return getAngle(organism, nearestFood), nearestDist


class Food():

    def __init__(self, pos = None):

        if pos:
            self.pos = pos
        else:
            self.pos = randomPos()                     
        self.food = 1
        

def randomPos():

    pos = {'x':uniform(0,DIMENSIONS['x']),
           'y':uniform(0,DIMENSIONS['x'])}

    return pos

def getDistance(a, b):

    return sqrt((a.pos['x'] - b.pos['x'])**2
                + (a.pos['y'] - b.pos['y'])**2)

def getAngle(a,b):

    # Angle of b from a
    dx = b.pos['x'] - a.pos['x']
    dy = b.pos['y'] - a.pos['y']
    if dx == 0:
        if dy > 0:
            return pi/2
        else:
            return -pi/2
    elif dx > 0:
        return atan(dy/dx)
    else:
        return (pi - atan(dy/dx))
    
    
