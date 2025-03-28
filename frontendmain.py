import pygame
import math
import json
pygame.init()


################################### Simulation Variables ###################################
# Diplay/screen Setup
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Window")

# Color Variables if needed
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (76, 196, 134)

SLIDER_WIDTH = 100
SLIDER_HEIGHT = 10
KNOB_RADIUS = 10
SLIDER_TEXT_FONT = pygame.font.Font(None, 22)
SLIDER_NUMBER_FONT = pygame.font.Font(None, 25)
SUBTEXT_FONT = pygame.font.Font(None, 15)
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
        self.value = 1

    # Draw the slider
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=5)
        pygame.draw.circle(screen, GREEN, (self.knobPos, self.pos[1] + SLIDER_HEIGHT // 2), KNOB_RADIUS)
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

# Images
IMAGES = {}
IMAGES['mainbackground'] = pygame.image.load('assets/mainbackground.png').convert_alpha()
IMAGES['enc1'] = pygame.image.load('assets/enc1.png').convert_alpha()
IMAGES['enc2'] = pygame.image.load('assets/enc2.png').convert_alpha()
IMAGES['enc3'] = pygame.image.load('assets/enc3.png').convert_alpha()

## Page 1
# Sliders
sliders_1 = {}
sliders_1[0] = Slider(100, [60, 140], "How many days have the canids been in the enclosure")
sliders_1[1] = Slider(11, [60, 240], "How many social groups/families")

# Buttons
buttons_1 = {}
buttons_1[0] = Button([450, 180], [80,30], "Enclosure 1", GREEN, (154, 226, 187), (255, 249, 255))
buttons_1[1] = Button([450 + 90, 180], [80,30], "Enclosure 2", GREEN, (154, 226, 187), (255, 249, 255))
buttons_1[2] = Button([450 + 180, 180], [80,30], "Enclosure 3", GREEN, (154, 226, 187), (255, 249, 255))
buttons_1[3] = Button([50, 440], [80,30], "Foxes", GREEN, (154, 226, 187), (255, 249, 255))
buttons_1[4] = Button([160, 440], [80,30], "Coyotes", GREEN, (154, 226, 187), (255, 249, 255))
buttons_1[5] = Button([575, 490], [134,64], "Next", GREEN, (154, 226, 187), (255, 249, 255))


################################### Useful Formulas/Functions ###################################
def createSecondPage(numFamilies, canidType): # Returns the sliders and buttons as a table for the second page
    page_2 = {}
    slider_table = {}
    button_table = {}
    for i in range(numFamilies):
        slider = Slider(20, [60 + 250*math.floor(i/4), 170 + i%4*70], f"How many {canidType} in family {i + 1}")
        slider_table[i] = slider

    button_table[0] = Button([60, 500], [100,50], "Back", RED, GRAY, WHITE)
    button_table[1] = Button([575, 490], [134,64], "Start Simulation", GREEN, (154, 226, 187), (255, 249, 255))

    page_2[0] = slider_table
    page_2[1] = button_table

    return page_2

def incrementPixelCalculator(mouse_x, slider_x, slider_width, slider_inc): # Used for determining the amount of pixels the mouse needs to move for the next increment
    slider_pixel_inc = math.floor((mouse_x - slider_x)/(slider_width/slider_inc))*slider_width/slider_inc
    return slider_pixel_inc

def sliderValueCalculator(mouse_x, slider_x, slider_width, slider_inc): # Used for determining the actual value from the slider 
    slider_val = round(max(0, min((mouse_x - slider_x)/(slider_width/slider_inc), slider_inc)))
    return slider_val + 1

################################### Main Loop ###################################

running = True
page = 1
chosenCanid = "Foxes"
families = 1
days = 1
chosenEnclosure = 1
canidsPerFamily = []

firstPage = {}
firstPage[0] = sliders_1
firstPage[1] = buttons_1

secondPage = {}

while running:
    pygame.time.delay(FPS)  # Control frame rate
    
    # Override previous fills
    screen.fill(WHITE)
    screen.blit(IMAGES["mainbackground"], (0, 0))

    # Update page to corresponding number
    if page == 1:
        sliders = firstPage[0]
        buttons = firstPage[1]
        enclosureText = SLIDER_TEXT_FONT.render("Select an Enclosure", True, BLACK)
        screen.blit(enclosureText, (500, 150))
        speciesText = SLIDER_TEXT_FONT.render("Select a Canid", True, BLACK)
        screen.blit(speciesText, (95, 415))
        enclosureSelectionText = SUBTEXT_FONT.render(f"Chosen enclosure: {chosenEnclosure}", True, BLACK)
        screen.blit(enclosureSelectionText, (520, 220))
        speciesSelectionText = SUBTEXT_FONT.render(f"Chosen canid: {chosenCanid}", True, BLACK)
        screen.blit(speciesSelectionText, (90, 480))

        if chosenEnclosure == 1:
            screen.blit(IMAGES["enc1"], (525, 240))
        elif chosenEnclosure == 2:
            screen.blit(IMAGES["enc2"], (525, 250))
        elif chosenEnclosure == 3:
            screen.blit(IMAGES["enc3"], (525, 265))

    if page == 2:
        sliders = secondPage[0]
        buttons = secondPage[1]

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

        # Check all buttons and map them with a function
        for button in buttons.values():
            if button.isClicked(event):
                buttonType = button.get()
                    
                if buttonType == "Next":
                    days = sliders[0].getValue()
                    families = sliders[1].getValue()
                    page = 2
                    secondPage = createSecondPage(families, chosenCanid)
                if buttonType == "Back":
                    page -= 1

                if buttonType == "Start Simulation":
                    
                    # Run the simulation
                    for i in range(families):
                        canidsPerFamily.append(sliders[i].getValue())

                    # Load existing JSON data
                    with open("data.json", "r") as file:
                        data = json.load(file)

                    # Modify variables
                    data["families"] = families
                    data["chosenCanid"] = chosenCanid
                    data["days"] = days
                    data["chosenEnclosure"] = chosenEnclosure
                    data["canidsPerFamily"] = canidsPerFamily

                    # Write back to the file
                    with open("data.json", "w") as file:
                        json.dump(data, file, indent=4)

                    running = False
                    import frontendsim

                if buttonType == "Foxes":
                    chosenCanid = "Foxes"
                if buttonType == "Coyotes":
                    chosenCanid = "Coyotes"
                if buttonType == "Enclosure 1":
                    chosenEnclosure = 1
                if buttonType == "Enclosure 2":
                    chosenEnclosure = 2
                if buttonType == "Enclosure 3":
                    chosenEnclosure = 3
        
        # Check sliders
        for slider in sliders.values():
            slider.isSliding(event)

    if running:
        pygame.display.update()

# Quit Pygame
pygame.quit()
