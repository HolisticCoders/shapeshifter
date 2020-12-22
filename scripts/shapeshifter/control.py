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

    @classmethod
    def from_control(cls, transform):
        if isinstance(transform, basestring):
            transform = get_mobject(transform)
        transform_fn = om2.MFnTransform(transform)

        curves = []
        for i in range(transform_fn.childCount()):
            child = transform.child(i)
            if not child.hasFn(om2.MFn.kNurbsCurve):
                continue
            curve = Curve.from_curve(child)
            curves.append(curve)
        return cls(curves, transform)

    def create(self):
        if self.mobject is not None:
            raise RuntimeError(
                "Can't create a control that already has a transform. Use update instead"
            )
        self.mobject = get_mobject(cmds.createNode("transform"))

        for curve in self.curves:
            curve.create(self.mobject)
