import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import cos, sin, sqrt, pi
import math
from celluloid import Camera
from random import random, seed
from geom_algorithms import graham_scan, get_max_angle
from datetime import datetime


class Animator:
    def __init__(self, point_generator, generator_seed: int = 0) -> None:

        self.fig = plt.figure()
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
        return self.camera.animate(interval=1000)

    def iterate(self):
        points_to_generate = 1
        while self.generator.max_radius > self.convex_hall_max_radius:
            for _ in range(points_to_generate):
                self.points.append(self.generator.get_next())
            points_to_generate *= 2
            self.update_convex_hull()
            #self.snap()

        self.snap()
        self.del_convex_hall_vertices()


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
            max_angle = get_max_angle(vertices)
            # fig1 = plt.figure()
            # ax1 = fig1.gca()
            # ax1.set_xlim(-1, 1)
            # ax1.set_ylim(-1, 1)
            # for v in vertices:
            #     ax1.scatter(v[0], v[1])
            # fig1.show()

            self.convex_hall_max_radius = min_vector_len * cos(max_angle / 2)

    def snap(self):
        if not self.points:
            print('Nothing to snap')
            return None

        scale = 1 / max([sqrt(x**2 + y**2 ) for x,y in self.points])

        for point in self.points:
            plt.scatter(point[0] * scale, point[1] * scale, color='black')

        vertices = [self.points[idx] for idx in self.convex_hull_vertices_idxs]
        if vertices:
            points = vertices[:] + [vertices[0]]
            for point1, point2 in zip(points[:-1], points[1:]):
                coordinates_x = [point1[0] * scale, point2[0] * scale]
                coordinates_y = [point1[1] * scale, point2[1] * scale]
                plt.plot(coordinates_x, coordinates_y, color='black')

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
    animation.save(f'gifs/convex_hull_{iterations_num}(iterations){generator_seed}(seed).gif', writer='imagemagick')


main(iterations_num=40, generator_seed=0)
