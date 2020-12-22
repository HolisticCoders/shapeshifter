from collections import namedtuple
import maya.api.OpenMaya as om2
import maya.cmds as cmds

Color = namedtuple("Color", ["r", "g", "b"])


class Curve(object):
    def __init__(
        self,
        cvs,
        degree,
        form,
        knots,
        outlinerColor=Color(0, 0, 0),
        overrideColorRGB=Color(0, 0, 0),
        overrideEnabled=False,
        overrideRGBColors=False,
        useOutlinerColor=False,
        mobject=None,
    ):
        self.cvs = cvs
        self.degree = degree
        self.form = form
        self.knots = knots
        self.overrideEnabled = overrideEnabled
        self.overrideRGBColors = overrideRGBColors
        self.useOutlinerColor = useOutlinerColor
        self.mobject = mobject

        if isinstance(outlinerColor, list):
            self.outlinerColor = Color(
                outlinerColor[0],
                outlinerColor[1],
                outlinerColor[2],
            )
        elif isinstance(outlinerColor, Color):
            self.outlinerColor = outlinerColor
        else:
            raise TypeError("outlinerColor needs to be either a list or a Color")

        if isinstance(overrideColorRGB, list):
            self.overrideColorRGB = Color(
                overrideColorRGB[0],
                overrideColorRGB[1],
                overrideColorRGB[2],
            )
        elif isinstance(overrideColorRGB, Color):
            self.overrideColorRGB = overrideColorRGB
        else:
            raise TypeError("overrideColorRGB needs to be either a list or a Color")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_curve(cls, mobject):
        """Instantiate a Curve from a maya curve."""
        data = cls.get_shape_data(mobject)
        return cls(mobject=mobject, **data)

    @staticmethod
    def get_shape_data(curve):
        """Get all the necessary data to recreate the given curve."""
        if not curve.hasFn(om2.MFn.kNurbsCurve):
            raise TypeError(
                "curve should have the `kNurbsCurve` function set, not {}".format(
                    curve.apiTypeStr
                )
            )

        curve_fn = om2.MFnNurbsCurve(curve)
        name = curve_fn.name()

        knots = curve_fn.knots()
        cvs = curve_fn.cvPositions()
        form = curve_fn.form
        degree = curve_fn.degree
        overrideRGBColors = cmds.getAttr("{}.overrideRGBColors".format(name))
        overrideColorRGB = cmds.getAttr("{}.overrideColorRGB".format(name))[0]
        overrideColorRGB = Color(
            overrideColorRGB[0],
            overrideColorRGB[1],
            overrideColorRGB[2],
        )
        overrideEnabled = cmds.getAttr("{}.overrideEnabled".format(name))
        useOutlinerColor = cmds.getAttr("{}.useOutlinerColor".format(name))

        outlinerColor = cmds.getAttr("{}.outlinerColor".format(name))
        outlinerColor = Color(
            outlinerColor[0],
            outlinerColor[1],
            outlinerColor[2],
        )

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
        curve = om2.MFnNurbsCurve()
        self.mobject = curve.create(
            self.cvs,
            self.knots,
            self.degree,
            self.form,
            False,
            False,
            transform,
        )

        name = curve.name()

        cmds.setAttr("{}.overrideRGBColors".format(name), self.overrideRGBColors)
        cmds.setAttr(
            "{}.overrideColorRGB".format(name),
            self.overrideColorRGB.r,
            self.overrideColorRGB.g,
            self.overrideColorRGB.b,
        )
        cmds.setAttr("{}.overrideEnabled".format(name), self.overrideEnabled)
        cmds.setAttr("{}.useOutlinerColor".format(name), self.useOutlinerColor)
        cmds.setAttr(
            "{}.outlinerColor".format(name),
            self.outlinerColor.r,
            self.outlinerColor.g,
            self.outlinerColor.b,
        )
