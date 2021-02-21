import pygame, sys, random

#Configuración inicial
pygame.init()
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mouse.set_visible(False)
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

class Meteoro(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def movimiento_meteoro(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed


    def update(self):
        self.movimiento_meteoro()

# Variables generales
# Nave
spaceship = SpaceShip('spaceship/assets/spaceship.png', screen_width/2, 500, 10)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)
# Meteoro
meteoros_group = pygame.sprite.Group()

METEOROS_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOROS_EVENT, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == METEOROS_EVENT:
            meteoro_path = random.choice(('spaceship/assets/Meteor1.png', 'spaceship/assets/Meteor2.png', 'spaceship/assets/Meteor3.png'))
            random_x_pos = random.randrange(0, screen_width)
            random_y_pos = random.randrange(-1500, -50)
            random_x_speed = random.randrange(-1, 1)
            random_y_speed = random.randrange(3, 7)
            meteoro = Meteoro(meteoro_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
            meteoros_group.add(meteoro)
    
    screen.fill((40, 38, 42))

    spaceship_group.draw(screen)
    spaceship_group.update()

    meteoros_group.draw(screen)
    meteoros_group.update()

    pygame.display.update()
    clock.tick(120)