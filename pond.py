from organism import *
from pondConstants import *
from math import sqrt, atan, pi
from random import uniform

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

    def step(self):

        # Move the organisms, and check if they eat food
        for org in self.orgs:
            org.updateMetabolism()
            org.think()
            for food in self.food:
                if getDistance(org, food) < MAXIMUM_EATING_DISTANCE:
                    org.eat(food.food)
                    food.food = 0
                    
        # Lay any eggs
        for org in self.orgs:
            org.decrementTimeToEgg()
            if org.timeToEgg <= 0:
                self.eggs.append(org.layEgg())
                if not self.eggs[-1]:
                    self.eggs = self.eggs[:-1]
                
        # Hatch any eggs
        for egg in self.eggs:
            egg.decrementHatch()
            if egg.hatchTime <= 0:
                self.orgs.append(egg.hatch())
        
        # Check food to see if it needs to be deleted.
        self.removeEatenFood()
        self.removeDeadOrgs()
        self.removeHatchedEggs()
        
        # Update time and move on
        self.t += 1
        #print(f'Time: {self.t}')
        #print(f"Net food: {round(self.countNetFood(), 2)}")
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
        
    def removeEatenFood(self):
        
        newFood = []
        for food in self.food:
            if food.food != 0:
                newFood.append(food)
        self.food = newFood
        return
    
    def removeDeadOrgs(self):
        
        newOrgs = []
        for org in self.orgs:
            if org.alive:
                newOrgs.append(org)
        self.orgs = newOrgs
        return
    
    def removeHatchedEggs(self):
        
        newEggs = []
        for egg in self.eggs:
            if egg.hatchTime > 0:
                newEggs.append(egg)
        self.eggs = newEggs
        return
    
    def countNetFood(self):
        
        total = sum([i.food for i in self.food])
        total += sum([i.food for i in self.orgs])
        total += len(self.eggs)
        return total
        

class Food():

    def __init__(self, pos = None):

        if pos:
            self.pos = pos
        else:
            self.pos = randomPos()                     
        self.food = NEW_FOOD_VALUE
        

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
    
    
