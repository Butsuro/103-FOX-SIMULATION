import Fox_Class
import Masterarray as MA 
import FoodSpawn as FS 
import FoxTracking as FT
import json
import Fox_Class as F_CLASS
import numpy as np

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
            foxAgentList.append(F_CLASS.Fox(fox_id= fox_count, family= family_count, pos= spawn_pos[fox_count - 1], direction= [0, 0]))
            Master_array[1][spawn_pos[fox_count - 1][0]][spawn_pos[fox_count - 1][1]] = fox_count


# Actual sim
fox_spawn()

MA.print_large_2d_array(Master_array[1])

counter = 0
max_time =  enclosure_time * 86400
while(counter < max_time):
    counter += 1
    if counter % 86400 == 0:
        Master_array = FS.spawnitems(Master_array, Food_per_turn, 4, 7)
    else:
        for fox in foxAgentList: 
            Master_array = fox.move(Master_array, foxAgentList)

print("main sim complete")
#trap locations picker
            
locations = FT.findLargest(Master_array[2], num_traps, width, height)

for spot in locations:
    Master_array[2][spot[1]][spot[0]] = 1

counter = 0
final_len = len(foxAgentList) - num_traps
while(len(foxAgentList) > final_len):
    for fox in foxAgentList:
        Master_array = fox.move(Master_array, foxAgentList)
        if (np.array_equal(fox.pos, loc) for loc in locations):
            Master_array[1][round(fox.pos[1])][round(fox.pos[0])] = 0
            foxAgentList.remove(fox)
        else:
            Master_array = fox.move(Master_array, foxAgentList)



results = {
    "chosenEnclosure": enclosure_num,
    "Array": Master_array,
    "Trap_locations": locations 
}

with open("data.json", "w") as file:
    json.dump(results, file, indent = 4)