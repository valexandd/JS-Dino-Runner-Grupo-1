from random import randint

import pygame
from dino_runner.components.power_up.hammer import Hammer
from dino_runner.components.power_up.shield import Shield


class PowerUpManager:

    def __init__(self):
        self.power_ups = []
        self.when_shield_appears = 0
        self.when_hammer_appears = 0


    def generate_power_up(self, score):
        if len(self.power_ups) == 0:
            if self.when_shield_appears == score:
                self.when_shield_appears += randint(200, 300)
                self.power_ups.append(Shield())
            if self.when_hammer_appears == score:
                self.when_hammer_appears += randint(200,250)
                self.power_ups.append(Hammer())

    def update(self, game_speed, player, score):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(power_up.start_time, power_up.duration, power_up.type)
                self.power_ups.remove(power_up)


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_shield_appears = randint(200, 300)
        self.when_hammer_appears = randint(100,150)
