import maya.cmds as cmds

def get_mat_on_object(shape):
    """should not be passed the object itself, should be passed its shape node
        eg cmds.ls(sel=True, dag=True, s=True)
        returns list of all materials"""
    se = cmds.listConnections(shape, type='shadingEngine')
    mat = cmds.ls(cmds.listConnections(se), materials=True)
    return mat

def get_timeline_start_stop():
    """returns start and stop of main time slider as floats"""
    start = cmds.playbackOptions(q=True, ast=True)
    stop = cmds.playbackOptions(q=True, aet=True)
    return start, stop