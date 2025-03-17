def find_den(Den3, num):
    """Searches the enclosure (container) for a specific item (num) and returns their coordinates (1-based)."""
    den_locations = find_items(Den3, num)
    return den_locations
    

 # Find item locations (example: finding food with ID 6)
 # Change this to search for different items
#found_den = find_den(Den3, num)

#-------------------------------------------------------------------------------------------------------------------------------

def distance(coord1, coord2):
    # Calculate the Euclidean distance between two coordinates
    dist = math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
    return dist

def find_den_locations(enclosure, den_id, radius=2):
    found_den = find_den(enclosure[3], den_id)
    found_trees = find_items(enclosure[0], 1)
    unique_coordinates = []

    
    if not found_den:
        print("No dens found to compare.")
        return found_trees  # If there are no dens, all tree coordinates are unique

    for coord in found_trees:
        too_close = False
        # Check the distance between the coordinate from found_den and each coordinate from found_trees
        for coord2 in found_den:
            dist = distance(coord, coord2)
            if dist <= radius:  # If the distance is within the radius, don't add the coord from found_trees
                too_close = True
                break

        # Add the coordinate from found_trees to the result only if it's not too close to any den
        if not too_close:
            unique_coordinates.append(coord)

    return unique_coordinates
