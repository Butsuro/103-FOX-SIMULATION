import math
import matplotlib.pyplot as plt

# Function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

# Function to find closest food
def closest_food(fox_position, food_positions):
    return min(food_positions, key=lambda food: calculate_distance(*fox_position, *food))

# Example usage
fox_position = (0, 0)
food_positions = [(1, 5), (3, 4), (2, 2)]

closest_food_position = closest_food(fox_position, food_positions)
min_distance = calculate_distance(*fox_position, *closest_food_position)
print(f"Closest food: {closest_food_position} at {min_distance} meters.")

#----------------------------------------------------------------------------------------------------------------------#
# Plotting
plt.figure(figsize=(6, 6))
food_scatter = [plt.scatter(*food, color='blue') for food in food_positions]
fox_scatter = plt.scatter(*fox_position, color='red', s=100)

# Add labels
plt.text(fox_position[0], fox_position[1], 'Fox', color='red', fontsize=12, verticalalignment='bottom')
for food in food_positions:
    plt.text(food[0], food[1], f'{food}', color='blue', fontsize=12, verticalalignment='bottom')

# Set labels and display
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Fox and Food Positions')
plt.grid(True)

# Manually creating the legend with specific handles and labels
plt.legend([fox_scatter] + food_scatter, ['Fox'] + ['Food'])

plt.show()
