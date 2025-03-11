import pygame
import math
import Masterarray as master
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
HEATMAP_SCALE = 30  # How visible the heatmap will be
HEATMAP_COLOUR_SCALE = 1.75  # How quickly the heatmap will turn red
HEATMAP_TRANSPARENCY_SCALE = 10  # How quickly the heatmap will be visible
CHOSEN_CONTAINER = Container1

# Simulation Display Variables
XOFFSET = 50  # Simulation X extra space (effects environment size)
YOFFSET = 50  # Simulation Y extra space (effects environment size)
XDISPLACEMENT = 0  # How far to the right the environment is displaced
YDISPLACEMENT = 75  # How far down the environment is displaced
XBORDERLENGTH = 150  # How much empty space will be on the X
YBORDERLENGTH = 100  # How much empty space will be on the Y 


################################### Display Variables ###################################
# Diplay/screen Setup
SCREEN_MULTIPLIER = 10 # Controls how big the screen will be.
WIDTH, HEIGHT = len(CHOSEN_CONTAINER[0])*SCREEN_MULTIPLIER + XBORDERLENGTH, len(CHOSEN_CONTAINER)*SCREEN_MULTIPLIER + YBORDERLENGTH
FPS = 60
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
        self.rect = pygame.Rect(WIDTH - 125, YOFFSET + YDISPLACEMENT + 80*(self.order-1), 100, 50)
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
buttons[0] = Button(1, "Display Heatmap", (255, 50, 50), (255, 120, 120), (0, 0, 0), pygame.font.Font(None, 16))
buttons[1] = Button(2, "Display Traps", (252, 170, 6), (255, 209, 117), (0, 0, 0), pygame.font.Font(None, 16))

################################### Useful functions ###################################
# Returns an array of pixel sizes/location for each index in a 2D array, as well as the X and Y length of the array
def turnArrayToPixels(arr, pixelOffset):
    yLength = len(arr)
    xLength = len(arr[0])
    xPixel = math.floor((WIDTH-XBORDERLENGTH-XOFFSET)/xLength)  # Pixel x length of each block
    yPixel = math.floor((HEIGHT-YBORDERLENGTH-YOFFSET)/yLength)  # Pixel y length of each block
    pixelArr = []
    for y in range(yLength):
        row = []
        for x in range(len(arr[y])):

            # row[0] is pixel x position, row[1] is pixel y length, row[2] is pixel x size, row[3] is pixel y size
            row.append([XOFFSET + xPixel*x + XDISPLACEMENT, YOFFSET + yPixel*y + YDISPLACEMENT, xPixel-pixelOffset, yPixel-pixelOffset])
        pixelArr.append(row)
    return xLength, yLength, pixelArr

# Draws the environment array
def drawEnvironment(arr):
    xLength, yLength, pixelArr = turnArrayToPixels(arr, 1)

    # Draw each element of the 2D Array, and match them with a color
    for y in range(yLength):
        for x in range(len(arr[y])):
            if arr[y][x] != 0:
                # Make environment background black
                pygame.draw.rect(screen, BLACK, (pixelArr[y][x][0], pixelArr[y][x][1], pixelArr[y][x][2] + 1, pixelArr[y][x][3] + 1))
                # Draw the environment on top of the black
                pygame.draw.rect(screen, numColourLegend[arr[y][x]], (pixelArr[y][x][0], pixelArr[y][x][1], pixelArr[y][x][2], pixelArr[y][x][3]))

# Draws the heatmap
def drawHeatmap(arr):
    xLength, yLength, pixelArr = turnArrayToPixels(arr, 0)

    # Loop through the array and multiply the transparency with the amount of foxes
    for y in range(yLength):
        for x in range(xLength):
            pixel = pygame.Surface((pixelArr[y][x][2], pixelArr[y][x][3]))
            pixel.set_alpha(min(arr[y][x]*HEATMAP_SCALE*HEATMAP_TRANSPARENCY_SCALE, 180))  # transparency level
            pixel.fill((255,max(255 - arr[y][x]*HEATMAP_SCALE*HEATMAP_COLOUR_SCALE, 0),0))
            screen.blit(pixel, (pixelArr[y][x][0], pixelArr[y][x][1]))


################################### Simulation Loop ########################################
running = True
heatmapVisible = False
trapsVisible = False

print(WIDTH, HEIGHT)

while running:
    pygame.time.delay(FPS)

    # Fill the simulation every frame
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (XOFFSET, YOFFSET, WIDTH - 2*XOFFSET, HEIGHT - 2*YOFFSET))
    screen.blit(IMAGES["background"], (0, 0))
    drawEnvironment(CHOSEN_CONTAINER)
    if heatmapVisible:
        drawHeatmap(CHOSEN_CONTAINER)
    
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
                if buttonType == "Display Heatmap":
                    heatmapVisible = not heatmapVisible
                if buttonType == "Display Traps":
                    trapsVisible = not trapsVisible

    pygame.display.update()

# Quit pygame
pygame.quit()
