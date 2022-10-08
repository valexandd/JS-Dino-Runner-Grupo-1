import pygame
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.player_hearts.player_hearts_manager import PlayerHeartManager
from dino_runner.components.power_up.power_up_manager import PowerUpManager
from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, GAME_OVER_SOUND, HAMMER_TYPE, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, SOUND, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.heart_manager = PlayerHeartManager()

        self.score = Score()
        self.death_count = 0

    def reset_game(self):
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        self.score.reset_score()
        self.power_up_manager.reset_power_ups()
        self.heart_manager.reset_hearts()    
        
    def execute(self):
        self.executing = True
        while self.executing:
            pygame.mixer.music.load(SOUND)
            pygame.mixer.music.play(-1)
            if not self.playing:
                self.show_menu()
            
        pygame.quit()
    
    def run(self):
        self.reset_game()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.score.update(self)
        self.power_up_manager.update(self.game_speed, self.player, self.score.score)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.heart_manager.draw(self.screen)
        self.draw_power_up_active()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.message("Press any key to start", 25,half_screen_width, half_screen_height)
        else: 
            self.message("Press any key to restart", 25,half_screen_width, half_screen_height)
            self.message(f"Score: {self.score.score}", 20,half_screen_width, half_screen_height + 100)
            self.message(f"Deaths: {self.death_count}", 20,half_screen_width, half_screen_height + 150)
        self.screen.blit(RUNNING[0], (half_screen_width - 30, half_screen_height - 140))
        pygame.display.update()
        self.handle_key_events_on_menu()
        
    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def on_death (self):
        has_shield = (self.player.type == SHIELD_TYPE)
        has_hammer = (self.player.type == HAMMER_TYPE)
        is_invincinle = has_shield or self.heart_manager.heart_count > 0
        if not has_shield:
            if not has_hammer:
                self.heart_manager.reduce_heart()
            else:
                self.heart_manager.increase_heart()
        if not is_invincinle:
            pygame.time.delay(500)
            self.playing = False
            pygame.mixer.music.load(GAME_OVER_SOUND)
            pygame.mixer.music.play()
            self.death_count += 1
        return is_invincinle
        
    def message (self, msg, font_size, positon_x, position_y):
            font = pygame.font.Font(FONT_STYLE, font_size)
            text_component = font.render(msg, True, (0, 0, 0))
            text_rect = text_component.get_rect()
            text_rect.center = (positon_x, position_y)
            self.screen.blit(text_component, text_rect)
            
    def draw_power_up_active(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks()) / 1000)
            if time_to_show >= 0:
                self.message(f" {self.player.type.capitalize()} enabled for {time_to_show} seconds", 18, 500, 40)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
        
