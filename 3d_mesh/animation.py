from manim import *
import meshio
from typing import List, Set
import numpy as np

mesh = meshio.read(
    "meshes/circle.msh",  # string, os.PathLike, or a buffer/open file
    # "meshes/triangle.msh",  # string, os.PathLike, or a buffer/open file
    # file_format="stl",  # optional if filename is a path; inferred from extension
    # see meshio-convert -h for all possible formats
)

cells = mesh.cells[0].data
points = mesh.points

# scale point by 5
points = [[5 * x for x in point] for point in points]


class Vertex:
    def __init__(self, point, index, manim_object: Mobject):
        self.point = point
        self.index = index
        self.manim_object: Mobject = manim_object

    def __repr__(self):
        return f"Vertex({self.index})"


class Cell:
    def __init__(self, vertecies: List[Vertex], index, manim_object: Mobject):
        self.vertecies = vertecies
        self.index = index
        self.manim_object: Mobject = manim_object

    def __repr__(self):
        return f"Cell({self.vertecies}, {self.index})"


class Mesh:
    def __init__(self, points, cells):
        self.vertices: List[Vertex] = [
            Vertex(point, index, Dot(point=point, radius=0.05))
            for index, point in enumerate(points)
        ]
        self.cells: List[Cell] = []
        for index, cell in enumerate(cells):
            self.cells.append(
                Cell(
                    [self.vertices[i] for i in cell],
                    index,
                    Polygon(*[self.vertices[i].point for i in cell]).set_stroke(
                        color=WHITE, width=0.5
                    ),
                )
            )

    def get_neighbours(self, vertex: Vertex) -> Set[Vertex]:
        n = set()
        for cell in self.cells:
            if vertex in cell.vertecies:
                n.update(cell.vertecies)
        try:
            n.remove(vertex)
        except KeyError:
            pass
        return n

    def __repr__(self):
        return f"Mesh({self.vertices}, {self.polygons})"


class AnimationExample(ThreeDScene):
    def construct(self):
        # add coordinate system
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        axs = ThreeDAxes()
        self.add(axs)

        self.begin_ambient_camera_rotation(rate=0.1)

        mesh = Mesh(points, cells)

        print(f"Mesh with {len(mesh.vertices)} vertices and {len(mesh.cells)} cells")

        self.play(*[Create(c.manim_object) for c in mesh.cells])
        self.play(*[Create(v.manim_object) for v in mesh.vertices])

        # pick a vertex at random (use only vertecies that are between 1 < x < 2 radius from origin)
        vertex: Vertex = np.random.choice(
            [v for v in mesh.vertices if 1 < np.linalg.norm(v.point) < 2]
        )
        # change the color of the vertex
        self.play(vertex.manim_object.animate.set_color(RED))

        self.play(
            Flash(vertex.manim_object, color=RED),
        )

        # focus on the vertex
        self.move_camera(
            frame_center=vertex.point,
            zoom=4,
        )

        neighbour_v = mesh.get_neighbours(vertex)
        neighbour_c = [c for c in mesh.cells if vertex in c.vertecies]

        # change the color of the neighbour_v
        self.play(*[n.manim_object.animate.set_color(BLUE) for n in neighbour_v])

        # Fade out all the other vertices and cells
        self.play(
            *[
                FadeOut(v.manim_object)
                for v in mesh.vertices
                if v not in neighbour_v and v != vertex
            ],
            *[FadeOut(c.manim_object) for c in mesh.cells if vertex not in c.vertecies],
            FadeOut(axs),
        )

        # new polygons with the neighbours and the vertex
        vertex_up = vertex.manim_object.copy().set_z(0.5)

        # new calls with same vertecies but vertex replaced with vertex_up
        cells_new = []
        for c in neighbour_c:
            c_new = Polygon(
                *[
                    vertex_up.get_center() if v == vertex else v.point
                    for v in c.vertecies
                ]
            ).set_stroke(color=BLUE, width=2)
            cells_new.append(c_new)

        self.play(
            *[
                TransformFromCopy(c.manim_object, c_new)
                for c, c_new in zip(neighbour_c, cells_new)
            ],
        )

        self.wait(2)
