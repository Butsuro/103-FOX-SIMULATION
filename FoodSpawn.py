import Masterarray as MA 
import random as rd
import numpy as np 
def spawnitems(array_3d, num_items, layer, item_type):
 
    valid_positions = [(i, j) for i in range(array_3d.shape[1]) 
                   for j in range(array_3d.shape[2]) 
                   if (array_3d[0][i][j] not in {0, 4, 7}) and (array_3d[layer][i][j] == 0)]
     
    if len(valid_positions) < num_items:
        return
     
    else:
        selected_spots = rd.sample(valid_positions, num_items)
 
        for i,j in selected_spots:
            array_3d[layer][i][j] = item_type
        
        return array_3d
    
def generate_spawn_points(num_foxes, grid_height, grid_width, restriction_array):
    spawn_points = set()  # Store unique (y, x) spawn locations

    while len(spawn_points) < num_foxes:
        y = rd.randint(0, grid_height - 1)
        x = rd.randint(0, grid_width - 1)

        # Ensure the position is valid and not already taken
        if (y, x) not in spawn_points and restriction_array[y][x] not in [0, 4]:
            spawn_points.add((y, x))

    return list(spawn_points)