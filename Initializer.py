import Fox_Class
import Masterarray as MA 
import FoodSpawn as FS 
import FoxTracking as FT
import json
import Fox_Class as F_CLASS
import numpy as np
from tqdm import tqdm

#importing from data file
with open("data.json", "r") as file:
    user_input = json.load(file)

enclosure_num = user_input["chosenEnclosure"]
enclosure_time = user_input["days"]
num_each_fam = user_input["canidsPerFamily"]


num_canids = 0
for family in num_each_fam:
    num_canids += family 

#things we can adjust
num_traps = 4
Food_per_turn= num_canids
num_traps = 6

#Master array declaration
height = 0
width = 36
def pick_array(encolusure_num):
    if encolusure_num == 1:
        height = 20*3
        return MA.Master1, height
    if encolusure_num == 2:
        height = 16*3, height
        return MA.Master2
    else:
        height = 13*3
        return MA.Master3, height
Master_array, height = pick_array(enclosure_num)

##FOX spawn
foxAgentList = []
spawn_pos = FS.generate_spawn_points(num_canids, height, width, Master_array[0])
print(spawn_pos)
def fox_spawn():
    fox_count = 0
    family_count = 0
    for family in num_each_fam:
        family_count += 1
        for count in range(family):
            fox_count += 1
            foxAgentList.append(F_CLASS.Fox(fox_id= fox_count, family= family_count, pos= spawn_pos[fox_count - 1], direction= [0, 0], family_size= family))
            Master_array[1][spawn_pos[fox_count - 1][0]][spawn_pos[fox_count - 1][1]] = fox_count


# Actual sim
fox_spawn()

print("foxes spawned")
# MA.print_large_2d_array(Master_array[1])

counter = 0
max_time =  enclosure_time * 86400
print("starting simulation")
with tqdm(total=max_time, desc="Simulating Enclosure Time", unit="cycles", dynamic_ncols=True) as pbar:
    while(counter < max_time):
        counter += 1
        pbar.update(1)
        if counter-1 % 86400 == 0:
            Master_array = FS.spawnitems(Master_array, Food_per_turn, 4, 7)
        else:
            for fox in foxAgentList: 
                Master_array = fox.move(Master_array, foxAgentList)

print("main sim complete")

# MA.print_large_2d_array(Master_array[3])

#trap locations picker

print("picking traps")      
locations = FT.findLargest(Master_array[2], num_traps, width, height)

results = {
    "chosenEnclosure": enclosure_num,
    "heatmap": Master_array[2].tolist(),
    "Trap_locations": locations
}
with open("simoutput.json", "w") as file:
    json.dump(results, file, indent = 4)

for spot in locations:
    Master_array[5][spot[1]][spot[0]] = 1
print("traps placed")
counter = 0
final_len = len(foxAgentList) - num_traps
print("starting capture sim")
with tqdm(total=final_len, desc="Simulating Capture Time",  unit="Foxes caught", ncols= 200, position=0, leave=True) as pbar:
    while(len(foxAgentList) > final_len):
        for fox in foxAgentList:
            counter += 1
            Master_array = fox.move(Master_array, foxAgentList)
            if (np.array_equal(fox.pos, loc) for loc in locations):
                Master_array[1][round(fox.pos[0])][round(fox.pos[1])] = 0
                for homie in foxAgentList:
                    if (fox.family_id == homie.family_id):
                        homie.family_count = homie.family_count -1
                foxAgentList.remove(fox)
                pbar.update(1)
            if counter-1 % 86400 == 0:
                Master_array = FS.spawnitems(Master_array, Food_per_turn, 4, 7)
            else:
                Master_array = fox.move(Master_array, foxAgentList)
print("capture sim complete")
print("total time taken is:") 
print(counter/86400)


print("sending results")
results = {
    "chosenEnclosure": enclosure_num,
    "heatmap": Master_array[2].tolist(),
    "Trap_locations": locations
}

with open("simoutput.json", "w") as file:
    json.dump(results, file, indent = 4)

print("results sent")