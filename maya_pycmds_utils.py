import maya.cmds as mc
import logging

thisLogger = logging.getLogger("MayaPyCmdsUtilsLogger")
thisLogger.setLevel(logging.DEBUG)

def get_mat_on_object(shape):
    """should not be passed the object itself, should be passed its shape node
        eg cmds.ls(sl=True, dag=True, s=True)
        returns list of all materials"""
    se = mc.listConnections(shape, type='shadingEngine')
    mat = mc.ls(mc.listConnections(se), materials=True)
    return mat

def get_timeline_start_stop():
    """returns start and stop of main time slider as floats"""
    start = mc.playbackOptions(q=True, ast=True)
    stop = mc.playbackOptions(q=True, aet=True)
    return start, stop

def get_selected_objects_dag():
    sels = mc.ls(sl=True, dag=True, s=True)
    return sels

def get_transform_for_shape(shape):
    tr = mc.listRelatives(shape, type='transform', p=True)
    return tr

def filter_out_orig_shapes(shapeList):
    for shape in shapeList:
        if shape[-4:] == "Orig" or shape[-5:-1] == "Orig":
            shapeList.remove(shape)
    return shapeList

def filter_out_poly_shapes(shapeList):
    for shape in shapeList:
        if "polyS" in shape:
            shapeList.remove(shape)
    return shapeList

def get_mesh_light_shapes():
    dag = mc.ls(sl=True, dag=True, type='aiMeshLight')
    return dag

def get_point_light_shapes():
    dag = mc.ls(sl=True, dag=True, type='pointLight')
    return dag