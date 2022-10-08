from dino_runner.utils.constants import HEART


class Heart:
    def __init__(self, x_position, y_postion):
        self.image = HEART 
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_postion

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
