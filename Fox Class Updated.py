import numpy as np
import random as rd
import math
from time import sleep
food_id = 6
class Fox:
    def __init__(self, fox_id, family, size, speed, pos, direction):
        self.fox_id = fox_id
        self.family = family
        self.size = size
        self.speed = speed
        self.pos = np.array(pos)
        self.direction = unitVector(np.array(direction))
    
    def canidList(self, foxAgentList):
        foxPositionList = [[]]
        for fox in foxAgentList:
            if fox.fox_id == self.fox_id: continue
            foxPositionList.append([fox.pos, fox.family])
    
    def closestCanid(self, foxAgentList):
        foxPositionList = self.canidList(foxAgentList)
        closest = findClosest(self.pos, foxPositionList[0])
        dirVector = unitVector(closest[0])
        distance = closest[1]
        arrayPosition = closest[2]
        if distance < 10:
            if foxPositionList[arrayPosition][1] == self.family:
                dirVector *= rd.uniform(1,2)
                self.direction = unitVector(self.direction+dirVector)
            else: self.direction = unitVector(self.direction-dirVector)
    
    def findClosestFood(self, enclosure):
        foodList = find_items(enclosure, food_id)
        closest = findClosest(self.pos, foodList)
        dirVector = unitVector(closest[0])
        distance = closest[1]
        self.direction = dirVector
    
    def moveTo(self, enclosure, item_id): #inputs a thing and a fox, returns the direction vector to a fox
        itemList = find_items(enclosure, item_id)
        closest = findClosest(self.pos, itemList)
        dirVector = unitVector(closest[0])
        self.direction = dirVector
        
    def atAThing(self, enclosure, item_id):# thing and fox are same position
        itemList = find_items(enclosure, item_id)
        for item in itemList:
            if round(self.pos[1]) == item[0] and round(self.pos[0]) == item[1]:
                return True
                break
            else:
                return False
           
    def makeDen(self, masterArray):
        masterArray[3][self.pos[1]][self.pos[0]] = self.family
    
    def boundaryCheck(self, xSize, ySize):
        if self.pos[0]+self.direction[0] < 0 or self.pos[0]+self.direction[0] > xSize:
            self.direction[0] += -1*self.direction[0]*rd.uniform(1,2)
        if self.pos[1]+self.direction[1] < 0 or self.pos[1]+self.direction[1] > ySize:
            self.direction[1] += -1*self.direction[1]*rd.uniform(1,2)
        self.direction = unitVector(self.direction)
            
    def move(self, masterArray):
        self.boundaryCheck(xSize, ySize)
        if masterArray[1][round(self.pos[1])][round(self.pos[0])] == 0:
            self.pos = self.pos+self.direction
            masterArray[1][round(self.pos[1])][round(self.pos[0])] = self.fox_id
        
def unitVector(vector):
    if np.linalg.norm(vector) != 1:
        vector /= np.linalg.norm(vector)
    return vector

def findClosest(canidPosition, positionList):
        lowestDist = None
        counter = 0
        for position in positionList:
            counter += 1
            if lowestDist is None or lowestDist > np.linalg.norm(position-canidPosition):
                distVector = np.array(position-canidPosition)
                lowestDist = np.linalg.norm(distVector)
                arrayPosition = counter
        return [distVector, lowestDist, arrayPosition]

def find_items(enclosure, item_id):
    item_locations = []
    if item_id not in valid_ids:
        return []  # return empty list if num is not a known ID
    for i, row in enumerate(enclosure):  # loop through rows (meters in height)
        for j, value in enumerate(row):  # loop through columns (meters in width)
            if value == item_id:  # Check if the item is present
                item_locations.append(np.array(j, i))
    return item_locations

def exists(enclosure, item_id):# inputs thing and checks that thing
    itemList = find_items(enclosure, item_id)
    if len(itemList) != 0:
        return True
    else:
        return False

def createFoxAgents(numFoxes, numFamilies, startingPositions):
    foxAgents = []
    for i in range(numFoxes-1):
        foxAgents.append(Fox(i+1, rd.randint(1,numFamilies), rd.uniform(1,5), rd.uniform(35,55), startingPositions[0], startingPositions[1], [0,0]))
        
def moveCanid(foxAgentList, masterArray):
    counter = 0
    while(True):
        hour = int(counter/3600)
        day = int(hour/24)
        counter += 1
        for fox in foxAgentList:
            fox.move(masterArray)
            
#magn = np.linalg.norm(arr)
#print(rd.uniform(1,5))
#print(math.cos(math.radians(90)))
#for foxAgent in fox:
    #print(foxAgent)
#for fox in foxAgents:
    #print(fox.fox_id, " ", fox.pos, " ", fox.direction)
    #fox.move(foxAgents)
    #print(fox.fox_id, " ", fox.pos)
while(True):
    print(foxAgents[0].pos, " ", foxAgents[0].direction)
    for fox in foxAgents:
        fox.move(foxAgents)
    sleep(1)
