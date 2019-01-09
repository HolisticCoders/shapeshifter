import os
import json

from pprint import pprint
import maya.cmds as cmds


def get_shape_data(ctl):
    data = []
    shapes = cmds.listRelatives(ctl, shapes=True)
    for shape in shapes:
        shape_data = {}

        # get the degree
        shape_data['degree'] = cmds.getAttr(shape + '.degree')
        if shape_data['degree'] != 1:
            raise ValueError('Shapeshifter only supports degree 1 curves for now')

        # get the color
        shape_data['enable_overrides'] = cmds.getAttr(shape + '.overrideEnabled')
        shape_data['use_rgb'] = cmds.getAttr(shape + '.overrideRGBColors')
        shape_data['color_index'] = cmds.getAttr(shape + '.overrideColor')
        rgb_colors = []
        for color_channel in 'RGB':
            rgb_colors.append(cmds.getAttr(shape + '.overrideColor' + color_channel))
        shape_data['color_rgb'] = rgb_colors

        # get the cvs local position
        cvs = cmds.ls(shape + '.cv[*]', flatten=True)
        cvs_pos = []
        for cv in cvs:
            cvs_pos.append(cmds.xform(cv, q=True, t=True))
        shape_data['cvs'] = cvs_pos
        data.append(shape_data)

    return data

def save_shape(data, name):
    directory = os.path.dirname(__file__)
    print directory

def create_curve(data):
    transform = cmds.createNode('transform')
    for shape_data in data:
        crv = cmds.curve(
            degree=shape_data['degree'],
            point=shape_data['cvs'],
        )
        shape = cmds.listRelatives(crv, shapes=True)[0]
        cmds.parent(shape, transform, relative=True, shape=True)
        cmds.delete(crv)
        if shape_data['enable_overrides']:
            cmds.setAttr(shape + '.overrideEnabled', True)
            if shape_data['use_rgb']:
                cmds.setAttr(shape + '.overrideRGBColors', 1)
                for color_channel, value in zip('RGB', shape_data['color_rgb']):
                    print color_channel, value
                    cmds.setAttr(shape + '.overrideColor' + color_channel, value)
            else:
                cmds.setAttr(shape + '.overrideColor', shape_data['color_index'])

    return transform

def copy_shape_to(source, targets):
    if not isinstance(targets, list):
        targets = [targets]
    data = get_shape_data(source)
    for target in targets:
        temp = create_curve(data)
        new_shapes = cmds.listRelatives(temp, shapes=True)
        cmds.delete(cmds.listRelatives(target, shapes=True))
        for shape in new_shapes:
            cmds.parent(shape, target, relative=True, shape=True)
        cmds.delete(temp)
