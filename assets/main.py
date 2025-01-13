import pygame as pg
from game import Game

if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()
    pg.quit()