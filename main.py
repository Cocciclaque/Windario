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


level = SettingsAndLevelParser.Level(r"Levels\level1.dat").map
level2 = SettingsAndLevelParser.Level(r"Levels\level2.dat").map
LevelDisplay = levelRenderer.LevelRenderer(screen, 
                                           int(config.config["size_X"]), int(config.config["size_Y"]), 
                                           int(config.config["screen_X"]), int(config.config["screen_Y"]), 
                                           level, config.alias)

LevelDisplay2 = levelRenderer.LevelRenderer(screen,
                                            int(config.config["size_X"]), int(config.config["size_Y"]), 
                                           int(config.config["screen_X"]), int(config.config["screen_Y"]),
                                           level2, config.alias)

window = CustomRenderWindowRelative.WindowRelative((500, 0), (200, 200), LevelDisplay, screen)
window2 = CustomRenderWindowRelative.WindowRelative((700, 0), (300, 200), LevelDisplay2, screen)

player = PlayerCharacter.Player(screen, 200, 500, float(config.config["gravity"]), 500, config.parseConfig(r"Data\controls.dat"), r"Textures\TextureData\playerCharacter", clock, FPS)

# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)

def DoPlayerMovementAndKeys(keys):
    global done
    if keys["left"]:
        player.x -= player.speed * dt
        player.lookLeft()
        player.notIdle()
    if keys["left"] and player.currentAnimation != player.running:
        player.chooseAnimation(player.running)
        player.notIdle()
    if keys["right"]:
        player.x += player.speed * dt
        player.lookRight()
        player.notIdle()
    if keys["right"] and player.currentAnimation != player.running:
        player.chooseAnimation(player.running)
        player.notIdle()
    if keys["left"] == False and keys["right"] == False and player.currentAnimation == player.running:
        player.Playidle()
     

    if keys["exit"]:
        done = True

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

    
    screen.fill(transparent)

    # window.fill("lightblue")
    # window2.fill("darkblue")
    # window.drawWindow()
    LevelDisplay.renderGround()
    # window2.drawWindow()

    player.update(dt)
    
    
    if player.currentAnimation != player.idle:
        player.idle.animate()

    player.idleAnimation()

    DoPlayerMovementAndKeys(player.keys(dt))

    dt = clock.tick(FPS)/1024
    pygame.display.flip()