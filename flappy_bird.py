import pygame as pg
import random


pg.init()

# Game variables
SIZE = 800,800
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936

pipe_gap = 200
pipe_frequency = 1500 # milliseconds
last_pipe = pg.time.get_ticks() - pipe_frequency
ground_scroll = 0
ground_scroll_speed = 4
flying = False
game_over = False
running = True
score = 0
pass_pipe = False
fps_limit = 60


# Define font 
font = pg.font.SysFont('Bauhaus 93', 60)

# Define color 
white = (255,255,255)


# Load sprite images
bg = pg.image.load("img/bg.png")
ground_img = pg.image.load("img/ground.png")
button_img = pg.image.load('img/restart.png')


def draw_text(text, font, text_color, x,y):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))


def reset_game():
    
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT/2)
    score = 0
    return score

class Bird(pg.sprite.Sprite):

    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)

        self.images = []
        self.index = 0
        self.counter = 0
        
        for num in range(1,4):
            img = pg.image.load(f'img/bird{num}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False



    def update(self):

        global game_over, flying # Control flags for flapping bird and game over
        
        if flying == True:

            # Drop the birb
            self.vel += 0.5 

            if self.vel > 8:
                self.vel = 8
        
            if self.rect.bottom < 650: 
                self.rect.y += int(self.vel)



        # Handles the animation for the bird
        
        if game_over == False: # While the game isn't over, keep flapping

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

             # Jumping controls 
            
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False and game_over == False:
                self.vel = -10
                self.clicked = True

            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
             # Rotate the bird 
            
            self.image = pg.transform.rotate(self.images[self.index], -self.vel * 2 )


        
        else:

            
            self.image = pg.transform.rotate(self.images[self.index], -90)
       


class Pipe(pg.sprite.Sprite):

    def __init__(self,x,y,position):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pg.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]
        

    def update(self):
        self.rect.x -= ground_scroll_speed - 1
        if self.rect.right < 0:
            self.kill()

    
class Button():

    def __init__(self,x,y,image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

    def draw(self):
        
        action = False

        # Get mouse position 
        pos = pg.mouse.get_pos()

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True


        # Draw button 
        screen.blit(self.image,(self.rect.x, self.rect.y))


        return action





       

# Create the bird and the bird group to hold it
bird_group = pg.sprite.Group()
flappy = Bird(100, int(SCREEN_HEIGHT/2))
bird_group.add(flappy)


pipe_group = pg.sprite.Group()




screen = pg.display.set_mode(SIZE)
pg.display.set_caption("Flappy Bird")

clock = pg.time.Clock()

button = Button(SCREEN_WIDTH//2 - 50,SCREEN_HEIGHT//2 - 100, button_img)


# Main game loop
while running:

    clock.tick(fps_limit)


    # Draw background
    screen.blit(bg,(0,0))

    # Draw pipe (bomb)
    pipe_group.draw(screen)
    

    # Draw ground
    screen.blit(ground_img,(ground_scroll,650))


    # Draw birb
    bird_group.draw(screen)
    bird_group.update()

    # Check the score 
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    
    draw_text(str(score), font, white , int(SCREEN_WIDTH/2),20)


    
    # Look for collisions
    if pg.sprite.groupcollide(bird_group,pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    ## Check if the bird has hit the ground 

    if flappy.rect.bottom >= 650:
        flying = False
        game_over = True

    
    # If the game is not over, Scroll the ground
    if game_over == False and flying == True:

        # Generate new pipes 
        time_now = pg.time.get_ticks()

        if time_now - last_pipe > pipe_frequency:

            pipe_height = random.randint(-100,100)
            bottom_pipe = Pipe(SCREEN_WIDTH,int(SCREEN_HEIGHT/ 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH,int(SCREEN_HEIGHT/2) + pipe_height, 1)
            pipe_group.add(bottom_pipe,top_pipe)
            last_pipe = time_now


        ground_scroll -= ground_scroll_speed
        if  abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()


    # Check for Game over and reset 
    if game_over == True:
       if button.draw() == True:
            game_over = False
            score = reset_game()



   
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            flying = True


    pg.display.update()
    
pg.quit()
