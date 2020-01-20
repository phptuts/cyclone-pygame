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

GAME_COLORS = [(31, 119, 180), (255, 127, 14),
               (44, 160, 44), (214, 39, 40),
               (148, 103, 189), (140, 86, 75),
               (227, 119, 194), (127, 127, 127),
               (188, 189, 34), (23, 190, 207)]

# Assets

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
background_image = pygame.image.load('background.jpg')


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
    for i in range(0, number_of_circles):
        scores.append(random.randrange(10, 50))

    scores.append(100)
    random.shuffle(scores)
    for point in points:
        light_sprite = Light(point[0], point[1], size_small_circle, random.choice(GAME_COLORS), scores.pop(0))
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
        self.rect = self.image.get_rect()
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
        self.text = self.font.render(str(points), True, BLACK)
        self.image.blit(self.text, [self.rect.centerx - (self.text.get_rect().width / 2),
                                    self.rect.centery - (self.rect.height / 2)])

    def get_points(self):
        return self.points

    def set_points(self, new_points):
        self.points = new_points
        self.update_light = True
        self.is_on = False

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
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.font.render(str(self.points), True, BLACK)
        self.image.blit(self.text,
                        [self.size - (self.text.get_rect().width / 2), self.size - (self.text.get_rect().height / 2)])


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

number_of_circles = 25
create_lights_around_center(240, 20, number_of_circles)

running = True

next_light_timer = pygame.time.get_ticks() + 100
next_light = 0
light_list[next_light].toggle_light(True)
is_playing = False
points = 0

while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            points = light_list[next_light].get_points()
            random_points = []
            for i in range(0, number_of_circles):
                random_points.append(random.randrange(10, 50))

            random_points.append(100)
            random.shuffle(random_points)
            print(random_points)
            for i in range(0, number_of_circles + 1):
                light_list[i].set_points(random_points.pop(0))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and not is_playing:
            is_playing = True

    if pygame.time.get_ticks() > next_light_timer and is_playing:
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
    screen.blit(background_image, [0, 0])
    all_sprites.draw(screen)
    if not is_playing:
        game_text_top = pygame.font.SysFont('Comic Sans MS', 40).render("Press s to start", True, WHITE)
        game_text_top_x = (WIDTH / 2) - game_text_top.get_rect().width / 2
        game_text_top_y = 250

        game_text_bottom = pygame.font.SysFont('Comic Sans MS', 40).render("Press the space bar to play.", True, WHITE)
        game_text_bottom_x = (WIDTH / 2) - game_text_bottom.get_rect().width / 2
        game_text_bottom_y = 300

        screen.blit(game_text_bottom, [game_text_bottom_x, game_text_bottom_y])

        screen.blit(game_text_top, [game_text_top_x, game_text_top_y])

    if is_playing and points > 0:
        game_text_top = pygame.font.SysFont('Comic Sans MS', 40).render("Points: " + str(points), True, WHITE)
        game_text_top_x = (WIDTH / 2) - game_text_top.get_rect().width / 2
        game_text_top_y = 250

        screen.blit(game_text_top, [game_text_top_x, game_text_top_y])

    # Change so that it uses the top of the circle

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
