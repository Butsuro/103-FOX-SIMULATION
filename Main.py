import pygame
import math
import json
import Path_finder as pf
import sys
import multiprocessing

class Slider:
    def __init__(self, inc, pos, text):
        self.inc = inc
        self.pos = pos
        self.text = text
        self.knobPos = pos[0]
        self.width = 100
        self.height = 10
        self.knobRadius = 10
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.dragging = False
        self.value = 1
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect, border_radius=5)
        pygame.draw.circle(screen, (76, 196, 134), (self.knobPos, self.pos[1] + self.height // 2), self.knobRadius)
        slider_number_font = pygame.font.Font(None, 25)
        slider_text_font = pygame.font.Font(None, 22)
        numberText = slider_number_font.render(str(self.value), True, (0, 0, 0))
        screen.blit(numberText, (self.pos[0] + self.width + 20, self.pos[1] - 5))
        sliderText = slider_text_font.render(self.text, True, (0, 0, 0))
        screen.blit(sliderText, (self.pos[0] - 10, self.pos[1] - 30))
    def getValue(self):
        return self.value
    def isSliding(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if (self.knobPos - self.knobRadius <= mx <= self.knobPos + self.knobRadius and self.pos[1] - self.knobRadius <= my <= self.pos[1] + self.knobRadius):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = event.pos
            inc_px = math.floor((mx - self.pos[0]) / (self.width / self.inc)) * self.width / self.inc
            mx = self.pos[0] + inc_px
            self.knobPos = max(self.pos[0], min(mx, self.pos[0] + self.width))
            self.value = round(max(0, min((mx - self.pos[0]) / (self.width / self.inc), self.inc))) + 1

class Button:
    def __init__(self, pos, size, text, color, hoverColor, textColor):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.textColor = textColor
        self.font = pygame.font.Font(None, 20)
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

def createSecondPage(numFamilies, canidType):
    slider_table = {}
    button_table = {}
    for i in range(numFamilies):
        slider_table[i] = Slider(20, [60 + 250 * (i // 4), 170 + (i % 4) * 70], f"How many {canidType} in family {i + 1}")
    button_table[0] = Button([60, 500], [100, 50], "Back", (255, 0, 0), (200, 200, 200), (255, 255, 255))
    button_table[1] = Button([575, 490], [134, 64], "Start Simulation", (76, 196, 134), (154, 226, 187), (255, 255, 255))
    return {0: slider_table, 1: button_table}

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulation Window")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (76, 196, 134)
    SLIDER_TEXT_FONT = pygame.font.Font(None, 22)
    SUBTEXT_FONT = pygame.font.Font(None, 15)
    IMAGES = {
        'mainbackground': pygame.image.load(pf.resource_path("assets/mainbackground.png")).convert_alpha(),
        'enc1': pygame.image.load(pf.resource_path("assets/enc1.png")).convert_alpha(),
        'enc2': pygame.image.load(pf.resource_path("assets/enc2.png")).convert_alpha(),
        'enc3': pygame.image.load(pf.resource_path("assets/enc3.png")).convert_alpha()
    }
    sliders_1 = {
        0: Slider(100, [60, 140], "How many days have the canids been in the enclosure"),
        1: Slider(11, [60, 240], "How many social groups/families")
    }
    buttons_1 = {
        0: Button([450, 180], [80, 30], "Enclosure 1", GREEN, (154, 226, 187), WHITE),
        1: Button([540, 180], [80, 30], "Enclosure 2", GREEN, (154, 226, 187), WHITE),
        2: Button([630, 180], [80, 30], "Enclosure 3", GREEN, (154, 226, 187), WHITE),
        3: Button([50, 375], [80, 30], "Foxes", GREEN, (154, 226, 187), WHITE),
        4: Button([160, 375], [80, 30], "Coyotes", GREEN, (154, 226, 187), WHITE),
        5: Button([575, 490], [134, 64], "Next", GREEN, (154, 226, 187), WHITE),
        6: Button([50, 520], [80, 30], "False", GREEN, (154, 226, 187), WHITE),
        7: Button([160, 520], [80, 30], "True", GREEN, (154, 226, 187), WHITE)
    }
    running = True
    page = 1
    chosenCanid = "Foxes"
    families = 1
    days = 1
    chosenEnclosure = 1
    canidsPerFamily = []
    skip_trap = False
    simulationStarted = False
    firstPage = {0: sliders_1, 1: buttons_1}
    secondPage = {}
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        screen.blit(IMAGES['mainbackground'], (0, 0))
        if page == 1:
            sliders = firstPage[0]
            buttons = firstPage[1]
            screen.blit(SLIDER_TEXT_FONT.render("Select an Enclosure", True, BLACK), (500, 150))
            screen.blit(SLIDER_TEXT_FONT.render("Select a Canid", True, BLACK), (95, 350))
            screen.blit(SLIDER_TEXT_FONT.render("Skip Trap Sim", True, BLACK), (95, 495))
            screen.blit(SUBTEXT_FONT.render(f"Chosen enclosure: {chosenEnclosure}", True, BLACK), (520, 220))
            screen.blit(SUBTEXT_FONT.render(f"Chosen canid: {chosenCanid}", True, BLACK), (90, 415))
            screen.blit(SUBTEXT_FONT.render(f"Skip trap sim: {skip_trap}", True, BLACK), (90, 560))
            if chosenEnclosure == 1:
                screen.blit(IMAGES['enc1'], (525, 240))
            elif chosenEnclosure == 2:
                screen.blit(IMAGES['enc2'], (525, 250))
            else:
                screen.blit(IMAGES['enc3'], (525, 265))
        else:
            sliders = secondPage[0]
            buttons = secondPage[1]
        for s in sliders.values():
            s.draw(screen)
        for b in buttons.values():
            b.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for s in sliders.values():
                s.isSliding(event)
            for b in buttons.values():
                if b.isClicked(event):
                    bt = b.get()
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
                    elif bt == "Back":
                        page = 1
                    elif bt == "Start Simulation":
                        for i in range(families):
                            canidsPerFamily.append(sliders[i].getValue())
                        with open(pf.resource_path("data.json"), "r") as file:
                            data = json.load(file)
                        data.update({
                            "families": families,
                            "chosenCanid": chosenCanid,
                            "days": days,
                            "chosenEnclosure": chosenEnclosure,
                            "canidsPerFamily": canidsPerFamily,
                            "skip_trap": skip_trap
                        })
                        with open(pf.resource_path("data.json"), "w") as file:
                            json.dump(data, file, indent=4)
                        simulationStarted = True
                        running = False
        if running:
            pygame.display.update()
    pygame.quit()
    old_client_data = {
        "chosenCanid": "Foxes",
        "days": 1,
        "chosenEnclosure": 1,
        "canidsPerFamily": [1],
        "families": 1,
        "skip_trap": False
    }
    with open(pf.resource_path("data.json"), "w") as f:
        json.dump(old_client_data, f, indent=4)
    old_simulation_data = {
        "chosenEnclosure": 1,
        "heatmap": [[]],
        "Trap_locations": [[]],
        "Trap_info": []
    }
    with open(pf.resource_path("simoutput.json"), "w") as f:
        json.dump(old_simulation_data, f, indent=4)
    print("ended")
    if simulationStarted:
        try:
            from frontendsim import run_simulation
            run_simulation()
        except ImportError:
            import frontendsim
    sys.exit()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
