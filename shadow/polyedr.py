from math import pi
from functools import reduce
from operator import add

from common.r3 import R3


class Segment:
    """ Одномерный отрезок """
    # Параметры конструктора: начало и конец отрезка (числа)

    def __init__(self, start, end):
        self.start, self.end = start, end

    # Отрезок вырожден?
    def is_degenerate(self):
        return self.start >= self.end

    # Пересечение с отрезком
    def intersect(self, other):
        if other.start > self.start:
            self.start = other.start
        if other.end < self.end:
            self.end = other.end
        return self

    # Разность отрезков
    # Разность двух отрезков всегда является списком из двух отрезков!
    def subtraction(self, other):
        return [Segment(
            self.start,
            self.end if self.end < other.start else other.start
        ), Segment(
            self.start if self.start > other.end else other.end,
            self.end
        )]


class Edge:
    """ Ребро полиэдра """
    # Начало и конец стандартного одномерного отрезка
    SSTART, SEND = 0.0, 1.0

    # Параметры конструктора: начало и конец ребра (точки в R3)
    def __init__(self, start, end):
        self.start, self.end = start, end
        # Список «просветов»
        self.gaps = [Segment(Edge.SSTART, Edge.SEND)]

    # Учёт тени от одной грани
    def shadow(self, face):
        # «Вертикальная» грань не затеняет ничего
        if face.is_vertical():
            return
        # Нахождение одномерной тени на ребре
        shade = Segment(Edge.SSTART, Edge.SEND)
        for u, v in zip(face.vertices, face.v_normals()):
            shade.intersect(self.intersect_edge_with_normal(u, v))
            if shade.is_degenerate():
                return

        shade.intersect(
            self.intersect_edge_with_normal(
                face.vertices[0], face.h_normal()))
        if shade.is_degenerate():
            return
        # Преобразование списка «просветов», если тень невырождена
        gaps = [s.subtraction(shade) for s in self.gaps]
        self.gaps = [
            s for s in reduce(add, gaps, []) if not s.is_degenerate()]

    # Преобразование одномерных координат в трёхмерные
    def r3(self, t):
        return self.start * (Edge.SEND - t) + self.end * t

    # Пересечение ребра с полупространством, задаваемым точкой (a)
    # на плоскости и вектором внешней нормали (n) к ней
    def intersect_edge_with_normal(self, a, n):
        f0, f1 = n.dot(self.start - a), n.dot(self.end - a)
        if f0 >= 0.0 and f1 >= 0.0:
            return Segment(Edge.SEND, Edge.SSTART)
        if f0 < 0.0 and f1 < 0.0:
            return Segment(Edge.SSTART, Edge.SEND)
        x = - f0 / (f1 - f0)
        return Segment(Edge.SSTART, x) if f0 < 0.0 else Segment(x, Edge.SEND)

    def is_full(self):
        return (len(self.gaps) == 1
                and self.gaps[0].start == Edge.SSTART
                and self.gaps[0].end == Edge.SEND)


class Face:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertices: list[R3]):
        self.vertices = vertices
        self.edges = [Edge(vertices[i], vertices[i - 1])
                      for i in range(len(vertices))]

    # «Вертикальна» ли грань?
    def is_vertical(self):
        return self.h_normal().dot(Polyedr.V) == 0.0

    # Нормаль к «горизонтальному» полупространству
    def h_normal(self):
        n = (self.vertices[1] - self.vertices[0]) \
            .cross(self.vertices[2] - self.vertices[0])
        return n * (-1.0) if n.dot(Polyedr.V) < 0.0 else n

    # Нормали к «вертикальным» полупространствам, причём k-я из них
    # является нормалью к грани, которая содержит ребро, соединяющее
    # вершины с индексами k-1 и k
    def v_normals(self):
        return [self._vert(x) for x in range(len(self.vertices))]

    # Вспомогательный метод
    def _vert(self, k):
        n = (self.vertices[k] - self.vertices[k - 1]).cross(Polyedr.V)
        return n * \
            (-1.0) if n.dot(self.vertices[k - 1] - self.center()) < 0.0 else n

    # Центр грани
    def center(self):
        return sum(self.vertices, R3(0.0, 0.0, 0.0)) * \
            (1.0 / len(self.vertices))


class Polyedr:
    """ Полиэдр """
    # вектор проектирования
    V = R3(0.0, 0.0, 1.0)

    # Параметры конструктора: файл, задающий полиэдр
    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertices: list[R3] = []
        self.faces: list[Face] = []

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    self.scale = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    self.vertices.append(R3(x, y, z).rz(alpha).ry(beta)
                                         .rz(gamma) * self.scale)
                else:
                    self.faces.append(Face([
                        self.vertices[n - 1]
                        for n in map(int, line.split()[1:])
                    ]))

    # Метод изображения полиэдра
    def draw(self, tk=None):
        if tk: tk.clean()
        area = 0.0
        scale2 = self.scale / 2
        norm = Polyedr.V * (1 / self.scale / self.scale)
        for f in self.faces:
            full = True
            for e in f.edges:
                for f1 in self.faces:
                    e.shadow(f1)
                    full = full and e.is_full()
                if tk:
                    for s in e.gaps:
                        tk.draw_line(e.r3(s.start), e.r3(s.end))
            if full:
                center = f.center()
                if abs(center.x) > scale2 or abs(center.y) > scale2 \
                        or abs(center.z) > scale2:
                    for i in range(1, len(f.vertices) - 1):
                        s1 = f.vertices[i] - f.vertices[0]
                        s2 = f.vertices[i + 1] - f.vertices[0]
                        area += abs(s1.cross(s2).dot(norm)) / 2
        if tk: tk.update()
        return area
