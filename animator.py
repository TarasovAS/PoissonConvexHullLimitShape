import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import cos, sin, sqrt, pi
import math
from celluloid import Camera
from random import random, seed
from geomalg import graham_scan, get_min_angle
from datetime import datetime


class Animator:
    def __init__(self, point_generator, generator_seed: int = 0) -> None:

        self.fig = plt.figure()
        self.axis = self.fig.gca()
        self.camera = Camera(self.fig)

        self.generator_seed = generator_seed
        seed(self.generator_seed)
        self.points = []
        self.generator = point_generator
        self.convex_hall = ConvexHall()

        for i in range(10):
            self.points.append(self.generator.get_next())
        self.convex_hall.update_convex_hall(self.points)

    def film_iterates(self, iterates_num):
        for _ in range(iterates_num):
            self.iterate()
        return self.camera.animate()

    def iterate(self):
        points_to_generate = 1
        while self.generator.max_radius > self.convex_hall.max_radius:
            new_points = []
            for _ in range(points_to_generate):
                next_point = self.generator.get_next()
                new_points.append(next_point)
                self.points.append(next_point)
            points_to_generate *= 2
            self.convex_hall.update_convex_hall(new_points)
            self.snap()

        self.del_convex_hall_vertices()
        self.snap()
        self.convex_hall.update_convex_hall(self.points)

    def del_convex_hall_vertices(self):
        while self.convex_hall.vertices:
            vertex = self.convex_hall.vertices.pop()
            self.points.remove(vertex)

    def snap(self):
        self.axis.clear()

        for point in self.points:
            self.axis.scatter(point[0], point[1])

        if self.convex_hall.vertices:
            points = self.convex_hall.vertices[:] + self.convex_hall.vertices[0]
            for point1, point2 in zip(points[:-1], points[1:]):
                self.axis.plot([point1[0], point2[0]], [point1[1], point2[1]])

        self.camera.snap()


class PointGenerator:

    def __init__(self):
        self.max_radius: float = 1.0
        self.generated_points: int = 0

    def get_next(self):
        self.generated_points += 1
        angle = random * 2 * pi
        self.max_radius = 1 / self.generated_points
        return np.array([cos(angle), sin(angle)]) / self.generated_points


class ConvexHall:

    def __init__(self, points: list):
        self.vertices = points
        self.max_radius = np.inf
        if self.vertices:
            self.update_convex_hall(self.vertices)

    def update_convex_hall(self, points: list):
        self.vertices = graham_scan(self.vertices + points)

        min_vector_len = min([sqrt(x**2 + y**2) for x, y in self.vertices])
        min_angle = get_min_angle(self.vertices)
        self.max_radius = min_vector_len * cos(min_angle / 2)


def main(frames, generator_seed=0):
    print(0)
    generator = PointGenerator
    print(1)
    animator = Animator(generator, generator_seed)
    print(2)
    animation = animator.film_iterates(frames)
    print(3)
    animation.save(f'convex_hall_{frames}_frames_{generator_seed}_{datetime.today()}.gif', writer = 'imagemagick')

print(-2)
#main(frames = 1, generator_seed = 0)
print(-1)