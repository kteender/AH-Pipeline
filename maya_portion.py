import maya.cmds as cmds
import csv
import maya_pycmds_utils as utils
import imp
imp.reload(utils)
import json

CHANNEL_LIST = ['color']

def get_selected_objects_str():
    """Returns selected object names as strings, rather than unicode strings"""
    sel = cmds.ls(sl=True)
    selstr = []
    for s in sel:
        selstr.append(str(s))
    return selstr

def export_selected_abc():
    start, stop = utils.get_timeline_start_stop()
    objectsFlag = ""
    selected = get_selected_objects_str()
    path = "D:/_CURRENT/AH/AH_proj/cache/alembic/cube.abc"
    for s in selected:
        st = "-root |%s " % (s)
        objectsFlag += st 
    command = "-frameRange " + str(start) + " " + str(stop) +" -dataFormat ogawa " + objectsFlag + "-file " + path
    cmds.AbcExport( j = command)
    return

def create_selected_mat_json():
    selected = utils.get_selected_objects_dag()
    objDict = {}
    for shape in selected:
        mats = utils.get_mat_on_object(shape)
        matDict = {}
        for mat in mats:
            matChannelDict = {}
            matChannelNames = []
            for c in CHANNEL_LIST:
                ch = str(mat)+"."+c
                matChannelNames.append(ch)
            matCons = cmds.listConnections(mat, c=True, p=False, d=False, t='file')
            for i in range(0, len(matCons)):
                if i%2==0 and matCons[i] in matChannelNames:
                    filenode = matCons[i+1]
                    filename = cmds.getAttr(filenode+'.fileTextureName')
                    matChannelDict[matCons[i]] = filename
            for ch in matChannelNames:
                if ch not in matChannelDict:
                    val = cmds.getAttr(mat+ch)
                    matChannelDict[ch] = val
            matDict[mat] = matChannelDict
        obj = utils.get_transform_for_shape(shape)[0] 
        objDict[obj] = matDict
    return objDict



export_selected_abc()
