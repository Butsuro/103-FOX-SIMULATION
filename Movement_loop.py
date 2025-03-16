import Fox_Class

def moveFOX_pretrap(foxAgentList, masterArray, enclosure_time):
     counter = 0
     max_time =  enclosure_time * 86400
     while(counter < max_time):
         counter += 1
         for fox in foxAgentList: 
             fox.move(masterArray)