import envmap as EM
import numpy as np

# 1 [0] -> Enviorement
# 2 [1] -> Fox Positions
# 3 [2] -> Tracking Layer
# 4 [3] -> Dens
# 5 [4] -> Food
# 6 [5] -> traps

Master1 = np.zeros((6, (20*3), (12*3)))
Master2 = np.zeros((6, (16*3), (12*3)))
Master3 = np.zeros((6, (13*3), (12*3)))

Master1[0] = EM.Container1
Master2[0] = EM.Container2
Master3[0] = EM.container3


# # Loop through and print each 2D slice (top level)
# for i, level in enumerate(Master1):
#     print(f"Slice {i+1}:")
#     for row in level:
#         print(row)
#     print() 