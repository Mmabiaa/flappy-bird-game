import pygame as pg
from utils import pipe_gap

class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pg.image.load('img/pipe.png')
        if position == 1:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y - int(pipe_gap / 2)))
        else:
            self.rect = self.image.get_rect(topleft=(x, y + int(pipe_gap / 2)))

    def update(self, ground_scroll_speed):
        self.rect.x -= ground_scroll_speed - 1
        if self.rect.right < 0:
            self.kill()