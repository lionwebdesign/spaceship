import pygame, sys, random

#Configuración inicial
pygame.init()
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
game_font = pygame.font.Font(None, 40)
light_grey = (200, 200, 200)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

#Clases 
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.shield_surface = pygame.image.load('spaceship/assets/shield.png')
        self.escudos = 5

    def screen_constrain(self):
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        elif self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def display_escudo(self):
        for index, escudo in enumerate(range(self.escudos)):
            screen.blit(self.shield_surface, (10 + index * 40, 10))

    def get_damage(self, damage_amount):
        self.escudos -= damage_amount

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_escudo()

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
        if self.rect.centery >= screen_width + 100:
            self.kill()


    def update(self):
        self.movimiento_meteoro()

class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def trayectoria_laser(self):
        self.rect.centery -= self.speed
        if self.rect.centery <= -50:
            self.kill()

    def update(self):
        self.trayectoria_laser()

# Variables generales
# Nave
spaceship = SpaceShip('spaceship/assets/spaceship.png', screen_width/2, 500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)
# Meteoro
meteoros_group = pygame.sprite.Group()
METEOROS_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOROS_EVENT, 500)
#Laser
laser_group = pygame.sprite.Group()
#laser_timer = 0
#score 
score = 0

def puntaje():
    superficie_score = game_font.render(f'Puntuación: {score}', True, light_grey) 
    score_rect = superficie_score.get_rect(center = (screen_width/2, screen_height/2 + 40))
    screen.blit(superficie_score, score_rect)

def meteoros_setup():
    meteoro_path = random.choice(('spaceship/assets/Meteor1.png', 'spaceship/assets/Meteor2.png', 'spaceship/assets/Meteor3.png'))
    random_x_pos = random.randrange(0, screen_width)
    random_y_pos = random.randrange(-1500, -50)
    random_x_speed = random.randrange(-1, 1)
    random_y_speed = random.randrange(3, 7)
    meteoro = Meteoro(meteoro_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
    meteoros_group.add(meteoro)

def restart_setup():
    global score
    spaceship_group.sprite.escudos = 5
    meteoros_group.empty()
    score = 0

def main_game():
    laser_group.draw(screen)
    spaceship_group.draw(screen)
    meteoros_group.draw(screen)

    laser_group.update()
    spaceship_group.update()
    meteoros_group.update()

    #Colisiones
    #Nave y Meteoros
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteoros_group, True):
        spaceship_group.sprite.get_damage(1)
    #Laser y Meteoros
    for laser in laser_group:
        pygame.sprite.spritecollide(laser, meteoros_group, True)

    superficie_score = game_font.render(f'{score}', True, light_grey) 
    score_rect = superficie_score.get_rect(center = (screen_width - 50, 30))
    screen.blit(superficie_score, score_rect)

    return 1

def end_game():
    superficie_texto = game_font.render('Game Over', True, light_grey) 
    texto_rect = superficie_texto.get_rect(center = (screen_width/2, screen_height/2))
    screen.blit(superficie_texto, texto_rect)

    puntaje()

def loop_setup():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == METEOROS_EVENT:
            meteoros_setup()
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_laser_shot = Laser('spaceship/assets/Laser.png', event.pos, 15)
            laser_group.add(new_laser_shot)
        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.escudos <= 0:
            restart_setup()
            
    screen.fill((40, 38, 42))

while True:
    loop_setup()

    if spaceship_group.sprite.escudos > 0:
        score += main_game()
    else:
        end_game()
    

    pygame.display.update()
    clock.tick(120)