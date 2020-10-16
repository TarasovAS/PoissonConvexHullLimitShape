import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import cos, sin
import math
from random import random

plt.style.use('seaborn-pastel')

fig = plt.figure(figsize=(8,8))
ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
line, = ax.plot([], [], lw=3)

points_x, points_y = [],[]



def init():
    line.set_data([], [])
    return line,


def animate(i):
    angle = 2*math.pi*random()
    points_x.append(cos(angle)*i)
    points_y.append(sin(angle)*i)
    ax.clear()
    if len(points_x) > 3*i**0.5+1:
        points_x.pop(0)
        points_y.pop(0)
    scatter = ax.scatter(points_x,points_y)
    ax.set_xlim(-1-i,1+i)
    ax.set_ylim(-1 - i, 1 + i)
    return scatter,

frames = 225
anim = FuncAnimation(fig, animate, init_func=init,
                     frames=frames, interval=100, blit=True)

anim.save(f'points_{frames}_frames.gif', writer='imagemagick')