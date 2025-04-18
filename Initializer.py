import Fox_Class
import Masterarray as MA 
import FoodSpawn as FS 
import FoxTracking as FT
import json
import Fox_Class as F_CLASS
import numpy as np
from tqdm import tqdm
import Path_finder as pf

#importing from data file
with open(pf.resource_path("data.json"), "r") as file:
    user_input = json.load(file)

enclosure_num = user_input["chosenEnclosure"]
enclosure_time = user_input["days"]
num_each_fam = user_input["canidsPerFamily"]
Chosen_Canid = user_input["chosenCanid"]
skip_trap_sim = user_input["skip_trap"]

if Chosen_Canid == "Foxes":
    Is_fox = True
    cycle_multiplier = 86400
else:
    Is_fox = False
    cycle_multiplier = 34560

num_canids = 0
for family in num_each_fam:
    num_canids += family 

#things we can adjust
num_traps = num_canids
Food_per_turn= num_canids
break_after_one = False

#Master array declaration
height = 0
width = 36
def pick_array(encolusure_num):
    if encolusure_num == 1:
        height = 20*3
        return MA.Master1, height
    if encolusure_num == 2:
        height = 16*3
        return MA.Master2, height
    else:
        height = 13*3
        return MA.Master3, height
Master_array, height = pick_array(enclosure_num)

##FOX spawn
CanidAgentList = []
spawn_pos = FS.generate_spawn_points(num_canids, height, width, Master_array[0])
print(spawn_pos)
def fox_spawn():
    fox_count = 0
    family_count = 0
    for family in num_each_fam:
        family_count += 1
        for count in range(family):
            fox_count += 1
            CanidAgentList.append(F_CLASS.Fox(fox_id= fox_count, family= family_count, pos= spawn_pos[fox_count - 1], direction= [0, 0], family_size= family))
            Master_array[1][spawn_pos[fox_count - 1][0]][spawn_pos[fox_count - 1][1]] = fox_count

def Cayote_spawn():
    fox_count = 0
    family_count = 0
    for family in num_each_fam:
        family_count += 1
        for count in range(family):
            fox_count += 1
            CanidAgentList.append(F_CLASS.Cayote(fox_id= fox_count, family= family_count, pos= spawn_pos[fox_count - 1], direction= [0, 0], family_size= family))
            Master_array[1][spawn_pos[fox_count - 1][0]][spawn_pos[fox_count - 1][1]] = fox_count

# Actual sim
if Is_fox:
    fox_spawn()
    print("foxes spawned")

else:
    Cayote_spawn()
    print("cayotes spawned")

counter = 0
max_time =  enclosure_time * cycle_multiplier
print("starting simulation")
with tqdm(total=max_time, desc="Simulating Enclosure Time", unit="cycles", dynamic_ncols=True) as pbar:
    while(counter < max_time):
        counter += 1
        pbar.update(1)
        if counter-1 % cycle_multiplier == 0:
            Master_array = FS.spawnitems(Master_array, Food_per_turn, 4, 7)
        else:
            for Canid in CanidAgentList: 
                Master_array = Canid.move(Master_array, CanidAgentList)

print("main sim complete")


print("picking traps")      
locations = FT.findLargest(Master_array[2], num_traps, width, height)

for spot in locations:
    Master_array[5][spot[1]][spot[0]] = 1
print("traps placed")
counter = 0
final_len = len(CanidAgentList) - num_traps
trap_info = []
if not skip_trap_sim:
    print("starting capture sim")
    with tqdm(total=final_len, desc="Simulating Capture Time", unit=" Foxes caught", ncols=200, position=0, leave=False) as pbar:
        while(len(CanidAgentList) > final_len):
            counter += 1
            if counter-1 % cycle_multiplier == 0:
                Master_array = FS.spawnitems(Master_array, Food_per_turn, 4, 7)
            else:
                for Canid in CanidAgentList:
                    Master_array = Canid.move(Master_array, CanidAgentList)
                    if (Master_array[5][round(Canid.pos[0])][round(Canid.pos[1])] != 0):
                        Master_array[1][round(Canid.pos[0])][round(Canid.pos[1])] = 0
                        for homie in CanidAgentList:
                            if (Canid.family == homie.family):
                                homie.family_count = homie.family_size -1
                        CanidAgentList.remove(Canid)
                        print(f"trap at ({round(Canid.pos[1])}, {round(Canid.pos[0])}) (x,y) took {counter/cycle_multiplier * 24} hours to capture the canids")
                        trap_info.append(f"trap at ({round(Canid.pos[1])}, {round(Canid.pos[0])}) (x,y) took {(counter/cycle_multiplier * 24):.1f} hours")
                        if break_after_one:
                            break
                        pbar.update(1)
                    else:
                        Master_array = Canid.move(Master_array, CanidAgentList)
    print("capture sim complete")
    print("total time taken to capture is:") 
    print(f"{counter/cycle_multiplier} days")

else:
    trap_info = ["Trap Simulation was skipped"]

print("sending results")
results = {
    "chosenEnclosure": enclosure_num,
    "heatmap": Master_array[2].tolist(),
    "Trap_locations": locations,
    "Trap_info": trap_info
}

with open(pf.resource_path("simoutput.json"), "w") as file:
    json.dump(results, file, indent = 4)

print("results sent")
