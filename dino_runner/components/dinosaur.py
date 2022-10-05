import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING


class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_D = 340
    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_velocity = self.JUMP_VELOCITY

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if not self.dino_jump:
            if user_input[pygame.K_UP] :   
                self.dino_run = False 
                self.dino_jump = True
                self.dino_duck = False
            elif user_input[pygame.K_DOWN] :
                self.dino_run = False
                self.dino_jump = False
                self.dino_duck = True
            else:
                self.dino_run = True
                self.dino_jump = False
                self.dino_duck = False

        if self.step_index >= 9:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        self.dino_rect.y -= self.jump_velocity * 4
        self.jump_velocity -= 0.8

        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.dino_jump = False
            self.dino_rect.y = self.Y_POS
            self.jump_velocity = self.JUMP_VELOCITY

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_D
        self.step_index += 1
    
    def draw(self, screen):   
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
