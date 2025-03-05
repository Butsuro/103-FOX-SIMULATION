import envmap as EM
import numpy as np

Master1 = np.zeros((4, 20, 12))
Master2 = np.zeros((4, 16, 12))
Master3 = np.zeros((4, 13, 12))

Master1[0] = EM.Container1
Master2[0] = EM.Container2
Master3[0] = EM.container3


# # Loop through and print each 2D slice (top level)
# for i, level in enumerate(Master1):
#     print(f"Slice {i+1}:")
#     for row in level:
#         print(row)
#     print() 

