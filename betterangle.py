from __future__ import annotations

import numpy
from manim import *
from abc import ABC


def AngleLabel(self: DecimalNumber | Text | VMobject, angle: BetterAngle, radius: float):
    self.midpoint = angle.get_midpoint()
    self.center = angle.arc_center
    self.direction = self.midpoint - self.center

    if radius == 0:
        self.move_to(midpoint)
    else:
        self.move_to(self.center + (self.direction * radius))
    self.scale(0.6)
    return self


class BetterAngle(Sector, ABC):
    @staticmethod
    def from_three_points(A: np.ndarray | list[int], B: np.ndarray | list[int], C: np.ndarray | list[int], **kwargs) -> BetterAngle:
        return BetterAngle(Line(B, A), Line(B, C), **kwargs)

    def __init__(self, line1: Line, line2: Line, other_angle: bool = False, **kwargs):
        self.line1 = line1; self.line2 = line2

        if numpy.array_equal(line1.get_start(), line2.get_start()): #Allows for parralel lines (180 degrees)
            intersection = line1.get_start()
        elif numpy.array_equal(line1.get_end(), line2.get_end()):
            intersection = line1.get_end()
        else:
            # Can throw ValueError, which is why other checks exist
            intersection = line_intersection(
                [line1.get_start(), line1.get_end()],
                [line2.get_start(), line2.get_end()],
            )

        anglev1 = line1.get_angle()
        anglev2 = line2.get_angle()

        angle = abs(anglev1-anglev2)
        start_angle = min(anglev1,anglev2)

        if other_angle:
            start_angle = max(anglev1,anglev2)
            angle=(2*PI)-angle

        super().__init__(angle=angle, start_angle=start_angle, arc_center=intersection, **kwargs)
        line1.z_index=self.z_index+1 #Perhaps problematic
        line2.z_index=self.z_index+1

    def numberLabel(self, radius=0.7, unit = "^{\circ}", num_decimal_places = 0, **kwargs) -> DecimalAngleLabel:
        return AngleLabel(DecimalNumber(unit=unit, num_decimal_places=num_decimal_places, **kwargs), self, radius)
    def textLabel(self, radius=0.7, **kwargs) -> TextAngleLabel:
        return AngleLabel(Text(**kwargs), self, radius)