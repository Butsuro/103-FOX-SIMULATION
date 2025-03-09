import random


def generate_enclosure(rows=12, cols=20, food_count=10):  
    """Creates a 12x20 enclosure where each 0 represents a meter. Places food (6) randomly."""
    enclosure = [[0 for _ in range(cols)] for _ in range(rows)]  
    food_positions = set()

    # Place food items randomly
    while len(food_positions) < food_count:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)  # Random coordinates
        if (x, y) not in food_positions:  
            enclosure[x][y] = 6  # Place food
            food_positions.add((x, y))

    return enclosure, list(food_positions)

#------------------------------ACTUAL FUNCTION TO SEARCH--------------------------------

# Function to Find something (not nessesarily food
def find_food(enclosure):
    """Searches the enclosure for food (6) and returns their coordinates (1-based)."""
    food_locations = []
    for i, row in enumerate(enclosure):  # Loop through rows (meters in height)
        for j, value in enumerate(row):  # Loop through columns (meters in width)
            if value == 6:  # Check if food is present
                food_locations.append((i + 1, j + 1))  # Convert to 1-based indexing

    return food_locations


# Generate enclosure
enclosure, food_positions = generate_enclosure()

# Find food locations
found_food = find_food(enclosure)

# Display results
print("Enclosure Map (Each 0 represents 1 meter):")
for row in enclosure:
    print(" ".join(map(str, row)))
print("\nFood Locations (Coordinates in meters, 1-based index):")
print(found_food)
