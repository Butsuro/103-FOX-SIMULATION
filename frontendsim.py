import pygame
import math
import Masterarray as master
import numpy as np
import json
import subprocess
import time
import threading

import Initializer

pygame.init()

################################### Containers ###################################
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

################################### Simulation Variables ###################################
# Get client data from json file
with open("data.json", "r") as file:
    data = json.load(file)

CHOSEN_CONTAINER = data["chosenEnclosure"]
if CHOSEN_CONTAINER == 1:
    CHOSEN_CONTAINER = Container1
elif CHOSEN_CONTAINER == 2:
    CHOSEN_CONTAINER = Container2
else:
    CHOSEN_CONTAINER = Container3

HEATMAP_SCALE = 30  # How visible the heatmap will be
HEATMAP_COLOUR_SCALE = 0.4  # How quickly the heatmap will turn red
HEATMAP_TRANSPARENCY_SCALE = 0.6  # How quickly the heatmap will be visible

# Simulation Display Variables
X_OFFSET = 50  # Changes the x size of the environment
Y_OFFSET = 50  # Changes the Y size of the environment
X_DISPLACEMENT = 0  # How far to the right the environment is displaced
Y_DISPLACEMENT = 75  # How far down the environment is displaced
X_BORDER_LENGTH = 150  # How much empty space will be on the X
Y_BORDER_LENGTH = 100  # How much empty space will be on the Y 
X_BUTTON_DISPLACEMENT = 130 # How far to the left will the button be displayed

# Diplay/screen Setup
SCREEN_MULTIPLIER = 10 # Controls how big the screen will be.
WIDTH, HEIGHT = len(CHOSEN_CONTAINER[0])*SCREEN_MULTIPLIER + X_BORDER_LENGTH, len(CHOSEN_CONTAINER)*SCREEN_MULTIPLIER + Y_BORDER_LENGTH
RENDER_TIME = 30  # Delay between each frame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Window")

# Color Variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)
DARK_GREEN = (51,102,0)

# Classes
class Button:
    # Create the button class
    def __init__(self, order, text, color, hoverColor, textColor, font):
        self.order = order
        self.rect = pygame.Rect(WIDTH - X_BUTTON_DISPLACEMENT, Y_OFFSET + Y_DISPLACEMENT + 80*(self.order-1), 100, 50)
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.textColor = textColor
        self.font = font
    
    # Returns the button name
    def get(self):
        return self.text
    
    # Draw the button to the screen
    def draw(self, screen):
        mousePos = pygame.mouse.get_pos()
        
        # Change colour if hovering
        if self.rect.collidepoint(mousePos):
            currentColor = self.hoverColor
        else:
            currentColor = self.color
        
        pygame.draw.rect(screen, currentColor, self.rect, border_radius=5)
        textSurface = self.font.render(self.text, True, self.textColor)
        textRect = textSurface.get_rect(center=self.rect.center)
        screen.blit(textSurface, textRect)
    
    # Check if the button is clicked
    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

# Images
IMAGES = {}
IMAGES['background'] = pygame.image.load('assets/background.png').convert_alpha()

# Buttons
buttons = {}
buttons[0] = Button(1, "Toggle Grid", (76, 196, 134), (154, 226, 187), (255, 249, 255), pygame.font.Font(None, 16))
buttons[1] = Button(2, "Display Heatmap", (76, 196, 134), (154, 226, 187), (255, 249, 255), pygame.font.Font(None, 16))
buttons[2] = Button(3, "Display Traps", (76, 196, 134), (154, 226, 187), (255, 249, 255), pygame.font.Font(None, 16))


################################### Useful functions ###################################
# Returns an array of pixel sizes/location for each index in a 2D array, as well as the X and Y length of the array
# Requires a 2D array, and a pixel Offset amount (basically border size, 0 for no border)
def turnArrayToPixels(arr, pixelOffset):
    yLength = len(arr)
    xLength = len(arr[0])
    xPixel = math.floor((WIDTH-X_BORDER_LENGTH-X_OFFSET)/xLength)  # Pixel x length of each block
    yPixel = math.floor((HEIGHT-Y_BORDER_LENGTH-Y_OFFSET)/yLength)  # Pixel y length of each block
    pixelArr = []
    for y in range(yLength):
        row = []
        for x in range(len(arr[y])):

            # row[0] is pixel x position, row[1] is pixel y length, row[2] is pixel x size, row[3] is pixel y size
            row.append([X_OFFSET + xPixel*x + X_DISPLACEMENT, Y_OFFSET + yPixel*y + Y_DISPLACEMENT, xPixel-pixelOffset, yPixel-pixelOffset])
        pixelArr.append(row)
    return xLength, yLength, pixelArr

# Draws the environment array
def drawEnvironment(arr, gridsVisible):
    if gridVisible:
        pixelBorder = 1
    else:
        pixelBorder = 0

    xLength, yLength, pixelArr = turnArrayToPixels(arr, pixelBorder)

    # Make environment background black
    for y in range(yLength):
        for x in range(len(arr[y])):
            if arr[y][x] != 0:
                pygame.draw.rect(screen, BLACK, (pixelArr[y][x][0] - 2, pixelArr[y][x][1] - 2, pixelArr[y][x][2] + 4, pixelArr[y][x][3] + 4))

    # Draw each element of the 2D Array, and match them with a color
    for y in range(yLength):
        for x in range(len(arr[y])):
            if arr[y][x] != 0:
                pygame.draw.rect(screen, numColourLegend[arr[y][x]], (pixelArr[y][x][0], pixelArr[y][x][1], pixelArr[y][x][2], pixelArr[y][x][3]))

# Draws the heatmap
def drawHeatmap(arr):
    xLength, yLength, pixelArr = turnArrayToPixels(arr, 0)

    # Loop through the array and multiply the transparency with the amount of foxes
    for y in range(yLength):
        for x in range(xLength):
            if CHOSEN_CONTAINER[y][x] != 0:
                pixel = pygame.Surface((pixelArr[y][x][2], pixelArr[y][x][3]))
                pixel.set_alpha(min(arr[y][x]*HEATMAP_SCALE*HEATMAP_TRANSPARENCY_SCALE, 180))  # transparency level
                pixel.fill((255,max(255 - arr[y][x]*HEATMAP_SCALE*HEATMAP_COLOUR_SCALE, 0),0))
                screen.blit(pixel, (pixelArr[y][x][0], pixelArr[y][x][1]))


################################### Simulation Loop ########################################
running = True
heatmapVisible = False
trapsVisible = False
gridVisible = True

print(WIDTH, HEIGHT)
#subprocess.Popen(["python", "Initializer.py"])

# Get simulation data from json file
with open("simoutput.json", "r") as file:
    simData = json.load(file)

while running:
    pygame.time.delay(RENDER_TIME)

    # Fill the simulation every frame
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, WIDTH - 2*X_OFFSET, HEIGHT - 2*Y_OFFSET))
    screen.blit(IMAGES["background"], (0, 0))
    drawEnvironment(CHOSEN_CONTAINER, gridVisible)
    if heatmapVisible:
        drawHeatmap(simData["heatmap"])
    
    # Draw buttons
    for button in buttons.values():
        button.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check all buttons and map them with a function
        for button in buttons.values():
            if button.isClicked(event):
                buttonType = button.get()
                
                if buttonType == "Toggle Grid":
                    gridVisible = not gridVisible
                if buttonType == "Display Heatmap":
                    heatmapVisible = not heatmapVisible

                    """
                    SAMPLE HEAT MAP

                    rows, cols = len(CHOSEN_CONTAINER), 36
                    random_base = np.random.randint(0, 21, (rows, cols))
                    smoothed_array = random_base.copy()
                    for i in range(rows):
                        for j in range(cols):
                            neighbors = []
                            for di in [-1, 0, 1]:
                                for dj in [-1, 0, 1]:
                                    ni, nj = i + di, j + dj
                                    if 0 <= ni < rows and 0 <= nj < cols:
                                        neighbors.append(random_base[ni, nj])
                            smoothed_array[i, j] = np.mean(neighbors)
                    smoothed_array = np.clip(smoothed_array, 0, 20).astype(int)
                    """

                if buttonType == "Display Traps":
                    trapsVisible = not trapsVisible
                    
    pygame.display.update()

# Quit pygame
pygame.quit()
