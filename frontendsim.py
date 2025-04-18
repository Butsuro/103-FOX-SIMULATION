import pygame
import math
import Masterarray as master
import numpy as np
import json
import textwrap
import Path_finder as pf

print("\n" * 100)  # Pushes output off-screen

import Initializer
# Wait for the Initializer to finish

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
with open(pf.resource_path("data.json"), "r") as file:
    data = json.load(file)

CHOSEN_CONTAINER = data["chosenEnclosure"]
if CHOSEN_CONTAINER == 1:
    CHOSEN_CONTAINER = Container1
elif CHOSEN_CONTAINER == 2:
    CHOSEN_CONTAINER = Container2
else:
    CHOSEN_CONTAINER = Container3

HEATMAP_COLOUR_SCALE = 0.4  # How quickly the heatmap will turn red
HEATMAP_TRANSPARENCY_SCALE = 3  # How quickly the heatmap will be visible

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
IMAGES['background'] = pygame.image.load(pf.resource_path("assets/background.png")).convert_alpha()

# Buttons
buttons = {}
buttons[0] = Button(1, "Toggle Grid", (76, 196, 134), (154, 226, 187), (255, 249, 255), pygame.font.Font(None, 16))
buttons[1] = Button(2, "Display Heatmap", (76, 196, 134), (154, 226, 187), (255, 249, 255), pygame.font.Font(None, 16))
buttons[2] = Button(3, "Display Traps", (76, 196, 134), (154, 226, 187), (255, 249, 255), pygame.font.Font(None, 16))
buttons[3] = Button(
    4,                         # order: makes it draw below the third
    "View Trap Info",          # text
    (76,196,134),              # color
    (154,226,187),             # hover color
    (255,249,255),             # text color
    pygame.font.Font(None,16)  # font
)


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

# Finds the heatmap scale based on the 80th percentile of the heatmap array
def getHeatmapScale(arr):
    percentile = np.percentile(arr, 80)  # Find the 80th percentile value (this will be when the heatmap turns red)
    if percentile == 0:
        return 1
    else:
        return 255/percentile

# Draws the heatmap
def drawHeatmap(arr, scale):
    xLength, yLength, pixelArr = turnArrayToPixels(arr, 0)

    # Loop through the array and multiply the transparency with the amount of foxes
    for y in range(yLength):
        for x in range(xLength):
            if CHOSEN_CONTAINER[y][x] != 0:
                pixel = pygame.Surface((pixelArr[y][x][2], pixelArr[y][x][3]))
                pixel.set_alpha(min(arr[y][x]*scale*HEATMAP_TRANSPARENCY_SCALE, 180))  # transparency level
                pixel.fill((255,max(255 - arr[y][x]*scale*HEATMAP_COLOUR_SCALE, 0),0))
                screen.blit(pixel, (pixelArr[y][x][0], pixelArr[y][x][1]))

# Draws the traps. Requires the environment map and the trap location array
def drawTraps(arr, trapArray):
    xLength, yLength, pixelArr = turnArrayToPixels(arr, 0)
    for i in range(len(trapArray)):
            x = trapArray[i][0]
            y = trapArray[i][1]
            pixel = pygame.Surface((pixelArr[y][x][2], pixelArr[y][x][3]))
            pixel.fill((0,0,0))
            screen.blit(pixel, (pixelArr[y][x][0], pixelArr[y][x][1]))



################################### Simulation Loop ########################################
running = True
heatmapVisible = False
trapsVisible = False
gridVisible = True

running = True
page = 1

# Predefine the Back button for page 2
back_btn = pygame.font.Font(None,16)

#subprocess.run(["python3", "Initializer.py"])

# Get simulation data from json file
with open(pf.resource_path("simoutput.json"), "r") as file:
    simData = json.load(file)

while running:
    pygame.time.delay(RENDER_TIME)

    # ── PAGE 1: Environment + Controls ───────────────────────────────
    if page == 1:
        screen.fill(WHITE)
        screen.blit(IMAGES['background'], (0,0))

        # Draw environment
        drawEnvironment(CHOSEN_CONTAINER, gridVisible)
        if heatmapVisible:
            scale = getHeatmapScale(simData["heatmap"])
            drawHeatmap(simData["heatmap"], scale)
        if trapsVisible:
            drawTraps(CHOSEN_CONTAINER, simData["Trap_locations"])

        # Draw main buttons (0–3)
        for btn in buttons.values():
            btn.draw(screen)

    # ── PAGE 2: Trap Info List ───────────────────────────────────────
    else:  # page == 2
        screen.fill(WHITE)
        screen.blit(IMAGES['background'], (0,0))

        # Draw Back button in top-left
        b = Button(1, "Back", RED, GRAY, WHITE, pygame.font.Font(None,16))
        b.draw(screen)

        # Render Trap_info entries
        trap_info = simData.get("Trap_info", ["(no Trap_info)"])
        info_font = pygame.font.Font(None, 18)
        import textwrap
        x, y = 50, 100
        line_h = info_font.get_height() + 4

        for entry in trap_info:
            for line in textwrap.wrap(entry, width=40):
                screen.blit(info_font.render(line, True, BLACK), (x, y))
                y += line_h
            y += line_h  # extra space between entries

    # ── EVENT HANDLING ────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if page == 1:
                for btn in buttons.values():
                    if btn.isClicked(event):
                        t = btn.get()
                        if t == "Toggle Grid":
                            gridVisible = not gridVisible
                        elif t == "Display Heatmap":
                            heatmapVisible = not heatmapVisible
                        elif t == "Display Traps":
                            trapsVisible = not trapsVisible
                        elif t == "View Trap Info":
                            page = 2

            else:  # page == 2
                if b.isClicked(event):
                    page = 1

    pygame.display.update()

pygame.quit()
                    
pygame.display.update()

# Quit pygame
pygame.quit()
