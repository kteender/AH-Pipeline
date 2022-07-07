import sys
import argparse
import logging
import time
import json
import imp

import bpy
sys.path.append("D:\\_CURRENT\\AH\\AH_pipeline\\")
import blender_py_utils as utils

imp.reload(utils)

thisLogger = logging.getLogger("BlenderScriptLogger")
thisLogger.setLevel(logging.DEBUG)

HIGHLIGHT_NAMES = ["rig:margo_bun_geo", "rig:margo_hair_geo"]
NOHIGHLIGHT_NAMES = ["rig:mouthHighResBase","rig:margo_body_geo"]
EYE_NAMES = ['rig:eyeLeft_geo', 'rig:eyeRight_geo']
EYEMASK_NAMES = ["rig:eyeLeft_geo_mask", "rig:eyeRight_geo_mask"]
FACE_NAMES = ["rig:mouthHighResBase", "rig:noseLeft_geo"]

CHANNEL_LIST = ['color']

rigObjs = {0:HIGHLIGHT_NAMES, 1:NOHIGHLIGHT_NAMES, 2:EYEMASK_NAMES, 3:EYE_NAMES,
4:FACE_NAMES}
sceneCollections = {0:'highlight_geo', 1:'nohighlight', 2:'eye_mask', 3:'eyes', 4:'face'}

def get_args():
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
        parser = argparse.ArgumentParser()
        #parser.add_argument('-s1', '--sample_1', dest='sample_1', metavar='FILE')
        parser.add_argument('-p1', '--path1', dest='path1', type=str)
        parser.add_argument('-p2', '--path2', dest='path2', type=str)
        args = parser.parse_known_args(argv)[0]
        # print parameters
        thisLogger.info('path_1: ', args.path1)
        thisLogger.info('path_2: ', args.path2)
        return args.path1, args.path2

def import_abc(abcPath):
    bpy.ops.wm.alembic_import(filepath=abcPath)
    return

def sort_objects():
    objs = bpy.data.objects
    thisLogger.info("Objects are %s", objs)
    cols = bpy.data.collections
    pd = {}
    #Make a dictionary of objects:highest level parent
    for obj in objs:
        pd[obj] = obj
        p = obj.parent
        while p != None:
            pd[obj] = p
            p = p.parent
    for obj in objs:
        p2 = pd[obj]
        cc = None
        for c in cols:
            children = c.objects
            if obj.name in children:
                cc = c
                break
        if "2d" in p2.name.lower():
            if cc != cols['2d']:
                cols['2d'].objects.link(obj)
                cc.objects.unlink(obj)
            continue
        if "3d" in p2.name.lower():
            if cc != cols['nohighlight']:
                cols['nohighlight'].objects.link(obj)
                cc.objects.unlink(obj)
            continue
        if "camera" in p2.name.lower():
            if cc != cols['cameras']:
                cols['cameras'].objects.link(obj)
                cc.objects.unlink(obj)
            continue
        for k in rigObjs.keys():
            if p2.name in rigObjs[k]:
                col = sceneCollections[k]
                if cc != col:
                    cols[col].objects.link(obj)
                    cc.objects.unlink(obj)
                break
            else:
                continue

def apply_materials(path):
    f = open(path)
    matData = json.load(f)
    for obj in matData:
        for mat in matData[obj]:
            m = None
            try:
                m = bpy.data.materials[mat]
            except:
                thisLogger.info("Creating Material for %s" % mat)
                print("mat is")
                print(type(mat))
                print(mat)
                m = utils.create_material_from_dict(mat, matData[obj][mat], *CHANNEL_LIST)
            utils.apply_material_to_object(obj, m)
            


    

p1, p2 = get_args()
print("path1 is ", p1)
print("path2 is ", p2)
import_abc(p2)
sort_objects()
apply_materials(p1)

"""
Collections: 
2D objects - 2D objects
3D objects 
    highlight_hair -
        hair geo
    no highlight 
        body geo
        face shapes
    highlight -
        lights in the highlights
light?
"""