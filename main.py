import pygame, sys, random

#Configuración inicial
pygame.init()
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#Clases 
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

    def screen_constrain(self):
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        elif self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()

# Variables generales
spaceship = SpaceShip('spaceship/assets/spaceship.png', screen_width/2, 500, 10)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((40, 38, 42))

    spaceship_group.draw(screen)
    spaceship_group.update()

    pygame.display.update()
    clock.tick(120)