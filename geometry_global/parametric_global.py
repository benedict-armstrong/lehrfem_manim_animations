from manim import *


def get_incenter(A, B, C):
    a = np.linalg.norm(C - B)
    b = np.linalg.norm(C - A)
    c = np.linalg.norm(B - A)

    incenter = (a * A + b * B + c * C) / (a + b + c)

    return incenter


def calculate_affine_mapping_from_unit(a, b, c):
    """
    Calculate the affine mapping from the triangle unit triangle to the triangle defined by the points a, b, c

    f(x) = Ax +b
    """

    A = np.array(
        [
            [b[0] - a[0], c[0] - a[0]],
            [b[1] - a[1], c[1] - a[1]],
        ]
    )
    b = np.array([a[0], a[1]])

    return A, b


class ParametricPlotGlobal(Scene):
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
                Dot(coord, color=WHITE, radius=0.1)
                for coord in ref_triangle.get_vertices()
            ]
        )

        # place inside triangle at incenter
        ref_triangle_label = MathTex(r"\hat{K}", color=BLUE).move_to(
            get_incenter(*ref_triangle.get_vertices())
        )

        ref_group = VGroup(ref_triangle, ref_tria_points, ref_triangle_label)

        ### Draw second Triangle

        triangle = Polygon(*ax.c2p([[2, 0.3, 0], [2.5, 1.1, 0], [1.5, 1, 0]]))

        tria_points = VGroup(
            *[Dot(coord, color=WHITE, radius=0.1) for coord in triangle.get_vertices()]
        )

        # place inside triangle at incenter
        triangle_label = MathTex(r"K", color=BLUE).move_to(
            get_incenter(*triangle.get_vertices())
        )

        triangle_group = VGroup(triangle, tria_points, triangle_label)

        ### Calculate and show affine mapping

        A, b = calculate_affine_mapping_from_unit(*ax.p2c(triangle.get_vertices()))

        # affine_mapping = MathTex(
        #     rf"\Phi_K(\hat{{x}}) = \begin{{bmatrix}} {A[0]:.2f} & {B[0]:.2f} \\ {A[1]:.2f} & {B[1]:.2f} \end{{bmatrix}} x + \begin{{bmatrix}} {b[0]:.2f} \\ {b[1]:.2f} \end{{bmatrix}}"
        # ).to_corner(UR)

        # affine_mapping = MathTex(
        #     r"\Phi_K(\hat{x}) = \begin{bmatrix} a & b \\ c & d \end{bmatrix} x + \begin{bmatrix} x \\ y \end{bmatrix}"
        # ).to_corner(UR)

        arrow_group_color = GRAY
        ### Show arc pointing from one triangle to other and add lable to it
        K_hat_to_K = CurvedArrow(
            ax.c2p(*[0.75, 0.75, 0]),
            ax.c2p(*[1.25, 0.8, 0]),
            angle=-PI / 8,
            color=arrow_group_color,
        )

        K_to_K_hat = CurvedArrow(
            ax.c2p(*[1.25, 0.8, 0]),
            ax.c2p(*[0.75, 0.75, 0]),
            angle=-PI / 8,
            color=arrow_group_color,
        ).shift(0.4 * DOWN)

        K_hat_to_K_label = MathTex(r"\Phi_K", color=arrow_group_color).next_to(
            K_hat_to_K, UP
        )

        K_to_K_hat_label = MathTex(r"\Phi_K^{*}", color=arrow_group_color).next_to(
            K_to_K_hat, DOWN
        )

        arrows_group = VGroup(
            K_hat_to_K, K_hat_to_K_label, K_to_K_hat, K_to_K_hat_label
        )

        ### make copy of ref_group
        ref_group_copy = ref_group.copy()
        ref_group_copy.set_opacity(0.4)

        # function_call = MathTex(
        #     r"\vec{p}_1 = lf::geometry::Global(\vec{p}_0)"
        # ).to_corner(UR)

        function_call = Code(
            code="auto global = geometry->Global(local_points);",
            language="c++",
            style="monokai",
            insert_line_no=False,
        ).to_corner(UR)

        global_color = GREEN
        local_color = RED

        global_code = function_call.code.chars[0][5:11]
        global_code.set_color(global_color)
        local_code = function_call.code.chars[0][31:43]
        local_code.set_color(local_color)

        ### Animate
        self.add(function_call)
        self.add(ref_group)
        # self.add(affine_mapping)
        self.add(triangle_group)
        self.add(arrows_group)

        local = np.array(
            [
                [0.1, 0.6],
                [0.5, 0.2],
            ]
        )

        # print(local[0])
        # print(local[1])

        # print(A @ local[0] + b)
        # print(A @ local[1] + b)

        local_matrix = (
            DecimalMatrix(
                local.T, h_buff=1, v_buff=0.6, bracket_h_buff=0.1, bracket_v_buff=0.1
            )
            .move_to(local_code.get_center())
            .scale(0.7)
            .set_color(local_color)
        )

        global_sol = np.array([A @ local[0] + b, A @ local[1] + b])

        global_matrix = (
            DecimalMatrix(
                global_sol.T,
                h_buff=1,
                v_buff=0.6,
                bracket_h_buff=0.1,
                bracket_v_buff=0.1,
            )
            .move_to(global_code.get_center())
            .scale(0.7)
            .set_color(global_color)
        )

        self.wait(1.5)
        self.play(
            ReplacementTransform(local_code, local_matrix),
        )

        p_1 = Dot(ax.c2p(*local[0]), color=local_color, radius=0.1)
        p_2 = Dot(ax.c2p(*local[1]), color=local_color, radius=0.1)
        p_1_target = Dot(ax.c2p(*(A @ local[0] + b)), color=global_color, radius=0.1)
        p_2_target = Dot(ax.c2p(*(A @ local[1] + b)), color=global_color, radius=0.1)

        points_to_tranform = VGroup(p_1, p_2)
        transformed_points = VGroup(p_1_target, p_2_target)

        self.wait(1)

        self.play(
            TransformFromCopy(local_matrix, points_to_tranform),
        )

        self.wait(1)

        self.play(
            Transform(p_1, p_1_target),
            Transform(p_2, p_2_target),
        )

        self.wait(1)

        self.play(
            TransformFromCopy(transformed_points, global_matrix),
            Unwrite(global_code),
        )

        self.wait(3)
