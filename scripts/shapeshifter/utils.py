import maya.api.OpenMaya as om2


def get_mobject(node_name):
    sel = om2.MSelectionList()
    sel.add(node_name)
    return sel.getDependNode(0)
