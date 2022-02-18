import pygame
import os

class Settings(object):
    window_width = 1200
    window_height = 700
    window_title = "Astreroids 2"
    fps = 60
    
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    sound_path = os.path.join(file_path, "sounds")
    
    default_spawn_speed = 110
    max_asteroids = 5


class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.image = pygame.image.load(os.path.join(Settings.image_path, "bg.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(Settings.window_width, Settings.window_height))
        
    # draws the background    
    def draw(self, screen):
        screen.blit(self.image, (0,0))

# Class for the Timer made by our Teacher
class Timer(object):
    def __init__(self, duration, with_start=True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False
    
class Ship(pygame.sprite.Sprite):
    def __init__(self,game) -> None:
        super().__init__()  
        
        
class Astreroid(pygame.sprite.Sprite):
    def __init__(self,game) -> None:
        super().__init__()
        
class Game(object):
    def __init__(self) -> None:
        super().__init__()
        
        os.environ['SDL_VIDEO_WINDOW_CENTERED'] = "10, 50"
        
        pygame.init()
        pygame.display.set_caption(Settings.window_title)
        
        pygame.font.init()
        self.font_name = pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(self.font_name, 72)
        self.info_font = pygame.font.SysFont(self.font_name, 30)
        self.menu_font = pygame.font.SysFont(self.font_name, 40)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        
        self.pause = False
        self.start_screen = True
        self.game_over = False
        self.running = False
        
        
        self.asteroids = pygame.sprite.Group()  
        self.background = Background()
        self.spaceship = pygame.sprite.GroupSingle()
        self.spaceship.add(Ship("spaceship.png"))