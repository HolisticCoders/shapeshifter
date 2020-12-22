import maya.api.OpenMaya as om2
import maya.cmds as cmds

from shapeshifter.curve import Curve
from shapeshifter.utils import get_mobject


class Control(object):
    def __init__(self, curves, transform=None):
        self.mobject = transform
        self.curves = curves

    @classmethod
    def from_dict(cls, data):
        curves = []
        for curve_data in data.values():
            curve = Curve.from_dict(curve_data)
            curves.append(curve)

        return cls(curves)

    def create(self):
        if self.mobject is not None:
            raise RuntimeError(
                "Can't create a control that already has a transform. Use update instead"
            )
        self.mobject = get_mobject(cmds.createNode("transform"))

        for curve in self.curves:
            curve.create(self.mobject)
