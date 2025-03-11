import random

# Define ID for what number is what item
valid_ids = {0: "empty", 1: "tree", 2: "grass", 3: "dirt", 4: "fence", 5: "hut", 6: "food"}


def generate_enclosure(rows=36, cols=60, food_count=10):
    """Creates a 12x20 enclosure where each 0 represents a meter. Places food (6) randomly."""
    enclosure = [[0 for _ in range(cols)] for _ in range(rows)]  # Create a grid of zeros (empty meters)
    food_positions = set()

    # Place food items randomly
    while len(food_positions) < food_count:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)  # Random coordinates
        if (x, y) not in food_positions:  # unique food placement
            enclosure[x][y] = 6  # Place food
            food_positions.add((x, y))

    return enclosure



#-------------------------------------THE ACTUAL FUNCTION-----------------------------------------------------------------------------------------------------------------------------------------

def find_items(enclosure, num):
    """Searches the enclosure (container) for a specific item (num) and returns their coordinates (0-based)."""
    item_locations = []

    if num not in valid_ids:
        return []  # return empty list if num is not a known ID

    for i, row in enumerate(enclosure):  # loop through rows (meters in height)
        for j, value in enumerate(row):  # loop through columns (meters in width)
            if value == num:  # Check if the item is present
                item_locations.append((i, j))  # Keep 0-based indexing

    return item_locations

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Generate enclosure
enclosure = generate_enclosure()

# Find item locations (example: finding food with ID 6)
num = 6  # Change this to search for different items
found_items = find_items(enclosure, num)

# Display results
print("Enclosure Map (Each 0 represents 1 meter):")
for row in enclosure:
    print(" ".join(map(str, row)))

print(f"\nLocations of {num} ({valid_ids.get(num, 'Unknown')}):")
print(found_items)
