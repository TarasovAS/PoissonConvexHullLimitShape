import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import cos, sin, sqrt, pi
import math
from random import random
from geomalg import graham_scan, get_min_angle


class Animator:
    #TODO: вставить камеру из класса celluloid

    def __init__(self, point_generator):
        self.points = []
        self.generator = point_generator
        self.convex_hall = ConvexHall()

        for i in range(10):
            self.points.append(self.generator.get_next())
        self.convex_hall.update_convex_hall(self.points)

    def iterate(self):
        points_to_generate = 1
        while self.generator.max_radius > self.convex_hall.max_radius:
            new_points = []
            for i in range(points_to_generate):
                next_point = self.generator.get_next
                new_points.append(next_point)
                self.points.append(next_point)
            points_to_generate *= 2
            self.convex_hall.update_convex_hall(new_points)


    def add_point(self):
        self.points.append(self.generator.get_next)




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

    def __init__(self, points: list = []):
        self.vertices = points
        self.max_radius = np.inf
        if self.vertices:
            self.update_convex_hall(self.vertices)

    def update_convex_hall(self, points: list):
        self.vertices = graham_scan(self.vertices + points)

        min_vector_len = min([sqrt(x**2+y**2) for x,y in self.vertices])
        min_angle = get_min_angle(self.vertices)
        self.max_radius = min_vector_len * cos(min_angle / 2)


def main():
