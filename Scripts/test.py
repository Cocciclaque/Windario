import pygame
import win32api
import win32gui
import win32con


pygame.init()


screen = pygame.display.set_mode((1920, 1080))

subwindow = screen.subsurface((500, 100, 500, 900))

transparent = (255, 0, 128)
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)


x=500
y=100

xoff = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                x-=50
                xoff-=50
                subwindow = screen.subsurface((x, y, 500, 900))
            if event.key == pygame.K_d:
                x+=50
                xoff+=50
                subwindow = screen.subsurface((x, y, 500, 900))
            
    screen.fill(transparent)
    image = pygame.image.load(r"Textures\tile000.png").convert_alpha()
    imageblit = pygame.transform.scale(image, (200, 200))
    subwindow.fill("red")

    subwindow.blit(imageblit, (100-xoff, 100))
    subwindow.blit(imageblit, (300-xoff, 100))
    subwindow.blit(imageblit, (700-xoff, 100))

    pygame.display.flip()