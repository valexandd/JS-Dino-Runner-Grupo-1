import random
import pygame
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS
from .small_cactus import SmallCactus
from .large_cactus import LargeCactus

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game_speed, player, on_death):
        if len(self.obstacles) == 0:
            rndm = random.randint(0,1)
            if rndm == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rndm == 1 :
                self.obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                on_death()
                break
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
