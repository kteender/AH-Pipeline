import maya.cmds as mc
import csv
import maya_pycmds_utils as utils
import imp
imp.reload(utils)
import json
import logging

CHANNEL_LIST = ['color']
ABC_EXPORT_SETTING_FLAGS = ["uvWrite", "writeFaceSets", "writeUVSets", "worldSpace"]

#Set up logging for this script
thisLogger = logging.getLogger("MayaPortionLogger")
thisLogger.setLevel(logging.DEBUG)

def get_rigged_camera_transform():
    cs = mc.ls(ca=True, v=True)
    cams = []
    for c in cs:
        ct = utils.get_transform_for_shape(c)
        cams += ct
    thisLogger.debug("cams are %s" % (cams))
    return cams

def get_selected_objects_str():
    """Returns selected object names as strings, rather than unicode strings"""
    sel = mc.ls(sl=True, l=True)
    cam = get_rigged_camera_transform()
    #Only need to check cam[0] because runner script will exit if multiple visible cams
    if ("|"+cam[0]) not in sel:
        sel += cam
    thisLogger.info("sel is %s" % (sel))
    selstr = []
    for s in sel:
        selstr.append(str(s))
    thisLogger.info("cmd arg is %s" % (selstr))
    return selstr

def create_abc_export_cmd():
    """Returns a string mel command for exporting Alembic cache. You'll still have to 
    add a path to the end of the string"""
    start, stop = utils.get_timeline_start_stop()
    settingsFlags = ""
    for f in ABC_EXPORT_SETTING_FLAGS:
        settingsFlags += (" -"+f)
    objectsFlag = ""
    selected = get_selected_objects_str()
    for s in selected:
        st = "-root |%s " % (s)
        objectsFlag += st 
    command = "-frameRange " + str(start) + " " + str(stop) + settingsFlags + " -dataFormat ogawa " + objectsFlag + "-file "
    return command


#AbcExport -j "-frameRange 1 200 -uvWrite -writeFaceSets -writeUVSets -dataFormat ogawa -root |rig:margo_grp|rig:margo_geo_grp|rig:margo_body_geo -root |rig:margo_grp|rig:margo_geo_grp|rig:face_geo_grp|rig:eye_mask_grp|rig:eyeRight_geo_mask -root |rig:margo_grp|rig:margo_geo_grp|rig:face_geo_grp|rig:eye_mask_grp|rig:eyeLeft_geo_mask -root |rig:margo_grp|rig:margo_geo_grp|rig:face_geo_grp|rig:eyeRight_geo -root |rig:margo_grp|rig:margo_geo_grp|rig:face_geo_grp|rig:eyeLeft_geo -root |rig:margo_grp|rig:margo_geo_grp|rig:face_geo_grp|rig:noseLeft_geo -root |rig:margo_grp|rig:margo_geo_grp|rig:face_geo_grp|rig:mouthHighResBase -root |rig:margo_grp|rig:margo_geo_grp|rig:margo_hair_geo -root |rig:margo_grp|rig:margo_geo_grp|rig:margo_bun_geo -root |rig:default_camera -file D:/_CURRENT/AH/AH_proj/cache/alembic/ref.abc";
def test_log():
    thisLogger.warning("test warning")
    thisLogger.debug("test debug")
    thisLogger.critical("test crit")
    return

def create_selected_mat_dict():
    selected = utils.get_selected_objects_dag()
    thisLogger.info("selected is %s" % (selected))
    shapeDict = {}
    #Tries to get rid of 'Orig' shape nodes in the list
    shapeList = utils.filter_out_orig_shapes(selected)
    shapeList = utils.filter_out_poly_shapes(shapeList)
    for shape in shapeList:
        mats = utils.get_mat_on_object(shape)
        thisLogger.info("material on %s is %s" % (shape, mats))
        matDict = {}
        for mat in mats:
            matChannelDict = {}
            matChannelNames = []
            for c in CHANNEL_LIST:
                ch = str(mat)+"."+c
                matChannelNames.append(ch)
            matCons = mc.listConnections(mat, c=True, p=False, d=False, t='file')
            if matCons == None:
                thisLogger.info("%s material node has no connections" % (mat))
            else:
                for i in range(0, len(matCons)):
                    if i%2==0 and matCons[i] in matChannelNames:
                        filenode = matCons[i+1]
                        filename = mc.getAttr(filenode+'.fileTextureName')
                        matChannelDict[matCons[i]] = filename
            for ch in matChannelNames:
                if ch not in matChannelDict:
                    thisLogger.info("%s has no texture input, using default RBG" % (ch))
                    val = mc.getAttr(ch)
                    thisLogger.info("ch is %s val is %s "% (ch,val))
                    matChannelDict[ch] = val[0]
            matDict[mat] = matChannelDict
        #obj = utils.get_transform_for_shape(shape)[0]
        #tr = utils.get_transform_for_shape(shape)[0]
        shapeDict[shape] = matDict
        
        thisLogger.info(shapeDict)
    return shapeDict

def create_selected_light_dict():
    ml = utils.get_mesh_light_shapes()
    pl = utils.get_point_light_shapes()
    lights = ml+pl
    lightDict = {}
    for l in lights:
        attrDict = {}
        midTr = mc.listRelatives(l, type='transform', p=True)[0]
        topTr = mc.listRelatives(midTr, p=True)[0]

        nm = l.replace('Shape', '')

        col = l + ".color"
        colA = mc.getAttr(col)

        exp = l + '.aiExposure'
        expA = mc.getAttr(exp)

        if l in ml:
            shad = l + '.aiCastShadows'
            shadA = mc.getAttr(shad)
            shadCol = l + ".aiShadowColor"
            shadColA = mc.getAttr(shadCol)
            attrDict['lightType'] = 'mesh'
        elif l in pl:
            shadCol = l + ".shadowColor"
            shadColA = mc.getAttr(shadCol)
            shad = l + '.aiCastShadows'
            if shadColA == [(1.0, 1.0, 1.0)]:    
                shadA = False
            else:
                shadA = True
            attrDict['lightType'] = 'point'
        else:
            pass

        attrDict['name'] = nm  
        attrDict[exp] = expA
        attrDict[col] = colA[0]
        attrDict[shad] = shadA
        attrDict[shadCol] = shadColA[0]

        lightDict[topTr] = attrDict
    return lightDict

