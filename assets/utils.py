import pygame as pg

# Game constants
pipe_gap = 200
pipe_frequency = 1500 # milliseconds

# Define font 
font_path='Bauhaus 93'
font_size=60

# Define color 
white=(255,255,255)

def draw_text(screen,text,font_size,text_color,x,y):
    font=pg.font.SysFont(font_path,font_size)
    img=font.render(text=True,text_color=text_color)
    screen.blit(img,(x,y))