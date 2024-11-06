import manim as mn
from functools import singledispatchmethod
from typing import List, Set
import numpy as np


class Vertex(mn.Dot):
    def __init__(self, point):
        super().__init__(point=point, radius=0.05)
        self.point = point

    def __repr__(self):
        return f"Vertex({self.point})"


class Cell(mn.VGroup):
    def __init__(
        self,
        vertecies: List[Vertex],
        index: int,
        background: mn.ManimColor | None = None,
    ):
        super().__init__(*vertecies)

        self.edges = []
        self.vertecies = vertecies
        self.index = index

        # create edges
        for i in range(len(vertecies)):
            self.edges.append(
                mn.Line(
                    vertecies[i].point,
                    vertecies[(i + 1) % len(vertecies)].point,
                    stroke_width=0.5,
                )
            )

        if background:
            self.background = mn.Polygon(
                *[vertex.point for vertex in vertecies],
                fill_color=background,
                fill_opacity=0.5,
            )
            self.add(self.background)

        self.add(*self.edges)

    def __repr__(self):
        return f"Cell({self.vertecies}, {self.index})"


class Mesh(mn.VGroup):
    def __init__(self, points: np.ndarray, cells: np.ndarray):
        super().__init__()

        self.vertices: List[Vertex] = [Vertex(point) for point in points]

        self.cells: List[Cell] = [
            Cell([self.vertices[i] for i in cell], index)
            for index, cell in enumerate(cells)
        ]

        self.add(*self.cells)

    def __getitem__(self, index: int) -> Cell:
        return self.cells[index]

    @singledispatchmethod
    def hide(self, manim_object):
        self.remove(manim_object)

    @hide.register
    def _(self, vertex: Vertex):
        for cell in self.cells:
            cell.remove(vertex)

    @hide.register
    def _(self, cell: Cell):
        self.remove(cell)

    def get_neighbours(self, vertex: Vertex) -> Set[Vertex]:
        pass

    def __repr__(self):
        return f"Mesh({self.vertices}, {self.cells})"
