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
    thisLogger.info("Applying materials to %s" % obj)
    thisLogger.info("Mat getting applied is %s" % mat)

    if len(obj.material_slots) < 1:
        thisLogger.info("Creating material slot")
        obj.data.materials.append(mat)
        obj.material_slots[0].material = mat
        obj.active_material_index = 0
    else:
        obj.material_slots[0].material = mat
        obj.active_material_index = 0
    return