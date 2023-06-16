import pygame
import random
import sys

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, BULLET, BULLET_ENEMY

from game.components.spaceship import SpaceShip
from game.components.enemy_spaceship import Enemy
from game.components.bullet import Bullet




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
        self.enemy_2 = Enemy(400, 50)
        # bullet of the spaceship
        self.bullet_spaceship = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y, BULLET)
        self.bullet_enemy = Bullet(self.enemy.image_rect.centerx, self.enemy.image_rect.bottom, BULLET_ENEMY)
        #enemy firing frequency
        self.enemy_firing_frequency = None
        #variables Game Over
        self.game_over = False
        self.restart_status = False
        self.deaths = 0
        self.impacts = 0
        # Text font
        self.font = pygame.font.Font(None, 36)
        #Color
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.game_over_text = None
        self.restart_text = None
        self.deaths_text = None 
        self.restart = False

    def run(self):
        # Game loop: events - update - draw
        self.playing = True

        # while self.playing == True
        while self.playing: # Mientras el atributo playing (self.playing) sea true "repito"
            
            self.handle_events()
            self.update()
            self.draw()
            if self.game_over:
                self.game_over_screen()
            #pygame.display.update()
            
            #self.game_over(self.game_over_status)
        else:
            print("Something ocurred to quit the game!!!")


        
            
            
            

    def handle_events(self):
        # Para un "event" (es un elemento) en la lista (secuencia) que me retorna el metodo get()
        
        for event in pygame.event.get():
            # si el "event" type es igual a pygame.QUIT entonces cambiamos playing a False
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                sys.exit()
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
                    #bullet = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y)
                    #bullets.append(bullet)
                    #self.shoot(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y)
                    self.spaceship.shoot(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y)
                if event.key == pygame.K_r:
                    self.restart = True
                    self.game_over = False
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
        self.enemy.update()
        self.enemy_2.update()
        self.bullet_spaceship.shoot_eliminate(self.enemy, self.spaceship.bullets, 10, 1)
        self.bullet_spaceship.shoot_eliminate(self.enemy_2, self.spaceship.bullets, 10, 1)
        self.shoots_enemys(self.enemy)
        self.bullet_enemy.shoot_eliminate(self.spaceship, self.enemy.bullets, -20, 5)
        
        #if self.spaceship.image_rect is None:
        #    self.game_over = True

        print("esto es la variable game", self.game_over)
        
        
    def shoots_enemys(self, variable_enemy):
        self.enemy_firing_frequency = random.randint(0, 100)
        if variable_enemy.image_rect is not None and self.enemy_firing_frequency < 50:
            self.enemy.shoot(self.enemy.image_rect.centerx, self.enemy.image_rect.bottom)
            print(self.enemy_firing_frequency)
            # Comprobar colisión con la bala 
                
        else:
            #print("Continue")
            pass
    

        """ for bullet in bullets:
            bullet.update()
            if bullet.image_rect.top <= 0: 
                bullets.remove(bullet)
        
        for bullet in bullets:
            if self.enemy.image_rect is not None and bullet.image_rect.colliderect(self.enemy.image_rect):
                bullets.remove(bullet)
                self.enemy.image_rect = None
            elif self.enemy_2.image_rect is not None and bullet.image_rect.colliderect(self.enemy_2.image_rect):
                bullets.remove(bullet)
                self.enemy_2.image_rect = None """
        
    def game_over_screen(self):
        
        self.game_over_text = self.font.render("Game Over", True, self.RED)
        self.restart_text = self.font.render("Presiona 'R' para reiniciar", True, self.RED)
        self.deaths_text = self.font.render("Death Count: " + str(self.deaths), True, self.RED)
        self.screen.fill(self.WHITE)
        self.screen.blit(self.game_over_text, (SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2, 200))
        self.screen.blit(self.restart_text, (SCREEN_WIDTH // 2 - self.restart_text.get_width() // 2, 250))
        self.screen.blit(self.deaths_text, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 300))
        pygame.display.flip()
        
            
        
    
    def restart_game(self):
        self.restart = False
        self.deaths = 0
        self.impac = 0
        self.spaceship.bullets.clear()
        self.enemy.bullets.clear()
        self.spaceship.reset()
        
            


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()



        # dibujamos el objeto en pantalla
        if self.spaceship.image_rect is not None:
            self.screen.blit(self.spaceship.image, (self.spaceship.image_rect.x, self.spaceship.image_rect.y))

        # display the enemy spaceship in its current position 
        if self.enemy.image_rect is not None:
            self.screen.blit(self.enemy.image, self.enemy.image_rect)
        if self.enemy_2.image_rect is not None:
                self.screen.blit(self.enemy_2.image, self.enemy_2.image_rect)
        
        # show the positions of the bullets 
        for bullet in self.spaceship.bullets:
            self.screen.blit(bullet.image, bullet.image_rect)
        for bullet in self.enemy.bullets:
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
