from manim import *


class ParametricPlotExample(MovingCameraScene):
    def construct(self):
        ### Setup

        ax = Axes(
            # tips=False,
            x_range=[-0.5, 6, 1],
            y_range=[-0.5, 4, 1],
            axis_config={"include_numbers": True, "tip_shape": StealthTip},
        ).add_coordinates()

        self.add(ax)

        ### Draw triangle and points at vertices

        ref_triangle = Polygon(*ax.c2p([[1, 0, 0], [0, 1, 0], [0, 0, 0]]))

        ref_tria_points = VGroup(
            *[
                Dot(coord, color=RED, radius=0.1)
                for coord in ref_triangle.get_vertices()
            ]
        )

        # place inside triangle at center of mass
        ref_triangle_label = MathTex(r"\hat{K}", color=BLUE).next_to(
            ref_triangle.get_center(), UR, buff=0.2
        )

        ref_group = VGroup(ref_triangle, ref_tria_points, ref_triangle_label)

        self.add(ref_group)

        ### Define affine matrix

        mapping = np.array([[1, 2], [3, 4]])

        m0 = Matrix(mapping)

        # place matrix in top right corner of scene
        m0.to_corner(UR)

        self.add(m0)
