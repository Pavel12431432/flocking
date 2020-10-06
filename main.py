import math
from random import randint, gauss

import pygame
from pygame import gfxdraw

from boid import Boid

# define constants
WIDTH, HEIGHT = 640, 480
BOID_SPEED = 2
BOID_SIGHT_RADIUS = 75
ALIGN_FACTOR = 0.05
COHESION_FACTOR = 0.01
SEPARATION_FACTOR = 0.05

# pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flocking')
font = pygame.font.SysFont('consolas', 30)
clock = pygame.time.Clock()


# handle input
def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


# draw boids
def draw():
	screen.fill((0, 0, 0))
	for boid in flock:
		gfxdraw.filled_circle(screen, *tuple(map(int, boid.pos)), 2, (255, 255, 255))
	pygame.display.update()


# generate random initial velocity for boids
def make_rand_vector():
	vec = gauss(0, 1), gauss(0, 1)
	mag = math.sqrt(sum(x ** 2 for x in vec))
	return [x / mag for x in vec]


# generate the flock of boids
flock = [Boid((randint(0, WIDTH), randint(0, HEIGHT)), make_rand_vector(), BOID_SPEED, BOID_SIGHT_RADIUS, ALIGN_FACTOR,
			  COHESION_FACTOR, SEPARATION_FACTOR) for i in range(200)]

while True:
	flock_copy = flock
	for boid in flock:
		boid.flock(flock_copy)
		boid.update(WIDTH, HEIGHT)
	inp()
	draw()
	clock.tick(0)
