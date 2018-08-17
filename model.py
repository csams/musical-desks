#!/usr/bin/env python
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])


class Desk(object):
    def __init__(self, pos):
        self.pos = pos
        self.t_pos = Point(pos.y, pos.x)
        dom = [-1, 0, 1]
        self.around = set()
        for x in dom:
            for y in dom:
                p = Point(self.pos.x + x, self.pos.y + y)
                if p != self.pos:
                    self.around.add(p)

    def is_beside(self, other):
        return other.pos in self.around

    def __lt__(self, other):
        return self.t_pos < other.t_pos

    def __eq__(self, other):
        return type(other) == Desk and self.pos == other.pos

    __hash__ = object.__hash__

    def __repr__(self):
        return f"Desk({self.pos})"

    def __str__(self):
        return self.__repr__()


class Room(object):
    def __init__(self, width, height=None, ignore=None):
        self.width = width
        self.height = height if height is not None else width
        self.ignore = ignore or set()

        self.desks = []
        self.room = [[None for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p not in self.ignore:
                    d = Desk(p)
                    self.desks.append(d)
                    self.room[y][x] = d

    def get(self, x, y):
        for desk in self.row(y):
            if desk.pos.x == x:
                return desk

    def row(self, r):
        return filter(None, self.room[r])

    def column(self, c):
        return filter(None, [r[c] for r in self.room])
