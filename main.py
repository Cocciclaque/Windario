import pygame
import win32api
import win32con
import win32gui
import Scripts.SettingsAndLevelParser as SettingsAndLevelParser
import Scripts.levelRenderer as levelRenderer
import Scripts.windowrelative as CustomRenderWindowRelative
import Scripts.windowabsolute as CustomRenderWindowAbsolute
import Scripts.player as PlayerCharacter
import Scripts.animation as Animation
import Scripts.level as CustomLevel
import Scripts.transition as transition
import Scripts.background as background
import time
pygame.init()

clock = pygame.time.Clock()
FPS = 60
clock.tick(FPS)
dt = 0

height = 800
width = 1000

config = SettingsAndLevelParser.Config(r"Data\config.dat", r"Data\elementAlias.dat")
screen = pygame.display.set_mode((1000, 800), display=0) # For borderless, use pygame.NOFRAME
# pygame.display.toggle_fullscreen()



done = False
transparent = (255, 0, 128)# Transparency color
dark_red = (139, 0, 0)
sky = "#02bdf4"

bg = background.Background(screen, sky, r"Textures\TextureData\Clouds", (width, height))


level1 = SettingsAndLevelParser.Level(r"Levels\level1.dat").map
level2 = SettingsAndLevelParser.Level(r"Levels\level2.dat").map
LevelDisplay = levelRenderer.LevelRenderer(screen, int(config.config["tilesize"]),
                                           int(config.config["size_X"]), int(config.config["size_Y"]), 
                                           int(config.config["screen_X"]), int(config.config["screen_Y"]), 
                                           level1, config.alias, r"Textures\TextureData")

LevelDisplay2 = levelRenderer.LevelRenderer(screen, int(config.config["tilesize"]),
                                            int(config.config["size_X"]), int(config.config["size_Y"]), 
                                           int(config.config["screen_X"]), int(config.config["screen_Y"]),
                                           level2, config.alias, r"Textures\TextureData")


player = PlayerCharacter.Player(screen, int(config.config["tilesize"]), 200, 500, float(config.config["gravity"]), 500, 63, config.parseConfig(r"Data\controls.dat"), r"Textures\TextureData\playerCharacter", clock, FPS)

windows:list[CustomRenderWindowAbsolute.WindowAbsolute] = []

levelZero:CustomLevel.Level = CustomLevel.Level(screen, level1, (4, 12), (17, 13), 10, 10, LevelDisplay, clock, config, FPS)
levelOne:CustomLevel.Level = CustomLevel.Level(screen, level1, (4, 12), (17, 13), 1, 1, LevelDisplay, clock, config, FPS)
levelTwo:CustomLevel.Level = CustomLevel.Level(screen, level2, (4, 12), (10, 12), 1, 1, LevelDisplay2, clock, config, FPS)

levels:list[CustomLevel.Level] = [levelZero, levelOne, levelTwo]

activeLevel = 0

tilesize = levels[activeLevel].renderer.tilesize
levelOne.addEnemy(10*tilesize, 13*tilesize-20, 5, 150)

# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)

def DoPlayerMovementAndKeys(keys):
    global done
    global activeLevel
    anim = player.currentAnimation
    x = player.x
    currentColliders = player.doCollisions(collisions)[1]
    if keys["left"] and player.grounded == True:
        player.x -= player.speed * dt
        checkHorizontalCollisions(x, currentColliders)
        player.lookLeft()
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.currentAnimation = player.running
        
    if keys["left"] and player.grounded == False:
        player.x -= player.speed * dt
        checkHorizontalCollisions(x, currentColliders)
        player.lookLeft()
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.currentAnimation = player.falling
    if keys["right"] and player.grounded == True:
        player.x += player.speed * dt
        checkHorizontalCollisions(x, currentColliders)
        player.lookRight()
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.currentAnimation = player.running
    if keys["right"] and player.grounded == False:
        player.x += player.speed * dt
        checkHorizontalCollisions(x, currentColliders)
        player.lookRight()
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.currentAnimation = player.falling

    if keys["right"] == False and keys["left"] == False and player.grounded == True:
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.idle.lookdir = player.currentAnimation.lookdir
        player.currentAnimation = player.idle
    
    if keys["right"] == False and keys["left"] == False and player.grounded == False and player.currentAnimation != player.falling:
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.falling.lookdir = player.currentAnimation.lookdir
        player.currentAnimation = player.falling

    if keys["jump"] == True and player.grounded == True:
        player.jump(dt)
        player.grounded = False
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.falling.lookdir = player.currentAnimation.lookdir
        player.currentAnimation = player.falling
        player.currentAnimation.resetAnimation()
    
    if keys["right"] == True and keys["left"] == True and player.grounded == True:
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.idle.lookdir = player.currentAnimation.lookdir
        player.currentAnimation = player.idle
    
    if keys["right"] == True and keys["left"] == True and player.grounded == False:
        for elt in player.animations:
            elt.x = player.x
            elt.y = player.y
        player.falling.lookdir = player.currentAnimation.lookdir
        player.currentAnimation = player.falling

    if player.x <= 0:
            player.x += player.speed * dt

    if anim != player.currentAnimation:
        player.currentAnimation.resetAnimation()

    if keys["exit"]:
        done = True

def checkHorizontalCollisions(x, currentColliders):
    try:
        if player.doCollisions(collisions)[0] == True and player.grounded == True:
            if len(player.doCollisions(collisions)[1]) >= len(currentColliders)+2:
                player.x = x
        elif player.doCollisions(collisions)[0] == True and player.grounded == False:
                player.x = x
    except:
        pass


def transition():
    transitionDone = False
    font = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 45)
    win_abs  = font.render("You won !", True, (255, 255, 255))
    
    smallfont = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 20)

    button_surface = pygame.Surface((200, 75))
    button_game = pygame.Rect(width/2-100, height/4+150, 200, 75)
    button_game_text = smallfont.render("Next Level", True, (255, 255, 255))
    button_game_text_rect = button_game_text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))

    button_surface_quit = pygame.Surface((200, 75))
    button_quit = pygame.Rect(width/2-100, height/4+400, 200, 75)
    button_quit_text = smallfont.render("Exit game", True, (255, 255, 255))
    button_quit_text_rect = button_game_text.get_rect(center=(button_surface_quit.get_width()/2, button_surface_quit.get_height()/2))
    
    button_surface.blit(button_game_text, button_game_text_rect)
    button_surface_quit.blit(button_quit_text, button_quit_text_rect)
    

    while not transitionDone:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_game.collidepoint(event.pos):
                    transitionDone = True
                if button_quit.collidepoint(event.pos):
                    exit()    
                    


        screen.fill("#02bdf4")
        screen.blit(win_abs, (width/2-8*24, height/4))
        screen.blit(button_surface, (button_game.x, button_game.y))
        screen.blit(button_surface_quit, (button_quit.x, button_quit.y))
        pygame.display.flip()

def nextLevel():
    global activeLevel
    global tilesize
    global windows

    levels[activeLevel].naw = levels[activeLevel].startingnaw
    levels[activeLevel].nrw = levels[activeLevel].startingnrw

    copy = False

    activeLevel += 1
    if activeLevel == len(levels):
        activeLevel = 0

    windows = []
    player.x = levels[activeLevel].startX*tilesize
    player.y = levels[activeLevel].startY*tilesize
    player.vY = 0

    transition()

tilesize = levels[activeLevel].renderer.tilesize

def menu():
    menuDone = False
    font = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 45)
    win_abs  = font.render("Windario", True, (255, 255, 255))
    
    smallfont = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 20)

    button_surface = pygame.Surface((200, 75))
    button_game = pygame.Rect(width/2-100, height/4+150, 200, 75)
    button_game_text = smallfont.render("Play game", True, (255, 255, 255))
    button_game_text_rect = button_game_text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))

    button_surface_quit = pygame.Surface((200, 75))
    button_quit = pygame.Rect(width/2-100, height/4+400, 200, 75)
    button_quit_text = smallfont.render("Quit", True, (255, 255, 255))
    button_quit_text_rect = button_game_text.get_rect(center=(button_surface_quit.get_width()/2, button_surface_quit.get_height()/2))
    
    button_surface.blit(button_game_text, button_game_text_rect)
    button_surface_quit.blit(button_quit_text, button_quit_text_rect)
    

    while not menuDone:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_game.collidepoint(event.pos):
                    menuDone = True
                if button_quit.collidepoint(event.pos):
                    exit()


        screen.fill("#02bdf4")
        screen.blit(win_abs, (width/2-8*24, height/4))
        screen.blit(button_surface, (button_game.x, button_game.y))
        screen.blit(button_surface_quit, (button_quit.x, button_quit.y))
        pygame.display.flip()
            
def restart():
    restartDone = False
    font = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 45)
    win_abs  = font.render("You died !", True, (255, 255, 255))
    
    smallfont = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 20)

    button_surface = pygame.Surface((200, 75))
    button_game = pygame.Rect(width/2-100, height/4+150, 200, 75)
    button_game_text = smallfont.render("Try Again ?", True, (255, 255, 255))
    button_game_text_rect = button_game_text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))

    button_surface_quit = pygame.Surface((200, 75))
    button_quit = pygame.Rect(width/2-100, height/4+400, 200, 75)
    button_quit_text = smallfont.render("Give up", True, (255, 255, 255))
    button_quit_text_rect = button_game_text.get_rect(center=(button_surface_quit.get_width()/2, button_surface_quit.get_height()/2))
    
    button_surface.blit(button_game_text, button_game_text_rect)
    button_surface_quit.blit(button_quit_text, button_quit_text_rect)
    

    while not restartDone:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_game.collidepoint(event.pos):
                    restartDone = True
                if button_quit.collidepoint(event.pos):
                    exit()


        screen.fill("#02bdf4")
        screen.blit(win_abs, (width/2-8*24, height/4))
        screen.blit(button_surface, (button_game.x, button_game.y))
        screen.blit(button_surface_quit, (button_quit.x, button_quit.y))
        pygame.display.flip()

menu()

player.x = levels[activeLevel].startX*tilesize
player.y = levels[activeLevel].startY*tilesize
player.vY = 0
copy = False
copyfont = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 30)
win_abs  = copyfont.render("You are in copy mode.", True, (255, 255, 255))
mousepos = [500, 500]
mouseClicked = False
selectedTile = []
selectedTile2 = []
hoveredTile = []
displacementMode = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and levels[activeLevel].naw > 0:
                copy = not copy
        if event.type == pygame.MOUSEMOTION:
            mousepos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and selectedTile == []:
            selectedTile = hoveredTile
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and selectedTile != []:
            selectedTile2 = hoveredTile
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 2 and copy == True and displacementMode == False) or (event.type == pygame.KEYDOWN and event.key == pygame.K_r and copy == True and displacementMode == False and selectedTile != []):
            selectedTile = []
            selectedTile2 = []
            copy = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and copy == True and displacementMode == True:
            displacementMode = False
            selectedTile = []
            selectedTile2 = []

    if (copy and levels[activeLevel].naw > 0) or (copy and displacementMode == True and levels[activeLevel].naw == 0):

        
        for elt in windows:
            elt.fill(sky)
        bg.renderBackground()

        for elt in windows:
            elt.drawWindow()

        levels[activeLevel].render()



        if player.keys()["exit"]:
            done = True

        screen.blit(win_abs, (100, 10))
        
        mouseX = mousepos[0]
        mouseY = mousepos[1]
        hoveredTile = [round((mouseX-25)/tilesize), round((mouseY-25)/tilesize)]
        if displacementMode == False:
            if selectedTile != [] and selectedTile2 == []:
                if hoveredTile[0] < selectedTile[0]:
                    hoveredTile[0] = selectedTile[0]
                if hoveredTile[1] < selectedTile[1]:
                    hoveredTile[1] = selectedTile[1]
            if selectedTile == []:
                pygame.draw.rect(screen, "yellow", (hoveredTile[0]*tilesize, hoveredTile[1]*tilesize, 50, 50))
            elif selectedTile != [] and selectedTile2 == []:
                pygame.draw.rect(screen, "yellow", (selectedTile[0]*tilesize, selectedTile[1]*tilesize, 50, 50))   
                pygame.draw.rect(screen, "yellow", (hoveredTile[0]*tilesize, hoveredTile[1]*tilesize, 50, 50)) 
            elif selectedTile != [] and selectedTile2 != []:
                LevelDisplay3 = levelRenderer.LevelRenderer(screen, int(config.config["tilesize"]),
                                            int(config.config["size_X"]), int(config.config["size_Y"]), 
                                            int(config.config["screen_X"]), int(config.config["screen_Y"]), 
                                            level1, config.alias, r"Textures\TextureData")
                
                windows.append(CustomRenderWindowAbsolute.WindowAbsolute((selectedTile[0], selectedTile[1]), (selectedTile2[0]-selectedTile[0]+1, selectedTile2[1]-selectedTile[1]+1),
                                                                        tilesize, levels[activeLevel].renderer, screen, (selectedTile[0]*-1, selectedTile[1]*-1)))
                selectedTile, selectedTile2, levels[activeLevel].naw = [], [], levels[activeLevel].naw - 1
                displacementMode = True
        elif displacementMode == True:
            windows[-1].offX, windows[-1].offY = hoveredTile[0]-windows[-1].sizeX+1-windows[-1].posX, hoveredTile[1]-windows[-1].sizeY+1-windows[-1].posY
            windows[-1].update()
    else:
        collisions = []

        for elt in windows:
            elt.fill(sky)

        bg.renderBackground()

        
        
    
        for enemy in levels[activeLevel].enemies:
            enemy.update()
            enemy.animation.frame_time += dt
            if(enemy.isColliding(pygame.Rect(player.x+10, player.y+10, 30, 30))):
                restart()
                levels[activeLevel].reload()
                player.x = levels[activeLevel].startX*tilesize
                player.y = levels[activeLevel].startY*tilesize
                player.vY = 0

        collisions += levels[activeLevel].renderer.collisions
        
        for elt in windows:
            elt.drawWindow()
            col = elt.collisions
            collisions += [alt for alt in col if alt not in collisions]
        levels[activeLevel].render()

        if(player.doCollisions([pygame.Rect(levels[activeLevel].endX*tilesize-10, levels[activeLevel].endY*tilesize, tilesize+20, tilesize)])[1]) != 0:
            nextLevel()

        player.update(dt, collisions)

        player.idleAnimation()

        DoPlayerMovementAndKeys(player.keys())
    dt = clock.tick(FPS)/1024
    pygame.display.flip()
    