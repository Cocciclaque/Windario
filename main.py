import pygame
import win32api
import win32con
import win32gui
import Scripts.SettingsAndLevelParser as SettingsAndLevelParser
import Scripts.levelRenderer as levelRenderer

pygame.init()

config = SettingsAndLevelParser.Config(r"Data\config.dat", r"Data\elementAlias.dat")
screen = pygame.display.set_mode((int(config.config["screen_X"]), int(config.config["screen_Y"]))) # For borderless, use pygame.NOFRAME
done = False
transparent = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)


level = SettingsAndLevelParser.Level(r"Levels\level1.dat").map
LevelDisplay = levelRenderer.LevelRenderer(screen, 
                                           int(config.config["size_X"]), int(config.config["size_Y"]), 
                                           int(config.config["screen_X"]), int(config.config["screen_Y"]), 
                                           level, config.alias)





# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True


    screen.fill(transparent) 
    LevelDisplay.renderGround()
    pygame.draw.rect(screen, pygame.color.Color(255, 0, 0), ((50, 50, 50, 50)))

    pygame.display.update()