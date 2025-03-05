import pygame
import math
pygame.init()

# Diplay/screen Setup
WIDTH, HEIGHT = 500, 500
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Window")

# Color Variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)
DARK_GREEN = (51,102,0)

# Simulation Display Variables
XOFFSET = 75 # How far off on the X axis will the simulation be displayed
YOFFSET = 75 # How far off on the Y axis will the simulation be displayed 


testArray = [
    [1,2,3],
    [1,2,3],
    [1,2,3],
]

# Useful Functions
def turnArrayToCoords(arr):
    for 

# Simulation Loop
running = True
while running:
    pygame.time.delay(FPS)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(GRAY)
    pygame.draw.rect(screen, DARK_GREEN, (XOFFSET, YOFFSET, WIDTH - 2*XOFFSET, HEIGHT - 2*YOFFSET))
    pygame.display.update()

# Quit pygame
pygame.quit()