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
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Slider Variables
slider_inc = 6
slider_x = 100
slider_y = 400
slider_val = 0
slider_width = 100
slider_height = 10
slider_knob_x = slider_x
slider_knob_radius = 10
slider_dragging = False
font = pygame.font.Font(None, 36)
displayed_number = 0

# Useful Formulas
def incrementPixelCalculator(mouse_x, slider_x, slider_width, slider_inc): # Used for determining the amount of pixels the mouse needs to move for the next increment
    slider_pixel_inc = math.floor((mouse_x - slider_x)/(slider_width/slider_inc))*slider_width/slider_inc
    return slider_pixel_inc

def sliderValueCalculator(mouse_x, slider_x, slider_width, slider_inc): # Used for determining the actual value from the slider 
    slider_val = round(max(0, min((mouse_x - slider_x)/(slider_width/slider_inc), slider_inc)))
    return slider_val

# Main Loop
running = True
while running:
    pygame.time.delay(FPS)  # Control frame rate
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Get x and y coordinates of where the mouse clicked
            mouse_x, mouse_y = event.pos

            # Check to see if mouse is within the slider knob
            if (slider_knob_x - slider_knob_radius <= mouse_x <= slider_knob_x + slider_knob_radius and
                    slider_y - slider_knob_radius <= mouse_y <= slider_y + slider_knob_radius):
                slider_dragging = True
            
        # Check to see if user let go of mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False

        # If user clicked on the knob and is moving the mouse then move the slider too
        elif event.type == pygame.MOUSEMOTION and slider_dragging:
            mouse_x, _ = event.pos
            slider_pixel_inc = incrementPixelCalculator(mouse_x, slider_x, slider_width, slider_inc)
            mouse_x = slider_x + slider_pixel_inc
            slider_knob_x = max(slider_x, min(mouse_x, slider_x + slider_width)) # If the x pos of the mouse is too far, then default it to the edge of slider

            # Store the slider value
            slider_val = sliderValueCalculator(mouse_x, slider_x, slider_width, slider_inc)


    # Override previous fills
    screen.fill(WHITE)

    # Draw slider
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, RED, (slider_knob_x, slider_y + slider_height // 2), slider_knob_radius)
    displayed_number = slider_val
    number_text = font.render(str(displayed_number), True, BLACK)
    screen.blit(number_text, (slider_x + slider_width + 20, slider_y - 5))
            
    pygame.display.update()

# Quit Pygame
pygame.quit()