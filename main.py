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
import time
pygame.init()

clock = pygame.time.Clock()
FPS = 60
clock.tick(FPS)
dt = 0

config = SettingsAndLevelParser.Config(r"Data\config.dat", r"Data\elementAlias.dat")
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME, display=0) # For borderless, use pygame.NOFRAME
# pygame.display.toggle_fullscreen()


pygame.display.toggle_fullscreen()

done = False
transparent = (255, 0, 128)# Transparency color
dark_red = (139, 0, 0)


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

window = CustomRenderWindowRelative.WindowRelative((10, 6), (4, 4), int(config.config["tilesize"]), LevelDisplay, screen)
window2 = CustomRenderWindowRelative.WindowRelative((8, 6), (8, 6), int(config.config["tilesize"]), LevelDisplay2, screen)

player = PlayerCharacter.Player(screen, int(config.config["tilesize"]), 200, 500, float(config.config["gravity"]), 500, 63, config.parseConfig(r"Data\controls.dat"), r"Textures\TextureData\playerCharacter", clock, FPS)

windows = [window, window2]


levelOne:CustomLevel.Level = CustomLevel.Level(screen, level1, (4, 10), (27, 13), 1, 1, LevelDisplay, clock, config, FPS)
levelTwo:CustomLevel.Level = CustomLevel.Level(screen, level2, (4, 5), (10, 12), 0, 0, LevelDisplay2, clock, config, FPS)

levels:list[CustomLevel.Level] = [levelOne, levelTwo]

activeLevel = 0


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

    if keys["switch"]:
        nextLevel()

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


def nextLevel():
    global activeLevel
    activeLevel += 1
    if activeLevel == len(levels):
        activeLevel = 0

    player.x = levels[activeLevel].startX*levels[activeLevel].renderer.tilesize
    player.y = levels[activeLevel].startY*levels[activeLevel].renderer.tilesize
    player.vY = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            pass
            # if event.key == pygame.K_ESCAPE:
            #     done = True
            # if event.key == pygame.K_q:
            #     window.moveLeft()
            #     window2.moveLeft()
            # if event.key == pygame.K_d:
            #     window.moveRight()
            #     window2.moveRight()
            # if event.key == pygame.K_z:
            #     window.moveUp()
            #     window2.moveUp()
            # if event.key == pygame.K_s:
            #     window.moveDown()
            #     window2.moveDown()

    collisions = []

    
    screen.fill(transparent)
    # window2.fill("darkblue")
    # window2.drawWindow()
    # window.fill("lightblue")
    # window.drawWindow()
    
    levels[activeLevel].render()
    levels[activeLevel].tick(dt)

    collisions += levels[activeLevel].renderer.collisions + window2.collisions + window.collisions

    if(player.doCollisions([pygame.Rect(levels[activeLevel].endX*levels[activeLevel].renderer.tilesize-10, levels[activeLevel].endY*levels[activeLevel].renderer.tilesize, levels[activeLevel].renderer.tilesize+20, levels[activeLevel].renderer.tilesize)])[1]) != 0:
        nextLevel()

    player.update(dt, collisions)

    player.idleAnimation()

    DoPlayerMovementAndKeys(player.keys(dt))

    dt = clock.tick(FPS)/1024
    pygame.display.flip()