import Fox_Class
import Masterarray as MA 
import FoodSpawn as FS 

import Fox_Class as F_CLASS

#everything here is values which should be derrived from input
enclosure_num = 1
enclosure_time = 5
num_each_fam = [3, 7, 3]

# these are things we can adjust
Food_per_turn= 13

#Master array declaration
height = 0
width = 0
def pick_array(encolusure_num):
    if encolusure_num == 1:
        height = 20*3
        width = 12*3
        return MA.Master1
    if encolusure_num == 2:
        height = 16*3
        width = 12*3
        return MA.Master2
    else:
        height = 13*3
        width = 12*3
        return MA.Master3
Master_array = pick_array(enclosure_num)

##FOX spawn
foxAgentList = []
spawn_pos = FS.generate_spawn_points(1, height, width, Master_array[0])
def fox_spawn():
    fox_count = 0
    family_count = 0
    for family in num_each_fam:
        family_count += 1
        for count in range(family):
            fox_count += 1
            foxAgentList.append(F_CLASS.Fox(fox_id= fox_count, family= family_count, pos= spawn_pos[fox_count-1], direction= [0, 0]))
            Master_array[1][spawn_pos[fox_count-1][1]][spawn_pos[fox_count-1][0]] = fox_count


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
            
locations = []
