import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET, SPACESHIP_SHIELD, SHIELD
from game.components.bullet import Bullet
from game.components.power_up import Power_up

# casi Todo en pygame es un objeto
# Un personaje en mi juego es un objeto (instancia de algo)
# La nave (spaceship) es un personaje => necesito una clase


# SpaceShip es una clase derivada (hija) de Sprite

# spaceship tiene una "imagen"
class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (40, 60)
        self.image_size_with_shield = (60, 60)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = 40
        self.image_rect.y = 500
        self.move_left = False
        self.move_right = False
        self.spaceship_speed = 5
        self.move_down = False
        self.move_up = False
        self.bullets = []
        self.has_shield = False
        self.shiel_protection = 0
        self.impacts = 0
        self.deaths = 0
        self.score = 0
        self.list_power_up = []
        

    def update(self):
        if self.image_rect is not None:
            if self.move_left and self.image_rect.left > 0:
                self.image_rect.x -= self.spaceship_speed
            if self.move_right and self.image_rect.right < SCREEN_WIDTH:
                self.image_rect.x += self.spaceship_speed
            if self.move_up and self.image_rect.y > 0:
                self.image_rect.y -= self.spaceship_speed
            if self.move_down and self.image_rect.y <= SCREEN_HEIGHT - self.image_rect.height:
                self.image_rect.y += self.spaceship_speed
            if self.image_rect.left <= 0:
                self.image_rect.right = SCREEN_WIDTH
            elif self.image_rect.right >= SCREEN_WIDTH:
                self.image_rect.left = 0

    def shoot(self, x_position_center, y_position):
        self.bullet = Bullet(x_position_center, y_position, BULLET)
        self.bullets.append(self.bullet)
    
    def activate_shield(self):
        self.image = pygame.transform.scale(SPACESHIP_SHIELD, self.image_size_with_shield)
        self.has_shield = True
        self.shiel_protection = 5 
    
    def deactivate_shield(self):
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)  
        self.has_shield = False

    def detect_impact_bullet(self, bullets, spaceship, bullet_lethality):
        for bullet in bullets:
            if spaceship.image_rect is not None and bullet.image_rect.colliderect(spaceship.image_rect):
                bullets.remove(bullet)
                if self.shiel_protection >= 0: 
                    self.shiel_protection -= 1
                    print("shiel protection", self.shiel_protection)
                if self.shiel_protection <= 0:
                    self.deactivate_shield()
                    self.impacts += 1
                    if self.impacts>= bullet_lethality:
                        self.deaths += 1
                        spaceship.image_rect = None
                print("this is the impact of the SpaceShip", self.impacts)
    
    def delete_enemys(self, bullets, enemys):
        for bullet in bullets:
            for enemy in enemys:
                if enemy.image_rect is not None and bullet.image_rect.colliderect(enemy.image_rect):
                    power_up = Power_up(bullet.image_rect.centerx, bullet.image_rect.centery, SHIELD)
                    self.score += 1 
                    if self.has_shield:
                        bullets.remove(bullet)
                        enemy.image_rect = None
                    else:
                        self.list_power_up.append(power_up)
                        bullets.remove(bullet)
                        enemy.image_rect = None

    




