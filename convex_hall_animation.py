import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import cos, sin, sqrt, pi
import math
from celluloid import Camera
from random import random, seed
from geom_algorithms import graham_scan, get_min_angle
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

        for i in range(10):
            self.points.append(self.generator.get_next())

        self.convex_hull_vertices_idxs = []
        self.convex_hall_max_radius = 0
        self.update_convex_hull()

    def film_iterates(self, iterates_num):
        for _ in range(iterates_num):
            self.iterate()
        return self.camera.animate()

    def iterate(self):
        points_to_generate = 1
        while self.generator.max_radius > self.convex_hall_max_radius:
            for _ in range(points_to_generate):
                self.points.append(self.generator.get_next())
            points_to_generate *= 2
            self.update_convex_hull()
            self.snap()

        self.del_convex_hall_vertices()
        self.snap()

    def del_convex_hall_vertices(self):
        self.points = [point for idx, point in enumerate(self.points) if idx not in self.convex_hull_vertices_idxs]
        self.update_convex_hull()

    def update_convex_hull(self):
        if len(self.points) < 3:
            self.convex_hull_vertices_idxs = list(range(len(self.points)))
            self.convex_hall_max_radius = 0
        else:
            self.convex_hull_vertices_idxs = graham_scan(self.points)
            vertices = [self.points[idx] for idx in self.convex_hull_vertices_idxs]
            min_vector_len = min([sqrt(x ** 2 + y ** 2) for x, y in vertices])
            min_angle = get_min_angle(vertices)
            # fig1 = plt.figure()
            # ax1 = fig1.gca()
            # ax1.set_xlim(-1, 1)
            # ax1.set_ylim(-1, 1)
            # for v in vertices:
            #     ax1.scatter(v[0], v[1])
            # fig1.show()

            self.convex_hall_max_radius = min_vector_len * cos(min_angle / 2)

    def snap(self):
        #self.axis.clear()
        coord_lim = max([sqrt(x**2 + y**2) for x, y in self.points]) * 1.5
        self.axis.set_xlim(-coord_lim, coord_lim)
        self.axis.set_ylim(-coord_lim, coord_lim)

        for point in self.points:
            self.axis.scatter(point[0], point[1], color='black')

        vertices = [self.points[idx] for idx in self.convex_hull_vertices_idxs]
        if vertices:
            points = vertices[:] + vertices[0]
            for point1, point2 in zip(points[:-1], points[1:]):
                self.axis.plot([point1[0], point2[0]], [point1[1], point2[1]], color='black')
                self.camera.snap()


class PointGenerator:

    def __init__(self):
        self.max_radius: float = 1.0
        self.generated_points: int = 0

    def get_next(self):
        self.generated_points += 1
        angle = random() * 2 * pi
        self.max_radius = 1 / self.generated_points
        return np.array([cos(angle), sin(angle)]) / self.generated_points


def main(iterations_num, generator_seed=0):
    generator = PointGenerator()
    animator = Animator(generator, generator_seed)
    animation = animator.film_iterates(iterations_num)
    animation.save(f'convex_hull_{iterations_num}(iterations){generator_seed}(seed).gif', writer = 'imagemagick')


main(iterations_num = 6, generator_seed = 0)
