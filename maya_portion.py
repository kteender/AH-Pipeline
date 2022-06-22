import maya.cmds as cmds
import csv
import maya_pycmds_utils as utils
import json

CHANNEL_LIST = ['color']

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

def get_selected_objects_dag():
    sels = cmds.ls(sel=True, dag=True, s=True)
    return 

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

def create_selected_mat_json():
    selected = get_selected_objects_dag()
    objDict = {}
    for obj in selected:
        mats = utils.get_mat_on_object(obj)
        matDict = {}
        for mat in mats:
            matChannelDict = {}
            matChannelNames = []
            for c in CHANNEL_LIST:
                ch = str(mat)+"."+c
                matChannelNames.append(ch)
            matCons = cmds.listConnections(mat, c=True, p=False, d=False, t='file')
            for i in len(matCons):
                if i%2==0 and matCons[i] in matChannelNames:
                    filenode = matCons[i+1]
                    filename = cmds.getAttr(filenode+'.fileTextureName')
                    matChannelDict[matCons[i]] = filename
            for ch in matChannelNames:
                if ch not in matChannelDict:
                    val = cmds.getAttr(mat+ch)
                    matChannelDict[ch] = val
            matDict[mat] = matChannelDict
        objDict[obj] = matDict
    json.dumps(objDict)


export_selected_abc()
