import pygame
import os
import random
from math import sqrt, radians, cos, sin

class Settings(object):
    window_width = 1200
    window_height = 700
    window_title = "Asteroids"
    fps = 60
    
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    sound_path = os.path.join(file_path, "sounds")
    
    ship_scale = 2
    ship_rotation = 22.5
    max_ship_speed = 6
    
    spawn_speed = 2000
    asteroid_speed = (-3,3)
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
    def __init__(self) -> None:
        super().__init__()  
        self.idle_img = self.scale_ship(pygame.image.load(os.path.join(Settings.image_path, "ship.png")))
        self.accelerating_img = self.scale_ship(pygame.image.load(os.path.join(Settings.image_path,"ship_accelerating.png")))
        self.image = self.idle_img
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window_width// 2, Settings.window_height - 50)
        
        self.accelerating = False
        self.ship_rotation = 0
        self.rotation_delay = Timer(100)
        self.timer_acc = Timer(200)
        
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0
        
    def scale_ship(self, image):
        self.rect = image.get_rect() 
        return pygame.transform.scale(image, (
            (self.rect.width * Settings.ship_scale),
            (self.rect.height * Settings.ship_scale)
        ))
        
    #checks if a asteroid collides with the spaceship
    def collision(self):
        if pygame.sprite.spritecollide(self,game.asteroids, False, pygame.sprite.collide_mask):
            game.running = False
            
    def rotate(self, angle):
        ship_center = self.rect.center
        
        if self.rotation_delay.is_next_stop_reached():
            self.angle += angle
            self.angle %= 360
        
        if self.accelerating == True:
            self.image = self.accelerating_img
        elif self.accelerating == False:
            self.image = self.idle_img 
        
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = ship_center
        
    def accelerate(self):
        if self.timer_acc.is_next_stop_reached():
            if self.accelerating:
                angle = radians(self.angle)
                newspeed_x = self.speed_x - sin(angle)
                newspeed_y = self.speed_y - cos(angle)
                if abs(newspeed_x) < Settings.max_ship_speed and abs(newspeed_y) < Settings.max_ship_speed:
                    self.speed_x = newspeed_x
                    self.speed_y = newspeed_y
            
    def update(self):
        self.accelerate()
        self.rotate(self.ship_rotation)
        self.collision()
        
        self.rect.move_ip(self.speed_x, self.speed_y)
        
        if self.rect.right < 0:
            self.rect.left = Settings.window_width
        if self.rect.left > Settings.window_width:
            self.rect.right = 0
        
        if self.rect.bottom < 0:
            self.rect.top = Settings.window_height
        if self.rect.top > Settings.window_height:
            self.rect.bottom = 0
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
      
      
class Asteroid(pygame.sprite.Sprite):
    spawn_timer = Timer(Settings.spawn_speed)
    images = [pygame.image.load(image) for image in [
        os.path.join(Settings.image_path, "asteroid1.png"),
        os.path.join(Settings.image_path, "asteroid2.png"),
        os.path.join(Settings.image_path, "asteroid3.png")
    ]]
    
    def __init__(self) -> None:
        super().__init__()
        self.image = random.choice(Asteroid.images)
        self.rect = self.image.get_rect()
        self.find_spawn()
        
        self.speed = (random.randint(*Settings.asteroid_speed),random.randint(*Settings.asteroid_speed))
        if self.speed[0] == 0:
            self.speed = (1, self.speed[1])
            
    def spawn_asteroid():
        if len(game.asteroids) <= Settings.max_asteroids:
            game.asteroids.add(Asteroid())   
         
    def find_spawn(self):
        self.rect.top = random.randint(0,Settings.window_height - self.rect.height)
        self.rect.left = random.randint(0,Settings.window_width - self.rect.width)
        self.check_spawn()
        
    def check_spawn(self):
        for asteroid in game.asteroids:
            dist_x = abs(self.rect.center[0] - asteroid.rect.center[0])
            dist_y = abs(self.rect.center[1] - asteroid.rect.center[1])
            dist = (sqrt(dist_x ** 2 + dist_y ** 2) - self.rect.width // 2 - asteroid.rect.width // 2)
            if dist < 1:
                self.find_spawn()
                
    
     
    def update(self):
        
        self.rect.move_ip(self.speed)
        
        
        if self.rect.right < 0:
            self.rect.left = Settings.window_width
        if self.rect.left > Settings.window_width:
            self.rect.right = 0
        
        if self.rect.bottom < 0:
            self.rect.top = Settings.window_height
        if self.rect.top > Settings.window_height:
            self.rect.bottom = 0
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    
class Game(object):
    def __init__(self) -> None:
        super().__init__()
        
        os.environ['SDL_VIDEO_WINDOW_CENTERED'] = "10, 50"
        
        pygame.init()
        pygame.display.set_caption(Settings.window_title)
        
        """ for later use
        pygame.font.init()
        self.font_name = pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(self.font_name, 72)
        self.info_font = pygame.font.SysFont(self.font_name, 30)
        self.menu_font = pygame.font.SysFont(self.font_name, 40)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        """
        
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        
        """ For later too
        self.pause = False
        self.start_screen = True
        self.game_over = False
        
        """
        self.running = False
        
        self.timer = Timer(1000)
        self.spawn_timer = Timer(1000)

        self.asteroids = pygame.sprite.Group()  
        self.background = Background()
        self.ship = Ship()
        
     
    def run(self):
        self.running = True
        
        while self.running:
            self.clock.tick(Settings.fps)
            
            self.watch_for_events()
            
            self.update()
            self.draw()

            pygame.display.flip()
        pygame.quit()
    
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Checks for events if a key is pressed
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    self.ship.accelerating = True
                if event.key == pygame.K_LEFT:
                    self.ship.ship_rotation = Settings.ship_rotation 
                if event.key == pygame.K_RIGHT:
                    self.ship.ship_rotation = Settings.ship_rotation * -1
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.accelerating = False
                if event.key == pygame.K_LEFT:
                    self.ship.ship_rotation = 0
                if event.key == pygame.K_RIGHT:
                    self.ship.ship_rotation = 0
    
    def update(self):
        self.background.update()
        self.ship.update()
        self.asteroids.update()
       
        if Asteroid.spawn_timer.is_next_stop_reached():
            Asteroid.spawn_asteroid()
       
    def draw(self):
        self.background.draw(self.screen)
        self.ship.draw(self.screen)
        self.asteroids.draw(self.screen)
        
        pygame.display.flip()
            
if __name__ == "__main__":
    game = Game()
    game.run()
