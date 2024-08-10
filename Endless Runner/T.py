import pygame

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")

timer = pygame.time.Clock()
FPS = 60

layer = pygame.Rect(50, 5, 5, 50)
img = pygame.image.load("Assets\\btn\\ok.png")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    screen.blit(img,layer)
    timer.tick(FPS)
