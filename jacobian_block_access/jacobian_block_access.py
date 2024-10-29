from manim import *


# use wide aspcet ratio
config.pixel_height = 200
config.pixel_width = 800


class JacobianBlockAccess(Scene):
    def construct(self):
        matrix = Matrix(
            [[3, 5, 3, 2, 5, 3], [8, 3, 2, 1, 3, 2]],
            color=GRAY,
            bracket_v_buff=MED_LARGE_BUFF,
        )

        jac_text = Text(
            "jacobian =",
            font="Fira Mono",
            font_size=32,
            color=WHITE,
            weight="BOLD",
        ).next_to(matrix, LEFT, buff=0.5)

        g1 = VGroup(jac_text, matrix).move_to(ORIGIN)
        self.add(g1)

        highlight_1 = SurroundingRectangle(
            matrix.get_columns()[:2], buff=0.25, color=RED
        )
        highlight_2 = SurroundingRectangle(
            matrix.get_columns()[2:4], buff=0.25, color=RED
        )

        text_1 = Text(
            "Jacobian of 1st point",
            font="Fira Mono",
            font_size=32,
            color=RED,
            weight="BOLD",
        ).next_to(highlight_1, DR, aligned_edge=LEFT)

        angled_arrow_1 = (
            Elbow(width=0.2, angle=PI / 4)
            .set_stroke(width=7)
            .set_color(RED)
            .next_to(text_1, LEFT, buff=0.2)
        )

        text_group_1 = VGroup(angled_arrow_1, text_1)

        text_2 = Text(
            "Jacobian of 2nd point",
            font="Fira Mono",
            font_size=32,
            color=RED,
            weight="BOLD",
        ).next_to(highlight_2, DR, aligned_edge=LEFT)

        angled_arrow_2 = (
            Elbow(width=0.2, angle=PI / 4)
            .set_stroke(width=7)
            .set_color(RED)
            .next_to(text_2, LEFT, buff=0.2)
        )

        text_group_2 = VGroup(angled_arrow_2, text_2)

        self.play(
            Create(text_group_1),
            Create(highlight_1),
        )

        self.wait(1)

        self.play(
            Transform(highlight_1, highlight_2),
            Transform(text_group_1, text_group_2),
        )

        self.wait(1)
