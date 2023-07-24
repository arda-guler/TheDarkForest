import pygame
import random

class Photoid:
    def __init__(self, pos, dir, grid_size):
        self.pos = pos
        self.dir = dir

        img0 = pygame.image.load("data/img/photoid0.png")
        img1 = pygame.image.load("data/img/photoid1.png")
        img2 = pygame.image.load("data/img/photoid2.png")
        img3 = pygame.image.load("data/img/photoid3.png")
        img0 = pygame.transform.scale(img0, (grid_size, grid_size))
        img1 = pygame.transform.scale(img1, (grid_size, grid_size))
        img2 = pygame.transform.scale(img2, (grid_size, grid_size))
        img3 = pygame.transform.scale(img3, (grid_size, grid_size))
        self.images = [img0,
                       img1,
                       img2,
                       img3]

        self.newly_generated = True

    def move(self):
        if not self.newly_generated:
            if self.dir == 0:
                self.pos[1] -= 1
            elif self.dir == 1:
                self.pos[0] += 1
            elif self.dir == 2:
                self.pos[1] += 1
            else:
                self.pos[0] -= 1
        else:
            self.newly_generated = False

class Warden:
    def __init__(self, pos, dir, energy, grid_size):
        self.pos = pos
        self.dir = dir
        self.energy = energy

        ship_names = []
        ship_names_file = open("data/story/ship_names.txt")
        ship_name_lines = ship_names_file.readlines()
        for name in ship_name_lines:
            ship_names.append(name)

        self.ship_name = random.choice(ship_names)

        img0 = pygame.image.load("data/img/warden0.png")
        img1 = pygame.image.load("data/img/warden1.png")
        img2 = pygame.image.load("data/img/warden2.png")
        img3 = pygame.image.load("data/img/warden3.png")
        img0 = pygame.transform.scale(img0, (grid_size, grid_size))
        img1 = pygame.transform.scale(img1, (grid_size, grid_size))
        img2 = pygame.transform.scale(img2, (grid_size, grid_size))
        img3 = pygame.transform.scale(img3, (grid_size, grid_size))
        self.images = [img0,
                       img1,
                       img2,
                       img3]
