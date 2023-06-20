import pygame
import random
import sys

from game.utils.constants import ICON, TITLE, BULLET, BULLET_ENEMY, ENEMY_1, ENEMY_2
from game.components.spaceship import SpaceShip
from game.components.enemy_spaceship import Enemy
from game.components.bullet import Bullet
from game.components.draw_game import Draw_game

# Game tiene un "Spaceship" - Por lo general esto es iniciliazar un objeto Spaceship en el __init__
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.playing = False  # variable de control para salir del ciclo
        # Game tiene un "Spaceship"
        self.spaceship = SpaceShip()
        #Game has a enemy 
        self.enemys = [Enemy(500, 50, ENEMY_1), Enemy(400, 50, ENEMY_1), 
                        Enemy(300, 50,ENEMY_1), Enemy(200, 50, ENEMY_1), Enemy(100, 50, ENEMY_1), 
                        Enemy(100, 150, ENEMY_2), Enemy(200, 150, ENEMY_2), Enemy(300, 150, ENEMY_2),
                        Enemy(400, 150, ENEMY_2), Enemy(500, 150, ENEMY_2)]
        # bullet of the spaceship
        self.bullet_spaceship = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y, BULLET)
        # bullet of the enemy
        self.enemy_bullets = []
        for enemy_iter in self.enemys:
            self.enemy_bullets.append(Bullet(enemy_iter.image_rect.centerx, enemy_iter.image_rect.bottom, BULLET_ENEMY))
        #enemy firing frequency
        self.enemy_firing_frequency = None
        #variables Game Over
        self.game_over = None
        self.restart = False
        self.draw_game = Draw_game()
        self.win = None
        #sound
        #self.SOUND_SHOOT = pygame.mixer.Sound("Other\laser5.ogg")

    def run(self):
        # Game loop: events - update - draw
        self.playing = True

        # while self.playing == True
        while self.playing: # Mientras el atributo playing (self.playing) sea true "repito"
            
            if self.spaceship.image_rect is None:
                self.game_over = True
            
            if self.spaceship.score == len(self.enemys):
                self.win = True

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
                    #self.SOUND_SHOOT.play()
                elif event.key == pygame.K_RETURN:
                    self.win = True
                    print("you push enter")
                elif event.key == pygame.K_r:
                    if self.game_over:
                        self.restart_game()
                        self.game_over = False
                    if self.win:
                        self.restart_game()
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
        self.bullet_spaceship.update_bullet(self.spaceship.bullets,10)
        for iter_enemys in range(len(self.enemys)):
            self.shoots_enemys(self.enemys[iter_enemys])
            self.enemy_bullets[iter_enemys].update_bullet(self.enemys[iter_enemys].bullets, -20)
            self.spaceship.detect_impact_bullet(self.enemys[iter_enemys].bullets, self.spaceship, 5)

        for enemy in self.enemys:
            enemy.update()

        self.spaceship.delete_enemys(self.spaceship.bullets, self.enemys)
        for power in self.spaceship.list_power_up:
            power.update()
            if self.spaceship.image_rect is not None and self.spaceship.image_rect.colliderect(power.shield_image_rect):
                if not self.spaceship.has_shield:  
                    self.spaceship.list_power_up.remove(power)
                    self.spaceship.activate_shield()

                
    def shoots_enemys(self, variable_enemy):
        self.enemy_firing_frequency = random.randint(0, 100)
        if variable_enemy.image_rect is not None and self.enemy_firing_frequency < 1:
            variable_enemy.shoot(variable_enemy.image_rect.centerx, variable_enemy.image_rect.bottom)

    def restart_game(self):
        self.game_over = False
        self.impacts = 0
        self.shiel_protection = 0
        self.win = False
        self.spaceship = SpaceShip()
        self.enemys = [Enemy(500, 50, ENEMY_1), Enemy(400, 50, ENEMY_1), 
                        Enemy(300, 50,ENEMY_1), Enemy(200, 50, ENEMY_1), Enemy(100, 50, ENEMY_1), 
                        Enemy(100, 150, ENEMY_2), Enemy(200, 150, ENEMY_2), Enemy(300, 150, ENEMY_2),
                        Enemy(400, 150, ENEMY_2), Enemy(500, 150, ENEMY_2)]
        self.bullet_spaceship = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.y, BULLET)
        self.enemy_bullets = []
        for enemy_iter in range(len(self.enemys)):
            self.enemy_bullets.append(Bullet(self.enemys[enemy_iter].image_rect.centerx, self.enemys[enemy_iter].image_rect.bottom, BULLET_ENEMY))
            
    def draw(self):
        self.draw_game.draw(self.spaceship, self.enemys, self.game_over, self.win)
