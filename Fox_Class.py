import numpy as np
import random as rd
import math

food_id = 6
random_id = 13

class Fox:
    def __init__(self, fox_id, family,pos, direction):
        self.fox_id = fox_id
        self.family = family
        self.hunger = 0
        self.sleep_need = 0
        self.sleep_timer = 0
        self.Denning = 1
        self.GOtoDEN = 0
        self.GoToFreind = 0.3
        self.FamilyTime = 0
        self.randomness = 0.1
        self.den_timer = 0
        self.pos = np.array(pos)
        self.direction = unitVector(np.array(direction))
    
    def canidList(self, foxAgentList):
        foxPositionList = []
        for fox in foxAgentList:
            if fox.fox_id == self.fox_id: continue
            foxPositionList.append([fox.pos, fox.family])
        return foxPositionList
    
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

    def closestCanidFriend(self, foxAgentList):
        foxPositionList = self.canidList(foxAgentList)
        lowestDist = None
        counter = 0
        for fox in foxPositionList:
            if (lowestDist is None or lowestDist > np.linalg.norm(fox[0]-self.pos)) and self.family == fox[1]:
                distVector = np.array(fox[0]-self.pos)
                lowestDist = np.linalg.norm(distVector)
                arrayPosition = counter
                distVector = unitVector(distVector)
        return [distVector, lowestDist, arrayPosition]
    
    def findDenRadius(self, enclosure):
        familyDens = find_items(enclosure[3], self.family)
        closestDen = findClosest(self.pos, familyDens)
        return closestDen
    
    def moveTo(self, enclosure, item_id): #inputs a thing and a fox, returns the direction vector to a fox
        itemList = find_items(enclosure, item_id)
        closest = findClosest(self.pos, itemList)
        dirVector = unitVector(closest[0])
        return dirVector
        
    def atAThing(self, enclosure, item_id):
        # thing and fox are same position
        
            if enclosure[round(self.pos[1])][round(self.pos[0])] == item_id:
                return True
            else:
                return False
           
    def makeDen(self, masterArray):
        masterArray[3][self.pos[1]][self.pos[0]] = self.family
    
    def boundaryCheck(self,array):
        if array[0][self.pos[0]+self.direction[0]][self.pos[1]+self.direction[1]] == 4 or array[0][self.pos[0]+self.direction[0]][self.pos[1]+self.direction[1]] == 0:
            self.direction[0] = 0
            self.direction[1] = 0
        if array[1][self.pos[0]+self.direction[0]][self.pos[1]+self.direction[1]] != 4:
            self.direction[0] = 0
            self.direction[1] = 0
        else:
            self.direction = unitVector(self.direction)
            
    def move(self, masterArray, AgentList):
        self.direction = np.array(self.BrainFOX(masterArray, AgentList))
        self.boundaryCheck(masterArray)
        self.pos = self.pos+self.direction
        masterArray[1][round(self.pos[1])][round(self.pos[0])] = self.fox_id
        masterArray[2][round(self.pos[1])][round(self.pos[0])] += 1
        return masterArray

    def DenQuantReached(self, array):
        count = 0
        family_num = self.family
        for row in array[0]:
            for num in row:
                if num == family_num:
                    count += 1
        if count >= 3:
            return True
        else:
            return False

    
    def BrainFOX(self, array, foxAgentList):
        hunger = self.hunger
        sleep_need = self.sleep_need
        sleep_timer = self.sleep_timer
        Denning = self.Denning
        GOtoDEN = self.GOtoDEN
        GoToFreind = self.GoToFreind
        FamilyTime = self.FamilyTime
        randomness = self.randomness
        den_timer = self.den_timer
        denplus_id = self.family

        self.hunger += 1/86400
        self.GOtoDEN += 1/25200
        self.FamilyTime += 1/10000
        self.sleep_need += 1/50400
            

        if Denning >= 1:
            if self.DenQuantReached(array[3]):
                self.Denning = 0
            denLocations = find_den_locations(array, self.family)
            closestDen = findClosest(self.pos, denLocations)
            if denLocations[closestDen[2]][0] == round(self.pos[0]) and denLocations[closestDen[2]][1] == round(self.pos[1]):
                self.makeDen(array)
                return [0, 0]
            else:
                return closestDen[0]
        if den_timer >= 1:
            self.den_timer = den_timer - (1/1200)
            return [0, 0]
        if sleep_timer > 0:
            self.sleep_timer = sleep_timer - (1/36000)
            return [0,0]
        if hunger >= 1 and exists(array[4], food_id):
            if self.atAThing(array[4], food_id):
                self.hunger = 0
                self.GOtoDEN = 1
                return self.moveTo(array[3], denplus_id)
            else:
                return self.moveTo(array[4], food_id)
        if GOtoDEN >= 1:
            closestDenRadius = self.findDenRadius(array)
            if closestDenRadius[1] <= 2:
                self.GOtoDEN = 0
                self.den_timer = 1
                return [0,0] #changed from self.moveTo(array[3], denplus_id)
            else:
                return closestDenRadius[0]
        if sleep_need >= 1:
            if self.atAThing(array[3], denplus_id):
                self.sleep_timer = 1
                return [0, 0]
            else:
                self.GOtoDEN = 1
                return self.moveTo(array[3], denplus_id)
        if GoToFreind >= 1:
            closestFriend = self.closestCanidFriend(foxAgentList)
            if closestFriend[1] <= 1.3:
                self.FamilyTime = 1
                self.GoToFreind = 0.3
                return [0,0] #changed from return self.moveTo(array, family_id)
            else:
                return closestFriend[0]
        if FamilyTime > 0:
            self.FamilyTime = FamilyTime - (1/7200)
            closestFriend = self.closestCanidFriend(foxAgentList)
            return closestFriend[0]
        
        else:
            
            option = weighted_random_choice(hunger, sleep_need, GOtoDEN, GoToFreind, randomness)

            if option == "Hunger":
                self.hunger = 1
                return [0, 0]


            if option == "Sleep Need":
                self.sleep_need = 0
                self.sleep_timer = 1
                return [0, 0]
      
            if option == "Go to Den":
                self.GOtoDEN = 1
                return self.moveTo(array[3], denplus_id)
       
            if option == "Go to Friend":
                self.GoToFreind = 1
                closestFriend = self.closestCanidFriend(foxAgentList)
                return closestFriend[0]
      
            else:
                return self.moveTo(array, random_id)
    
def weighted_random_choice(a, b, c, d, e):
   # Define options and their dynamic weights
   options = ["Hunger", "Sleep Need", "Go to Den", "Go to Friend", "Randomness"]
   weights = [a, b, c, d, e]  # These values change each time the function runs


   # Normalize weights (only if they don't sum to 1, but not strictly necessary)
   total_weight = sum(weights)
   if total_weight > 0:
       normalized_weights = [w / total_weight for w in weights]
   else:
       normalized_weights = weights  # Avoid division by zero (all weights are 0)


   # Select a random option based on the weights
   selected_option = rd.choices(options, weights=normalized_weights, k=1)[0]


   return selected_option
        
def unitVector(vector):
    if np.linalg.norm(vector) != 1 and np.linalg.norm(vector) != 0:
        vector /= np.linalg.norm(vector)
    return vector

def findClosest(canidPosition, positionList):
        lowestDist = None
        counter = 0
        arrayPosition = -1
        for position in positionList:
            if lowestDist is None or lowestDist > np.linalg.norm(position-canidPosition):
                distVector = np.array(position-canidPosition)
                lowestDist = np.linalg.norm(distVector)
                arrayPosition = counter
                distVector = unitVector(distVector)
            counter += 1
        return [distVector, lowestDist, arrayPosition]

def find_items(enclosure, item_id):
    item_locations = []
    for i, row in enumerate(enclosure):  # loop through rows (meters in height)
        for j, value in enumerate(row):  # loop through columns (meters in width)
            if value == item_id:  # Check if the item is present
                item_locations.append(np.array((j, i)))
    return item_locations

def exists(enclosure, item_id):# inputs thing and checks that thing
    for i, row in enumerate(enclosure):  # loop through rows (meters in height)
        for j, value in enumerate(row):  # loop through columns (meters in width)
            if value == item_id:  # Check if the item is present
                return True
    return False

def createFoxAgents(numFoxes, numFamilies, startingPositions):
    foxAgents = []
    for i in range(numFoxes):
        foxAgents.append(Fox(i+1, rd.randint(1,numFamilies), rd.uniform(1,5), rd.uniform(35,55), startingPositions[i][0], startingPositions[i][1], [0,0]))
        

def find_den(Den3, num):
    """Searches the enclosure (container) for a specific item (num) and returns their coordinates (1-based)."""
    den_locations = find_items(Den3, num)
    return den_locations
    

 # Find item locations (example: finding food with ID 6)
 # Change this to search for different items
#found_den = find_den(Den3, num)

#-------------------------------------------------------------------------------------------------------------------------------

def distance(coord1, coord2):
    # Calculate the Euclidean distance between two coordinates
    dist = math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
    return dist

def find_den_locations(enclosure, den_id, radius=2):
    found_den = find_den(enclosure[3], den_id)
    found_trees = find_items(enclosure[0], 1)
    unique_coordinates = []

    
    if not found_den:
        print("No dens found to compare.")
        return found_trees  # If there are no dens, all tree coordinates are unique

    for coord in found_trees:
        too_close = False
        # Check the distance between the coordinate from found_den and each coordinate from found_trees
        for coord2 in found_den:
            dist = distance(coord, coord2)
            if dist <= radius:  # If the distance is within the radius, don't add the coord from found_trees
                too_close = True
                break

        # Add the coordinate from found_trees to the result only if it's not too close to any den
        if not too_close:
            unique_coordinates.append(coord)

    return unique_coordinates
            
#magn = np.linalg.norm(arr)
#print(rd.uniform(1,5))
#print(math.cos(math.radians(90)))
#for foxAgent in fox:
    #print(foxAgent)
#for fox in foxAgents:
    #print(fox.fox_id, " ", fox.pos, " ", fox.direction)
    #fox.move(foxAgents)
    #print(fox.fox_id, " ", fox.pos)
# while(True):
#     print(foxAgents[0].pos, " ", foxAgents[0].direction)
#     for fox in foxAgents:
#         fox.move(foxAgents)
#     sleep(1)
