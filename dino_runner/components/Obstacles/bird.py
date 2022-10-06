from .obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, images):
        type = 0
        super().__init__(images, type)
        self.step_index = 0
        self.rect.y = 250

    def draw(self, screen):
        if self.step_index >= 9:
            self.step_index = 0
        screen.blit(self.images[self.step_index // 5], self.rect)
        self.step_index += 1
        

