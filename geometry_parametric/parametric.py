from manim import *


def get_incenter(A, B, C):
    a = np.linalg.norm(C - B)
    b = np.linalg.norm(C - A)
    c = np.linalg.norm(B - A)

    incenter = (a * A + b * B + c * C) / (a + b + c)

    return incenter


def calculate_affine_mapping(A, B, C, A_prime, B_prime, C_prime):
    # Calculate the affine mapping from triangle ABC to triangle A'B'C'
    # using the formula:
    # f(x) = Ax + b
    # where A = B - A, B = C - A, b = A'

    A = B - A
    B = C - A
    b = A_prime

    return A, B, b


class ParametricPlotExample(Scene):
    def construct(self):
        ### Setup

        ax = Axes(
            # tips=False,
            x_range=[-0.1, 3, 1],
            y_range=[-0.1, 1.5, 1],
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

        # place inside triangle at incenter
        ref_triangle_label = MathTex(r"\hat{K}", color=BLUE).move_to(
            get_incenter(*ref_triangle.get_vertices())
        )

        ref_group = VGroup(ref_triangle, ref_tria_points, ref_triangle_label)

        self.add(ref_group)

        ### Draw second Triangle

        triangle = Polygon(*ax.c2p([[2, 0.3, 0], [2.5, 1.1, 0], [1.5, 1, 0]]))

        tria_points = VGroup(
            *[Dot(coord, color=RED, radius=0.1) for coord in triangle.get_vertices()]
        )

        # place inside triangle at incenter
        triangle_label = MathTex(r"K", color=BLUE).move_to(
            get_incenter(*triangle.get_vertices())
        )

        triangle_group = VGroup(triangle, tria_points, triangle_label)

        ### Calculate and show affine mapping

        A, B, b = calculate_affine_mapping(
            *ref_triangle.get_vertices(), *triangle.get_vertices()
        )

        # affine_mapping = MathTex(
        #     rf"\Phi_K(\hat{{x}}) = \begin{{bmatrix}} {A[0]:.2f} & {B[0]:.2f} \\ {A[1]:.2f} & {B[1]:.2f} \end{{bmatrix}} x + \begin{{bmatrix}} {b[0]:.2f} \\ {b[1]:.2f} \end{{bmatrix}}"
        # ).to_corner(UR)

        affine_mapping = MathTex(
            r"\Phi_K(\hat{x}) = \begin{bmatrix} a & b \\ c & d \end{bmatrix} x + \begin{bmatrix} x \\ y \end{bmatrix}"
        ).to_corner(UR)

        ### Show arc pointing from one triangle to other and add lable to it
        K_hat_to_K = CurvedArrow(
            ax.c2p(*[0.75, 0.75, 0]),
            ax.c2p(*[1.25, 0.8, 0]),
            angle=-PI / 8,
            color=YELLOW,
        )

        K_to_K_hat = CurvedArrow(
            ax.c2p(*[1.25, 0.8, 0]),
            ax.c2p(*[0.75, 0.75, 0]),
            angle=-PI / 8,
            color=YELLOW,
        ).shift(0.4 * DOWN)

        K_hat_to_K_label = MathTex(r"\Phi_K", color=YELLOW).next_to(K_hat_to_K, UP)

        K_to_K_hat_label = MathTex(r"\Phi_K^{*}", color=YELLOW).next_to(
            K_to_K_hat, DOWN
        )

        arrows_group = VGroup(
            K_hat_to_K, K_hat_to_K_label, K_to_K_hat, K_to_K_hat_label
        )

        ### make copy of ref_group
        ref_group_copy = ref_group.copy()
        ref_group_copy.set_opacity(0.25)

        ### Animate
        self.add(affine_mapping)

        self.wait(1)

        self.add(ref_group_copy)

        self.play(Transform(ref_group, triangle_group), run_time=2)

        self.play(Create(arrows_group))

        self.wait(5)
