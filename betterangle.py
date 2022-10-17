from __future__ import annotations

import numpy
from manim import *
from abc import ABC


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

        super().__init__(angle=angle, start_angle=start_angle, arc_center=intersection, **kwargs)
        line1.z_index=self.z_index+1 #Perhaps problematic
        line2.z_index=self.z_index+1
