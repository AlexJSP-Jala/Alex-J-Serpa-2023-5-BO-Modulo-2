import pygame
from pygame.sprite import Sprite


from game.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG, FPS, GAME_OVER

class Draw_game(Sprite):
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0


        #Color
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        # Text font
        self.font = pygame.font.SysFont("Algerian", 60)
        self.font_score = pygame.font.Font(None, 30)
        #Text game over
        self.game_over_text = None
        self.restart_text = None
        self.deaths_text = None 
        #win
        self.win_text = None
        self.score_text = None


    def draw(self, spaceship, enemys, game_over, win):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        # dibujamos el objeto en pantalla
        if spaceship.image_rect is not None:
            self.screen.blit(spaceship.image, (spaceship.image_rect.x, spaceship.image_rect.y))
        # display the enemy spaceship in its current position
        for iter_enemys in range(len(enemys)): 
            if enemys[iter_enemys].image_rect is not None:
                self.screen.blit(enemys[iter_enemys].image, enemys[iter_enemys].image_rect)
            # show the positions of the enemy bullets
            for bullet in enemys[iter_enemys].bullets:
                self.screen.blit(bullet.image, bullet.image_rect)
        #enemy gift
        for powers in spaceship.list_power_up:
            self.screen.blit(powers.shield_image, powers.shield_image_rect)
        # show the positions of the spaceship bullets 
        for bullet in spaceship.bullets:
            self.screen.blit(bullet.image, bullet.image_rect)

        if game_over:
            self.game_over_screen(spaceship)
        
        if win:
            self.win_screen(spaceship)

        count_text = self.font_score.render("Count: " + str(spaceship.impacts), True, self.RED)
        score_text = self.font_score.render("Score: " + str(spaceship.score*100), True, self.GREEN)
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
    
    def game_over_screen(self, spaceship):
        self.game_over_text = self.font.render("GAME OVER", True, self.YELLOW)
        self.restart_text = self.font.render("Presiona 'R' para reiniciar", True, self.YELLOW)
        self.deaths_text = self.font.render("Death Count: " + str(spaceship.deaths), True, self.RED)
        self.bullet_count = self.font.render("Bullet Count: " + str(spaceship.impacts), True, self.BLACK)
        #self.screen.fill(self.WHITE)
        self.screen.blit(GAME_OVER, (0, 0))
        self.screen.blit(self.game_over_text, (SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2, 200))
        self.screen.blit(self.restart_text, (SCREEN_WIDTH // 2 - self.restart_text.get_width() // 2, 250))
        self.screen.blit(self.deaths_text, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 300))
        self.screen.blit(self.bullet_count, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 350))
    
    def win_screen(self, spaceship):
        self.win_text = self.font.render("Congratulations", True, self.BLACK)
        self.restart_text = self.font.render("Presiona 'R' para reiniciar", True, self.BLACK)
        self.score_text = self.font.render("Score: " + str(spaceship.score*100), True, self.RED)
        #self.bullet_count = self.font.render("Bullet Count: " + str(spaceship.impacts), True, self.BLACK)
        self.screen.fill(self.WHITE)
        #self.screen.blit(GAME_OVER, (0, 0))
        self.screen.blit(self.win_text, (SCREEN_WIDTH // 2 - self.win_text.get_width() // 2, 200))
        self.screen.blit(self.restart_text, (SCREEN_WIDTH // 2 - self.restart_text.get_width() // 2, 250))
        #self.screen.blit(self.deaths_text, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 300))
        #self.screen.blit(self.bullet_count, (SCREEN_WIDTH // 2 - self.deaths_text.get_width() // 2, 350))
        