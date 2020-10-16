from math import atan2 as arctg
from math import pi


def signed_area_of_triangle(a, b, c):
    """ compute signed area of triangle """
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])


def graham_scan(points):
    """ from list of points select vertices of their convex hall """
    n = len(points)  # число точек
    p = range(n)  # список номеров точек
    for i in range(1, n):
        if points[p[i]][0] < points[p[0]][0]:  # если p[i]-ая точка лежит левее p[0]-ой точки
            p[i], p[0] = p[0], p[i]  # меняем местами номера этих точек
    for i in range(2, n):  # сортировка вставкой
        j = i
        while j > 1 and (signed_area_of_triangle(points[p[0]], points[p[j - 1]], points[p[j]]) < 0):
            p[j], p[j - 1] = p[j - 1], p[j]
            j -= 1
    convex_hall = [p[0], p[1]]  # создаем стек
    for i in range(2, n):
        while signed_area_of_triangle(points[convex_hall[-2]], points[convex_hall[-1]], points[p[i]]) < 0:
            del convex_hall[-1]  # pop(convex_hall)
        convex_hall.append(p[i])  # push(convex_hall,p[i])
    return convex_hall


def get_min_angle(points: list) -> float:
    points = points[:] + [points[0]]
    return min([get_angle(p1, p2) for p1, p2 in zip(points[:-1], points[1:])])


def get_angle(p1,p2):
    angle = arctg(p2[0], p2[1]) - arctg(p1[0],p1[1])
    if angle < 0:
        angle += 2*pi
    assert 0 <= angle <= 2*pi
    return angle


