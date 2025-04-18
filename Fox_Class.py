import numpy as np
import random as rd
import math
import Masterarray as MA
food_id = 6
random_id = 13

class Fox:
    def __init__(self, fox_id, family,pos, direction, family_size):
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
        self.family_size = family_size
        self.pos = np.array(pos)
        self.direction = unitVector(np.array(direction))
    
    def canidList(self, foxAgentList):
        foxPositionList = []
        for fox in foxAgentList:
            if fox.fox_id != self.fox_id: 
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
        distVector = None
        arrayPosition = None
        for fox in foxPositionList:
            if (lowestDist is None or lowestDist >= np.linalg.norm(fox[0]-self.pos)) and self.family == fox[1]:
                distVector = np.array(fox[0]-self.pos)
                lowestDist = np.linalg.norm(distVector)
                arrayPosition = fox[0]
                distVector = unitVector(distVector)
        if distVector is None or arrayPosition is None:
        # Handle the case when no valid fox is found (you can return a default or raise an error)
            return [None, None, None]
            
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
        masterArray[3][round(self.pos[1])][round(self.pos[0])] = self.family
    
    #(np.array_equal(new_pos, fox.pos) and self.fox_id != fox.fox_id for fox in AgentList) 
    def move(self, masterArray, AgentList):
        brain_output = self.BrainFOX(masterArray, AgentList)
        asleep = False
        if str(brain_output) == "sleeping":
            brain_output = [0, 0]
            asleep = True
        self.direction = np.array(brain_output)
        
        if self.direction is None:
            valuex = rd.randint(-1, 1)
            valuey = rd.randint(-1, 1)
            self.direction = [valuex, valuey]

        new_pos = np.round(self.pos+self.direction)
        
        
        if masterArray[0][round(new_pos[0])][round(new_pos[1])] == 4 or masterArray[0][round(new_pos[0])][round(new_pos[1])]  == 0:
            new_pos = self.pos
        if masterArray[1][round(new_pos[0])][round(new_pos[1])] != 0:
            new_pos = self.pos

        masterArray[1][round(self.pos[0])][round(self.pos[1])] = 0
        self.pos = new_pos
        if np.isnan(self.pos[0]) or np.isnan(self.pos[1]):
            raise ValueError(f"Invalid position detected: {self.pos}") 
        
        masterArray[1][round(self.pos[0])][round(self.pos[1])] = self.fox_id
        if not asleep:
            masterArray[2][round(self.pos[0])][round(self.pos[1])] += 1
        return masterArray

    
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
        self.GOtoDEN += 1/43200
        self.GoToFreind += 1/20000
        self.sleep_need += 1/50400
            

        if Denning >= 1:
            if DenQuantReached(self.family, array[3]):
                self.Denning = 0
            denLocations = find_den_locations(array, radius= 2)
            closestDen = findClosest(self.pos, denLocations)
            if denLocations[closestDen[2]][0] == round(self.pos[0]) and denLocations[closestDen[2]][1] == round(self.pos[1]):
                self.makeDen(array)
                return [0, 0]
            else:
                return closestDen[0]
        if den_timer >= 1:
            self.den_timer = den_timer - (1/900)
            return [0, 0]
        if sleep_timer > 0:
            self.sleep_need = 0
            self.GOtoDEN = 0
            self.sleep_timer = sleep_timer - (1/36000)
            return "sleeping"
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
        if GoToFreind >= 1 and self.family_size > 1:
            # print("Freind Triggered")
            closestFriend = self.closestCanidFriend(foxAgentList)
            if closestFriend[1] == None:
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]
            if closestFriend[1] <= 1.5:
                # print("closest freind in radius")
                self.FamilyTime = 1 
                self.GoToFreind = 0.0
                return [0,0] #changed from return self.moveTo(array, family_id)
            else:
                return closestFriend[0]
        if FamilyTime > 0:
            self.GoToFreind = 0.0
            self.FamilyTime = FamilyTime - (1/10)
            closestFriend = self.closestCanidFriend(foxAgentList)
            return closestFriend[0]
        
        else:
            
            option = weighted_random_choice(hunger, sleep_need, GOtoDEN, GoToFreind, randomness)

            if option == "Hunger":
                self.hunger = 1
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]


            if option == "Sleep Need":
                self.sleep_need = 0
                self.sleep_timer = 1
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]
      
            if option == "Go to Den":
                self.GOtoDEN = 1
                return self.moveTo(array[3], denplus_id)
       
            if option == "Go to Friend" and self.family_size > 1:
                self.GoToFreind = 1
                closestFriend = self.closestCanidFriend(foxAgentList)
                return closestFriend[0]
      
            else:
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]
    
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

def DenQuantReached(family_num ,array):
    count = 0
    for row in array:
        for num in row:
            if num == family_num:
                count += 1
    if count >= 3:
        return True
    else:
        return False
        
def unitVector(vector):
    vector = np.array(vector, dtype=np.float64)  # Ensure it's a NumPy array
    magnitude = np.linalg.norm(vector)

    if magnitude == 0:  # Prevent division by zero
        return np.zeros_like(vector) 
    
    return vector / magnitude 

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
        

def find_dens(enclosure):
    den_locations = []
    for i, row in enumerate(enclosure):  # loop through rows (meters in height)
        for j, value in enumerate(row):  # loop through columns (meters in width)
            if value != 0:  # Check if the item is present
                den_locations.append(np.array((j, i)))
    return den_locations
    

 # Find item locations (example: finding food with ID 6)
 # Change this to search for different items
#found_den = find_den(Den3, num)

#-------------------------------------------------------------------------------------------------------------------------------

def distance(coord1, coord2):
    # Calculate the Euclidean distance between two coordinates
    dist = math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
    return dist

def find_den_locations(enclosure, radius=2):
    found_den = find_dens(enclosure[3])
    found_trees = find_items(enclosure[0], 1)
    unique_coordinates = []

    
    if not found_den:
        # print("No dens found to compare.")
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
            
class Cayote:
    def __init__(self, fox_id, family,pos, direction, family_size):
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
        self.family_size = family_size
        self.pos = np.array(pos)
        self.direction = unitVector(np.array(direction))
    
    def canidList(self, foxAgentList):
        foxPositionList = []
        for fox in foxAgentList:
            if fox.fox_id != self.fox_id: 
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
        distVector = None
        arrayPosition = None
        for fox in foxPositionList:
            if (lowestDist is None or lowestDist >= np.linalg.norm(fox[0]-self.pos)) and self.family == fox[1]:
                distVector = np.array(fox[0]-self.pos)
                lowestDist = np.linalg.norm(distVector)
                arrayPosition = fox[0]
                distVector = unitVector(distVector)
        if distVector is None or arrayPosition is None:
        # Handle the case when no valid fox is found (you can return a default or raise an error)
            return [None, None, None]
            
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
        masterArray[3][round(self.pos[1])][round(self.pos[0])] = self.family
    
    def move(self, masterArray, AgentList):
        brain_output = self.BrainCayote(masterArray, AgentList)
        asleep = False
        if str(brain_output) == "sleeping":
            brain_output = [0, 0]
            asleep = True
        self.direction = np.array(brain_output)

        if self.direction is None:
            valuex = rd.randint(-1, 1)
            valuey = rd.randint(-1, 1)
            self.direction = [valuex, valuey]
        
        new_pos = np.round(self.pos+self.direction)
        
        
        if masterArray[0][round(new_pos[0])][round(new_pos[1])] == 4 or masterArray[0][round(new_pos[0])][round(new_pos[1])]  == 0:
            new_pos = self.pos
        if masterArray[1][round(new_pos[0])][round(new_pos[1])] != 0:
            new_pos = self.pos

        masterArray[1][round(self.pos[0])][round(self.pos[1])] = 0
        self.pos = new_pos
        if np.isnan(self.pos[0]) or np.isnan(self.pos[1]):
            raise ValueError(f"Invalid position detected: {self.pos}") 
        
        masterArray[1][round(self.pos[0])][round(self.pos[1])] = self.fox_id
        if not asleep:
            masterArray[2][round(self.pos[0])][round(self.pos[1])] += 1
        return masterArray

    
    def BrainCayote(self, array, foxAgentList):
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

        self.hunger += 1/34560
        self.GoToFreind += 1/10000
        self.sleep_need += 1/17280
            


        if sleep_timer > 0:
            self.sleep_need = 0
            self.sleep_timer = sleep_timer - (1/17280)
            return "sleeping"
        if hunger >= 1 and exists(array[4], food_id):
            if self.atAThing(array[4], food_id):
                self.hunger = 0
                self.GOtoDEN = 1
                return self.moveTo(array[3], denplus_id)
            else:
                return self.moveTo(array[4], food_id)
        if sleep_need >= 1:
            self.sleep_timer = 1
            return [0,0]
        if GoToFreind >= 1 and self.family_size > 1:
            # print("Freind Triggered")
            closestFriend = self.closestCanidFriend(foxAgentList)
            if closestFriend[1] == None:
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]
            if closestFriend[1] <= 1.5:
                # print("closest freind in radius")
                self.FamilyTime = 1 
                self.GoToFreind = 0.0
                return [0,0] #changed from return self.moveTo(array, family_id)
            else:
                return closestFriend[0]
        if FamilyTime > 0:
            self.GoToFreind = 0.0
            self.FamilyTime = FamilyTime - (1/10)
            closestFriend = self.closestCanidFriend(foxAgentList)
            return closestFriend[0]
        
        else:
            
            option = weighted_random_choice(hunger, sleep_need, GOtoDEN, GoToFreind, randomness)

            if option == "Hunger":
                self.hunger = 1
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]


            if option == "Sleep Need":
                self.sleep_need = 0
                self.sleep_timer = 1
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]
       
            if option == "Go to Friend" and self.family_size > 1:
                self.GoToFreind = 1
                closestFriend = self.closestCanidFriend(foxAgentList)
                return closestFriend[0]
      
            else:
                valuex = rd.randint(-1, 1)
                valuey = rd.randint(-1, 1)
                return [valuex, valuey]
