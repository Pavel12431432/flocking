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

	# update position and velocity
	def update(self, screen_width, screen_height):
		self.pos = tuple(map(sum, zip(self.pos, self.velocity)))
		self.pos = self.pos[0] % screen_width, self.pos[1] % screen_height
		self.velocity = tuple(map(sum, zip(self.velocity, self.acceleration)))
		self.velocity = norm(self.velocity, self.max_speed)

	# flocking mechanic
	def flock(self, flock):
		alignment = 0, 0
		cohesion = 0, 0
		separation = 0, 0
		total = 0
		for boid in flock:
			# check if current boid is approximately within sight_radius
			# using Manhattan distance to compute faster (almost twice as fast)
			dist = abs(self.pos[0] - boid.pos[0]) + abs(self.pos[1] - boid.pos[1])
			if dist <= self.sight_radius and dist:
				# calculate alignment and cohesion
				alignment = tuple(map(sum, zip(alignment, boid.velocity)))
				cohesion = tuple(map(sum, zip(cohesion, boid.pos)))
				# calculate the vector opposite the current boid
				# with a magnitude inversely proportional to the distance
				opposite_dir = (self.pos[0] - boid.pos[0]) / dist, (self.pos[1] - boid.pos[1]) / dist
				separation = separation[0] + opposite_dir[0], separation[1] + opposite_dir[1]
				total += 1
		# check if a boid is within sight_radius
		if total:
			# steer towards the average heading of local flockmates
			alignment = tuple(map(lambda x: x / total * self.align_factor, alignment))
			# steer to average position of local flockmates
			cohesion = (cohesion[0] / total - self.pos[0]) * self.cohesion_factor, \
					   (cohesion[1] / total - self.pos[1]) * self.cohesion_factor
		# steer to avoid crowding local flockmates
		separation = tuple(map(lambda x: x * self.separation_factor, separation))
		# update the acceleration
		self.acceleration = tuple(map(sum, zip(alignment, cohesion, separation)))


# normalize a vector to a certain magnitude
def norm(a, mag):
	v = math.sqrt(a[0] ** 2 + a[1] ** 2) / mag
	if v == 0:
		return 0
	return a[0] / v, a[1] / v
