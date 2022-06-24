import maya.cmds as cmds
import logging

thisLogger = logging.getLogger("MayaPyCmdsUtilsLogger")
thisLogger.setLevel(logging.DEBUG)

def get_mat_on_object(shape):
    """should not be passed the object itself, should be passed its shape node
        eg cmds.ls(sl=True, dag=True, s=True)
        returns list of all materials"""
    se = cmds.listConnections(shape, type='shadingEngine')
    mat = cmds.ls(cmds.listConnections(se), materials=True)
    return mat

def get_timeline_start_stop():
    """returns start and stop of main time slider as floats"""
    start = cmds.playbackOptions(q=True, ast=True)
    stop = cmds.playbackOptions(q=True, aet=True)
    return start, stop

def get_selected_objects_dag():
    sels = cmds.ls(sl=True, dag=True, s=True)
    return sels

def get_transform_for_shape(shape):
    tr = cmds.listRelatives(shape, type='transform', p=True)
    return tr

def filter_out_orig_shapes(shapeList):
    for shape in shapeList:
        if shape[-4:] == "Orig":
            shapeList.remove(shape)
    return shapeList

#def get_object_full_namepath(obj):
