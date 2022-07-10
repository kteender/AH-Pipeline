import bpy
import os

def apply_material_to_object(obj, mat):
    if len(obj.material_slots) < 1:
        obj.data.materials.append(mat)
    else:
        obj.material_slots[0].material = mat
    return
