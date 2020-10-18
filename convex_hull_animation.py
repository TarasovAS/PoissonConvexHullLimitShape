import numpy as np
from matplotlib import pyplot as plt
from math import cos, sin, sqrt, pi
from celluloid import Camera
from random import random, seed
from geom_algorithms import graham_scan, get_max_angle
import os
import argparse


class Animator:
    def __init__(self, point_generator, generator_seed: int = 0) -> None:

        self.fig = plt.figure(figsize=(8, 8))
        plt.axis('off')
        self.camera = Camera(self.fig)
        self.plot_scale = 1
        self.iteration_number = 0

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
        return self.camera.animate(interval=150)

    def iterate(self):
        points_to_generate = 1
        self.iteration_number += 1
        self.snap(update_scale=True)
        while self.generator.max_radius > self.convex_hall_max_radius:
            for _ in range(points_to_generate):
                self.points.append(self.generator.get_next())
            points_to_generate += len(self.points) // 5 + 1
            self.update_convex_hull()
        self.snap()
        self.snap(draw_convex_hull=True)
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
            max_angle = get_max_angle(vertices)

            self.convex_hall_max_radius = min_vector_len * cos(max_angle / 2)

    def snap(self, draw_convex_hull: bool = False, update_scale: bool = False):
        if not self.points:
            print('Nothing to snap')
            return None
        if update_scale:
            self.plot_scale = 1 / max([sqrt(x**2 + y**2 ) for x, y in self.points])

        for point in self.points:
            plt.scatter(point[0] * self.plot_scale, point[1] * self.plot_scale, color='black')

        vertices = [self.points[idx] for idx in self.convex_hull_vertices_idxs]
        if vertices and draw_convex_hull:
            points = vertices[:] + [vertices[0]]
            for point1, point2 in zip(points[:-1], points[1:]):
                coordinates_x = [point1[0] * self.plot_scale, point2[0] * self.plot_scale]
                coordinates_y = [point1[1] * self.plot_scale, point2[1] * self.plot_scale]
                plot_ = plt.plot(coordinates_x, coordinates_y, color='red')
                plt.legend(plot_, [f'iteration number {self.iteration_number}'])
            for point in vertices:
                plt.scatter(point[0] * self.plot_scale, point[1] * self.plot_scale, color='red')

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

    if 'gifs' not in os.listdir(os.curdir):
        os.mkdir('gifs')
    animation.save(f'gifs/convex_hull_{iterations_num}(iterations){generator_seed}(seed).gif', writer='imagemagick')


main(iterations_num=15, generator_seed=5)
