import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pg.image.load(f'img/bird{num}.png') for num in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False

    def update(self, flying, game_over):
        if flying:
            self.vel += 0.5 
            if self.vel > 8:
                self.vel = 8
            
            if self.rect.bottom < 650: 
                self.rect.y += int(self.vel)

            if not game_over:
                self.counter += 1
                flap_cooldown = 5

                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

                if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.vel = -10
                    self.clicked = True

                if pg.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                self.image = pg.transform.rotate(self.images[self.index], -self.vel * 2)
            else:
                self.image = pg.transform.rotate(self.images[self.index], -90)