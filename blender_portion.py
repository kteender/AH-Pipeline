import sys
import argparse
import logging
import json
import imp

from pkg_resources import empty_provider
import mathutils
import subprocess
import os

import bpy
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
target = os.path.join(sys.prefix, 'lib', 'site-packages')
print("python exe is")
print(python_exe)
sys.path.append("D:\\_CURRENT\\AH\\AH_pipeline\\")
import blender_py_utils as utils
imp.reload(utils)

try:
    from PIL import Image
except:
    sys.path.append("C:\\Users\\Clown Car\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python310\\site-packages\\")
    from PIL import Image

#thisLogger = logging.getLogger("BlenderScriptLogger")
bLogger = logging.getLogger(__name__)
thisLogger = logging.getLogger(__name__+' Blender Portion Logger')
thisLogger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
fm = logging.Formatter(fmt=' %(name)s : %(levelname)-8s : %(message)s')
sh.setFormatter(fm)
thisLogger.addHandler(sh)

HIGHLIGHT_NAMES = ["rig:margo_bun_geo", "rig:margo_hair_geo"]
NOHIGHLIGHT_NAMES = ["rig:margo_body_geo"]
EYE_NAMES = ['rig:eyeLeft_geo', 'rig:eyeRight_geo']
EYEMASK_NAMES = ["rig:eyeLeft_geo_mask", "rig:eyeRight_geo_mask"]
FACE_NAMES = ["rig:mouth_geo", "rig:noseLeft_geo"]

MAT_CHANNEL_LIST = ['color']
LIGHT_CHANNEL_LIST = ['color', 'aiShadowColor', 'aiExposure', 'aiCastShadows']
CHANNEL_MAP = {
    'color':'Color',
    'aiShadowColor':'Color',
    'aiExposure':'Strength',
    'aiCastShadows':'use_shadow'
}


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
        parser.add_argument('-p3', '--path3', dest='path3', type=str)
        args = parser.parse_known_args(argv)[0]
        # print parameters
        thisLogger.info('path_1: ', args.path1)
        thisLogger.info('path_2: ', args.path2)
        thisLogger.info('path_3: ', args.path3)
        return args.path1, args.path2, args.path3

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
            thisLogger.info('obj is %s', obj)
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
        if "highlight" in p2.name.lower():
            if cc != cols['highlight_lights']:
                cols['highlight_lights'].objects.link(obj)
                cc.objects.unlink(obj)
            continue
        for k in rigObjs.keys():
            thisLogger.info("Current collection is %s" % cc)
            if p2.name in rigObjs[k]:
                col = sceneCollections[k]
                thisLogger.info("New collection is %s" % col)
                if cc != cols[col]:
                    cols[col].objects.link(obj)
                    cc.objects.unlink(obj)
                break
            else:
                continue

def create_material_from_dict(nm, d, *args):
    mat = bpy.data.materials.new(nm)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.remove(nt.nodes['Material Output'])
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    mat.node_tree.links.clear()
    moN = nt.nodes.new('ShaderNodeOutputMaterial')
    shN = nt.nodes.new('ShaderNodeBsdfDiffuse')
    mat.node_tree.links.new(shN.outputs['BSDF'], moN.inputs['Surface'])

    for a in args:
        if a  == 'color':
            k = nm+ ".color"
            col = d[k]
            if isinstance(col, str):
                size = (1000,1000)
                with Image.open(col) as im:
                    size = im.size
                size = list(size)
                txN = nt.nodes.new('ShaderNodeTexImage')
                txI = bpy.data.images.new(col, width=size[0], height=size[1])
                txI.source = 'FILE'
                txI.filepath = col
                txN.image = txI
                mat.node_tree.links.new(txN.outputs['Color'], shN.inputs['Color'])
            else:
                col.append(1.0)
                shN.inputs['Color'].default_value = col
    return mat

def apply_materials(path):
    f = open(path)
    matData = json.load(f)
    for obj in matData:
        objMats = []
        thisLogger.info("obj is %s" % (obj))
        for mat in matData[obj]:
            m = None
            try:
                m = bpy.data.materials[mat]
                objMats.append(m)
            except:
                thisLogger.info("Creating Material for %s" % mat)
                m = create_material_from_dict(mat, matData[obj][mat], *MAT_CHANNEL_LIST)
                objMats.append(m)
        tr = obj.replace("Shape", "")
        thisLogger.info("tr for %s is %s" % (obj, tr))
        thisLogger.info("mat list is %s" % objMats)
        if tr in bpy.data.objects and bpy.data.objects[tr].type == 'MESH':
            thisLogger.info("%s in object list" % tr)
            if len(objMats) in range(0,2):
                utils.apply_material_to_object(bpy.data.objects[tr], objMats[0])
            else:
                thisLogger.warning("Multiple materials found on %s. This pipeline supports 1 material per object. Found materials:" % tr)
                for mat in objMats:
                    thisLogger.warning(mat)

def set_up_lights(path, matName):
    f= open(path)
    lightData = json.load(f)
    thisLogger.info("light data is %s" % lightData)
    mat = bpy.data.materials[matName]
    for obj in lightData:
        meshLightCounter = 0
        meshLights = []
        
        if lightData[obj]['lightType'] == 'point':
            #handles annoying maya bug where point light shape append #s at the end
            parentName = lightData[obj]['name']
            lightName = parentName + '_light'
            if bpy.context.scene.objects.get(lightName) != None:
                continue

            l =  bpy.data.lights.new(lightName, type='POINT')
            lo = bpy.data.objects.new(lightName, object_data=l)
            bpy.data.collections['lights'].objects.link(lo)

            for c in LIGHT_CHANNEL_LIST:
                shapeName = bpy.data.objects[obj].children[0].name+"Shape"
                thisLogger.info('light shape name is %s' % shapeName)
                digits = ""
                lSh = ""
                for char in shapeName:
                    try:
                        int(char)
                        digits += char
                        thisLogger.info('replacing digit in light shape name, new name is %s' % lSh)
                    except:
                        lSh += char
                lSh += digits
                thisLogger.info('light shape name is %s' % lSh)

                k = str(lSh+"."+c)
                if c == 'color':
                    col1 = lightData[obj][k]
                    thisLogger.info('light is %s' % obj)
                    thisLogger.info('col1 is %s' % col1)
                    #col1.append(1.0)
                    l.color = col1
                    continue
                if c == 'aiShadowColor':
                    continue
                if c == 'aiExposure':
                    exp = lightData[obj][k]
                    val = float(exp)*100000
                    l.energy = val
                    continue
                if c == 'aiCastShadows':
                    l.use_shadow = lightData[obj][k]
                    continue
            
            o = bpy.data.objects[parentName]
            thisLogger.info("making a light called %s" % o)
            utils.copy_transforms(lo, o, False)

        if lightData[obj]['lightType'] == 'mesh':
            meshLight, grp = utils.create_node_group_in_mat(mat, obj)
            meshLights.append(grp)

            emN1 = meshLight.nodes.new('ShaderNodeEmission')
            emN2 = meshLight.nodes.new('ShaderNodeEmission')
            ngoN = meshLight.nodes.new('NodeGroupOutput')
            mthN = meshLight.nodes.new('ShaderNodeMath')
            mixN = meshLight.nodes.new('ShaderNodeMixShader')
            pthN = meshLight.nodes.new('ShaderNodeLightPath')

            for c in LIGHT_CHANNEL_LIST:
                lSh = bpy.data.objects[obj].children[0].name+"Shape"
                k = str(lSh+"."+c)
                if c == 'color':
                    col1 = lightData[obj][k]
                    thisLogger.info('light is %s' % obj)
                    thisLogger.info('col1 is %s' % col1)
                    col1.append(1.0)
                    emN1.inputs['Color'].default_value = col1
                    continue
                if c == 'aiShadowColor':
                    col2 =  lightData[obj][k]
                    col2.append(1.0)
                    emN2.inputs['Color'].default_value = col2
                    continue
                if c == 'aiExposure':
                    exp = lightData[obj][k]
                    emN1.inputs['Strength'].default_value = exp
                    emN2.inputs['Strength'].default_value = exp
                    continue
                if c == 'aiCastShadows':
                    continue

            mthN.operation = 'GREATER_THAN'

            meshLight.links.new(pthN.outputs['Ray Depth'], mthN.inputs['Value'])
            meshLight.links.new(mthN.outputs['Value'], mixN.inputs['Fac'])
            meshLight.links.new(emN1.outputs['Emission'], mixN.inputs[2])
            meshLight.links.new(emN2.outputs['Emission'], mixN.inputs[1])
            meshLight.links.new(mixN.outputs['Shader'], ngoN.inputs[0])
            
            moNm = mat.node_tree.nodes['Material Output']
            rmL = [l for l in mat.node_tree.links if l.to_node == moNm][0]
            shOld = rmL.from_node
            mat.node_tree.links.remove(rmL)
            objNm = mat.node_tree.nodes.new('ShaderNodeObjectInfo')
            mthNm = mat.node_tree.nodes.new('ShaderNodeMath')
            mixNm = mat.node_tree.nodes.new('ShaderNodeMixShader')

            mthNm.operation = 'GREATER_THAN'
            mthNm.inputs[2].default_value = meshLightCounter

            mat.node_tree.links.new(objNm.outputs['Object Index'], mthNm.inputs['Value'])
            mat.node_tree.links.new(mthNm.outputs['Value'], mixNm.inputs['Fac'])
            mat.node_tree.links.new(shOld.outputs[0], mixNm.inputs[1])
            mat.node_tree.links.new(grp.outputs[0], mixNm.inputs[2])
            mat.node_tree.links.new(mixNm.outputs[0], moNm.inputs['Surface'])

            meshLightCounter += 1
            bpy.data.objects[obj].pass_index = meshLightCounter
        bpy.data.objects[obj].visible_camera = False          
    return
               

p1, p2, p3 = get_args()
bpy.context.scene.render.engine = 'CYCLES'
import_abc(p3)
sort_objects()
apply_materials(p1)

set_up_lights(p2, 'light_mat')

set_up_lights(p2, 'black_mat')
for obj in bpy.data.objects:
    if obj.name in HIGHLIGHT_NAMES or obj.name in NOHIGHLIGHT_NAMES or obj.name in FACE_NAMES:
        utils.add_subd(obj)
"""
for o in bpy.data.collections['2d'].objects:
    o.is_shadow_catcher = True
"""
camCol = bpy.data.collections['cameras']
if len(camCol.objects) < 1:
    thisLogger.critical("No camera found in %s" % camCol)
elif len(camCol.objects) > 1:
    thisLogger.critical("Mutliple cameras found in %s:" % camCol)
    for obj in camCol.objects:
        thisLogger.info(obj)
else:
    cam = camCol.objects[0]
    bpy.context.scene.camera = cam

for o in bpy.data.collections['2d'].objects:
    shadowCatchO = o.copy()
    bpy.data.collections['shadow_catch'].objects.link(shadowCatchO)
    shadowCatchO.is_shadow_catcher = True
    shadowCatchO.visible_shadow = False
    o.visible_shadow = False




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