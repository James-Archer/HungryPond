from organismConstants import *
from organismNames import *
from random import gauss, uniform, choice
import neuralnetwork as NN
from math import sin, cos, pi

''' The initial network configuration to act as the brain
Three inputs:
  self.food
  nearest food direction
  nearest food distance

Two outputs:
  speed
  direction

Two laters with two neurons each
'''

BASE_NETWORK = NN.Network()
BASE_NETWORK.createNetwork([3,2],[2,2])

class Organism:

    def __init__(self, pond):

        self.BASE_STATS = {"strength":abs(gauss(MEAN_STRENGTH, STRENGTH_SD)),
                      "speed":abs(gauss(MEAN_SPEED, SPEED_SD)),
                      "vision":abs(gauss(MEAN_VISION, VISION_SD)),
                      "diet":None,
                      "colour":None
                      }

        self.CALC_STATS = {"metabolism":0,
                      "eggFreq":abs(gauss(MEAN_EGGFREQ, EGGFREQ_SD)),
                      "eggTime":abs(gauss(MEAN_EGGTIME, EGGTIME_SD)),
                      "carnFeat":0
                      }
        
        self.name = f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}"

        self.alive = True
        self.food = 1
        self.pos = {'x':0,'y':0}
        self.brain = BASE_NETWORK.copyNetwork()
        self.brain.populateNetwork()
        self.updateAll()
        
        # Really scramble the brain
        for i in range(100):
            self.brain.mutate()
        self.pond = pond

    def __str__(self):

        s = "--------" + self.name + "--------\n"
        for key, value in self.BASE_STATS.items():
            s += str(key) + ": " + str(value) + "\n"
        s += "Time to egg: " + str(self.timeToEgg) + "\n"
        s += "\n"
        for key, value in self.CALC_STATS.items():
            s += str(key) + ": " + str(value) + "\n"

        s += 'Position: {}, {}\n'.format(self.pos['x'], self.pos['y'])

        return s

    def think(self):
        food_angle, food_dist = self.pond.getNearestFood(self)
        speed, direction = self.brain.runInputs([self.food,
                                                food_angle/2*pi,
                                                food_dist])

        self.move(speed, direction*2*pi)
        
    def move(self, speed, direction):

        newX = self.pos['x'] + self.BASE_STATS['speed'] * speed * cos(direction)
        newY = self.pos['y'] + self.BASE_STATS['speed'] * speed * sin(direction)
        
        if newX >= self.pond.dimensions['x'] or newX <= 0:
            newX = self.pos['x'] - self.BASE_STATS['speed'] * speed * cos(direction)
        if newY >= self.pond.dimensions['y'] or newY <= 0:
            newY = self.pos['y'] - self.BASE_STATS['speed'] * speed * cos(direction)
        
        self.pos['x'] = newX
        self.pos['y'] = newY
        # Reduce food by how much was moved, plus base metabolism loss
        self.food -= EFFICIENCY * (speed + 1) * self.CALC_STATS["metabolism"]
        self.checkAlive()

        
    def eat(self, food):

        self.food += food
        
    def decrementTimeToEgg(self):
        
        self.timeToEgg -= 1
        
    def updateAll(self):
        
        self.updateCarnFeat()
        self.updateEggFreq()
        self.updateEggTime()
        self.updateMetabolism()
        self.updateTimeToEgg()
        
    def updateTimeToEgg(self):
        
        self.timeToEgg = int(1/self.CALC_STATS['eggFreq'])
        if self.timeToEgg < 1:
            self.timeToEgg = 1

    def updateMetabolism(self):

        self.CALC_STATS["metabolism"] = (self.BASE_STATS["strength"]
                                    + self.BASE_STATS["speed"])
        if self.BASE_STATS["diet"] == "meat":
            self.CALC_STATS["metabolism"] /= 2

    def updateEggFreq(self):

        pass

    def updateEggTime(self):

        pass

    def updateCarnFeat(self):

        pass

    def layEgg(self):

        self.updateTimeToEgg()
        if self.food >= 1:
            self.food -= 1
            return Egg(self)
        else:
            return False
    
    def checkAlive(self):
        
        if self.food <= 0:
            self.alive = False

class Egg():

    def __init__(self, organism):
        
        self.BASE_STATS = {"strength":abs(gauss(organism.BASE_STATS["strength"], STRENGTH_SD)),
                      "speed":abs(gauss(organism.BASE_STATS["speed"], SPEED_SD)),
                      "vision":abs(gauss(organism.BASE_STATS["vision"], VISION_SD)),
                      "diet":organism.BASE_STATS["diet"],
                      "colour":organism.BASE_STATS["colour"]
                      }

        self.CALC_STATS = {"metabolism":0,
                      "eggFreq":abs(gauss(organism.CALC_STATS["eggFreq"], EGGFREQ_SD)),
                      "eggTime":abs(gauss(organism.CALC_STATS["eggFreq"], EGGTIME_SD)),
                      "carnFeat":organism.CALC_STATS["carnFeat"]
                      }
        self.hatchTime = organism.CALC_STATS["eggTime"]
        self.pos = {'x':float(organism.pos['x']),'y':float(organism.pos['y'])}
        self.pond = organism.pond

    def hatch(self):

        newOrg = Organism(self.pond)
        for key, value in self.CALC_STATS.items():
            newOrg.CALC_STATS[key] = value
        for key, value in self.BASE_STATS.items():
            newOrg.BASE_STATS[key] = value
        newOrg.pos = {'x':float(self.pos['x']),'y':float(self.pos['y'])}
        newOrg.updateAll()
        return newOrg
    
    def decrementHatch(self):
        
        self.hatchTime -= 1
