import pygame
from random import randint
from sys import exit
from keyboard import is_pressed, on_press
from math import pi as PI


GREEN = (0, 255, 0)

running = True
def quit():
    global running
    running = False

class Data:
    def __init__(self, data: dict) -> None:
        for key, value in data.items():
            setattr(self, key, value)

class Page:
    def __init__(self):
        self.entity_list = []

    def add(self, entity):
        self.entity_list.append(entity)

    def activate(self):
        global ActivePage
        ActivePage = self

    def isActive(self) -> bool:
        return ActivePage == self

ActivePage = Page()

class Entity:
    def __init__(self, data: dict, page: Page = None) -> None:
        self.methods = {}
        self.remove = False
        self.data = Data(data)
        self.page = page
        if page != None: page.entity_list.append(self)
        
    def update(self, function):
        self.function = function

        self.update = self._temp
        self._temp = None
        del self._temp

        return None
    
    def delete(self):
        self.remove = True
        self.page.entity_list = list(filter(lambda x: not x.remove, self.page.entity_list))

    def _temp(self):
        self.function(self.data, self)

    def method(self, function):
        self.methods[function.__name__] = function

    def call(self, method_name: str):
        self.methods[method_name](self.data, self)
        

#CONSTANTS
SCREEN_SIZE = (800, 400)
WINDOW_TITLE = r"Philosopher's Odyssey"
FPS = 24
GRAVITY = 5
JUMP_STRENGTH = 50
PROGRESSION_SPEED = 2
PROGRESSION_INTERVAL = 5
POWER_UP_RECHARGE = 60

#INIT
pygame.init()
pygame.display.set_caption(WINDOW_TITLE)

pygame.display.set_icon(pygame.image.load(r"res/icon.png"))

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.mouse.set_visible(0)

background = pygame.surface.Surface(SCREEN_SIZE)
background.fill("Black")

#Pages
ControlScreen = Page()
image = Entity({"surface": pygame.image.load(r"res/ControlScreen.jpg")}, ControlScreen)
@image.update
def update(data, self):
    screen.blit(data.surface, (0, 0))

MainMenu = Page()

CharacterSelect = Page()

data = {
    "t1": pygame.font.Font("kongtext.ttf", 50).render("Philosopher's", True, (0, 200, 0)),
    "t1_2": pygame.font.Font("kongtext.ttf", 50).render("Philosopher's", True, GREEN),
    "t2": pygame.font.Font("kongtext.ttf", 50).render("Oddysey", True, (0, 200, 0)),
    "t2_2": pygame.font.Font("kongtext.ttf", 50).render("Oddysey", True, GREEN),
    "play": pygame.font.Font("kongtext.ttf", 26).render("Play as:", True, GREEN)
}
GameOverScreen = Page()

Score_Show = Entity({}, GameOverScreen)
@Score_Show.update
def update(data, self):
    text = pygame.font.Font("kongtext.ttf", 30)

    seconds = Score_Counter.data.time_survived / 24
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    time_string = f"{hours}h {minutes}m {seconds}s"
    
    if hours == 0:
        time_string = time_string.replace(f"{hours}h ", "")
    
    if minutes == 0:
        time_string = time_string.replace(f"{minutes}m ", "")
    
    bombs = text.render(f"Bombs Avoided: {Score_Counter.data.bombs_avoided}", True, (0, 255, 0))
    timer = text.render(f"Time Survived: {time_string}", True, (0, 255, 0))

    screen.blit(bombs, bombs.get_rect(midbottom=(SCREEN_SIZE[0] // 2 - 120, SCREEN_SIZE[1] // 2)))
    screen.blit(timer, bombs.get_rect(midtop=(SCREEN_SIZE[0] // 2 - 120, SCREEN_SIZE[1] // 2 + 10)))
    
title = Entity(data, CharacterSelect)
GameOverScreen.add(title)
MainMenu.add(title)

@title.update
def update(data, self):
    rect = data.t1.get_rect(midbottom=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 6))
    screen.blit(data.t1, rect)
    
    rect = data.t1_2.get_rect(midbottom=(SCREEN_SIZE[0] // 2 + 3, SCREEN_SIZE[1] // 6 + 3))
    screen.blit(data.t1_2, rect)

    rect = data.t2.get_rect(midtop=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 5))
    screen.blit(data.t2, rect)
    
    rect = data.t2_2.get_rect(midtop=(SCREEN_SIZE[0] // 2 + 3, SCREEN_SIZE[1] // 5 + 3))
    screen.blit(data.t2_2, rect)
    
    rect = data.play.get_rect(midbottom=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    if CharacterSelect.isActive(): screen.blit(data.play, rect) 

mainmenu_btns = [
    Entity({"Name": "Play", "position": (401, 244)}, MainMenu),
    Entity({"Name": "Controls", "position": (401, 272)}, MainMenu),
    Entity({"Name": "Credits", "position": (401, 300)}, MainMenu),
    Entity({"Name": "Exit", "position": (401, 328)}, MainMenu)
]

characterselect_btns = [
    Entity({"Name": "Heraclitus", "position": (228, 247)}, CharacterSelect),
    Entity({"Name": "Pythagoras", "position": (228, 284)}, CharacterSelect),
    Entity({"Name": "Anaximander", "position": (564, 247)}, CharacterSelect),
    Entity({"Name": "Anaximenes", "position": (552, 283)}, CharacterSelect),
    Entity({"Name": "Thales", "position": (387, 325)}, CharacterSelect)
]

gameoverscreen_btns = [
    Entity({"Name": "Main Menu", "position": (401, 302)}, GameOverScreen),
    Entity({"Name": "Retry", "position": (401, 330)}, GameOverScreen),
    Entity({"Name": "Exit", "position": (401, 358)}, GameOverScreen)
]

def update(data, self):
    font = pygame.font.Font("kongtext.ttf", 26).render(data.Name, True, GREEN)
    rect = font.get_rect(center=data.position)
    screen.blit(font, rect)

for button in characterselect_btns + gameoverscreen_btns + mainmenu_btns:
    button.update(update)


cursor = Entity({"selected": 0, "buttons": mainmenu_btns, "surface": pygame.font.Font("kongtext.ttf", 26).render(">", True, GREEN), "flash_count": 0}, CharacterSelect)
GameOverScreen.add(cursor)
MainMenu.add(cursor)

@cursor.update
def update(data, self):
    data.flash_count += 1
    if data.flash_count < 10: self.call("display")
    if data.flash_count >= 20: data.flash_count = 0

@cursor.method
def display(data, self):
    position = data.buttons[data.selected].data.position
    name = data.buttons[data.selected].data.Name
    rect = pygame.font.Font("kongtext.ttf", 26).render(name, True, GREEN).get_rect(center=position)

    screen.blit(data.surface, data.surface.get_rect(topright=rect.topleft))

white_overlay = Entity({"opacity": 255}, GameOverScreen)
@white_overlay.update
def update(data, self):
    surface = pygame.surface.Surface(SCREEN_SIZE)
    surface.fill("White")

    data.opacity -= 2 * 255 / FPS
    surface.set_alpha(int(data.opacity))

    screen.blit(surface, (0, 0))

GameScreen = Page()

#Background
bg = Entity({"x": 0, "surface": pygame.image.load("res/background.jpg")}, GameScreen)
@bg.update
def update(data, self):
    data.x += ground.data.speed // 10
    data.x %= 1472

    screen.blit(data.surface, (-data.x, -10))
    screen.blit(data.surface, (-data.x + 1472, -10))

#Ground
data = {"speed": 10, "speed_up_time": FPS * PROGRESSION_INTERVAL, "x": 0, "surface": pygame.image.load("res/ground.png")}

ground = Entity(data, GameScreen)
@ground.update
def update(data, self):
    data.x += data.speed
    data.x %= 1472

    screen.blit(data.surface, (-data.x, 8))
    screen.blit(data.surface, (-data.x + 1472, 8))

    data.speed_up_time -= 1
    if data.speed_up_time <= 0:
        data.speed_up_time = FPS * PROGRESSION_INTERVAL
        data.speed += PROGRESSION_SPEED

#Player
data = {
    "ground_speed": 10,
    "power_up_timer": 0,
    "vy": 0,
    "y": 225,
    "state": "falling",
    "surface": None,

    "surfaces": {
        "running": None,
        "sliding": pygame.image.load(r"res/Placeholder.png"),
        "power": pygame.image.load(r"res/Placeholder.png")
    }
}


player = Entity(data, GameScreen)

@player.update
def update(data, self):
    player_rect = data.surface.get_rect(midbottom=(100, data.y))

    if data.power_up_timer >= 1:
        data.power_up_timer -= 1

    if data.state == "running":
        if is_pressed("w") or is_pressed("up"):
            player.call("jump")
        elif is_pressed("s") or is_pressed("down"):
            data.state = "sliding" 
            data.surface = data.surfaces["sliding"]


    if data.state == "sliding":
        if not (is_pressed("s") or is_pressed("down")):
            data.surface = data.surfaces["running"]
            data.state = "running"


    elif data.state == "falling":
        data.vy += GRAVITY
        data.y += data.vy

        if is_pressed("s") or is_pressed("down") and data.vy < 30:
            data.vy = 30


    elif data.state == "power":
        data.power_up_timer -= 1

        if data.power_up_timer < 1:
            data.power_up_timer = FPS * 30
            data.state = "falling"
            data.surface = data.surfaces["running"]
            ground.data.speed = int(data.ground_speed)
            enemy_generator.data.spawn_interval *= 5

    ground_rect = pygame.Rect(0, 350 - data.vy, SCREEN_SIZE[0], 100)

    if player_rect.colliderect(ground_rect):
        data.vy = 0
        data.y = 350
        data.state = "running"

    player_rect = data.surface.get_rect(midbottom=(100, data.y))
    screen.blit(data.surface, player_rect)

@player.method
def jump(data, self):

    data.state = "falling"
    data.vy -= JUMP_STRENGTH

@player.method
def power_up(data, self):
    data.state = "power"
    data.power_up_timer = FPS * 10
    data.surface = player.data.surfaces["power"]
    data.vy = 0

    enemy_generator.data.spawn_timer //=  5
    enemy_generator.data.spawn_interval //= 5

    data.ground_speed = str(ground.data.speed)
    ground.data.speed *= 5

enemy_generator = Entity({"spawn_timer": 0, "spawn_interval": FPS * 2, "enemy_list": []}, GameScreen)
@enemy_generator.update
def update(data, self):
    data.spawn_timer -= 1

    if player.data.state == "power" and player.data.power_up_timer <= FPS * 2:
        return False

    if data.spawn_timer <= 0:
        data.spawn_timer = data.spawn_interval

        enemy = Entity({
            "x": SCREEN_SIZE[0],
            "y": randint(50, 270),
            "surface": pygame.image.load("res/Enemy.png")
            }, 
            GameScreen)
        
        data.enemy_list.append(enemy)

        @enemy.update
        def _update(data, self):
            data.x -= ground.data.speed

            if player.data.surface.get_rect(midbottom=(100, player.data.y)).colliderect(pygame.Rect(data.x + 20, data.y + 2 + 20, 40 - 20, 74 - 20)) and player.data.state != "power":
                cursor.data.buttons = gameoverscreen_btns
                cursor.data.selected = 0
                cursor.data.flash_screen = 0
                white_overlay.data.opacity = 255
                GameOverScreen.activate()

            if data.x <= -100:
                self.delete()
                Score_Counter.data.bombs_avoided += 1
            else:
                screen.blit(data.surface, (data.x, data.y))        

#Score Counter
Score_Counter = Entity({"bombs_avoided": 0, "time_survived": 0, "font": pygame.font.Font("kongtext.ttf", 20)}, GameScreen)
@Score_Counter.update
def update(data, self):
    data.time_survived += 1
    text = data.font.render(f"Score: {data.bombs_avoided}", True, (0, 255, 0))

    screen.blit(text, (10, 10))

Power_Display = Entity({}, GameScreen)
@Power_Display.update
def update(data, self):
    pygame.draw.circle(screen, (255, 255, 255), (45, 75), 31)
    screen.blit(player.data.surfaces["icon"], (17, 47))

    pos = (20 - 5, 50 - 5 + 1), (20 - 5 + 1, 50 - 5 + 1), (20 - 5, 50 - 5), (20 - 5 + 1, 50 - 5), (20 - 5, 50 - 5 + 1), (20 - 5 + 1, 50 - 5 + 1), (20 - 5, 50 - 5), (20 - 5 + 1, 50 - 5)
    if player.data.state != "power":
        if ((FPS * 30 - player.data.power_up_timer) / (FPS * 30)) == 1:
            for position in pos:
                pygame.draw.arc(screen, (200, 200, 200), list(position) + [60, 60], 0, (PI * 2) * ((FPS * 30 - player.data.power_up_timer) / (FPS * 30)), 2)
        else:
            for position in pos:
                pygame.draw.arc(screen, (100, 100, 100), list(position) + [60, 60], 0, (PI * 2) * ((FPS * 30 - player.data.power_up_timer) / (FPS * 30)), 2)
    else:
        for position in pos:
            pygame.draw.arc(screen, (100, 100, 100), list(position) + [60, 60], 0, (PI * 2) * ((player.data.power_up_timer) / (FPS * 10)), 2)


MainMenu.activate()

@on_press
def callback(event):
    if MainMenu.isActive():
        selected = cursor.data.selected

        if (event.name == "w" or event.name == "up") and selected > 0:
            cursor.data.selected -= 1
            cursor.data.flash_count = 0
        elif (event.name == "s" or event.name == "down") and selected < 3:
            cursor.data.selected += 1
            cursor.data.flash_count = 0
        elif event.name == "space":
            cursor.data.flash_count = 0
            name = mainmenu_btns[cursor.data.selected].data.Name

            if name == "Play":
                cursor.data.buttons = characterselect_btns

                CharacterSelect.activate()

            if name == "Credits":
                Credits.activate()

            if name == "Controls":
                ControlScreen.activate()
                
            elif name == "Exit":
                quit()

    elif CharacterSelect.isActive():
        selected = cursor.data.selected

        if (event.name == "w" or event.name == "up")  and selected > 0:
            cursor.data.selected -= 1
            cursor.data.flash_count = 0
        elif (event.name == "s" or event.name == "down")  and selected < 4:
            cursor.data.selected += 1
            cursor.data.flash_count = 0
        elif event.name == "space":
            cursor.data.flash_count = 0
            name = characterselect_btns[cursor.data.selected].data.Name

            texture = pygame.image.load(f"art/{name}/character.png")

            player.data.surfaces["running"] = texture
            player.data.surface = texture
            player.data.surfaces["icon"] = pygame.image.load(f"art/{name}/icon.png")

            player.data.surfaces["power"] = pygame.image.load(f"art/{name}/power.png")

            width, height = texture.get_size()

            width = width / height * 60
            height = 60

            player.data.surfaces["sliding"] = pygame.transform.scale(texture, (width, height))

            #Start Game
            player.data.power_up_timer = 0
            player.data.vy = 0
            player.data.y = 225
            player.data.state = "falling"
            player.data.surface = player.data.surfaces["running"]

            for enemy in enemy_generator.data.enemy_list:
                enemy.delete()

            player.call("power_up")
            player.data.power_up_timer = FPS * 2

            player.data.ground_speed = 10

            Score_Counter.data.time_survived = 0
            Score_Counter.data.bombs_avoided = 0
            GameScreen.activate()

    elif GameOverScreen.isActive():
        selected = cursor.data.selected
        if (event.name == "w" or event.name == "up")  and selected > 0:
            cursor.data.selected -= 1
            cursor.data.flash_count = 0
        elif (event.name == "s" or event.name == "down")  and selected < 2:
            cursor.data.selected += 1
            cursor.data.flash_count = 0
        elif event.name == "space":
            name = gameoverscreen_btns[cursor.data.selected].data.Name

            if name == "Retry":
                player.data.power_up_timer = 0
                player.data.vy = 0
                player.data.y = 225
                player.data.state = "falling"
                player.data.surface = player.data.surfaces["running"]

                for enemy in enemy_generator.data.enemy_list:
                    enemy.delete()

                player.call("power_up")
                player.data.power_up_timer = FPS * 2
    
                player.data.ground_speed = 10

                Score_Counter.data.time_survived = 0
                Score_Counter.data.bombs_avoided = 0
                GameScreen.activate()

            elif name == "Main Menu":
                cursor.data.buttons = mainmenu_btns
                cursor.data.selected = 0
                cursor.data.flash_screen = 0
                MainMenu.activate()

            elif name == "Exit":
                quit()

    elif ControlScreen.isActive() and event.name == "space":
        MainMenu.activate()


    elif Credits.isActive() and event.name == "space" and Credit_Page.data.y >= 1951:
        MainMenu.activate()
        Credit_Page.data.y = 0


Credits = Page()
Credit_Page = Entity({"y": 0, "surface": pygame.image.load(r"res/Credits.jpg")}, Credits)
@Credit_Page.update
def update(data, self):
    screen.blit(data.surface, (-1, -data.y))
    if data.y < 2352 - 400: data.y += 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        

    screen.blit(background, (0, 0))
    for entity in ActivePage.entity_list:
        entity.update()

    if GameScreen.isActive():

        if is_pressed("space") and player.data.state != "power" and player.data.power_up_timer <= 0:
            player.call("power_up")

    elif Credits.isActive() and is_pressed("s") and Credit_Page.data.y < 1942:
        Credit_Page.data.y += 5

    pygame.display.update()
    pygame.mouse.set_pos(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

    clock.tick(FPS)
    
pygame.quit()
exit()