import pygame
import math
import Masterarray as master
pygame.init()

######## Containers #################
# Container 1 is rightmost container
Container1 = master.Master1[0]

# Container 2 is middle Container
Container2 = master.Master2[0]

# Container 3 is the leftmost container
Container3 = master.Master3[0]

#Legend is as follows:
#  1 -> Tree
#  2 -> Grass
#  3 -> Dirt
#  4 -> Fence
#  5 -> Hut
#  6 -> Food
#  7 -> Special Dirt(No spawning zone)
#  0 -> empty
numColourLegend = {
    1: (61, 94, 71),
    2: (63, 125, 83),
    3: (159, 141, 127),
    4: (112, 112, 112),
    5: (0,0,0),
    6: (250, 178, 0),
    7: (159, 141, 127),
    0: (0,0,0)
}

######## Simulation Variables ########
HEATMAP_SCALE = 30  # How visible the heatmap will be
HEATMAP_COLOUR_SCALE = 1.75  # How quickly the heatmap will turn red
HEATMAP_TRANSPARENCY_SCALE = 1.75  # How quickly the heatmap will be visible
CHOSEN_CONTAINER = Container1

######## Display Variables ###########
# Diplay/screen Setup
SCREEN_MULTIPLIER = 10 # Controls how big the screen will be.
WIDTH, HEIGHT = len(CHOSEN_CONTAINER[0])*SCREEN_MULTIPLIER, len(CHOSEN_CONTAINER)*SCREEN_MULTIPLIER
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Window")

# Simulation Display Variables
XOFFSET = 25  # How far off on the X axis will the simulation be displayed
YOFFSET = 25  # How far off on the Y axis will the simulation be displayed 

# Color Variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)
DARK_GREEN = (51,102,0)

# Images
IMAGES = {}
IMAGES['tree'] = pygame.image.load('assets/smalltree.png').convert_alpha()

######## Useful functions #############
# Returns an array of pixel sizes/location for each index in a 2D array, as well as the X and Y length of the array
def turnArrayToPixels(arr):
    yLength = len(arr)
    xLength = len(arr[0])
    xPixel = (WIDTH-2*XOFFSET)/xLength  # Pixel x length of each block
    yPixel = (HEIGHT-2*YOFFSET)/yLength  # Pixel y length of each block
    pixelArr = []
    for y in range(yLength):
        row = []
        for x in range(len(arr[y])):

            # row[0] is pixel x position, row[1] is pixel y length, row[2] is pixel x size, row[3] is pixel y size
            row.append([XOFFSET + xPixel*x, YOFFSET + yPixel*y, xPixel+1, yPixel+1])
        pixelArr.append(row)
    return xLength, yLength, pixelArr

# Draws the environment array
def drawEnvironment(arr):
    xLength, yLength, pixelArr = turnArrayToPixels(arr)

    # Draw each element of the 2D Array, and match them with a color
    for y in range(yLength):
        for x in range(len(arr[y])):
            pygame.draw.rect(screen, numColourLegend[arr[y][x]], (pixelArr[y][x][0], pixelArr[y][x][1], pixelArr[y][x][2], pixelArr[y][x][3]))

# Draws the heatmap
def drawHeatmap(arr):
    xLength, yLength, pixelArr = turnArrayToPixels(arr)

    # Loop through the array and multiply the transparency with the amount of foxes
    for y in range(yLength):
        for x in range(xLength):
            pixel = pygame.Surface((pixelArr[y][x][2], pixelArr[y][x][3]))
            pixel.set_alpha(150)  # transparency level
            pixel.fill((255,max(255 - arr[y][x]*HEATMAP_SCALE*HEATMAP_COLOUR_SCALE, 0),0))
            screen.blit(pixel, (pixelArr[y][x][0], pixelArr[y][x][1]))


######## Simulation Loop #############
running = True
while running:
    pygame.time.delay(FPS)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the simulation every frame
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (XOFFSET, YOFFSET, WIDTH - 2*XOFFSET, HEIGHT - 2*YOFFSET))
    drawEnvironment(CHOSEN_CONTAINER)
    #drawHeatmap(CHOSEN_CONTAINER)
    pygame.display.update()

# Quit pygame
pygame.quit()
