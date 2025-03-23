import Fox_Class
import Masterarray as MA 
import FoodSpawn as FS 
import FoxTracking as FT
import json
import Fox_Class as F_CLASS

#importing from data file
with open("data.json", "r") as file:
    user_input = json.load(file)

enclosure_num = user_input["chosenEnclosure"]
enclosure_time = user_input["days"]
num_each_fam = user_input["canidsPerFamily"]

# these are things we can adjust
num_canids = 0
for family in num_each_fam:
    num_canids += family 

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
def fox_spawn():
    fox_count = 0
    family_count = 0
    for family in num_each_fam:
        family_count += 1
        for count in range(family):
            fox_count += 1
            foxAgentList.append(F_CLASS.Fox(fox_id= count +1, family= family_count, pos= spawn_pos[count], direction= [0, 0]))
            Master_array[1][spawn_pos[count][0]][spawn_pos[count][1]] = count +1


# Actual sim
fox_spawn()

counter = 0
max_time =  enclosure_time * 86400
while(counter < max_time):
    counter += 1
    if counter % 86400 == 0:
        Master_array = FS.spawnitems(Master_array, Food_per_turn, 4, 7)
    else:
        for fox in foxAgentList: 
            Master_array = fox.move(Master_array, foxAgentList)

#trap locations picker
            
locations = FT.findLargest(Master_array[2], num_traps, width, height)

for spot in locations:
    Master_array[2][spot[1]][spot[0]] = 1

counter = 0
final_len = len(foxAgentList) - 8
while(len(foxAgentList) > final_len):
    for fox in foxAgentList:
        Master_array = fox.move(Master_array, foxAgentList)
        if fox.pos in locations:
            Master_array[1][fox.pos[1]][fox.pos[0]] = 0
            locations.remove(fox)


results = {
    "chosenEnclosure": enclosure_num,
    "Array": Master_array,
    "Trap_locations": locations 
}

with open("data.json", "w") as file:
    json.dump(results, file, indent = 4)