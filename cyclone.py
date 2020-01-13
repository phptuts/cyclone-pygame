# Pygame template
import pygame
import random
import os
import math
from pygame import gfxdraw

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Assets

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


def points_on_circumference(center=(0, 0), r=50, n=100):
    return [
        (
            center[0] + (math.cos(2 * math.pi / n * x) * r),  # x
            center[1] + (math.sin(2 * math.pi / n * x) * r)  # y

        ) for x in range(0, n + 1)]


def create_lights_around_center(size_large_circle, size_small_circle, number_of_circles):
    cx = WIDTH / 2
    cy = HEIGHT / 2
    points = points_on_circumference((cx, cy), size_large_circle, number_of_circles)
    for point in points:
        all_sprites.add(Light(point[0], point[1], size_small_circle, GREEN))


class Light(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.Surface([size * 3, size * 3], pygame.SRCALPHA, 32)
        self.image.convert()
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, WHITE, (self.size, self.size), size)
        gfxdraw.aacircle(self.image, self.size, self.size, self.size, WHITE)
        gfxdraw.filled_circle(self.image, self.size, self.size, self.size, WHITE)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.change_light_time = pygame.time.get_ticks() + 1000
        self.state = 'off'
        self.color = color

    def update(self):
        if self.change_light_time < pygame.time.get_ticks():
            self.change_light_time = pygame.time.get_ticks() + 1000
            if self.state == 'on':
                self.state = 'off'
                # pygame.draw.circle(self.image, BLUE, (self.size, self.size), self.size)
                gfxdraw.aacircle(self.image, self.size, self.size, self.size, self.color)
                gfxdraw.filled_circle(self.image, self.size, self.size, self.size, self.color)

            else:
                self.state = 'on'
                # pygame.draw.circle(self.image, WHITE, (self.size, self.size), self.size)
                gfxdraw.aacircle(self.image, self.size, self.size, self.size, WHITE)
                gfxdraw.filled_circle(self.image, self.size, self.size, self.size, WHITE)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
light = Light(100, 100, 30, GREEN)
all_sprites.add(light)

create_lights_around_center(200, 20, 10)

running = True

while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / Render
    screen.fill(RED)
    all_sprites.draw(screen)

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
