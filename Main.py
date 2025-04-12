import pygame
import math
import json
pygame.init()


################################### Simulation Variables ###################################
# Display/screen Setup
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Window")

# Color Variables
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

################################### Classes ###################################
class Slider:
    def __init__(self, inc, pos, text):
        self.inc = inc
        self.pos = pos
        self.text = text
        self.knobPos = pos[0]
        self.rect = pygame.Rect(pos[0], pos[1], SLIDER_WIDTH, SLIDER_HEIGHT)
        self.dragging = False
        self.value = 1

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=5)
        pygame.draw.circle(screen, GREEN, (self.knobPos, self.pos[1] + SLIDER_HEIGHT // 2), KNOB_RADIUS)
        numberText = SLIDER_NUMBER_FONT.render(str(self.value), True, BLACK)
        screen.blit(numberText, (self.pos[0] + SLIDER_WIDTH + 20, self.pos[1] - 5))

        sliderText = SLIDER_TEXT_FONT.render(self.text, True, BLACK)
        screen.blit(sliderText, (self.pos[0] - 10, self.pos[1] - 30))

    def getValue(self):
        return self.value

    def isSliding(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if (self.knobPos - KNOB_RADIUS <= mx <= self.knobPos + KNOB_RADIUS and
                self.pos[1] - KNOB_RADIUS <= my <= self.pos[1] + KNOB_RADIUS):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = event.pos
            inc_px = math.floor((mx - self.pos[0]) / (SLIDER_WIDTH / self.inc)) * SLIDER_WIDTH / self.inc
            mx = self.pos[0] + inc_px
            self.knobPos = max(self.pos[0], min(mx, self.pos[0] + SLIDER_WIDTH))
            self.value = round(max(0, min((mx - self.pos[0]) / (SLIDER_WIDTH / self.inc), self.inc))) + 1


class Button:
    def __init__(self, pos, size, text, color, hoverColor, textColor):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.textColor = textColor
        self.font = BUTTON_FONT

    def get(self):
        return self.text

    def draw(self, screen):
        mousePos = pygame.mouse.get_pos()
        currentColor = self.hoverColor if self.rect.collidepoint(mousePos) else self.color
        pygame.draw.rect(screen, currentColor, self.rect, border_radius=5)
        txt = self.font.render(self.text, True, self.textColor)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def isClicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


################################### Helper Functions ###################################
def createSecondPage(numFamilies, canidType):
    slider_table = {}
    button_table = {}
    for i in range(numFamilies):
        slider_table[i] = Slider(20, [60 + 250 * (i // 4), 170 + (i % 4) * 70],
                                 f"How many {canidType} in family {i + 1}")
    button_table[0] = Button([60, 500], [100, 50], "Back", RED, GRAY, WHITE)
    button_table[1] = Button([575, 490], [134, 64], "Start Simulation", GREEN, (154, 226, 187), WHITE)
    return {0: slider_table, 1: button_table}


################################### Load Assets ###################################
IMAGES = {
    'mainbackground': pygame.image.load('assets/mainbackground.png').convert_alpha(),
    'enc1': pygame.image.load('assets/enc1.png').convert_alpha(),
    'enc2': pygame.image.load('assets/enc2.png').convert_alpha(),
    'enc3': pygame.image.load('assets/enc3.png').convert_alpha(),
}


################################### Page 1 Setup ###################################
sliders_1 = {
    0: Slider(100, [60, 140], "How many days have the canids been in the enclosure"),
    1: Slider(11,  [60, 240], "How many social groups/families")
}

buttons_1 = {
    0: Button([450, 180], [80, 30],  "Enclosure 1",      GREEN, (154, 226, 187), WHITE),
    1: Button([540, 180], [80, 30], "Enclosure 2",      GREEN, (154, 226, 187), WHITE),
    2: Button([630, 180], [80, 30], "Enclosure 3",      GREEN, (154, 226, 187), WHITE),
    3: Button([50, 440-65], [80, 30],  "Foxes",            GREEN, (154, 226, 187), WHITE),
    4: Button([160, 440-65], [80, 30], "Coyotes",          GREEN, (154, 226, 187), WHITE),
    5: Button([575, 490], [134, 64], "Next",             GREEN, (154, 226, 187), WHITE),
    6: Button([50, 520],  [80, 30],  "False",      GREEN, (154, 226, 187), WHITE),
    7: Button([160, 520], [80, 30],  "True",       GREEN, (154, 226, 187), WHITE),
}

################################### Main Loop ###################################
running = True
page = 1
chosenCanid = "Foxes"
families = 1
days = 1
chosenEnclosure = 1
canidsPerFamily = []
skip_trap = False

firstPage  = {0: sliders_1, 1: buttons_1}
secondPage = {}

while running:
    pygame.time.delay(FPS)
    screen.fill(WHITE)
    screen.blit(IMAGES['mainbackground'], (0, 0))

    # --- Draw Page Content ---
    if page == 1:
        sliders = firstPage[0]
        buttons = firstPage[1]

        # Titles & subtext
        screen.blit(SLIDER_TEXT_FONT.render("Select an Enclosure", True, BLACK), (500, 150))
        screen.blit(SLIDER_TEXT_FONT.render("Select a Canid",     True, BLACK), (95,  350))
        screen.blit(SLIDER_TEXT_FONT.render("Skip Trap Sim", True, BLACK), (95, 495))
        screen.blit(SUBTEXT_FONT.render(f"Chosen enclosure: {chosenEnclosure}", True, BLACK), (520, 220))
        screen.blit(SUBTEXT_FONT.render(f"Chosen canid: {chosenCanid}",         True, BLACK), (90,  480-65))
        screen.blit(SUBTEXT_FONT.render(f"Skip trap sim: {skip_trap}",           True, BLACK), (90,  560))

        # Enclosure image
        if chosenEnclosure == 1:
            screen.blit(IMAGES['enc1'], (525, 240))
        elif chosenEnclosure == 2:
            screen.blit(IMAGES['enc2'], (525, 250))
        else:
            screen.blit(IMAGES['enc3'], (525, 265))

    else:  # page == 2
        sliders = secondPage[0]
        buttons = secondPage[1]

    # Draw sliders & buttons
    for s in sliders.values(): s.draw(screen)
    for b in buttons.values(): b.draw(screen)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Sliders
        for s in sliders.values():
            s.isSliding(event)

        # Buttons
        for b in buttons.values():
            if b.isClicked(event):
                bt = b.get()
                # Page 1 handlers
                if bt == "Next":
                    days = sliders_1[0].getValue()
                    families = sliders_1[1].getValue()
                    page = 2
                    secondPage = createSecondPage(families, chosenCanid)

                elif bt == "False":
                    skip_trap = False
                elif bt == "True":
                    skip_trap = True

                elif bt in ("Foxes", "Coyotes"):
                    chosenCanid = bt
                elif bt.startswith("Enclosure"):
                    chosenEnclosure = int(bt.split()[-1])

                # Page 2 handlers
                elif bt == "Back":
                    page = 1
                elif bt == "Start Simulation":
                    for i in range(families):
                        canidsPerFamily.append(sliders[i].getValue())

                    with open("data.json", "r") as file:
                        data = json.load(file)

                    data.update({
                        "families": families,
                        "chosenCanid": chosenCanid,
                        "days": days,
                        "chosenEnclosure": chosenEnclosure,
                        "canidsPerFamily": canidsPerFamily,
                        "skip_trap": skip_trap
                    })

                    with open("data.json", "w") as file:
                        json.dump(data, file, indent=4)

                    running = False
                    pygame.quit()
                    import frontendsim

    if running:
        pygame.display.update()

pygame.quit()

# Reset client data
old_client_data = {
    "chosenCanid": "Foxes",
    "days": 1,
    "chosenEnclosure": 1,
    "canidsPerFamily": [1],
    "families": 1,
    "skip_trap": False
}
with open("data.json", "w") as f:
    json.dump(old_client_data, f, indent=4)

# Reset simulation data
old_simulation_data = {
    "chosenEnclosure": 1,
    "heatmap": [[]],
    "Trap_locations": [[]],
    "Trap_info": []
}
with open("simoutput.json", "w") as f:
    json.dump(old_simulation_data, f, indent=4)

print("ended")
