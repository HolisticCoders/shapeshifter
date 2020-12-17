import maya.api.OpenMaya as om2


class Shape(object):
    def __init__(
        self,
        cvs,
        degree,
        form,
        knots,
        name,
        outlinerColor,
        overrideColorRGB,
        overrideEnabled,
        overrideRGBColors,
        useOutlinerColor,
        shape=None,
    ):
        self.cvs = cvs
        self.degree = degree
        self.form = form
        self.knots = knots
        self.name = name
        self.outlinerColor = outlinerColor
        self.overrideColorRGB = overrideColorRGB
        self.overrideEnabled = overrideEnabled
        self.overrideRGBColors = overrideRGBColors
        self.useOutlinerColor = useOutlinerColor
        self.shape = shape

    @classmethod
    def from_dict(cls, data):
        name = data.keys()[0]
        data = data[name]
        return cls(name=name, **data)

    @classmethod
    def from_curve(cls, curve):
        """pseudo code for now just to get the idea."""
        raise NotImplementedError
        name = curve.name()
        data = cls.get_curve_data(curve)
        data = {name: data}
        shape = curve
        return cls(shape=shape, **data)

    def create(self, parent=None):
        if parent is None:
            raise NotImplementedError(
                "Shape.create isn't yet supported without a parent node."
            )

        new_curve = om2.MFnNurbsCurve()
        self.shape = new_curve.create(
            self.cvs,
            self.knots,
            self.degree,
            self.form,
            False,
            False,
            parent,
        )
