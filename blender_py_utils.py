import bpy
import os
import logging

bLogger = logging.getLogger(__name__)
thisLogger = logging.getLogger(__name__+' Blender Py Utils Logger')
thisLogger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
fm = logging.Formatter(fmt=' %(name)s : %(levelname)-8s : %(message)s')
sh.setFormatter(fm)
thisLogger.addHandler(sh)

def apply_material_to_object(obj, mat):
    thisLogger.info("Applying %s material to %s" % (mat, obj))
    if len(obj.material_slots) < 1:
        thisLogger.info("Creating material slot")
        obj.data.materials.append(mat)
        obj.material_slots[0].material = mat
        obj.active_material_index = 0
    else:
        thisLogger.info("Putting in slot 0")
        obj.material_slots[0].material = mat
        obj.active_material_index = 0
    return

def add_subd(obj):
    thisLogger.info("Adding subdivision modifier to %s" % obj)
    obj.modifiers.new("subd", type='SUBSURF')
    return

def create_node_group_in_mat(mat, nm):
    ng = bpy.data.node_groups.new(nm, 'ShaderNodeTree')
    ngn  = mat.node_tree.nodes.new('ShaderNodeGroup')
    ngn.node_tree = ng
    return ng, ngn
