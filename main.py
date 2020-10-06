import pygame
from pygame import gfxdraw
from random import randint, gauss
from boid import Boid

WIDTH, HEIGHT = 800, 600
BOID_SPEED = 2
BOID_SIGHT_RADIUS = 75
ALIGN_FACTOR = 0.05
COHESION_FACTOR = 0.01
SEPARATION_FACTOR = 0.05

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flocking')
font = pygame.font.SysFont('consolas', 15)
clock = pygame.time.Clock()


def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


def draw():
	screen.fill((0, 0, 0))
	for boid in flock:
		gfxdraw.aacircle(screen, *tuple(map(int, boid.pos)), 2, (255, 255, 255))
	pygame.display.update()


def make_rand_vector(dims):
	vec = [gauss(0, 1) for i in range(dims)]
	mag = sum(x ** 2 for x in vec) ** .5
	return [x / mag for x in vec]


# noinspection ProblematicWhitespace
flock = [Boid((randint(0, WIDTH), randint(0, HEIGHT)), make_rand_vector(2), BOID_SPEED, BOID_SIGHT_RADIUS, ALIGN_FACTOR,
			  COHESION_FACTOR, SEPARATION_FACTOR) for i in range(100)]

while True:
	draw()
	inp()
	flock_copy = flock
	for boid in flock:
		boid.align(flock_copy)
		boid.cohesion(flock_copy)
		boid.separation(flock_copy)
		boid.update(WIDTH, HEIGHT)
	clock.tick(60)
