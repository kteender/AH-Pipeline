import maya.cmds as cmds
import csv
import maya_pycmds_utils as utils

def get_timeline_start_stop():
    start = cmds.playbackOptions(q=True, ast=True)
    stop = cmds.playbackOptions(q=True, aet=True)
    return start, stop

def get_selected_objects():
    #namespaces will not mess this up
    sel = cmds.ls(sl=True)
    selstr = []
    for s in sel:
        selstr.append(str(s))
    return selstr

def export_selected_abc():
    start, stop = get_timeline_start_stop()
    objectsFlag = ""
    selected = get_selected_objects()
    path = "D:/_CURRENT/AH/AH_proj/cache/alembic/cube.abc"
    for s in selected:
        st = "-root |%s " % (s)
        objectsFlag += st 
    command = "-frameRange " + str(start) + " " + str(stop) +" -dataFormat ogawa " + objectsFlag + "-file " + path
    cmds.AbcExport( j = command)
    return

def create_selected_mat_dict():
    selected = get_selected_objects()


export_selected_abc()
