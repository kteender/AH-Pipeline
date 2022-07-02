import sys
import argparse
import logging
import time
import bpy

thisLogger = logging.getLogger("BlenderScriptLogger")
thisLogger.setLevel(logging.DEBUG)

HIGHLIGHT_NAMES = ["rig:margo_bun_geo", "rig:margo_hair_geo"]
NOHIGHLIGHT_NAMES = ["rig:noseLeft_geo", "rig:mouthHighResBase",
"rig:margo_body_geo", "rig:eyeRight_geo_mask", "rig:eyeRight"]
EYE_NAMES = ['rig:eyeLeft_geo', 'rig:eyeRight_geo']
EYEMASK_NAMES = ["rig:eyeLeft_geo_mask", "rig:eyeRight_geo_mask"]
FACE_NAMES = ["rig:mouthHighResBase", "rig:noseLeft_geo"]

collections = {HIGHLIGHT_NAMES:'highlight_geo', NOHIGHLIGHT_NAMES:'nohighlight',
EYEMASK_NAMES:'eye_mask', EYE_NAMES:'eyes', FACE_NAMES:'face'}

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
            cols['2d'].objects.link(obj)
            cc.objects.unlink(obj)
        if "3d" in p2.name.lower():
            cols['nohighlight'].objects.link(obj)
            cc.objects.unlink(obj)
        for k in collections.keys():
            if p2.name in k:
                col = collections[k]
                cols[col].objects.link(obj)
                cc.object.unlink(obj)
                break
            else:
                continue







p1, p2 = get_args()
print("path1 is ", p1)
print("path2 is ", p2)
import_abc(p2)

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