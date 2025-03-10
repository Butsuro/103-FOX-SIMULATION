import random
import Masterarray as MA

def turn(Level_sleep, Level_hunger):
    Level_sleep = Level_sleep + 0.2
    Level_hunger = Level_hunger + 0.2

def DenQuantReached(family_num, array):
    count = 0
    for row in array[0]:
        for num in row:
            if num == family_num:
                count += 1
    
    if count >= 3:
        return True
    else:
        return False


def BrainMove():
    hunger = 1
    sleep = 1
    Denning = 1