from manim import *
import meshio
import numpy as np
from manim_mesh import Mesh


mesh = meshio.read(
    "meshes/circle.msh",
    # "meshes/triangle.msh"
)

cells = mesh.cells[0].data
points = mesh.points


class AnimationExample(ThreeDScene):
    def construct(self):
        # add coordinate system
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES)
        axs = ThreeDAxes()

        mesh = Mesh(points * 4, cells)
        print(f"Mesh with {len(mesh.vertices)} vertices and {len(mesh.cells)} cells")

        ### Animation ###

        # inital state
        self.add(axs)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.add(mesh)
        self.wait(1)

        # animate

        cell = mesh[0]
        cell.set_color(RED)

        self.move_camera(
            frame_center=cell.get_center(),
            zoom=4,
        )

        self.wait(1)

        mesh.hide(cell)

        self.wait(2)
