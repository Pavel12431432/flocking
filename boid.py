import math


class Boid:
	def __init__(self, pos, velocity, max_speed, sight_radius, align_factor, cohesion_factor, separation_factor):
		self.pos = pos
		self.velocity = velocity
		self.acceleration = 0, 0

		self.max_speed = max_speed
		self.sight_radius = sight_radius
		self.align_factor = align_factor
		self.cohesion_factor = cohesion_factor
		self.separation_factor = separation_factor

	def update(self, screen_width, screen_height):
		self.pos = tuple(map(sum, zip(self.pos, self.velocity)))
		self.pos = self.pos[0] % screen_width, self.pos[1] % screen_height
		self.velocity = tuple(map(sum, zip(self.velocity, self.acceleration)))
		self.velocity = norm(self.velocity, self.max_speed)
		self.acceleration = 0, 0

	def align(self, flock):
		direction = 0, 0
		total = 0
		for boid in flock:
			if math.sqrt((self.pos[0] - boid.pos[0]) ** 2 + (self.pos[1] - boid.pos[1]) ** 2) <= self.sight_radius:
				direction = tuple(map(sum, zip(direction, boid.velocity)))
				total += 1
		if total:
			self.acceleration = tuple(map(lambda x: x / total * self.align_factor, direction))

	def cohesion(self, flock):
		direction = 0, 0
		total = 0
		for boid in flock:
			if math.sqrt((self.pos[0] - boid.pos[0]) ** 2 + (self.pos[1] - boid.pos[1]) ** 2) <= self.sight_radius:
				direction = tuple(map(sum, zip(direction, boid.pos)))
				total += 1
		if total:
			direction = (direction[0] / total - self.pos[0]) * self.cohesion_factor, \
						(direction[1] / total - self.pos[1]) * self.cohesion_factor
			self.acceleration = tuple(map(sum, zip(self.acceleration, direction)))

	def separation(self, flock):
		direction = 0, 0
		total = 0
		for boid in flock:
			dist = math.sqrt((self.pos[0] - boid.pos[0]) ** 2 + (self.pos[1] - boid.pos[1]) ** 2)
			if dist <= self.sight_radius:
				op_dir = -(boid.pos[0] - self.pos[0]) / max(dist, 0.01), -(boid.pos[1] - self.pos[1]) / max(dist, 0.01)
				direction = direction[0] + op_dir[0], direction[1] + op_dir[1]
				total += 1
		if total:
			self.acceleration = tuple(
				map(lambda x: x[0] + x[1] * self.separation_factor, zip(self.acceleration, direction)))


def norm(a, div):
	v = math.sqrt(a[0] ** 2 + a[1] ** 2) / div
	if v == 0:
		return 0
	return a[0] / v, a[1] / v