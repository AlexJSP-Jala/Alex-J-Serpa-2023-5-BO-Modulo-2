import pygame
import random
import sys

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, BULLET, BULLET_ENEMY, ENEMY_1, ENEMY_2
from game.utils.constants import GAME_OVER
from game.components.spaceship import SpaceShip
from game.components.enemy_spaceship import Enemy
from game.components.bullet import Bullet
from game.components.shield import Shield_spaceship

# Game tiene un "Spaceship" - Por lo general esto es iniciliazar un objeto Spaceship en el __init__
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
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
        #Game shielf
        self.shield_spaceship = Shield_spaceship()
        #Game has a enemy 
        self.enemys = [Enemy(500, 50, ENEMY_1), Enemy(400, 50, ENEMY_1), 
                        Enemy(300, 50,ENEMY_1), Enemy(200, 50, ENEMY_1), Enemy(100, 50, ENEMY_1), 
                        Enemy(100, 150, ENEMY_2), Enemy(200, 150, ENEMY_2), Enemy(300, 150, ENEMY_2),
                        Enemy(400, 150, ENEMY_2), Enemy(500, 150, ENEMY_2)]
        self.enemy_gift = 0
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
        # Text font
        self.font = pygame.font.SysFont("Algerian", 60)
        self.font_score = pygame.font.Font(None, 30)
        #Color
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.game_over_text = None
        self.restart_text = None
        self.deaths_text = None 
        self.bullet_count = None
        self.score_text = None
        self.restart = False
        #sound
        #self.SOUND_SHOOT = pygame.mixer.Sound("Other\laser5.ogg")
        

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
                    #self.SOUND_SHOOT.play()
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
        self.shield_spaceship.update()
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

    def game_over_screen(self):
        self.game_over_text = self.font.render("GAME OVER", True, self.YELLOW)
        self.restart_text = self.font.render("Presiona 'R' para reiniciar", True, self.YELLOW)
        self.deaths_text = self.font.render("Death Count: " + str(self.spaceship.deaths), True, self.RED)
        self.bullet_count = self.font.render("Bullet Count: " + str(self.spaceship.impacts), True, self.BLACK)
        #self.screen.fill(self.WHITE)
        self.screen.blit(GAME_OVER, (0, 0))
        self.screen.blit(self.game_over_text, (SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2, 200))
        self.screen.blit(self.restart_text, (SCREEN_WIDTH // 2 - self.restart_text.get_width() // 2, 250))
        self.screen.blit(self.deaths_text, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 300))
        self.screen.blit(self.bullet_count, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 350))

    def restart_game(self):
        self.game_over = False
        self.impacts = 0
        self.shiel_protection = 0
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
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        # dibujamos el objeto en pantalla
        if self.spaceship.image_rect is not None:
            self.screen.blit(self.spaceship.image, (self.spaceship.image_rect.x, self.spaceship.image_rect.y))
        # display the enemy spaceship in its current position
        for iter_enemys in range(len(self.enemys)): 
            if self.enemys[iter_enemys].image_rect is not None:
                self.screen.blit(self.enemys[iter_enemys].image, self.enemys[iter_enemys].image_rect)
            # show the positions of the enemy bullets
            for bullet in self.enemys[iter_enemys].bullets:
                self.screen.blit(bullet.image, bullet.image_rect)
        #enemy gift
        for powers in self.spaceship.list_power_up:
            self.screen.blit(powers.shield_image, powers.shield_image_rect)
        # show the positions of the spaceship bullets 
        for bullet in self.spaceship.bullets:
            self.screen.blit(bullet.image, bullet.image_rect)

        if self.game_over:
            self.game_over_screen()

        count_text = self.font_score.render("Count: " + str(self.spaceship.impacts), True, self.RED)
        score_text = self.font_score.render("Score: " + str(self.spaceship.score*100), True, self.GREEN)
        self.screen.blit(count_text, (10, 10))
        self.screen.blit(score_text, (10, 30))

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
