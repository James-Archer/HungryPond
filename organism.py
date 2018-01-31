from organismConstants import *
from random import gauss, uniform
from NeuralNetwork import *
from math import sin, cos

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

BASE_NETWORK = Network()
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

        self.food = 1
        self.pos = {'x':0,'y':0}
        self.brain = BASE_NETWORK.copyNetwork()
        self.brain.mutate()
        self.pond = pond

    def __str__(self):

        s = ""
        for key, value in self.BASE_STATS.items():
            s += str(key) + ": " + str(value) + "\n"
        s += "\n"
        for key, value in self.CALC_STATS.items():
            s += str(key) + ": " + str(value) + "\n"

        s += 'Position: {}, {}\n'.format(self.pos['x'], self.pos['y'])

        return s

    def think(self):

        food_angle, food_dist = self.pond.getNearestFood(self)
        speed, direction = self.brain.runInputs([self.food,
                                                food_angle,
                                                food_dist])

        self.move(speed, direction)
        
    def move(self, speed, direction):

        self.pos['x'] += self.BASE_STATS['speed'] * speed * cos(direction)
        self.pos['y'] += self.BASE_STATS['speed'] * sin(direction)
        self.food -= 0.001 * speed * self.CALC_STATS["metabolism"]

        
    def eat(self, food):

        self.food += food


    def updateMetabolism(self):

        self.CALC_STATS["metabolism"] = (self.BASE_STATS["strength"]
                                    + self.BASE_STATS["speed"])
        if self.BASE_STAT["diet"] == "meat":
            self.CALC_STATS["metabolism"] /= 2

    def updateEggFreq(self):

        pass

    def updateEggTime(self):

        pass

    def updateCarnFeat(self):

        pass

    def layEgg(self):

        return Egg(self)

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
        self.pos = organism.pos

    def hatch(self):

        newOrg = Organism()
        for key, value in self.CALC_STATS.items():
            newOrg.CALC_STATS[key] = value
        for key, value in self.BASE_STATS.items():
            newOrg.BASE_STATS[key] = value
        newOrg.pos = self.pos
        return newOrg
