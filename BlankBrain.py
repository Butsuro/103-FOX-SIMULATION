import random
import Masterarray as MA



def turn(Level_sleep, Level_hunger):
   Level_sleep = Level_sleep + 0.2
   Level_hunger = Level_hunger + 0.2


def DenQuantReached(family_num, array):
   count = 0
   for row in array[0]:
       for num in row:
           if num == family_num:
               count += 1
  
   if count >= 3:
       return True
   else:
       return False


#moves fox towards a thing then does the action if they are the same location as the thing
def moveto(thing, fox):
   return 1


def atathing(thing, fox):
   return 1


def exists(thing):
   return 1


def weighted_random_choice(a, b, c, d, e, f, g):
   # Define options and their dynamic weights
   options = ["Hunger", "Sleep Need", "Sleep Timer", "Denning", "Go to Den", "Go to Friend", "Randomness"]
   weights = [a, b, c, d, e, f, g]  # These values change each time the function runs


   # Normalize weights (only if they don't sum to 1, but not strictly necessary)
   total_weight = sum(weights)
   if total_weight > 0:
       normalized_weights = [w / total_weight for w in weights]
   else:
       normalized_weights = weights  # Avoid division by zero (all weights are 0)


   # Select a random option based on the weights
   selected_option = random.choices(options, weights=normalized_weights, k=1)[0]


   return selected_option


def BrainFOX(self, array):
   hunger = 0
   sleep_need = 0
   sleep_timer = 0
   Denning = 1
   GOtoDEN = 0
   GoToFreind = 0.3
   FamilyTime = 0
   randomness = 0.1 
   den_timer = 0

   if Denning >= 1:
       if DenQuantReached(self.family, array):
           Denning = 0
       if atathing("den", self):
           den_timer = 1
           array[3][self.pos[0]][self.pos[1]] = self.family
           return [0, 0]
       else:
           return moveto("den", self)
   if den_timer >= 1:
       if DenQuantReached(self.family, array):
           den_timer = 0
       else:
           den_timer = den_timer - (1/1200)
   if sleep_timer > 0:
       sleep_timer = sleep_timer - (1/36000)
       return [0,0]
   if hunger >= 1 and exists("food"):
       if atathing("food", self):
           hunger = 0
           GOtoDEN = 1
           return moveto("den", self)
       else:
           return moveto("food", self)
   if GOtoDEN >= 1:
       if atathing("den+", self):
           GOtoDEN = 0
           return moveto("den+", self)
       else:
           return moveto("den+", self)
   if sleep_need >= 1:
       if atathing("den+", self):
           sleep_timer =1
           return [0, 0]
       else:
           GOtoDEN = 1
           return moveto("den+", self)
   if GoToFreind >= 1:
       if atathing("family", self):
            FamilyTime = 1
            GoToFreind = 0.3
            return moveto("family", self)
       else:
           return moveto("family", self)
   if FamilyTime > 0:
        FamilyTime = FamilyTime - (1/7200)
        return moveto("family", self)
       
   else:
       option = weighted_random_choice(hunger, sleep_need, sleep_timer, Denning, GOtoDEN, GoToFreind, randomness)

       if option == "Hunger":
           hunger = 1
           return [0, 0]


       if option == "Sleep Need":
           sleep_need = 0
           sleep_timer = 1
           return [0, 0]
      
       if option == "Go to Den":
           GOtoDEN = 1
           return moveto("den+", self)
       
       if option == "Go to Friend":
           GoToFreind = 1
           return moveto("freind", self)
      
       else:
           return moveto ("random", self)