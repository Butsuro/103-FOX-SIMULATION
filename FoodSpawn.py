import Masterarray as MA 
import random
import numpy as np

def spawnitems(array_3d, num_items, layer, item_type):

    valid_positions = [(i, j) for i in range(array_3d.shape[1]) 
                   for j in range(array_3d.shape[2]) 
                   if array_3d[0][i][j] not in {0, 4, 7}]
    
    if len(valid_positions) < num_items:
        return
    
    else:
        selected_spots = random.sample(valid_positions, num_items)

        for i,j in selected_spots:
            array_3d[layer][i][j] = item_type
    
    print(f"Modified Layer {layer}:\n", array_3d[layer])

spawnitems(MA.Master1, 5, 2, 7)
    