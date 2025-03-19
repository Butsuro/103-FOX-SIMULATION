import Fox_Class
import Masterarray as MA 
import FoodSpawn as FS 

import Fox_Class

def moveFOX_pretrap(foxAgentList, masterArray, enclosure_time):
     counter = 0
     max_time =  enclosure_time * 86400
     while(counter < max_time):
         counter += 1
         if counter % 86400 == 0:
             return 0
         else:
            for fox in foxAgentList: 
                fox.move(masterArray)