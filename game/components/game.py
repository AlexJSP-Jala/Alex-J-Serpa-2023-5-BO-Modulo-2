import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE

from game.components.spaceship import SpaceShip
from game.components.enemy_spaceship import Enemy
from game.components.bullet import Bullet, bullets




# Game tiene un "Spaceship" - Por lo general esto es iniciliazar un objeto Spaceship en el __init__
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False  # variable de control para salir del ciclo
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0

        # Game tiene un "Spaceship"
        self.spaceship = SpaceShip()
        #Game has a enemy 
        self.enemy = Enemy(500, 50)
        # bullet of the spaceship
        #self.bullet = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y )
        

    def run(self):
        # Game loop: events - update - draw
        self.playing = True

        # while self.playing == True
        while self.playing: # Mientras el atributo playing (self.playing) sea true "repito"
            self.handle_events()
            self.update()
            self.draw()
            #self.spaceship_movements()
            
        else:
            print("Something ocurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        
        # Para un "event" (es un elemento) en la lista (secuencia) que me retorna el metodo get()
        for event in pygame.event.get():
            # si el "event" type es igual a pygame.QUIT entonces cambiamos playing a False
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right = True
                elif event.key == pygame.K_UP:  # Nueva tecla agregada: flecha hacia arriba
                    self.spaceship.move_up = True
                elif event.key == pygame.K_DOWN:  # Nueva tecla agregada: flecha hacia abajo
                    self.spaceship.move_down = True
                elif event.key == pygame.K_x:
                    bullet = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y)
                    bullets.append(bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right = False
                elif event.key == pygame.K_UP:  # Nueva tecla agregada: flecha hacia arriba
                    self.spaceship.move_up = False
                elif event.key == pygame.K_DOWN:  # Nueva tecla agregada: flecha hacia abajo
                    self.spaceship.move_down = False
        

    def update(self):
        # pass
        self.spaceship.update()
        

        for bullet in bullets:
            bullet.update()
            if bullet.image_rect.bottom <= 0: 
                bullets.remove(bullet)
        
        for bullet in bullets:
            if self.enemy.image_rect is not None and bullet.image_rect.colliderect(self.enemy.image_rect):
                bullets.remove(bullet)
                self.enemy.image_rect = None

        self.enemy.update()
        


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        


        # dibujamos el objeto en pantalla
        self.screen.blit(self.spaceship.image, (self.spaceship.image_rect.x, self.spaceship.image_rect.y))
        # display the enemy spaceship in its current position 
        if self.enemy.image_rect is not None:
            self.screen.blit(self.enemy.image, self.enemy.image_rect)
        # show the positions of the bullets 
        for bullet in bullets:
            self.screen.blit(bullet.image, bullet.image_rect)
            


        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed
