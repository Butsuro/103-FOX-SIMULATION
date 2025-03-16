import pygame
import math
pygame.init()


################################### Simulation Variables ###################################
# Diplay/screen Setup
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Window")

# Color Variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

SLIDER_WIDTH = 100
SLIDER_HEIGHT = 10
KNOB_RADIUS = 10
SLIDER_TEXT_FONT = pygame.font.Font(None, 25)
SLIDER_NUMBER_FONT = pygame.font.Font(None, 25)

BUTTON_FONT = pygame.font.Font(None, 20)

# Classes
class Slider:
    # Create the slider class
    def __init__(self, inc, pos, text):
        self.inc = inc
        self.pos = pos
        self.text = text
        self.knobPos = pos[0]
        self.rect = pygame.Rect(pos[0], pos[1], SLIDER_WIDTH, SLIDER_HEIGHT)
        self.dragging = False
        self.value = 0

    # Draw the slider
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=5)
        pygame.draw.circle(screen, RED, (self.knobPos, self.pos[1] + SLIDER_HEIGHT // 2), KNOB_RADIUS)
        numberText = SLIDER_NUMBER_FONT.render(str(self.value), True, BLACK)
        screen.blit(numberText, (self.pos[0] + SLIDER_WIDTH + 20, self.pos[1] - 5))

        sliderText = SLIDER_TEXT_FONT.render(self.text, True, BLACK)
        screen.blit(sliderText, (self.pos[0] - 10, self.pos[1] - 30))
    
    # Returns the slider's value
    def getValue(self):
        return self.value
    
    # Check if sliding
    def isSliding(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Get x and y coordinates of where the mouse clicked
            mouse_x, mouse_y = event.pos

            # Check to see if mouse is within the slider knob
            if (self.knobPos - KNOB_RADIUS <= mouse_x <= self.knobPos + KNOB_RADIUS and
                    self.pos[1] - KNOB_RADIUS <= mouse_y <= self.pos[1] + KNOB_RADIUS):
                self.dragging = True
            
        # Check to see if user let go of mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        # If user clicked on the knob and is moving the mouse then move the slider too
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = event.pos
            slider_pixel_inc = incrementPixelCalculator(mouse_x, self.pos[0], SLIDER_WIDTH, self.inc)
            mouse_x = self.pos[0] + slider_pixel_inc

            # If the x pos of the mouse is too far, then default it to the edge of slider
            self.knobPos = max(self.pos[0], min(mouse_x, self.pos[0] + SLIDER_WIDTH))

            # Store the slider value
            self.value = sliderValueCalculator(mouse_x, self.pos[0], SLIDER_WIDTH, self.inc)


class Button:
    # Create the button class
    def __init__(self, pos, size, text, color, hoverColor, textColor):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.textColor = textColor
        self.font = BUTTON_FONT
    
    # Returns the button name
    def get(self):
        return self.text
    
    # Check to see if mouse is hovering over button
    def checkHover(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            return True

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


# Sliders
sliders = {}
sliders[0] = Slider(100, [75, 100], "How many days have the canids been in the enclosure")
sliders[1] = Slider(11, [75, 200], "How many social groups/families")
sliders[2] = Slider(20, [75, 300], "How many canids in the enclosure")

# Buttons
buttons = {}
buttons[0] = Button([450, 180], [80,30], "Enclosure 1", RED, GRAY, WHITE)
buttons[1] = Button([450 + 90, 180], [80,30], "Enclosure 2", RED, GRAY, WHITE)
buttons[2] = Button([450 + 180, 180], [80,30], "Enclosure 3", RED, GRAY, WHITE)
buttons[3] = Button([100, 440], [80,30], "Fox", RED, GRAY, WHITE)
buttons[4] = Button([210, 440], [80,30], "Coyote", RED, GRAY, WHITE)
buttons[5] = Button([600, 500], [100,50], "Next", RED, GRAY, WHITE)

################################### Useful Formulas ###################################
def incrementPixelCalculator(mouse_x, slider_x, slider_width, slider_inc): # Used for determining the amount of pixels the mouse needs to move for the next increment
    slider_pixel_inc = math.floor((mouse_x - slider_x)/(slider_width/slider_inc))*slider_width/slider_inc
    return slider_pixel_inc

def sliderValueCalculator(mouse_x, slider_x, slider_width, slider_inc): # Used for determining the actual value from the slider 
    slider_val = round(max(0, min((mouse_x - slider_x)/(slider_width/slider_inc), slider_inc)))
    return slider_val

################################### Main Loop ###################################
running = True
page = 1
chosenCanid = "Foxes"
families = 1
canids = 1
chosenEnclosure = 1

while running:
    pygame.time.delay(FPS)  # Control frame rate
    
    # Override previous fills
    screen.fill(WHITE)

    enclosureText = SLIDER_TEXT_FONT.render("Select an Enclosure", True, BLACK)
    screen.blit(enclosureText, (500, 150))
    speciesText = SLIDER_TEXT_FONT.render("Select a Canid", True, BLACK)
    screen.blit(speciesText, (135, 395))

    # Draw sliders
    for slider in sliders.values():
        slider.draw(screen)
    # Draw buttons
    for button in buttons.values():
        button.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check sliders
        for slider in sliders.values():
            slider.isSliding(event)
            
    pygame.display.update()

# Quit Pygame
pygame.quit()

# Run the simulation
import frontendsim
