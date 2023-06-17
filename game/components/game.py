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
        self.enemys = [Enemy(500, 50), Enemy(400, 50)]
        # bullet of the spaceship
        self.bullet_spaceship = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y, BULLET)
        # bullet of the enemy
        self.enemy_bullets = []
        for enemy_iter in range(0,2):
            self.enemy_bullets.append(Bullet(self.enemys[enemy_iter].image_rect.centerx, self.enemys[enemy_iter].image_rect.bottom, BULLET_ENEMY))
        
        #enemy firing frequency
        self.enemy_firing_frequency = None
        #variables Game Over
        self.game_over = None
        self.deaths = 0
        self.impacts = 0
        # Text font
        self.font = pygame.font.Font(None, 36)
        #Color
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.game_over_text = None
        self.restart_text = None
        self.deaths_text = None 
        self.bullet_count = None
        self.score_text = None
        self.restart = False

    def run(self):
        # Game loop: events - update - draw
        self.playing = True

        # while self.playing == True
        while self.playing: # Mientras el atributo playing (self.playing) sea true "repito"
            
            if self.spaceship.image_rect is None:
                self.game_over = True
                
                
                
            self.handle_events()
            self.update()
            self.draw()
            
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
                elif event.key == pygame.K_UP:  
                    self.spaceship.move_up = True
                elif event.key == pygame.K_DOWN:  
                    self.spaceship.move_down = True
                elif event.key == pygame.K_x and self.spaceship.image_rect is not None:
                    self.spaceship.shoot(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y)
                elif event.key == pygame.K_r:
                    if self.game_over:
                        self.restart_game()
                        self.game_over = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right = False
                elif event.key == pygame.K_UP:  
                    self.spaceship.move_up = False
                elif event.key == pygame.K_DOWN: 
                    self.spaceship.move_down = False
            

    def update(self):
        # pass
        self.spaceship.update()
        self.enemys[0].update()
        self.enemys[1].update()
        self.bullet_spaceship.shoot_eliminate(self.enemys[0], self.spaceship.bullets, 10, 1)
        self.bullet_spaceship.shoot_eliminate(self.enemys[1], self.spaceship.bullets, 10, 1)
        self.shoots_enemys(self.enemys[0])
        self.shoots_enemys(self.enemys[1])
        self.enemy_bullets[0].shoot_eliminate(self.spaceship, self.enemys[0].bullets, -20, 5)
        self.enemy_bullets[1].shoot_eliminate(self.spaceship, self.enemys[1].bullets, -20, 5)

        #print("esto es la variable game", self.game_over)
        
        
    def shoots_enemys(self, variable_enemy):
        self.enemy_firing_frequency = random.randint(0, 100)
        if variable_enemy.image_rect is not None and self.enemy_firing_frequency < 50:
            variable_enemy.shoot(variable_enemy.image_rect.centerx, variable_enemy.image_rect.bottom)
            #print(self.enemy_firing_frequency)
        else:
            #print("Continue")
            pass
    
        
    def game_over_screen(self):
        
        self.game_over_text = self.font.render("Game Over", True, self.GREEN)
        self.restart_text = self.font.render("Presiona 'R' para reiniciar", True, self.GREEN)
        self.deaths_text = self.font.render("Death Count: " + str(self.enemy_bullets[0].deaths), True, self.GREEN)
        self.bullet_count = self.font.render("Bullet Count: " + str(self.enemy_bullets[0].impact), True, self.GREEN)
        self.screen.fill(self.WHITE)
        self.screen.blit(self.game_over_text, (SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2, 200))
        self.screen.blit(self.restart_text, (SCREEN_WIDTH // 2 - self.restart_text.get_width() // 2, 250))
        self.screen.blit(self.deaths_text, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 300))
        self.screen.blit(self.bullet_count, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 350))

        
    
    def restart_game(self):
        self.game_over = False
        self.impacts = 0
        self.spaceship = SpaceShip()
        self.enemys = [Enemy(500, 50), Enemy(400, 50)]
        self.bullet_spaceship = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y, BULLET)
        self.enemy_bullets = []
        for enemy_iter in range(0, 2):
            self.enemy_bullets.append(Bullet(self.enemys[enemy_iter].image_rect.centerx, self.enemys[enemy_iter].image_rect.bottom, BULLET_ENEMY))
            
            


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()



        # dibujamos el objeto en pantalla
        if self.spaceship.image_rect is not None:
            self.screen.blit(self.spaceship.image, (self.spaceship.image_rect.x, self.spaceship.image_rect.y))

        # display the enemy spaceship in its current position 
        if self.enemys[0].image_rect is not None:
            self.screen.blit(self.enemys[0].image, self.enemys[0].image_rect)
        if self.enemys[1].image_rect is not None:
            self.screen.blit(self.enemys[1].image, self.enemys[1].image_rect)
        
        # show the positions of the bullets 
        for bullet in self.spaceship.bullets:
            self.screen.blit(bullet.image, bullet.image_rect)
        for bullet in self.enemys[0].bullets:
            self.screen.blit(bullet.image, bullet.image_rect)
        for bullet in self.enemys[1].bullets:
            self.screen.blit(bullet.image, bullet.image_rect)
        
        if self.game_over:
            self.game_over_screen()
            
            
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        #self.score_text = self.font.render("Score: " + str(self.bullet_enemy.impact), True, self.RED)
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed
