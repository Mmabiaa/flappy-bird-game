import pygame as pg
import random
from bird import Bird
from pipe import Pipe
from button import Button
from utils import *

class Game:
    def __init__(self):
        # Initialize game variables and Pygame components here.
        
        # Game variables
        self.size = (800, 800)
        self.screen_width = 864
        self.screen_height = 936
        
        # Game state variables
        global pipe_gap, pipe_frequency, last_pipe, ground_scroll_speed
        
        # Initialize Pygame components.
        pg.display.set_caption("Flappy Bird")
        
        # Load images and fonts.
        global bg, ground_img, button_img
        
        bg = pg.image.load("img/bg.png")
        ground_img = pg.image.load("img/ground.png")
        
        
        # Create sprite groups.
        self.bird_group = pg.sprite.Group()
        self.flappy = Bird(100, 468)
        self.bird_group.add(self.flappy)
        
        # Pipe group and other variables.
        global pipe_group, last_pipe, ground_scroll
        
        pipe_group = pg.sprite.Group()
        
        last_pipe = pg.time.get_ticks() - pipe_frequency
        
        # Initialize other variables.
        global ground_scroll
        
        ground_scroll = 0
        button_img = pg.image.load('img/restart.png')
        # Button for restarting the game.
        self.button = Button(self.screen_width // 2 - 50, 
                             self.screen_height // 2 - 100,
                             button_img)

    def reset_game(self):
        flappy = Bird(100, int(936/2))
        pipe_group.empty()
        score = 0
        flappy.rect.x = 100
        flappy.rect.y = int(self.screen_height / 2)
        
    def run(self):
        
        clock = pg.time.Clock()
        
        flying = False
        game_over = False
        score = 0
        
        while True: 
            button_img = pg.image.load('img/restart.png')
            button = Button(382, 368, button_img)
            flappy = Bird(100, int(936/2))
            clock.tick(60)
            SIZE = 800,800
            screen = pg.display.set_mode(SIZE)
            bird_group = pg.sprite.Group()

            # Draw background and other elements.
            screen.blit(bg,(0,0))
            pipe_group.draw(screen)
            screen.blit(ground_img,(0,650))
            bird_group.draw(screen)
            bird_group.update(flying, game_over)

            # Check the score logic...
            if len(pipe_group) > 0:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                        and not pass_pipe:
                    pass_pipe=True
                
                if pass_pipe:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        score += 1
                        pass_pipe=False
            
            draw_text(screen, str(0), font_size=60,
                      text_color=white,
                      x=432,
                      y=20)

            # Look for collisions.
            if pg.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
                game_over=True
            
            # Check if the bird has hit the ground.
            if flappy.rect.bottom >= 650:
                flying=False 
                game_over=True
            
            # If the game is not over...
            if not game_over and flying:

                # Generate new pipes...
                time_now=pg.time.get_ticks()
                
                if time_now - last_pipe > pipe_frequency:
                    pipe_height=random.randint(-100,100)
                    bottom_pipe=Pipe(self.screen_width,int(self.screen_height/2)+pipe_height,-1)
                    top_pipe=Pipe(self.screen_width,int(self.screen_height/2)+pipe_height,+1)
                    pipe_group.add(bottom_pipe,top_pipe)
                    last_pipe=time_now
                
                ground_scroll -= ground_scroll_speed
                
                if abs(ground_scroll) > 35: 
                    ground_scroll=0
                
                pipe_group.update(ground_scroll_speed)

            # Check for Game Over and reset...
            if game_over:
               if button.draw(screen):
                    game_over=False 
                    score=self.reset_game()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    flying=True

            pg.display.update()