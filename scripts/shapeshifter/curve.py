import maya.api.OpenMaya as om2
import maya.cmds as cmds

from shapeshifter.utils import get_mobject


class Curve(object):
    def __init__(
        self,
        cvs,
        degree,
        form,
        knots,
        outlinerColor,
        overrideColorRGB,
        overrideEnabled,
        overrideRGBColors,
        useOutlinerColor,
        mobject=None,
        curve=None,
    ):
        self.cvs = cvs
        self.degree = degree
        self.form = form
        self.knots = knots
        self.outlinerColor = outlinerColor
        self.overrideColorRGB = overrideColorRGB
        self.overrideEnabled = overrideEnabled
        self.overrideRGBColors = overrideRGBColors
        self.useOutlinerColor = useOutlinerColor
        self.mobject = mobject
        self.curve = curve

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_curve(cls, mobject):
        """Instantiate a Curve from a maya curve."""
        if not mobject.hasFn(om2.MFn.kNurbsCurve):
            raise TypeError("curve should have the `kNurbsCurve` function set")
        curve = om2.MFnNurbsCurve(mobject)

        data = cls.get_shape_data(mobject)

        return cls(mobject=mobject, curve=curve, **data)

    @staticmethod
    def get_shape_data(curve):
        """Get all the necessary data to recreate the given curve."""
        if not curve.hasFn(om2.MFn.kNurbsCurve):
            raise TypeError("curve should have the `kNurbsCurve` function set")

        curve = om2.MFnNurbsCurve(curve)
        name = curve.name()

        knots = curve.knots()
        cvs = curve.cvPositions()
        form = curve.form
        degree = curve.degree
        overrideRGBColors = cmds.getAttr("{}.overrideRGBColors".format(name))
        overrideColorRGB = cmds.getAttr("{}.overrideColorRGB".format(name))[0]
        overrideEnabled = cmds.getAttr("{}.overrideEnabled".format(name))
        useOutlinerColor = cmds.getAttr("{}.useOutlinerColor".format(name))
        outlinerColor = cmds.getAttr("{}.outlinerColor".format(name))

        data = {
            "knots": knots,
            "cvs": cvs,
            "form": form,
            "degree": degree,
            "overrideRGBColors": overrideRGBColors,
            "overrideColorRGB": overrideColorRGB,
            "overrideEnabled": overrideEnabled,
            "useOutlinerColor": useOutlinerColor,
            "outlinerColor": outlinerColor,
        }
        return data

    def create(self, transform):
        """Create the maya curve."""
        self.curve = om2.MFnNurbsCurve()
        self.mobject = self.curve.create(
            self.cvs,
            self.knots,
            self.degree,
            self.form,
            False,
            False,
            transform,
        )

        name = self.curve.name()

        cmds.setAttr("{}.overrideRGBColors".format(name), self.overrideRGBColors)
        cmds.setAttr(
            "{}.overrideColorRGB".format(name),
            self.overrideColorRGB[0],
            self.overrideColorRGB[1],
            self.overrideColorRGB[2],
        )
        cmds.setAttr("{}.overrideEnabled".format(name), self.overrideEnabled)
        cmds.setAttr("{}.useOutlinerColor".format(name), self.useOutlinerColor)
        cmds.setAttr(
            "{}.outlinerColor".format(name),
            self.outlinerColor[0],
            self.outlinerColor[1],
            self.outlinerColor[2],
        )
