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
    scores = []
    for i in range(0, 10):
        scores.append(random.randrange(10, 50))

    scores.append(100)
    random.shuffle(scores)

    for point in points:
        light_sprite = Light(point[0], point[1], size_small_circle, GREEN, scores.pop(0))
        all_sprites.add(light_sprite)
        light_sprites.add(light_sprite)
        light_list.append(light_sprite)


class Light(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, points):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.Surface([size * 2, size * 2], pygame.SRCALPHA, 32)
        self.image.convert()
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, WHITE, (self.size, self.size), size)
        gfxdraw.aacircle(self.image, self.size, self.size, self.size, WHITE)
        gfxdraw.filled_circle(self.image, self.size, self.size, self.size, WHITE)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.change_light_time = pygame.time.get_ticks() + 1000
        self.is_on = False
        self.update_light = False
        self.color = color
        self.points = points
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.font.render(str(points), True, (199, 77, 227))
        self.image.blit(self.text, [self.rect.centerx - (self.text.get_rect().width / 2), self.rect.centery - (self.rect.height / 2)])

    def get_points(self):
        return self.points

    def toggle_light(self, is_on):
        self.is_on = is_on
        self.update_light = True

    def update(self):
        if self.is_on and self.update_light:
            self.is_on = False
            gfxdraw.aacircle(self.image, self.size, self.size, self.size, self.color)
            gfxdraw.filled_circle(self.image, self.size, self.size, self.size, self.color)
        elif self.update_light:
            self.is_on = True
            gfxdraw.aacircle(self.image, self.size, self.size, self.size, WHITE)
            gfxdraw.filled_circle(self.image, self.size, self.size, self.size, WHITE)

        self.update_light = False
        self.image.blit(self.text, [self.size  - (self.text.get_rect().width / 2), self.size  - (self.text.get_rect().height / 2)])


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.font.init()  # you have to call this at the start,

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cyclone Game')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
light_sprites = pygame.sprite.Group()
light_list = []

create_lights_around_center(200, 40, 10)

running = True

next_light_timer = pygame.time.get_ticks() + 100
next_light = 0
light_list[next_light].toggle_light(True)

while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print(light_list[next_light].get_points())


    if pygame.time.get_ticks() > next_light_timer:
        next_light_timer = pygame.time.get_ticks() + 100
        light_list[next_light].toggle_light(False)
        if next_light >= len(light_list) - 1:
            next_light = 0
        else:
            next_light += 1

        light_list[next_light].toggle_light(True)

    # Update
    all_sprites.update()

    # Draw / Render
    screen.fill(RED)
    all_sprites.draw(screen)
    # Change so that it uses the top of the circle

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
